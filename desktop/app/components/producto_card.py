# desktop/app/components/producto_card.py
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
    QStyle,      
    QStyleOption
)
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt
import requests

from form.producto_form import ProductoForm
from form.promocion_form import PromocionForm

from services.rubro_service import RubroService
from services.proveedor_service import ProveedorService
from services.promocion_service import PromocionService
from services.producto_promocion_service import ProductoPromocionService

from style.components.producto_card_styles import get_producto_card_style, ESTILO_CONFIRM_DIALOG


class ProductoCard(QWidget):

    def __init__(self, producto, service, refresh_callback):
        super().__init__()

        self.producto = producto
        self.service = service
        self.refresh = refresh_callback

        # Permitir la compresión fluida dentro del layout de la grid
        self.setMinimumWidth(0)

        self.rubro_service = RubroService(self.service.http)
        self.proveedor_service = ProveedorService(self.service.http)
        self.promocion_service = PromocionService(self.service.http)
        self.producto_promocion_service = ProductoPromocionService(self.service.http)

        self.tiene_promocion = False
        self.promocion_rel_id = None

        self.check_promocion()

        # Layout principal de la tarjeta
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # =========================
        # IMAGEN
        # =========================
        self.img_label = QLabel()
        self.img_label.setObjectName("product_image")
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.img_label.setMinimumSize(120, 120)

        if producto.get("img"):
            try:
                response = requests.get(producto["img"], timeout=5)
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                self.img_label.setPixmap(
                    pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                )
            except Exception:
                self.img_label.setText("Error al cargar imagen")
        else:
            self.img_label.setText("Sin imagen")

        layout.addWidget(self.img_label)

        # =========================
        # ETIQUETA DE PROMOCIÓN
        # =========================
        if self.tiene_promocion:
            promo_label = QLabel("🔥 EN PROMOCIÓN")
            promo_label.setObjectName("promo_tag")
            promo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(promo_label)

        # =========================
        # INFORMACIÓN DEL PRODUCTO
        # =========================
        nombre = QLabel(producto["nombre"])
        nombre.setObjectName("product_title")
        nombre.setWordWrap(True)
        layout.addWidget(nombre)
        
        # Mostrar Rubros asociados
        rubros = producto.get("rubros", [])
        nombres_rubros = ", ".join([r["nombre"] for r in rubros if isinstance(r, dict)]) or "Sin rubro"
        lbl_rubros = QLabel(f"🏷️ {nombres_rubros}")
        lbl_rubros.setObjectName("product_rubros")
        lbl_rubros.setWordWrap(True)
        layout.addWidget(lbl_rubros)
        
        # Mostrar Proveedores asociados
        proveedores = producto.get("proveedores", [])
        nombres_prov = ", ".join([p["nombre"] for p in proveedores if isinstance(p, dict)]) or "Sin proveedor"
        lbl_prov = QLabel(f"🏭 {nombres_prov}")
        lbl_prov.setObjectName("product_proveedores")
        lbl_prov.setWordWrap(True)
        layout.addWidget(lbl_prov)
        
        lbl_id = QLabel(f"ID: {producto['id']}")
        lbl_id.setObjectName("product_id")
        layout.addWidget(lbl_id)

        meta_layout = QHBoxLayout()
        lbl_precio = QLabel(f"${float(producto['precio_base']):.2f}")
        lbl_precio.setObjectName("product_price")

        lbl_stock = QLabel(f"Stock: {producto['stock']}")
        lbl_stock.setObjectName("product_stock")

        meta_layout.addWidget(lbl_precio)
        meta_layout.addStretch()
        meta_layout.addWidget(lbl_stock)
        layout.addLayout(meta_layout)

        layout.addStretch()

        # =========================
        # BOTONES DE ACCIÓN
        # =========================
        self.btn_edit = QPushButton("Editar")
        self.btn_delete = QPushButton("Eliminar")
        self.btn_promo = QPushButton("+ Promo")
        self.btn_remove_promo = QPushButton("- Promo")

        self.btn_edit.setObjectName("btn_edit")
        self.btn_delete.setObjectName("btn_delete")
        self.btn_promo.setObjectName("btn_promo")
        self.btn_remove_promo.setObjectName("btn_remove")

        self.btn_edit.clicked.connect(self.open_edit_form)
        self.btn_delete.clicked.connect(self.delete)
        self.btn_promo.clicked.connect(self.open_promocion_form)
        self.btn_remove_promo.clicked.connect(self.remove_promocion)

        actions_layout_top = QHBoxLayout()
        actions_layout_top.addWidget(self.btn_edit)

        if self.tiene_promocion:
            actions_layout_top.addWidget(self.btn_remove_promo)
        else:
            actions_layout_top.addWidget(self.btn_promo)

        layout.addLayout(actions_layout_top)
        layout.addWidget(self.btn_delete)

        self.apply_card_styles()
        self.setLayout(layout)

    def apply_card_styles(self):
        """Aplica el estilo desacoplado según si tiene o no promoción activa."""
        obj_name = "active_promo_card" if self.tiene_promocion else "standard_card"
        self.setObjectName(obj_name)
        self.setStyleSheet(get_producto_card_style(obj_name, self.tiene_promocion))

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, painter, self)
        painter.end()

    # =========================
    # LÓGICA OPERATIVA
    # =========================
    def check_promocion(self):
        try:
            promociones = self.producto_promocion_service.listar()
            data = promociones.get("results", promociones)
            for rel in data:
                if rel["producto"] == self.producto["id"]:
                    self.tiene_promocion = True
                    self.promocion_rel_id = rel["id"]
                    break
        except Exception:
            pass

    def open_edit_form(self):
        self.form = ProductoForm(
            self.service,
            self.rubro_service,
            self.proveedor_service,
            self.refresh,
            self.producto
        )
        self.form.show()

    def open_promocion_form(self):
        self.form = PromocionForm(
            self.producto,
            self.promocion_service,
            self.producto_promocion_service,
            self.refresh
        )
        self.form.show()

    def remove_promocion(self):
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Icon.Question)
        box.setWindowTitle("Confirmar")
        box.setText("¿Quitar promoción?")
        box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        box.setStyleSheet(ESTILO_CONFIRM_DIALOG)

        if box.exec() != QMessageBox.StandardButton.Yes:
            return
        try:
            self.producto_promocion_service.eliminar(self.promocion_rel_id)
            QMessageBox.information(self, "OK", "Promoción eliminada")
            self.refresh()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def delete(self):
        nombre_prod = self.producto.get("nombre", "este producto")

        box = QMessageBox(self)
        box.setIcon(QMessageBox.Icon.Question)
        box.setWindowTitle("Confirmar Eliminación")
        box.setText(f"¿Está seguro de que desea eliminar el producto '{nombre_prod}'?")
        box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        box.setStyleSheet(ESTILO_CONFIRM_DIALOG)

        if box.exec() == QMessageBox.StandardButton.Yes:
            try:
                self.service.eliminar(self.producto["id"])
                self.refresh()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))