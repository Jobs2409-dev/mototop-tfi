# C:\Users\jonat\MotoTop\desktop\app\views\pedido_view.py
import traceback
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QScrollArea,
    QMessageBox
)
from PyQt6.QtCore import Qt
from components.pedido_card import PedidoCard
from form.pedido_form import PedidoForm
from style.views.pedido_view_style import ESTILO_ADMIN_PEDIDOS

class PedidoView(QWidget):

    def __init__(self, pedido_service, cliente_service, vendedor_service, producto_service):
        super().__init__()

        self.service = pedido_service
        self.cliente_service = cliente_service
        self.vendedor_service = vendedor_service
        self.producto_service = producto_service

        # ID para controlar el fondo general desde el QSS
        self.setObjectName("main_view")
        self.setStyleSheet(ESTILO_ADMIN_PEDIDOS)

        # Layout principal con mejor espaciado (padding)
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Contenedor de botones horizontales
        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(10)
        
        # Botón Nuevo Pedido configurado con su ID de estilo
        self.btn_new = QPushButton("Nuevo pedido")
        self.btn_new.setObjectName("btn_nuevo_pedido")
        self.btn_new.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_new.clicked.connect(self.open_form)
        botones_layout.addWidget(self.btn_new)

        # Botón Refrescar
        self.btn_refrescar = QPushButton("Refrescar")
        self.btn_refrescar.setObjectName("btn_refrescar")
        self.btn_refrescar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_refrescar.clicked.connect(self.refresh_pedidos)
        botones_layout.addWidget(self.btn_refrescar)

        # Botón Limpiar Pantalla
        self.btn_limpiar = QPushButton("Limpiar pantalla")
        self.btn_limpiar.setObjectName("btn_limpiar")
        self.btn_limpiar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_limpiar.clicked.connect(self.limpiar_pantalla)
        botones_layout.addWidget(self.btn_limpiar)
        
        # Agregar stretch para que los botones se alineen a la izquierda
        botones_layout.addStretch()
        
        layout.addLayout(botones_layout)

        # Configuración del área de Scroll
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        # Contenedor interno del scroll
        self.container = QWidget()
        self.container.setObjectName("scroll_container")
        
        # Layout de la lista (Separación sutil de 10px entre cada tarjeta de pedido)
        self.list_layout = QVBoxLayout()
        self.list_layout.setContentsMargins(10, 10, 10, 10)
        self.list_layout.setSpacing(10) 
        
        self.container.setLayout(self.list_layout)
        self.scroll.setWidget(self.container)

        layout.addWidget(self.scroll)
        self.setLayout(layout)


        self.load_data()
        
    def load_data(self, nuevo_pedido=None):
        try:
            # 1. Limpieza segura de la UI existente
            while self.list_layout.count():
                item = self.list_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
                else:
                    del item 

            # 2. Consumo del servicio
            pedidos = self.service.listar()
            
            # Si el servicio devuelve un entero (ej: código de error) o None, abortamos preventivamente
            if isinstance(pedidos, int) or pedidos is None:
                raise TypeError("La API no devolvió una respuesta válida.")

            pedidos_data = pedidos.get("results", pedidos)

            # Si el resultado no es una lista o es un diccionario vacío, normalizamos
            if not isinstance(pedidos_data, list):
                pedidos_data = []

            # 3. Validación de seguridad para nuevo_pedido
            # Si nuevo_pedido es un entero (ID), evitamos que rompa la validación .get()
            if nuevo_pedido is not None and isinstance(nuevo_pedido, dict):
                pedido_id = nuevo_pedido.get("id")
                if pedido_id is not None and not any(isinstance(p, dict) and p.get("id") == pedido_id for p in pedidos_data):
                    pedidos_data.insert(0, nuevo_pedido)

            # 4. Renderizado de Tarjetas con control de tipo
            for pedido in pedidos_data:
                # Nos aseguramos de que cada pedido sea efectivamente un diccionario antes de crear la Card
                if isinstance(pedido, dict):
                    card = PedidoCard(
                        pedido,
                        self.service,
                        self.load_data
                    )
                    self.list_layout.addWidget(card)

            self.list_layout.addStretch()

        except Exception as e:
            error_msg = str(e)
            print(f"Error cargando pedidos: {error_msg}")
            import traceback
            print(traceback.format_exc())
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los pedidos: {error_msg}")
     
     
    def open_form(self):
        self.form = PedidoForm(
            self.service,
            self.cliente_service,
            self.vendedor_service,
            self.producto_service,
            self.load_data
        )
        self.form.show()

    def refresh_pedidos(self):
        """Recarga la lista de pedidos desde el servidor"""
        self.load_data()

    def limpiar_pantalla(self):
        """Limpia todos los pedidos de la pantalla"""
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                del item
        self.list_layout.addStretch()

