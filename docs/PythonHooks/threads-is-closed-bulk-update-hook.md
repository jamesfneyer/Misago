# `threads_is_closed_bulk_update_hook`

```python
from misago.graphql.public.mutations.hooks.threadsisclosedbulkupdate import threads_is_closed_bulk_update_hook

threads_is_closed_bulk_update_hook.call_action(
    action: ThreadsIsClosedBulkUpdateAction,
    context: GraphQLContext,
    cleaned_data: ThreadsIsClosedBulkUpdateInput,
)
```

A filter for the function used by `threadsIsClosedBulkUpdate` GraphQL mutation to update threads in the database.

Returns `list` of `Thread` dataclasses with updated threads data.


## Required arguments

### `action`

```python
async def close_threads(context: GraphQLContext, cleaned_data: ThreadsIsClosedBulkUpdateInput) -> List[Thread]:
    ...
```

Next filter or built-in function used to update the threads in the database.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


### `cleaned_data`

```python
Dict[str, Any]
```

A dict with already validated and cleaned input data. Will contain at least `threads` and `is_closed` keys:

```python
class ThreadsIsClosedBulkUpdateInput(TypedDict):
    threads: List[Thread]
    is_closed: bool
```