# C:\Users\jonat\MotoTop\desktop\app\views\envio_view.py
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
    QAbstractItemView
)

from services.pedido_service import PedidoService
from form.envio_form import EnvioForm
from views.select_pedido_envio_view import SelectPedidoEnvioView
from style.views.envio_view_styles import QSS_STYLE

class EnvioView(QWidget):

    def __init__(self, envio_service):
        super().__init__()

        self.envio_service = envio_service
        self.pedido_service = PedidoService(envio_service.http)

        self.init_ui()
        self.cargar_datos()

    def init_ui(self):
        self.setObjectName("EnvioView")
        self.setStyleSheet(QSS_STYLE)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Botones de Acción
        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(8)

        self.btn_actualizar = QPushButton("🔄 Actualizar")
        self.btn_crear = QPushButton("＋ Crear envío")
        self.btn_crear.setObjectName("btn_crear")
        self.btn_editar = QPushButton("✏️ Editar envío")

        botones_layout.addWidget(self.btn_actualizar)
        botones_layout.addWidget(self.btn_crear)
        botones_layout.addWidget(self.btn_editar)
        botones_layout.addStretch()

        # Tabla Estilizada
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID",
            "Pedido",
            "Cliente",
            "Empresa",
            "Tracking",
            "Estado",
        ])
        
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setStretchLastSection(True)

        layout.addLayout(botones_layout)
        layout.addWidget(self.table)

        self.setLayout(layout)

        # Eventos
        self.btn_actualizar.clicked.connect(self.cargar_datos)
        self.btn_crear.clicked.connect(self.crear_envio)
        self.btn_editar.clicked.connect(self.editar_envio)

    def cargar_datos(self):
        """Carga la lista de envíos mapeando clientes con una sola consulta a pedidos para no saturar la API."""
        try:
            envios_res = self.envio_service.listar()
            envios = envios_res.get("results", envios_res) if isinstance(envios_res, dict) else envios_res

            # Traer lista de pedidos en una sola petición para optimizar
            pedidos_res = self.pedido_service.listar()
            lista_pedidos = pedidos_res.get("results", pedidos_res) if isinstance(pedidos_res, dict) else pedidos_res
            
            # Crear mapa rápido por ID: {id: cliente_nombre}
            mapa_pedidos = {}
            for p in lista_pedidos:
                cli = p.get("cliente", {})
                if isinstance(cli, dict):
                    nombre_cli = f"{cli.get('nombre', '')} {cli.get('apellido', '')}".strip()
                else:
                    nombre_cli = f"Cliente #{cli}"
                mapa_pedidos[p["id"]] = nombre_cli

            self.table.setRowCount(len(envios))

            for row, envio in enumerate(envios):
                pedido_id = envio.get("pedido")
                
                # Si 'pedido' viene como diccionario anidado desde el backend
                if isinstance(pedido_id, dict):
                    p_id_str = str(pedido_id.get("id"))
                    cliente = mapa_pedidos.get(pedido_id.get("id"), "")
                else:
                    p_id_str = str(pedido_id)
                    cliente = mapa_pedidos.get(pedido_id, "")

                empresa = str(envio.get("empresa_transporte") or "")
                tracking = str(envio.get("tracking_code") or "")
                estado = str(envio.get("estado_envio") or "").upper()

                self.table.setItem(row, 0, QTableWidgetItem(str(envio["id"])))
                self.table.setItem(row, 1, QTableWidgetItem(f"Pedido #{p_id_str}"))
                self.table.setItem(row, 2, QTableWidgetItem(cliente))
                self.table.setItem(row, 3, QTableWidgetItem(empresa))
                self.table.setItem(row, 4, QTableWidgetItem(tracking if tracking else "-"))
                self.table.setItem(row, 5, QTableWidgetItem(estado))

        except Exception as e:
            QMessageBox.critical(self, "Error al Cargar Envíos", str(e))

    def crear_envio(self):
        dialog = EnvioForm(
            envio_service=self.envio_service,
            pedido_service=self.pedido_service,
            parent=self
        )
        if dialog.exec():
            self.cargar_datos()

    def abrir_formulario_envio(self, pedido):
        dialog = EnvioForm(
            pedido=pedido,
            envio_service=self.envio_service,
            on_success=self.cargar_datos
        )
        dialog.exec()

    def editar_envio(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Selección Requerida", "Debe seleccionar un envío para editar.")
            return

        try:
            envio_id = int(self.table.item(row, 0).text())
            envio = self.envio_service.obtener(envio_id)

            dialog = EnvioForm(
                envio_service=self.envio_service,
                pedido_service=self.pedido_service,
                envio=envio,
                parent=self
            )
            if dialog.exec():
                self.cargar_datos()

        except Exception as e:
            QMessageBox.warning(self, "Error al Editar", str(e))