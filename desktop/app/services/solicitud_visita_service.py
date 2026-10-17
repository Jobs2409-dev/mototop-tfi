# desktop/app/services/solicitud_visita_service.py

class SolicitudVisitaService:
    def __init__(self, http_client):
        self.http = http_client

    def obtener_solicitudes(self):
        """Consulta todas las solicitudes de visita a la API central."""
        res = self.http.get("solicitudes-visita/")
        if res.status_code == 200:
            data = res.json()
            return data.get("results", data) if isinstance(data, dict) else data
        return []

    def asignar_vendedor(self, solicitud_id, vendedor_id):
        """Asigna un vendedor a una solicitud de visita específica."""
        res = self.http.post(
            f"solicitudes-visita/{solicitud_id}/asignar-vendedor/",
            {"vendedor_id": vendedor_id}
        )
        return res.status_code == 200

    def cambiar_estado(self, solicitud_id, nuevo_estado):
        """Actualiza el estado de la solicitud enviando el diccionario directamente al post."""
        res = self.http.post(
            f"solicitudes-visita/{solicitud_id}/cambiar-estado/",
            {"estado": nuevo_estado}
        )
        return res.status_code == 200