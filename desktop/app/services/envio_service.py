# desktop/app/services/envio_service.py

class EnvioService:

    def __init__(self, http):
        self.http = http

    def _procesar_respuesta(self, response):
        """Verifica la respuesta de la API y extrae el mensaje de error de Django si existe."""
        if response.status_code >= 400:
            try:
                data = response.json()
                if isinstance(data, dict):
                    if "non_field_errors" in data:
                        mensaje = "\n".join(data["non_field_errors"])
                    elif "detail" in data:
                        mensaje = str(data["detail"])
                    else:
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
        return response.json() if response.content else {}

    def listar(self):
        response = self.http.get("envios/")
        return self._procesar_respuesta(response)

    def obtener(self, envio_id):
        response = self.http.get(f"envios/{envio_id}/")
        return self._procesar_respuesta(response)

    def crear(self, data):
        response = self.http.post("envios/", data=data)
        return self._procesar_respuesta(response)

    def actualizar(self, envio_id, data):
        response = self.http.put(f"envios/{envio_id}/", data=data)
        return self._procesar_respuesta(response)

    def eliminar(self, envio_id):
        response = self.http.delete(f"envios/{envio_id}/")
        if response.status_code >= 400:
            self._procesar_respuesta(response)