from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QHBoxLayout, QLabel, QScrollArea, QGridLayout, QMessageBox
)
from PyQt6.QtCore import Qt

from services.rubro_service import RubroService
from services.proveedor_service import ProveedorService
from form.producto_form import ProductoForm
from components.producto_card import ProductoCard
from style.views.producto_view_styles import ESTILO_PRODUCTO_VIEW


class ProductoView(QWidget):

    def __init__(self, producto_service):
        super().__init__()

        self.service = producto_service
        self.rubro_service = RubroService(self.service.http)
        self.proveedor_service = ProveedorService(self.service.http)

        self.page = 1
        self.has_next = False
        self.has_prev = False

        self.setStyleSheet(ESTILO_PRODUCTO_VIEW)

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # =========================
        # TOP BAR
        # =========================
        top_bar = QHBoxLayout()

        self.btn_new = QPushButton("Nuevo")
        self.btn_new.setObjectName("btn_nuevo_producto")

        self.btn_prev = QPushButton("Anterior")
        self.btn_prev.setProperty("class", "btn_secondary_action")

        self.btn_next = QPushButton("Siguiente")
        self.btn_next.setProperty("class", "btn_secondary_action")

        self.btn_refresh = QPushButton("Recargar")
        self.btn_refresh.setProperty("class", "btn_secondary_action")

        self.lbl_page = QLabel("Página: 1")
        self.lbl_page.setObjectName("lbl_numero_pagina")

        top_bar.addWidget(self.btn_new)
        top_bar.addWidget(self.btn_prev)
        top_bar.addWidget(self.btn_next)
        top_bar.addWidget(self.btn_refresh)
        top_bar.addWidget(self.lbl_page)
        top_bar.addStretch()

        self.btn_prev.clicked.connect(self.prev_page)
        self.btn_next.clicked.connect(self.next_page)
        self.btn_refresh.clicked.connect(self.load_data)
        self.btn_new.clicked.connect(self.open_form)

        # =========================
        # GRID DE CARDS
        # =========================
        self.container = QWidget()
        self.grid = QGridLayout()
        self.grid.setSpacing(12)
        self.grid.setContentsMargins(0, 0, 0, 0)

        # Repartir equitativamente el ancho en 3 columnas
        for col in range(3):
            self.grid.setColumnStretch(col, 1)

        self.container.setLayout(self.grid)

        self.scroll = QScrollArea()
        self.scroll.setObjectName("scroll_productos")
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll.setWidget(self.container)

        layout.addLayout(top_bar)
        layout.addWidget(self.scroll)

        self.setLayout(layout)
        self.load_data()

    # =========================

    def load_data(self):
        try:
            data = self.service.listar(self.page)

            productos = data.get("results", data)
            self.has_next = data.get("next") is not None
            self.has_prev = data.get("previous") is not None

            # Limpiar grid
            for i in reversed(range(self.grid.count())):
                widget = self.grid.itemAt(i).widget()
                if widget:
                    widget.setParent(None)

            cols = 3
            for i, p in enumerate(productos):
                card = ProductoCard(p, self.service, self.load_data)
                
                row = i // cols
                col = i % cols
                self.grid.addWidget(card, row, col)

            self.lbl_page.setText(f"Página: {self.page}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los productos: {str(e)}")

    # =========================

    def next_page(self):
        if self.has_next:
            self.page += 1
            self.load_data()

    def prev_page(self):
        if self.has_prev:
            self.page -= 1
            self.load_data()

    # =========================

    def open_form(self):
        self.form = ProductoForm(
            self.service,
            self.rubro_service,
            self.proveedor_service,
            self.load_data
        )
        self.form.show()