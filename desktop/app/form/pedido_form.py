# desktop/app/form/pedido_form.py
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QMessageBox,
    QLabel,
    QComboBox,
    QHBoxLayout,
    QSpinBox,
    QTextEdit,
    QApplication,
    QFormLayout
)
from PyQt6.QtCore import Qt
from style.form.pedidos_form_styles import ESTILO_FORM_PEDIDO

from form.cliente_form import ClienteForm
from services.zona_service import ZonaService
from services.user_service import UserService

class PedidoForm(QWidget):

    def __init__(self, pedido_service, cliente_service, v_service, producto_service, on_success):
        super().__init__()

        self.pedido_service = pedido_service
        self.cliente_service = cliente_service
        self.vendedor_service = v_service
        self.producto_service = producto_service
        self.on_success = on_success

        self.setWindowTitle("Nuevo Pedido")
        self.resize(500, 600)
        self.setObjectName("pedido_form_window")
        self.setStyleSheet(ESTILO_FORM_PEDIDO)

        self.productos_cache = [] # Cache local para evitar peticiones HTTP repetitivas
        self.productos = []

        # Layout Principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Form Layout para alinear campos limpia y ordenadamente
        form_layout = QFormLayout()
        form_layout.setSpacing(12)

        # Combo Cliente + Botón de alta rápida (ÚNICA FILA)
        cliente_layout = QHBoxLayout()
        self.cliente_combo = QComboBox()
        self.btn_add_cliente = QPushButton("+")
        self.btn_add_cliente.setObjectName("btn_add_cliente")
        self.btn_add_cliente.setFixedWidth(35)
        self.btn_add_cliente.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_add_cliente.clicked.connect(self.abrir_nuevo_cliente)
        
        cliente_layout.addWidget(self.cliente_combo)
        cliente_layout.addWidget(self.btn_add_cliente)
        form_layout.addRow("Cliente:", cliente_layout)
        
        # Combo Vendedor
        self.vendedor_combo = QComboBox()
        self.vendedor_combo.addItem("Sin vendedor", None)
        form_layout.addRow("Vendedor (opcional):", self.vendedor_combo)

        # Combo Origen
        self.origen_combo = QComboBox()
        self.origen_combo.addItem("Local", "local")
        self.origen_combo.addItem("Mobile", "mobile")
        self.origen_combo.addItem("Web", "web")
        form_layout.addRow("Origen:", self.origen_combo)

        # Observaciones
        self.observaciones = QTextEdit()
        self.observaciones.setFixedHeight(70)
        form_layout.addRow("Observaciones:", self.observaciones)

        main_layout.addLayout(form_layout)

        # Sección dinámica de Artículos / Detalles
        lbl_articulos = QLabel("Artículos del Pedido")
        lbl_articulos.setStyleSheet("font-size: 14px; font-weight: bold; color: #1e1e24; border-bottom: 1px solid #cbd5e1; padding-bottom: 3px;")
        main_layout.addWidget(lbl_articulos)

        self.detalles_layout = QVBoxLayout()
        self.detalles_layout.setSpacing(8)
        main_layout.addLayout(self.detalles_layout)

        # Botones de Acción inferiores
        self.btn_add_producto = QPushButton("+ Agregar Producto")
        self.btn_add_producto.setObjectName("btn_agregar")
        self.btn_add_producto.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_add_producto.clicked.connect(self.add_producto_row)
        main_layout.addWidget(self.btn_add_producto)

        main_layout.addStretch()

        self.btn_save = QPushButton("GUARDAR PEDIDO")
        self.btn_save.setObjectName("btn_guardar_pedido")
        self.btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_save.clicked.connect(self.save)
        main_layout.addWidget(self.btn_save)

        self.setLayout(main_layout)

        # Inicialización de Datos y carga de filas
        self.preload_data()
        self.add_producto_row()

    def preload_data(self):
        """ Carga los datos iniciales y cachea la lista de productos de forma síncrona """
        try:
            # Clientes
            clientes = self.cliente_service.listar()
            clientes_data = clientes.get("results", clientes)
            for c in clientes_data:
                self.cliente_combo.addItem(f"{c['nombre']} {c.get('apellido','')}", c["id"])

            # Vendedores
            vendedores = self.vendedor_service.listar()
            vendedores_data = vendedores.get("results", vendedores)
            for v in vendedores_data:
                self.vendedor_combo.addItem(f"{v['nombre']} {v.get('apellido','')}", v["id"])

            # Cachear Productos de forma local
            prod_data = self.producto_service.listar()
            self.productos_cache = prod_data.get("results", prod_data)

        except Exception as e:
            QMessageBox.critical(self, "Error de Conexión", f"No se pudieron inicializar los datos: {e}")

    def add_producto_row(self):
        if not self.productos_cache:
            # Si falló la precarga o no hay productos, intentamos buscarlos una vez
            try:
                prod_data = self.producto_service.listar()
                self.productos_cache = prod_data.get("results", prod_data)
            except Exception:
                QMessageBox.warning(self, "Advertencia", "No hay productos cargados en el sistema.")
                return

        row = QHBoxLayout()
        row.setSpacing(8)

        combo = QComboBox()
        for p in self.productos_cache:
            combo.addItem(p["nombre"], p["id"])

        cantidad = QSpinBox()
        cantidad.setMinimum(1)
        cantidad.setMaximum(9999)

        btn_delete = QPushButton("X")
        btn_delete.setObjectName("btn_eliminar_fila")
        btn_delete.setFixedWidth(30)
        btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)

        row.addWidget(combo, 4) # El combo toma más espacio horizontal
        row.addWidget(cantidad, 1)
        row.addWidget(btn_delete, 0)

        self.detalles_layout.addLayout(row)

        detalle = {
            "combo": combo,
            "cantidad": cantidad,
            "layout": row
        }
        self.productos.append(detalle)

        btn_delete.clicked.connect(lambda: self.remove_producto_row(detalle))

    def remove_producto_row(self, detalle):
        # 1. Eliminar visualmente los componentes del layout dinámico
        for i in reversed(range(detalle["layout"].count())):
            item = detalle["layout"].itemAt(i)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        # 2. Remover el layout secundario vacío del layout contenedor padre (Previene fugas de memoria)
        self.detalles_layout.removeItem(detalle["layout"])
        detalle["layout"].deleteLater()

        # 3. Removerlo del tracking de datos de la instancia
        if detalle in self.productos:
            self.productos.remove(detalle)

    def save(self):
        try:
            detalles = []
            for d in self.productos:
                # Comprobación de seguridad: omitir filas destruidas que no se hayan limpiado
                if d["combo"].currentData() is not None:
                    detalles.append({
                        "producto": d["combo"].currentData(),
                        "cantidad": d["cantidad"].value()
                    })

            if not detalles:
                raise ValueError("Debe ingresar al menos un producto en el pedido.")

            data = {
                "cliente": self.cliente_combo.currentData(),
                "origen": self.origen_combo.currentData(),
                "observaciones": self.observaciones.toPlainText().strip(),
                "detalles": detalles
            }

            vendedor_id = self.vendedor_combo.currentData()
            if vendedor_id is not None:
                data["vendedor"] = vendedor_id

            pedido_creado = self.pedido_service.crear(data)

            QMessageBox.information(self, "Éxito", "Pedido creado correctamente.")
            self.on_success(pedido_creado)
            QApplication.processEvents()
            self.close()

        except ValueError as ve:
            QMessageBox.warning(self, "Validación", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el pedido: {e}")
            
    
    def abrir_nuevo_cliente(self):
        zona_service = ZonaService(self.cliente_service.http)
        user_service = UserService(self.cliente_service.http)

        self.cliente_window = ClienteForm(
            cliente_service=self.cliente_service,
            zona_service=zona_service,
            user_service=user_service,
            on_success=self.recargar_clientes
        )
        self.cliente_window.show()

    def recargar_clientes(self):
        self.cliente_combo.clear()
        clientes = self.cliente_service.listar()
        clientes_data = clientes.get("results", clientes)
        for c in clientes_data:
            self.cliente_combo.addItem(f"{c['nombre']} {c.get('apellido','')}".strip(), c["id"])
        # Selecciona el último creado
        if self.cliente_combo.count() > 0:
            self.cliente_combo.setCurrentIndex(self.cliente_combo.count() - 1)