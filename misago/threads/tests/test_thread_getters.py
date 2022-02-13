import pytest

from ..get import get_threads_by_id, get_threads_page


@pytest.fixture
def threads(thread, user_thread, closed_thread):
    return sorted(
        [thread, user_thread, closed_thread], key=lambda x: x.last_post_id, reverse=True
    )


@pytest.mark.asyncio
async def test_threads_can_be_get_by_id(thread):
    assert [thread] == await get_threads_by_id([thread.id])


@pytest.mark.asyncio
async def test_getting_threads_by_nonexistant_id_returns_empty_list(db):
    assert await get_threads_by_id([1]) == []


@pytest.mark.asyncio
async def test_threads_page_is_retrieved(thread, threads):
    page = await get_threads_page(10, categories_ids=[thread.category_id])
    assert page.results == threads
    assert page.page_info.start_cursor == page.results[0].last_post_id
    assert page.page_info.end_cursor == page.results[-1].last_post_id
    assert page.page_info.has_next_page is False
    assert page.page_info.has_previous_page is False
    assert page.page_info.next_cursor is None
    assert page.page_info.previous_cursor is None


@pytest.mark.asyncio
async def test_threads_page_after_cursor_is_retrieved(thread, threads):
    page = await get_threads_page(
        10,
        categories_ids=[thread.category_id],
        after=threads[0].last_post_id,
    )
    assert page.results == threads[1:]
    assert page.page_info.start_cursor == page.results[0].last_post_id
    assert page.page_info.end_cursor == page.results[-1].last_post_id
    assert page.page_info.has_next_page is False
    assert page.page_info.has_previous_page is True
    assert page.page_info.next_cursor is None
    assert page.page_info.previous_cursor == threads[0].last_post_id


@pytest.mark.asyncio
async def test_threads_page_before_cursor_is_retrieved(thread, threads):
    page = await get_threads_page(
        10,
        categories_ids=[thread.category_id],
        before=threads[-1].last_post_id,
    )
    assert page.results == threads[:-1]
    assert page.page_info.start_cursor == page.results[0].last_post_id
    assert page.page_info.end_cursor == page.results[-1].last_post_id
    assert page.page_info.has_next_page is True
    assert page.page_info.has_previous_page is False
    assert page.page_info.next_cursor == threads[-1].last_post_id
    assert page.page_info.previous_cursor is None


@pytest.mark.asyncio
async def test_threads_page_is_filtered_by_starter(user_thread, threads):
    page = await get_threads_page(
        10,
        categories_ids=[user_thread.category_id],
        starter_id=user_thread.starter_id,
    )
    assert page.results == [user_thread]


@pytest.mark.asyncio
async def test_threads_page_is_filtered_by_categories(threads, closed_category_thread):
    page = await get_threads_page(
        10,
        categories_ids=[closed_category_thread.category_id],
    )
    assert page.results == [closed_category_thread]
