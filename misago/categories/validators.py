from typing import Optional

from ..types import Category
from .errors import CategoryInvalidParentError


def validate_category_parent(
    category: Category, parent: Optional[Category]
) -> Optional[Category]:
    if parent:
        error = CategoryInvalidParentError(category_id=parent.id)
        if category.id == parent.id:
            raise error
        if parent.parent_id:
            raise error
        if category.is_parent(parent):
            raise error
        if category.has_children():
            raise error

    return parent