# desktop/app/components/factura_dialog.py
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
    QHBoxLayout
)
from style.components.factura_dialog_style import ESTILO_DIALOG_FACTURA

class FacturaDialog(QDialog):

    def __init__(self, factura, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Factura #{factura['id']}")
        self.resize(520, 460)
        
        # Seteo de la hoja de estilos unificada
        self.setStyleSheet(ESTILO_DIALOG_FACTURA)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # Cabecera de diálogo
        title = QLabel(f"Factura #{factura['id']}  —  Pedido #{factura['pedido']}")
        title.setObjectName("title_dialog")
        layout.addWidget(title)

        status_text = "🟢 Pagada" if factura.get('pagada') else "🔴 Pendiente de Pago"
        status_label = QLabel(f"Estado del documento: {status_text}")
        status_label.setStyleSheet("font-weight: 600; color: #4a5568;")
        layout.addWidget(status_label)

        date_label = QLabel(f"Fecha de emisión: {factura.get('fecha_emision', '-')}")
        date_label.setStyleSheet("color: #718096;")
        layout.addWidget(date_label)

        total_label = QLabel(f"Monto Total Recaudado: ${factura.get('total', 0)}")
        total_label.setObjectName("total_dialog")
        layout.addWidget(total_label)

        details_label = QLabel("Items / Conceptos facturados:")
        details_label.setStyleSheet("font-weight: bold; color: #1e1e24;")
        layout.addWidget(details_label)

        # Procesamiento del desglose de productos formato Ticket
        text = ""
        for detalle in factura.get('detalles', []):
            producto = detalle.get('producto', {})
            nombre = producto.get('nombre', 'Producto')
            cantidad = detalle.get('cantidad', 0)
            precio_unitario = detalle.get('precio_unitario', 0)
            subtotal = detalle.get('subtotal', 0)
            text += f"• {nombre:<25} x{cantidad:<4} @ ${precio_unitario:<8} = ${subtotal}\n"

        detalles = QTextEdit()
        detalles.setReadOnly(True)
        detalles.setPlainText(text if text else "Sin detalles disponibles de artículos.")
        layout.addWidget(detalles)

        # Layout inferior de cierre
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        close_button = QPushButton("Cerrar Visor")
        close_button.setObjectName("btn_cerrar_dialog")
        from PyQt6.QtCore import Qt # Asegurar importación del cursor
        close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)