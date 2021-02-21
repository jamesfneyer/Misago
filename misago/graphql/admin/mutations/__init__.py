from .changesettings import change_settings_mutation
from .createcategory import create_category_mutation
from .editcategory import edit_category_mutation
from .login import login_mutation


mutations = [
    change_settings_mutation,
    create_category_mutation,
    edit_category_mutation,
    login_mutation,
]
