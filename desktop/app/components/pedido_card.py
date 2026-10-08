# desktop/app/components/pedido_card.py
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
    QHBoxLayout
)
from PyQt6.QtCore import Qt

from components.factura_dialog import FacturaDialog
from style.components.pedido_card_styles import ESTILO_CARD_PEDIDO


class PedidoCard(QWidget):

    def __init__(self, pedido, service, refresh_callback):
        super().__init__()

        self.pedido = pedido
        self.service = service
        self.refresh = refresh_callback

        # 1. Aplicamos la hoja de estilos unificada
        self.setStyleSheet(ESTILO_CARD_PEDIDO)

        # 2. Layout Raíz
        root_layout = QVBoxLayout()
        root_layout.setContentsMargins(0, 4, 0, 4)
        self.setLayout(root_layout)

        # 3. Marco físico contenedor de la tarjeta
        self.card_frame = QWidget()
        self.card_frame.setObjectName("contenedor_card")
        
        card_layout = QVBoxLayout(self.card_frame)
        card_layout.setContentsMargins(15, 15, 15, 15)
        card_layout.setSpacing(10)

        # ==========================================
        # PRIMERA LÍNEA: ID, CLIENTE, ESTADO
        # ==========================================
        header_layout = QHBoxLayout()
        
        id_label = QLabel(f"Pedido #{pedido['id']}")
        id_label.setObjectName("id_pedido")
        
        cliente = pedido.get('cliente')
        if isinstance(cliente, dict):
            nombre_cliente = f"{cliente.get('nombre', '')} {cliente.get('apellido','')}".strip()
        elif isinstance(cliente, int) or (isinstance(cliente, str) and str(cliente).isdigit()):
            nombre_cliente = f"Cliente ID: {cliente}"
        else:
            nombre_cliente = "Cliente no especificado"

        cliente_label = QLabel(nombre_cliente)
        cliente_label.setObjectName("cliente_pedido")
        
        estado_raw = pedido.get('estado', 'pendiente')
        estado = estado_raw.lower() if estado_raw else 'pendiente'
        
        estado_label = QLabel(f" {estado.capitalize()} ")
        estado_label.setObjectName(f"badge_{estado}")
        estado_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        header_layout.addWidget(id_label)
        header_layout.addWidget(cliente_label)
        header_layout.addWidget(estado_label)
        header_layout.addStretch()
        card_layout.addLayout(header_layout)
        
        # ==========================================
        # SEGUNDA LÍNEA: VENDEDOR, ORIGEN, FECHA, TOTAL
        # ==========================================
        details_layout = QHBoxLayout()
        
        # Identificación comercial del vendedor / canal
        vendedor = pedido.get('vendedor')
        origen_raw = pedido.get('origen', 'N/A')
        origen_str = str(origen_raw).lower()

        if isinstance(vendedor, dict):
            nombre = vendedor.get('nombre', '')
            apellido = vendedor.get('apellido', '')
            vendedor_text = f"{nombre} {apellido}".strip() or "Vendedor sin nombre"
        elif vendedor is not None:
            vendedor_text = f"Vendedor #{vendedor}"
        elif origen_str == 'mobile':
            vendedor_text = "Vendedor Mobile (No asignado)"
        elif origen_str == 'web':
            vendedor_text = "Tienda Online (Portal Web)"
        elif origen_str == 'local':
            vendedor_text = "MOTO-TOP (Casa Central)"
        else:
            vendedor_text = "Venta Directa"

        vendedor_label = QLabel(f"Vend: {vendedor_text}")
        vendedor_label.setObjectName("meta_info")

        # Etiqueta de Origen
        origen_label = QLabel(f"Origen: {str(origen_raw).capitalize()}")
        origen_label.setObjectName("meta_info")

        # Formateo legible de fecha y hora
        fecha_raw = pedido.get('fecha_pedido', '')
        if fecha_raw:
            try:
                clean_date = str(fecha_raw).replace('Z', '').split('.')[0]
                dt = datetime.fromisoformat(clean_date)
                fecha_text = dt.strftime("%d/%m/%Y %H:%M hs")
            except Exception:
                fecha_text = str(fecha_raw)
        else:
            fecha_text = "-"

        fecha_label = QLabel(f"📅 {fecha_text}")
        fecha_label.setObjectName("meta_info")
        
        total_label = QLabel(f"Total: ${float(pedido.get('total', 0)):.2f}")
        total_label.setObjectName("total_pedido")

        details_layout.addWidget(vendedor_label)
        details_layout.addWidget(origen_label)
        details_layout.addWidget(fecha_label)
        details_layout.addStretch()
        details_layout.addWidget(total_label)
        card_layout.addLayout(details_layout)

        # ==========================================
        # TERCERA LÍNEA: DETALLE DE PRODUCTOS
        # ==========================================
        if pedido.get('detalles'):
            productos_layout = QHBoxLayout()
            productos_text = []
            for d in pedido['detalles']:
                producto = d.get('producto')
                if isinstance(producto, dict):
                    productos_text.append(f"{producto.get('nombre', 'Producto')} x{d.get('cantidad', 1)}")
                else:
                    productos_text.append(f"Prod ID: {producto} x{d.get('cantidad', 1)}")
            
            productos_label = QLabel(" • ".join(productos_text))
            productos_label.setObjectName("meta_info")
            productos_label.setWordWrap(True)
            productos_layout.addWidget(productos_label)
            card_layout.addLayout(productos_layout)

        # ==========================================
        # CUARTA LÍNEA: ACCIONES DISPONIBLES
        # ==========================================
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(8)

        if estado == 'pendiente':
            btn_confirmar = QPushButton("Confirmar")
            btn_confirmar.setObjectName("btn_confirmar")
            btn_confirmar.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_confirmar.clicked.connect(self.confirmar_pedido)

            btn_cancelar = QPushButton("Cancelar")
            btn_cancelar.setObjectName("btn_cancelar")
            btn_cancelar.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_cancelar.clicked.connect(self.cancelar_pedido)

            actions_layout.addWidget(btn_confirmar)
            actions_layout.addWidget(btn_cancelar)
            actions_layout.addStretch()
            card_layout.addLayout(actions_layout)

        elif estado == 'confirmado':
            if not pedido.get('facturada', False):
                btn_factura = QPushButton("Generar factura")
                btn_factura.setObjectName("btn_factura")
                btn_factura.setCursor(Qt.CursorShape.PointingHandCursor)
                btn_factura.clicked.connect(self.generar_factura)
                actions_layout.addWidget(btn_factura)
            else:
                btn_ver_factura = QPushButton("Ver factura")
                btn_ver_factura.setObjectName("btn_factura")
                btn_ver_factura.setCursor(Qt.CursorShape.PointingHandCursor)
                btn_ver_factura.clicked.connect(self.ver_factura)
                actions_layout.addWidget(btn_ver_factura)
            
            actions_layout.addStretch()
            card_layout.addLayout(actions_layout)

        root_layout.addWidget(self.card_frame)

    # ==========================================
    # MÉTODOS OPERATIVOS
    # ==========================================
    def confirmar_pedido(self):
        box = QMessageBox(self)
        box.setWindowTitle("Confirmar Pedido")
        box.setText("¿Está seguro de que desea confirmar este pedido?")
        btn_si = box.addButton("Sí", QMessageBox.ButtonRole.YesRole)
        btn_no = box.addButton("No", QMessageBox.ButtonRole.NoRole)
        box.exec()

        if box.clickedButton() != btn_si:
            return

        try:
            self.service.confirmar(self.pedido['id'])

            # Si el pedido es local, facturamos directo en mostrador
            if self.pedido.get('origen') == 'local':
                self.service.generar_factura(self.pedido['id'])
                QMessageBox.information(
                    self, 
                    "Venta Concretada", 
                    "Pedido confirmado y Factura generada automáticamente."
                )
            else:
                box_factura = QMessageBox(self)
                box_factura.setWindowTitle("Generar Factura")
                box_factura.setText("Pedido confirmado. ¿Desea generar la factura comercial ahora?")
                btn_fact_si = box_factura.addButton("Sí", QMessageBox.ButtonRole.YesRole)
                btn_fact_no = box_factura.addButton("No", QMessageBox.ButtonRole.NoRole)
                box_factura.exec()

                if box_factura.clickedButton() == btn_fact_si:
                    self.generar_factura()

            self.refresh()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo confirmar el pedido: {e}")

    def cancelar_pedido(self):
        box = QMessageBox(self)
        box.setWindowTitle("Cancelar Pedido")
        box.setText("¿Está seguro de que desea cancelar este pedido?")
        btn_si = box.addButton("Sí", QMessageBox.ButtonRole.YesRole)
        btn_no = box.addButton("No", QMessageBox.ButtonRole.NoRole)
        box.exec()

        if box.clickedButton() != btn_si:
            return

        try:
            self.service.cancelar(self.pedido['id'])
            QMessageBox.information(
                self,
                "Pedido cancelado",
                "El pedido fue cancelado correctamente."
            )
            self.refresh()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cancelar el pedido: {e}")

    def generar_factura(self):
        try:
            self.service.generar_factura(self.pedido['id'])
            QMessageBox.information(
                self,
                "Factura creada",
                "La factura se generó correctamente."
            )
            self.refresh()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo generar la factura: {e}")

    def ver_factura(self):
        try:
            factura = self.service.obtener_factura(self.pedido['id'])
            dialog = FacturaDialog(factura, self)
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar la factura: {e}")