from controllers._base_controller import app
from controllers.index_controller import *
from controllers.admin_controller import *
from controllers.user_controller import *

# FastAPIのルーティング用関数
app.add_api_route('/', index)
app.add_api_route('/admin', admin)  # management view for administrator
app.add_api_route('/users', users)  # management view for administrator