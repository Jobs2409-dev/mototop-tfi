# desktop/app/services/pago_service.py

class PagoService:

    def __init__(self, http):
        self.http = http

    def _procesar_respuesta(self, response):
        """
        Analiza el código de estado HTTP. 
        Si hay un error (400, 500, etc.), parsea el JSON del backend y lanza una Exception.
        """
        # Si el status code indica error
        if response.status_code >= 400:
            try:
                data = response.json()
                if isinstance(data, dict):
                    # Formatea mensajes de error de DRF/serializers
                    if "non_field_errors" in data:
                        mensaje = "\n".join(data["non_field_errors"])
                    elif "detail" in data:
                        mensaje = str(data["detail"])
                    else:
                        # Une los mensajes de validación por campo (ej. "monto: El monto no puede superar...")
                        errores = []
                        for campo, msgs in data.items():
                            msg_str = " ".join(msgs) if isinstance(msgs, list) else str(msgs)
                            errores.append(f"{campo.capitalize()}: {msg_str}")
                        mensaje = "\n".join(errores)
                elif isinstance(data, list):
                    mensaje = "\n".join(data)
                else:
                    mensaje = str(data)
            except Exception:
                mensaje = f"Error del servidor (HTTP {response.status_code})"
            
            raise Exception(mensaje)

        # Si todo salió bien y hay contenido, devuelve el JSON
        return response.json() if response.content else {}

    def listar(self):
        response = self.http.get("pagos/")
        return response.json()

    def obtener(self, pago_id):
        response = self.http.get(f"pagos/{pago_id}/")
        return response.json()

    def crear(self, data):
        response = self.http.post("pagos/", data=data)
        return self._procesar_respuesta(response)

    def actualizar(self, pago_id, data):
        response = self.http.put(f"pagos/{pago_id}/", data=data)
        return self._procesar_respuesta(response)

    def eliminar(self, pago_id):
        response = self.http.delete(f"pagos/{pago_id}/")
        if response.status_code >= 400:
            self._procesar_respuesta(response)

    def listar_por_factura(self, factura_id):
        response = self.http.get(f"pagos/?factura={factura_id}")
        return response.json()