# desktop/app/dialogs/select_pedido_dialog.py
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QHeaderView,
    QAbstractItemView,
    QLabel
)

class SelectPedidoDialog(QDialog):

    def __init__(self, pedidos_disponibles, parent=None):
        super().__init__(parent)
        self.pedidos = pedidos_disponibles
        self.pedido_seleccionado = None

        self.setWindowTitle("Seleccionar Pedido Confirmado")
        self.resize(600, 380)

        layout = QVBoxLayout()
        layout.setSpacing(12)

        lbl = QLabel("Seleccione el pedido para el cual registrará el envío:")
        lbl.setStyleSheet("font-weight: bold; color: #495057;")
        layout.addWidget(lbl)

        # Tabla de selección
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID Pedido", "Cliente", "Fecha", "Total"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self._cargar_pedidos()
        layout.addWidget(self.table)

        # Botones
        btn_layout = QHBoxLayout()
        self.btn_confirmar = QPushButton("Seleccionar")
        self.btn_confirmar.setStyleSheet("""
            QPushButton {
                background-color: #ea4335;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #d93025; }
        """)
        self.btn_confirmar.clicked.connect(self._confirmar_seleccion)

        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.clicked.connect(self.reject)

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancelar)
        btn_layout.addWidget(self.btn_confirmar)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def _cargar_pedidos(self):
        self.table.setRowCount(len(self.pedidos))
        for row, p in enumerate(self.pedidos):
            cli = p.get("cliente", {})
            nombre_cli = f"{cli.get('nombre', '')} {cli.get('apellido', '')}".strip() if isinstance(cli, dict) else f"Cliente #{cli}"
            
            self.table.setItem(row, 0, QTableWidgetItem(f"#{p['id']}"))
            self.table.setItem(row, 1, QTableWidgetItem(nombre_cli))
            self.table.setItem(row, 2, QTableWidgetItem(str(p.get("fecha_creacion", "-"))[:10]))
            self.table.setItem(row, 3, QTableWidgetItem(f"$ {float(p.get('total', 0)):.2f}"))

    def _confirmar_seleccion(self):
        row = self.table.currentRow()
        if row >= 0:
            self.pedido_seleccionado = self.pedidos[row]
            self.accept()