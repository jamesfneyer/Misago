from datetime import datetime
from typing import Any, Dict, Optional, Protocol

from .post import Post
from .thread import Thread
from .user import User


class CreatePostAction(Protocol):
    async def __call__(
        self,
        thread: Thread,
        body: dict,
        *,
        poster: Optional[User] = None,
        poster_name: Optional[str] = None,
        edits: Optional[int] = 0,
        posted_at: Optional[datetime] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> Post:
        ...


class CreatePostFilter(Protocol):
    async def __call__(
        self,
        action: CreatePostAction,
        thread: Thread,
        body: dict,
        *,
        poster: Optional[User] = None,
        poster_name: Optional[str] = None,
        edits: Optional[int] = 0,
        posted_at: Optional[datetime] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> Post:
        ...