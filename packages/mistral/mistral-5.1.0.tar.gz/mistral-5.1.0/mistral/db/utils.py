# Copyright 2016 - Nokia Networks
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import functools

from oslo_db import exception as db_exc
from oslo_log import log as logging
from oslo_service import loopingcall

from mistral import context
from mistral import exceptions as exc
from mistral.services import security


LOG = logging.getLogger(__name__)


@loopingcall.RetryDecorator(max_retry_count=100, inc_sleep_time=0,
                            exceptions=db_exc.DBDeadlock)
def _with_auth_context(auth_ctx, func, *args, **kw):
    """Runs the given function with the specified auth context.

    :param auth_ctx: Authentication context.
    :param func: Function to run with the specified auth context.
    :param args: Function positional arguments.
    :param kw: Function keywork arguments.
    :return: Function result.
    """
    old_auth_ctx = context.ctx() if context.has_ctx() else None

    context.set_ctx(auth_ctx)

    try:
        return func(*args, **kw)
    except db_exc.DBDeadlock as e:
        LOG.exception(
            "DB deadlock detected, operation will be retried: %s", func
        )

        raise e
    finally:
        context.set_ctx(old_auth_ctx)


def retry_on_deadlock(func):
    """Decorates the given function so that it retries on a DB deadlock.

    :param func: Function to decorate.
    :return: Decorated function.
    """
    @functools.wraps(func)
    def decorate(*args, **kw):
        # We can't use RetryDecorator from oslo_service directly because
        # it runs a decorated function in a different thread and hence
        # the function doesn't have access to authentication context
        # set as a thread local variable.
        # The solution is to reuse RetryDecorator but explicitly set
        # auth context in the new thread that RetryDecorator spawns.
        # In order to do that we need an additional helper function.

        auth_ctx = context.ctx() if context.has_ctx() else None

        return _with_auth_context(auth_ctx, func, *args, **kw)

    return decorate


def check_db_obj_access(db_obj):
    """Check accessbility to db object."""
    ctx = context.ctx()
    is_admin = ctx.is_admin

    if not is_admin and db_obj.project_id != security.get_project_id():
        raise exc.NotAllowedException(
            "Can not access %s resource of other projects, ID: %s" %
            (db_obj.__class__.__name__, db_obj.id)
        )

    if not is_admin and hasattr(db_obj, 'is_system') and db_obj.is_system:
        raise exc.InvalidActionException(
            "Can not modify a system %s resource, ID: %s" %
            (db_obj.__class__.__name__, db_obj.id)
        )
