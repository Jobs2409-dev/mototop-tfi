# desktop/app/views/factura_view.py
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QScrollArea,
    QMessageBox,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt

from style.views.factura_view_style import ESTILO_VIEW_FACTURA


class FacturaView(QWidget):

    def __init__(self, factura_service):
        super().__init__()

        self.service = factura_service
        self.setWindowTitle("Facturas")
        self.resize(550, 700)
        
        self.setObjectName("main_factura_view")
        self.setStyleSheet(ESTILO_VIEW_FACTURA)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        top_bar = QHBoxLayout()
        self.btn_refresh = QPushButton("Recargar")
        self.btn_refresh.setObjectName("btn_recargar")
        self.btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_refresh.clicked.connect(self.load_data)
        
        top_bar.addWidget(self.btn_refresh)
        top_bar.addStretch()
        layout.addLayout(top_bar)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.container = QWidget()
        self.container.setObjectName("scroll_container")
        
        self.list_layout = QVBoxLayout()
        self.list_layout.setSpacing(12) 
        self.list_layout.setContentsMargins(10, 10, 10, 10)
        self.container.setLayout(self.list_layout)

        self.scroll.setWidget(self.container)
        layout.addWidget(self.scroll)

        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        try:
            while self.list_layout.count():
                item = self.list_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
                else:
                    del item 

            facturas = self.service.listar()
            facturas_data = facturas.get("results", facturas)

            if not facturas_data:
                empty_label = QLabel("No hay facturas generadas.")
                empty_label.setObjectName("meta_info_factura")
                empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.list_layout.addWidget(empty_label)
            else:
                for factura in facturas_data:
                    self.list_layout.addWidget(self.build_card(factura))

            self.list_layout.addStretch()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar las facturas: {e}")

    def build_card(self, factura):
        card = QWidget()
        card.setObjectName("contenedor_factura_card")
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(15, 15, 15, 15)
        card_layout.setSpacing(10)

        # 1. Línea Superior: Título y Estado Badge
        header_layout = QHBoxLayout()
        title = QLabel(f"Factura #{factura['id']} — Pedido #{factura.get('pedido', '-')}")
        title.setObjectName("title_factura")
        
        is_pagada = factura.get("pagada", False)
        status_label = QLabel(" Pagada " if is_pagada else " Pendiente ")
        status_label.setObjectName("badge_pagada" if is_pagada else "badge_pendiente")
        status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        header_layout.addWidget(title)
        header_layout.addWidget(status_label)
        header_layout.addStretch()
        card_layout.addLayout(header_layout)

        # 2. Datos del Cliente
        pedido_data = factura.get('pedido_detalle') or {}
        cliente = factura.get('cliente') or pedido_data.get('cliente')
        if isinstance(cliente, dict):
            cliente_nombre = f"{cliente.get('nombre', '')} {cliente.get('apellido', '')}".strip()
            cliente_doc = cliente.get('nro_documento', '')
            cliente_text = f"Cliente: {cliente_nombre} (DNI/CUIT: {cliente_doc})" if cliente_doc else f"Cliente: {cliente_nombre}"
        elif cliente:
            cliente_text = f"Cliente ID: {cliente}"
        else:
            cliente_text = "Cliente: Mostrador / Consumidor Final"

        lbl_cliente = QLabel(cliente_text)
        lbl_cliente.setObjectName("cliente_factura")
        card_layout.addWidget(lbl_cliente)

        # 3. Línea Central: Fecha Formateada y Total
        info_layout = QHBoxLayout()
        
        fecha_raw = factura.get('fecha_emision', '')
        if fecha_raw:
            try:
                clean_date = str(fecha_raw).replace('Z', '').split('.')[0]
                dt = datetime.fromisoformat(clean_date)
                fecha_text = dt.strftime("%d/%m/%Y %H:%M hs")
            except Exception:
                fecha_text = str(fecha_raw)
        else:
            fecha_text = "-"

        date_label = QLabel(f"📅 Fecha: {fecha_text}")
        date_label.setObjectName("meta_info_factura")
        
        total_label = QLabel(f"Total: ${float(factura.get('total', 0)):.2f}")
        total_label.setObjectName("total_factura")
        
        info_layout.addWidget(date_label)
        info_layout.addStretch()
        info_layout.addWidget(total_label)
        card_layout.addLayout(info_layout)

        # 4. Desglose de Productos
        if factura.get('detalles'):
            prod_container = QWidget()
            prod_container.setStyleSheet("background-color: #f8f9fa; border-radius: 4px; padding: 5px;")
            prod_layout = QVBoxLayout(prod_container)
            prod_layout.setSpacing(4)
            prod_layout.setContentsMargins(8, 8, 8, 8)

            for detalle in factura['detalles']:
                product = detalle.get('producto', {})
                product_name = product.get('nombre', 'Producto') if isinstance(product, dict) else f"Prod ID: {product}"
                cantidad = detalle.get('cantidad', 0)
                subtotal = detalle.get('subtotal', 0)
                
                detail_line = QLabel(f"• {product_name} x{cantidad}  —  Subtotal: ${float(subtotal):.2f}")
                detail_line.setObjectName("meta_info_factura")
                prod_layout.addWidget(detail_line)
                
            card_layout.addWidget(prod_container)

        # 5. Línea Inferior: Acciones de Caja
        actions_layout = QHBoxLayout()
        btn_pagos = QPushButton("Administrar Pagos")
        btn_pagos.setObjectName("btn_pagos")
        btn_pagos.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_pagos.clicked.connect(lambda _, f=factura: self.abrir_pagos(f))
        
        actions_layout.addWidget(btn_pagos)
        actions_layout.addStretch()
        card_layout.addLayout(actions_layout)
        
        return card

    def abrir_pagos(self, factura):
        from services.pago_service import PagoService
        from views.pago_view import PagoView

        pago_service = PagoService(self.service.http)

        self.pago_view = PagoView(
            factura=factura,
            pago_service=pago_service
        )
        self.pago_view.show()