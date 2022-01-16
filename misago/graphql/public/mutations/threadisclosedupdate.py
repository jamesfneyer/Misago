from typing import Dict, List, Tuple

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import PositiveInt, create_model

from ....errors import ErrorsList
from ....loaders import load_thread, store_thread
from ....threads.close import close_thread
from ....threads.models import Thread
from ....validation import (
    CategoryModeratorValidator,
    ThreadCategoryValidator,
    ThreadExistsValidator,
    UserIsAuthorizedRootValidator,
    Validator,
    validate_data,
    validate_model,
)
from ... import GraphQLContext
from ...errorhandler import error_handler
from .hooks.threadisclosedupdate import (
    ThreadIsClosedUpdateInput,
    ThreadIsClosedUpdateInputModel,
    thread_is_closed_update_hook,
    thread_is_closed_update_input_hook,
    thread_is_closed_update_input_model_hook,
)

thread_is_closed_update_mutation = MutationType()


@thread_is_closed_update_mutation.field("threadIsClosedUpdate")
@error_handler
@convert_kwargs_to_snake_case
async def resolve_thread_is_closed_update(
    _, info: GraphQLResolveInfo, *, input: dict  # pylint: disable=redefined-builtin
):
    input_model = await thread_is_closed_update_input_model_hook.call_action(
        create_input_model, info.context
    )
    cleaned_data, errors = validate_model(input_model, input)

    if cleaned_data.get("thread"):
        thread = await load_thread(info.context, cleaned_data["thread"])
    else:
        thread = None

    if cleaned_data:
        validators: Dict[str, List[Validator]] = {
            "thread": [
                ThreadExistsValidator(info.context),
                ThreadCategoryValidator(
                    info.context, CategoryModeratorValidator(info.context)
                ),
            ],
            ErrorsList.ROOT_LOCATION: [UserIsAuthorizedRootValidator(info.context)],
        }
        cleaned_data, errors = await thread_is_closed_update_input_hook.call_action(
            validate_input_data, info.context, validators, cleaned_data, errors
        )

    if errors:
        return {"errors": errors, "thread": thread}

    thread = await thread_is_closed_update_hook.call_action(
        thread_is_closed_action, info.context, cleaned_data
    )

    return {"thread": thread}


async def create_input_model(context: GraphQLContext) -> ThreadIsClosedUpdateInputModel:
    return create_model(
        "ThreadIsClosedUpdateInputModel",
        thread=(PositiveInt, ...),
        is_closed=(bool, ...),
    )


async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: ThreadIsClosedUpdateInput,
    errors: ErrorsList,
) -> Tuple[ThreadIsClosedUpdateInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def thread_is_closed_action(
    context: GraphQLContext, cleaned_data: ThreadIsClosedUpdateInput
) -> Thread:
    thread = cleaned_data["thread"]
    thread = await close_thread(thread, cleaned_data["is_closed"])

    store_thread(context, thread)

    return thread