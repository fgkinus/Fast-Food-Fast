from app.Accounts.Views import namespace as auth_ns
from app.MenuItems.Views import namespace as menu_ns

# A dictionary of key value pairs of namespace and path
urls = {
    auth_ns: '/api/v1',
    menu_ns: '/api/v1/menu'
}
