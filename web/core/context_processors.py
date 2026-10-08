# web/core/context_processors.py
# Para no repetir código en las vistas, 
# se puede usar un context processor para pasar la variable a todas las 
# plantillas.
import requests
from django.conf import settings

def pedidos_cliente_context(request):
    token = request.session.get('access_token')
    cliente_id = request.session.get('cliente_id')
    tiene_pedidos = False

    if token and cliente_id:
        base_api = settings.API_BASE_URL.rstrip('/')
        if not base_api.endswith('/api'):
            base_api = f"{base_api}/api"

        headers = {'Authorization': f'Bearer {token}'}

        try:
            res_pedidos = requests.get(f"{base_api}/pedidos/", headers=headers, timeout=3)
            if res_pedidos.status_code == 200:
                data_p = res_pedidos.json()
                lista_p = data_p.get('results', data_p) if isinstance(data_p, dict) else data_p
                
                for p in lista_p:
                    c_id = p.get('cliente')
                    if isinstance(c_id, dict):
                        c_id = c_id.get('id')
                    if c_id == cliente_id:
                        tiene_pedidos = True
                        break
        except requests.exceptions.RequestException:
            tiene_pedidos = False

    return {
        'usuario_tiene_pedidos': tiene_pedidos
    }