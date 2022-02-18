import pytest

from ..loaders import threads_loader


@pytest.mark.asyncio
async def test_threads_loader_loads_thread(graphql_context, thread):
    loaded_thread = await threads_loader.load(graphql_context, thread.id)
    assert loaded_thread == thread