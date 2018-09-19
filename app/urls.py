from app.V1.Accounts.Views import namespace as auth_ns
from app.V1.MenuItems.Views import namespace as menu_ns
from app.V1.Orders.Views import namespace as order_ns

# A dictionary of key value pairs of namespace and path
urls = {
    auth_ns: '/api/v1',
    menu_ns: '/api/v1/menu',
    order_ns: '/api/v1/orders'
}
