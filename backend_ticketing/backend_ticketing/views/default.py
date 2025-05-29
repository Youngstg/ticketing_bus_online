# backend_ticketing/views/default.py
from pyramid.view import view_config
from pyramid.response import Response
from ..models.mymodel import Bus # Impor model yang relevan

@view_config(route_name='home', renderer='json')
def home_view(request):
    return {'message': 'Welcome to Whiish Bus Ticketing API'}


# @view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
# def home_view(request):
#     # Dapatkan sesi dari request
#     db_session = request.dbsession
#     try:
#         buses = db_session.query(Bus).order_by(Bus.name).all()
#     except Exception as e:
#         # Handle error jika ada, misalnya log error
#         print(f"Error querying buses: {e}")
#         buses = []
#     return {'project': 'Backend Ticketing', 'buses': buses}

# @view_config(route_name='add_bus_form', renderer='string') # Contoh sederhana tanpa template
# def add_bus_form_view(request):
#     # Contoh cara menambah data
#     if request.method == 'POST':
#         bus_name = request.params.get('name')
#         bus_capacity = request.params.get('capacity')
#         if bus_name and bus_capacity:
#             try:
#                 new_bus = Bus(name=bus_name, capacity=int(bus_capacity))
#                 request.dbsession.add(new_bus)
#                 # request.dbsession.flush() # Untuk mendapatkan ID jika perlu sebelum commit
#                 # Transaksi akan di-commit oleh pyramid_tm
#                 return Response(f"Bus '{bus_name}' added! (Check database or home page)")
#             except Exception as e:
#                 return Response(f"Error adding bus: {e}", status=500)
#         else:
#             return Response("Name and capacity are required.", status=400)

#     # Form HTML sederhana untuk GET request
#     return """
#     <form method="POST">
#         <label for="name">Bus Name:</label><br>
#         <input type="text" id="name" name="name"><br>
#         <label for="capacity">Capacity:</label><br>
#         <input type="number" id="capacity" name="capacity"><br><br>
#         <input type="submit" value="Add Bus">
#     </form>
#     """

# def includeme(config):
#     config.add_static_view('static', 'static', cache_max_age=3600)
#     config.add_route('home', '/')
#     config.add_route('add_bus_form', '/add_bus')
#     config.scan()