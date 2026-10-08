# desktop/app/form/envio_form.py
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QComboBox,
    QDateTimeEdit,
    QFormLayout,
    QCheckBox
)
from PyQt6.QtCore import QDateTime, Qt
from dialogs.select_pedido_dialog import SelectPedidoDialog
from style.form.envio_form_styles import QSS_STYLE


class EnvioForm(QDialog):

    def __init__(self, envio_service, pedido_service, envio=None, parent=None):
        super().__init__(parent)

        self.envio_service = envio_service
        self.pedido_service = pedido_service
        self.envio = envio
        self.pedido_seleccionado = None

        self.setWindowTitle("Editar Envío" if envio else "Nuevo Envío de Transporte")
        self.resize(520, 540)
        self.setStyleSheet(QSS_STYLE)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(14)

        form_layout = QFormLayout()
        form_layout.setSpacing(12)

        # Campo / Selector de Pedido
        pedido_container = QHBoxLayout()
        self.lbl_pedido = QLabel("Ningún pedido seleccionado")
        self.lbl_pedido.setStyleSheet("font-weight: bold; color: #d93025;")
        
        self.btn_buscar_pedido = QPushButton("🔍 Buscar Pedido")
        self.btn_buscar_pedido.clicked.connect(self._buscar_pedido)
        
        pedido_container.addWidget(self.lbl_pedido)
        pedido_container.addStretch()
        pedido_container.addWidget(self.btn_buscar_pedido)
        form_layout.addRow("Pedido Asignado:", pedido_container)

        # Empresa Transporte
        self.empresa_transporte = QComboBox()
        self.empresa_transporte.setEditable(True)
        form_layout.addRow("Empresa de Transporte:", self.empresa_transporte)
        self._cargar_empresas_transporte()

        # Tracking
        self.tracking_code = QLineEdit()
        self.tracking_code.setPlaceholderText("Ej: TRK123456789")
        form_layout.addRow("Código de Tracking:", self.tracking_code)

        # Estado del Envío
        self.estado_envio = QComboBox()
        self.estado_envio.addItem("Recibido", "recibido")
        self.estado_envio.addItem("En preparación", "preparacion")
        self.estado_envio.addItem("Enviado", "enviado")
        self.estado_envio.addItem("Entregado", "entregado")
        self.estado_envio.addItem("Cancelado", "cancelado")
        form_layout.addRow("Estado:", self.estado_envio)

        # Fechas
        formato_display = "yyyy-MM-dd HH:mm"
        ahora = QDateTime.currentDateTime()

        self.fecha_envio = QDateTimeEdit()
        self.fecha_envio.setCalendarPopup(True)
        self.fecha_envio.setDateTime(ahora)
        self.fecha_envio.setDisplayFormat(formato_display)
        form_layout.addRow("Fecha de Envío:", self.fecha_envio)

        self.fecha_estimada = QDateTimeEdit()
        self.fecha_estimada.setCalendarPopup(True)
        self.fecha_estimada.setDateTime(ahora.addDays(3))
        self.fecha_estimada.setDisplayFormat(formato_display)
        form_layout.addRow("Fecha Estimada:", self.fecha_estimada)

        # Fecha Entrega (Opcional)
        entrega_container = QHBoxLayout()
        self.chk_entrega = QCheckBox("Registrar entrega final")
        self.chk_entrega.toggled.connect(lambda enabled: self.fecha_entrega.setEnabled(enabled))

        self.fecha_entrega = QDateTimeEdit()
        self.fecha_entrega.setCalendarPopup(True)
        self.fecha_entrega.setDateTime(ahora)
        self.fecha_entrega.setDisplayFormat(formato_display)
        self.fecha_entrega.setEnabled(False)

        entrega_container.addWidget(self.chk_entrega)
        entrega_container.addWidget(self.fecha_entrega)
        form_layout.addRow("Fecha Entrega:", entrega_container)

        main_layout.addLayout(form_layout)
        main_layout.addStretch()

        self.btn_save = QPushButton("Guardar Envío")
        self.btn_save.setObjectName("btn_save")
        self.btn_save.clicked.connect(self.save)
        main_layout.addWidget(self.btn_save)

        self.setLayout(main_layout)

        if self.envio:
            self._load_envio()

    def _buscar_pedido(self):
        try:
            pedidos_res = self.pedido_service.listar()
            pedidos = pedidos_res.get("results", pedidos_res) if isinstance(pedidos_res, dict) else pedidos_res
            pedidos_confirmados = [p for p in pedidos if p.get("estado") == "confirmado"]

            envios_res = self.envio_service.listar()
            envios = envios_res.get("results", envios_res) if isinstance(envios_res, dict) else envios_res
            pedidos_con_envio = {e["pedido"]["id"] if isinstance(e["pedido"], dict) else e["pedido"] for e in envios}

            # En modo edición permitimos conservar el pedido actual
            p_actual_id = self.pedido_seleccionado["id"] if self.pedido_seleccionado else None
            disponibles = [p for p in pedidos_confirmados if p["id"] not in pedidos_con_envio or p["id"] == p_actual_id]

            if not disponibles:
                QMessageBox.information(self, "Atención", "No hay pedidos confirmados sin envío asignado.")
                return

            dialog = SelectPedidoDialog(disponibles, self)
            if dialog.exec():
                self.pedido_seleccionado = dialog.pedido_seleccionado
                self.lbl_pedido.setText(f"Pedido #{self.pedido_seleccionado['id']}")
                self.lbl_pedido.setStyleSheet("font-weight: bold; color: #0d6efd;")

        except Exception as e:
            QMessageBox.critical(self, "Error al Cargar Pedidos", str(e))

    def _load_envio(self):
        p_id = self.envio["pedido"]["id"] if isinstance(self.envio["pedido"], dict) else self.envio["pedido"]
        try:
            self.pedido_seleccionado = self.pedido_service.obtener(p_id)
            self.lbl_pedido.setText(f"Pedido #{p_id}")
            self.lbl_pedido.setStyleSheet("font-weight: bold; color: #0d6efd;")
        except Exception:
            self.lbl_pedido.setText(f"Pedido #{p_id}")

        # Deshabilitar cambio de pedido en modo edición para mantener integridad
        self.btn_buscar_pedido.setEnabled(False)

        self.empresa_transporte.setCurrentText(self.envio.get("empresa_transporte", ""))
        self.tracking_code.setText(self.envio.get("tracking_code") or "")

        estado = self.envio.get("estado_envio", "recibido")
        idx = self.estado_envio.findData(estado)
        if idx >= 0:
            self.estado_envio.setCurrentIndex(idx)

        if self.envio.get("fecha_envio"):
            dt = QDateTime.fromString(self.envio["fecha_envio"], Qt.DateFormat.ISODate)
            if dt.isValid(): self.fecha_envio.setDateTime(dt)

        if self.envio.get("fecha_estimada"):
            dt = QDateTime.fromString(self.envio["fecha_estimada"], Qt.DateFormat.ISODate)
            if dt.isValid(): self.fecha_estimada.setDateTime(dt)

        if self.envio.get("fecha_entrega"):
            dt = QDateTime.fromString(self.envio["fecha_entrega"], Qt.DateFormat.ISODate)
            if dt.isValid():
                self.chk_entrega.setChecked(True)
                self.fecha_entrega.setDateTime(dt)

    def save(self):
        try:
            if not self.pedido_seleccionado:
                raise ValueError("Debe seleccionar un pedido para registrar el envío.")

            if not self.empresa_transporte.currentText().strip():
                raise ValueError("Debe indicar la empresa de transporte.")

            data = {
                "pedido": self.pedido_seleccionado["id"],
                "empresa_transporte": self.empresa_transporte.currentText().strip(),
                "tracking_code": self.tracking_code.text().strip() or None,
                "estado_envio": self.estado_envio.currentData(),
                "fecha_envio": self.fecha_envio.dateTime().toString(Qt.DateFormat.ISODate),
                "fecha_estimada": self.fecha_estimada.dateTime().toString(Qt.DateFormat.ISODate),
                "fecha_entrega": (
                    self.fecha_entrega.dateTime().toString(Qt.DateFormat.ISODate)
                    if self.chk_entrega.isChecked() else None
                ),
            }

            if self.envio:
                self.envio_service.actualizar(self.envio["id"], data)
                QMessageBox.information(self, "Éxito", "Envío actualizado correctamente.")
            else:
                self.envio_service.crear(data)
                QMessageBox.information(self, "Éxito", "Envío registrado correctamente.")

            self.accept()

        except ValueError as e:
            QMessageBox.warning(self, "Validación", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error al Guardar", str(e))

    def _cargar_empresas_transporte(self):
        try:
            envios = self.envio_service.listar()
            lista = envios.get("results", envios) if isinstance(envios, dict) else envios
            empresas = sorted({e.get("empresa_transporte", "").strip() for e in lista if e.get("empresa_transporte")})
            self.empresa_transporte.addItems(empresas)
        except Exception:
            pass