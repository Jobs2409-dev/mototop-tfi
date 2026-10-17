# desktop/app/views/solicitud_visita_view.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QComboBox
)
from PyQt6.QtCore import Qt
from style.views.solicitud_visita_styles import ESTILO_SOLICITUD_VISITA


class SolicitudVisitaView(QWidget):
    def __init__(self, solicitud_service, vendedor_service):
        super().__init__()
        self.solicitud_service = solicitud_service
        self.vendedor_service = vendedor_service
        self.vendedores_cache = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)

        # Barra Superior de Acciones
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        
        btn_recargar = QPushButton("Recargar")
        btn_recargar.setObjectName("btn_recargar")
        btn_recargar.clicked.connect(self.load_data)

        top_layout.addWidget(btn_recargar)
        top_layout.addStretch()
        layout.addLayout(top_layout)

        # Configuración de Tabla
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "ID", "Comercio", "Contacto", "Teléfono", "Email", "Dirección", "Zona", "Vendedor Asignado", "Estado"
        ])
        
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setDefaultSectionSize(40)
        self.table.setShowGrid(True)
        
        layout.addWidget(self.table)

        # Aplicar Hoja de Estilos
        self.setStyleSheet(ESTILO_SOLICITUD_VISITA)

        self.load_data()

    def load_vendedores(self):
        """Carga los vendedores desde la API a través de VendedorService/HttpClient"""
        try:
            # Obtener lista de vendedores activos/totales de la API
            res = self.vendedor_service.http.get("vendedores/")
            if res.status_code == 200:
                data = res.json()
                self.vendedores_cache = data.get("results", data) if isinstance(data, dict) else data
            else:
                self.vendedores_cache = []
        except Exception:
            self.vendedores_cache = []

    def load_data(self):
        # 1. Cargar lista actualizada de vendedores
        self.load_vendedores()

        # 2. Cargar solicitudes de visita
        solicitudes = self.solicitud_service.obtener_solicitudes()
        self.table.setRowCount(0)

        for row, s in enumerate(solicitudes):
            self.table.insertRow(row)

            solicitud_id = s.get("id")

            # Datos básicos
            item_id = QTableWidgetItem(str(solicitud_id or ""))
            item_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.table.setItem(row, 0, item_id)
            self.table.setItem(row, 1, QTableWidgetItem(str(s.get("comercio", ""))))
            self.table.setItem(row, 2, QTableWidgetItem(str(s.get("contacto", ""))))
            self.table.setItem(row, 3, QTableWidgetItem(str(s.get("telefono", ""))))
            self.table.setItem(row, 4, QTableWidgetItem(str(s.get("email", ""))))
            self.table.setItem(row, 5, QTableWidgetItem(f"{s.get('direccion', '')} ({s.get('localidad', '')})"))

            # Zona
            zona_data = s.get("zona")
            zona_nombre = zona_data.get("nombre") if isinstance(zona_data, dict) else str(zona_data or "")
            self.table.setItem(row, 6, QTableWidgetItem(zona_nombre))

            # =========================================================
            # DESPLEGABLE DE VENDEDORES (QComboBox)
            # =========================================================
            combo_vendedor = QComboBox()
            combo_vendedor.addItem("Sin Asignar", None)

            vendedor_actual = s.get("vendedor")
            vendedor_actual_id = vendedor_actual.get("id") if isinstance(vendedor_actual, dict) else vendedor_actual

            for v in self.vendedores_cache:
                v_id = v.get("id")
                v_nombre = f"{v.get('nombre', '')} {v.get('apellido', '')}".strip()
                combo_vendedor.addItem(v_nombre, v_id)

            # Seleccionar vendedor asignado actualmente
            if vendedor_actual_id:
                index = combo_vendedor.findData(vendedor_actual_id)
                if index >= 0:
                    combo_vendedor.setCurrentIndex(index)

            combo_vendedor.blockSignals(True)
            self.table.setCellWidget(row, 7, combo_vendedor)
            combo_vendedor.blockSignals(False)

            combo_vendedor.currentIndexChanged.connect(
                lambda idx, sid=solicitud_id, cb=combo_vendedor: self.on_vendedor_changed(sid, cb)
            )

            # =========================================================
            # DESPLEGABLE DE ESTADO (QComboBox)
            # =========================================================
            combo_estado = QComboBox()
            estados = [
                ("Pendiente", "pendiente"),
                ("Asignado", "asignado"),
                ("Contactado", "contactado"),
                ("Cancelado", "cancelado"),
            ]
            
            for texto, valor in estados:
                combo_estado.addItem(texto, valor)

            estado_actual = str(s.get("estado", "pendiente")).lower()
            idx_e = combo_estado.findData(estado_actual)
            if idx_e >= 0:
                combo_estado.setCurrentIndex(idx_e)

            combo_estado.blockSignals(True)
            self.table.setCellWidget(row, 8, combo_estado)
            combo_estado.blockSignals(False)

            combo_estado.currentIndexChanged.connect(
                lambda idx, sid=solicitud_id, cb=combo_estado: self.on_estado_changed(sid, cb)
            )

    def on_vendedor_changed(self, solicitud_id, combo_box):
        vendedor_id = combo_box.currentData()
        if not vendedor_id:
            return

        exito = self.solicitud_service.asignar_vendedor(solicitud_id, vendedor_id)

        if exito:
            QMessageBox.information(
                self, 
                "Éxito", 
                f"Solicitud #{solicitud_id} asignada a '{combo_box.currentText()}'."
            )
            # Al asignar vendedor, recargamos para que el estado se actualice automáticamente a 'Asignado'
            self.load_data()
        else:
            QMessageBox.warning(
                self, 
                "Error", 
                f"No se pudo asignar el vendedor a la solicitud #{solicitud_id}."
            )
            self.load_data()

    def on_estado_changed(self, solicitud_id, combo_box):
        nuevo_estado = combo_box.currentData()
        exito = self.solicitud_service.cambiar_estado(solicitud_id, nuevo_estado)

        if exito:
            QMessageBox.information(
                self, 
                "Éxito", 
                f"Estado de la solicitud #{solicitud_id} actualizado a '{combo_box.currentText()}'."
            )
        else:
            QMessageBox.warning(
                self, 
                "Error", 
                f"No se pudo actualizar el estado de la solicitud #{solicitud_id}."
            )
            self.load_data()