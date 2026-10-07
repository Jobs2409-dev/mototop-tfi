# desktop/app/components/compra_card.py
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
    QHBoxLayout,
    QFrame
)
from PyQt6.QtCore import Qt
from style.components.compra_card_styles import QSS_STYLE


class CompraCard(QWidget):

    def __init__(self, compra, service, refresh_callback):
        super().__init__()

        self.compra = compra
        self.service = service
        self.refresh = refresh_callback

        self.setStyleSheet(QSS_STYLE)

        # Usamos un layout principal transparente y metemos un QFrame interno
        # para simular la tarjeta sin interferir con layouts del QGridLayout exterior
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        card_frame = QFrame()
        card_frame.setObjectName("card_frame")
        
        card_layout = QVBoxLayout(card_frame)
        card_layout.setContentsMargins(15, 15, 15, 15)
        card_layout.setSpacing(8)

        # Header interno de la card (ID y Estado lado a lado)
        header_layout = QHBoxLayout()
        
        lbl_id = QLabel(f"Compra #{compra['id']}")
        lbl_id.setObjectName("lbl_id")
        header_layout.addWidget(lbl_id)
        header_layout.addStretch()

        lbl_estado = QLabel(compra['estado'])
        if compra['estado'] == "recibida":
            lbl_estado.setObjectName("lbl_estado_recibida")
        else:
            lbl_estado.setObjectName("lbl_estado_pendiente")
            
        header_layout.addWidget(lbl_estado)
        card_layout.addLayout(header_layout)

        # Datos informativos en gris intermedio
        proveedor = compra.get("proveedor")
        card_layout.addWidget(QLabel(f"<b>Proveedor:</b> {proveedor}"))
        card_layout.addWidget(QLabel(f"📅 {compra['fecha_compra']}"))

        # Sección de productos
        lbl_prod_title = QLabel("📦 Productos:")
        lbl_prod_title.setStyleSheet("font-weight: bold; margin-top: 5px; color: #212529;")
        card_layout.addWidget(lbl_prod_title)

        for detalle in compra["detalles"]:
            producto = detalle["producto"]["nombre"]
            cantidad = detalle["cantidad"]
            lbl_item = QLabel(f"• {producto} x{cantidad}")
            lbl_item.setStyleSheet("color: #6c757d; margin-left: 5px;")
            card_layout.addWidget(lbl_item)

        card_layout.addSpacing(5)
        card_layout.addStretch()

        # Footer interno de la card (Total y Acción)
        footer_layout = QHBoxLayout()
        
        lbl_total = QLabel(f"${compra['total']}")
        lbl_total.setObjectName("lbl_total")
        footer_layout.addWidget(lbl_total, alignment=Qt.AlignmentFlag.AlignVCenter)
        footer_layout.addStretch()

        self.btn_recibir = QPushButton("Recibir")
        self.btn_recibir.setObjectName("btn_recibir")

        if compra["estado"] == "recibida":
            self.btn_recibir.setEnabled(False)

        self.btn_recibir.clicked.connect(self.recibir)
        footer_layout.addWidget(self.btn_recibir)
        
        card_layout.addLayout(footer_layout)
        
        main_layout.addWidget(card_frame)
        self.setLayout(main_layout)

    def recibir(self):
        try:
            self.service.recibir(self.compra["id"])
            QMessageBox.information(
                self,
                "OK",
                "Compra recibida"
            )
            self.refresh()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )
            
            