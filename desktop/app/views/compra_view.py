# desktop/app/views/compra_view.py
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QScrollArea,
    QGridLayout,
    QMessageBox,
    QHBoxLayout,
    QLabel
)

from components.compra_card import CompraCard
from form.compra_form import CompraForm

from services.proveedor_service import ProveedorService
from services.producto_service import ProductoService
from style.views.compra_view_styles import QSS_STYLE

class CompraView(QWidget):

    def __init__(self, compra_service):
        super().__init__()

        self.service = compra_service

        self.proveedor_service = ProveedorService(
            self.service.http
        )

        self.producto_service = ProductoService(
            self.service.http
        )

        self.setObjectName("CompraView")
        self.setStyleSheet(QSS_STYLE)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Encabezado superior alineado
        header_layout = QHBoxLayout()
        
        self.lbl_titulo = QLabel("Gestión de Compras")
        self.lbl_titulo.setObjectName("lbl_titulo")
        header_layout.addWidget(self.lbl_titulo)
        header_layout.addStretch()

        self.btn_new = QPushButton("＋ Nueva compra")
        self.btn_new.setObjectName("btn_new")
        self.btn_new.clicked.connect(self.open_form)
        header_layout.addWidget(self.btn_new)

        layout.addLayout(header_layout)

        # =========================
        # SCROLL
        # =========================

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.container = QWidget()
        self.container.setObjectName("scroll_container")

        self.grid = QGridLayout()
        self.grid.setSpacing(15)  # Separación limpia entre tarjetas

        self.container.setLayout(self.grid)
        self.scroll.setWidget(self.container)

        layout.addWidget(self.scroll)
        self.setLayout(layout)

        self.load_data()

    # =========================

    def load_data(self):
        try:
            while self.grid.count():
                item = self.grid.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

            compras = self.service.listar()
            compras_data = compras.get(
                "results",
                compras
            )

            row = 0
            col = 0

            for compra in compras_data:
                card = CompraCard(
                    compra,
                    self.service,
                    self.load_data
                )

                self.grid.addWidget(card, row, col)
                col += 1

                if col > 2:
                    col = 0
                    row += 1

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar las compras: {str(e)}")

    # =========================

    def open_form(self):
        self.form = CompraForm(
            self.service,
            self.proveedor_service,
            self.producto_service,
            self.load_data
        )
        self.form.show()
        
