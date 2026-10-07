# desktop/app/form/producto_form.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QListWidget, QLabel, QMessageBox, QListWidgetItem, QFileDialog, QApplication
)
from PyQt6.QtCore import Qt

from style.form.producto_form_styles import ESTILO_PRODUCTO_FORM


class ProductoForm(QWidget):

    def __init__(self, producto_service, rubro_service, proveedor_service, on_success, producto=None):
        super().__init__()

        self.producto_service = producto_service
        self.rubro_service = rubro_service
        self.proveedor_service = proveedor_service
        self.on_success = on_success
        self.producto = producto

        self.image_path = None

        self.setWindowTitle("Editar Producto" if self.producto else "Nuevo Producto")
        self.resize(550, 750)
        self.setObjectName("producto_form_window")
        self.setStyleSheet(ESTILO_PRODUCTO_FORM)

        # Layout Principal General
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(15)

        # =========================
        # DATOS BÁSICOS DEL PRODUCTO
        # =========================
        lbl_seccion_prod = QLabel("Datos del Producto")
        lbl_seccion_prod.setObjectName("section_title")
        main_layout.addWidget(lbl_seccion_prod)

        self.nombre = QLineEdit()
        self.nombre.setPlaceholderText("Nombre del producto")

        numeric_layout = QHBoxLayout()
        self.precio = QLineEdit()
        self.precio.setPlaceholderText("Precio base ($)")
        self.stock = QLineEdit()
        self.stock.setPlaceholderText("Stock inicial")
        numeric_layout.addWidget(self.precio)
        numeric_layout.addWidget(self.stock)

        main_layout.addWidget(self.nombre)
        main_layout.addLayout(numeric_layout)

        # =========================
        # GESTIÓN DE IMAGEN
        # =========================
        img_layout = QHBoxLayout()
        self.btn_img = QPushButton("Seleccionar Imagen")
        self.btn_img.setObjectName("secondary_button")
        self.btn_img.clicked.connect(self.select_image)

        self.lbl_img = QLabel("Sin imagen seleccionada")
        self.lbl_img.setObjectName("image_status")
        img_layout.addWidget(self.btn_img)
        img_layout.addWidget(self.lbl_img, 1)
        main_layout.addLayout(img_layout)

        # =========================
        # SECCIÓN SELECCIÓN DE LISTAS
        # =========================
        main_layout.addWidget(QLabel("Asignar Rubros (Selección múltiple):"))
        self.rubros_list = QListWidget()
        self.rubros_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.rubros_list.setFixedHeight(100)
        main_layout.addWidget(self.rubros_list)

        main_layout.addWidget(QLabel("Asignar Proveedores (Selección múltiple):"))
        self.prov_list = QListWidget()
        self.prov_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.prov_list.setFixedHeight(100)
        main_layout.addWidget(self.prov_list)

        # =========================
        # BOTONES INTERRUPTORES (TOGGLES)
        # =========================
        toggle_layout = QHBoxLayout()
        
        self.btn_toggle_rubro = QPushButton("+ Administrar Rubros")
        self.btn_toggle_rubro.setCheckable(True)
        self.btn_toggle_rubro.setObjectName("toggle_button")
        self.btn_toggle_rubro.clicked.connect(self.toggle_rubro_panel)

        self.btn_toggle_prov = QPushButton("+ Administrar Proveedores")
        self.btn_toggle_prov.setCheckable(True)
        self.btn_toggle_prov.setObjectName("toggle_button")
        self.btn_toggle_prov.clicked.connect(self.toggle_proveedor_panel)

        toggle_layout.addWidget(self.btn_toggle_rubro)
        toggle_layout.addWidget(self.btn_toggle_prov)
        main_layout.addLayout(toggle_layout)

        # =========================
        # PANEL OCULTO: NUEVO RUBRO
        # =========================
        self.panel_rubro = QWidget()
        self.panel_rubro.setObjectName("sub_panel")
        self.panel_rubro.setVisible(False)
        
        rubro_layout = QVBoxLayout(self.panel_rubro)
        rubro_layout.setContentsMargins(10, 10, 10, 10)
        
        lbl_r = QLabel("Nuevo Rubro")
        lbl_r.setObjectName("sub_title")
        rubro_layout.addWidget(lbl_r)
        
        self.rubro_input = QLineEdit()
        self.rubro_input.setPlaceholderText("Nombre del nuevo rubro")
        rubro_layout.addWidget(self.rubro_input)

        btn_r_actions = QHBoxLayout()
        self.btn_add_rubro = QPushButton("Guardar Rubro")
        self.btn_add_rubro.setObjectName("action_green")
        self.btn_add_rubro.clicked.connect(self.create_rubro)

        self.btn_delete_rubro = QPushButton("Eliminar Seleccionado")
        self.btn_delete_rubro.setObjectName("action_red")
        self.btn_delete_rubro.clicked.connect(self.delete_rubro)
        
        btn_r_actions.addWidget(self.btn_add_rubro)
        btn_r_actions.addWidget(self.btn_delete_rubro)
        rubro_layout.addLayout(btn_r_actions)
        
        main_layout.addWidget(self.panel_rubro)

        # =========================
        # PANEL OCULTO: NUEVO PROVEEDOR
        # =========================
        self.panel_proveedor = QWidget()
        self.panel_proveedor.setObjectName("sub_panel")
        self.panel_proveedor.setVisible(False)
        
        prov_layout = QVBoxLayout(self.panel_proveedor)
        prov_layout.setContentsMargins(10, 10, 10, 10)
        
        lbl_p = QLabel("Nuevo Proveedor")
        lbl_p.setObjectName("sub_title")
        prov_layout.addWidget(lbl_p)

        self.prov_nombre = QLineEdit()
        self.prov_nombre.setPlaceholderText("Razón Social / Nombre")
        prov_layout.addWidget(self.prov_nombre)

        prov_h2 = QHBoxLayout()
        self.prov_tel = QLineEdit()
        self.prov_tel.setPlaceholderText("Teléfono")
        self.prov_email = QLineEdit()
        self.prov_email.setPlaceholderText("Email")
        prov_h2.addWidget(self.prov_tel)
        prov_h2.addWidget(self.prov_email)
        prov_layout.addLayout(prov_h2)

        btn_p_actions = QHBoxLayout()
        self.btn_add_prov = QPushButton("Guardar Proveedor")
        self.btn_add_prov.setObjectName("action_green")
        self.btn_add_prov.clicked.connect(self.create_proveedor)

        self.btn_delete_prov = QPushButton("Eliminar Seleccionado")
        self.btn_delete_prov.setObjectName("action_red")
        self.btn_delete_prov.clicked.connect(self.delete_proveedor)
        
        btn_p_actions.addWidget(self.btn_add_prov)
        btn_p_actions.addWidget(self.btn_delete_prov)
        prov_layout.addLayout(btn_p_actions)

        main_layout.addWidget(self.panel_proveedor)

        # =========================
        # ACCIÓN PRINCIPAL DE GUARDADO
        # =========================
        main_layout.addStretch()
        
        self.btn_save = QPushButton("GUARDAR PRODUCTO")
        self.btn_save.setObjectName("main_save_button")
        self.btn_save.clicked.connect(self.save)
        main_layout.addWidget(self.btn_save)

        self.setLayout(main_layout)

        # Cargar opciones y datos existentes si es edición
        self.load_options()

        if self.producto:
            self.load_producto()

    # =========================
    # LÓGICA DE PANELES OCULTOS
    # =========================
    def toggle_rubro_panel(self, checked):
        self.panel_rubro.setVisible(checked)
        if checked:
            self.btn_toggle_rubro.setText("- Ocultar Rubros")
            self.btn_toggle_prov.setChecked(False)
            self.panel_proveedor.setVisible(False)
            self.btn_toggle_prov.setText("+ Administrar Proveedores")
        else:
            self.btn_toggle_rubro.setText("+ Administrar Rubros")

    def toggle_proveedor_panel(self, checked):
        self.panel_proveedor.setVisible(checked)
        if checked:
            self.btn_toggle_prov.setText("- Ocultar Proveedores")
            self.btn_toggle_rubro.setChecked(False)
            self.panel_rubro.setVisible(False)
            self.btn_toggle_rubro.setText("+ Administrar Rubros")
        else:
            self.btn_toggle_prov.setText("+ Administrar Proveedores")

    # =========================
    # CARGA DE DATOS
    # =========================
    def load_options(self):
        try:
            self.rubros_list.clear()
            self.prov_list.clear()

            rubros = self.rubro_service.listar()
            proveedores = self.proveedor_service.listar()

            rubros_data = rubros.get("results", rubros)
            proveedores_data = proveedores.get("results", proveedores)

            for r in rubros_data:
                item = QListWidgetItem(r["nombre"])
                item.setData(1, r["id"])
                self.rubros_list.addItem(item)

            for p in proveedores_data:
                item = QListWidgetItem(p["nombre"])
                item.setData(1, p["id"])
                self.prov_list.addItem(item)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def get_selected_ids(self, list_widget):
        return [item.data(1) for item in list_widget.selectedItems()]

    def refresh_lists(self):
        self.load_options()
        QApplication.processEvents()
        if self.rubros_list.count():
            self.rubros_list.scrollToBottom()
        if self.prov_list.count():
            self.prov_list.scrollToBottom()

    def select_item_by_id(self, list_widget, item_id):
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            if item and item.data(1) == item_id:
                list_widget.setCurrentItem(item)
                list_widget.scrollToItem(item)
                return

    # =========================
    # GESTIÓN DE RUBROS
    # =========================
    def create_rubro(self):
        try:
            nombre = self.rubro_input.text().strip()
            if not nombre:
                raise ValueError("Debe ingresar el nombre del nuevo rubro.")

            rubro_creado = self.rubro_service.crear({"nombre": nombre})
            self.rubro_input.clear()
            self.refresh_lists()
            if rubro_creado.get("id") is not None:
                self.select_item_by_id(self.rubros_list, rubro_creado["id"])

        except ValueError as ve:
            QMessageBox.warning(self, "Validación requerida", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def delete_rubro(self):
        try:
            if not self.rubros_list.selectedItems():
                raise ValueError("Seleccione al menos un rubro para eliminar.")
                
            for item in self.rubros_list.selectedItems():
                self.rubro_service.eliminar(item.data(1))

            self.refresh_lists()

        except ValueError as ve:
            QMessageBox.warning(self, "Validación requerida", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    # =========================
    # GESTIÓN DE PROVEEDORES
    # =========================
    def create_proveedor(self):
        try:
            nombre = self.prov_nombre.text().strip()
            if not nombre:
                raise ValueError("Debe ingresar la Razón Social o Nombre del proveedor.")

            data = {
                "nombre": nombre,
                "telefono": self.prov_tel.text().strip(),
                "email": self.prov_email.text().strip(),
            }

            proveedor_creado = self.proveedor_service.crear(data)
            self.prov_nombre.clear()
            self.prov_tel.clear()
            self.prov_email.clear()

            self.refresh_lists()
            if proveedor_creado.get("id") is not None:
                self.select_item_by_id(self.prov_list, proveedor_creado["id"])

        except ValueError as ve:
            QMessageBox.warning(self, "Validación requerida", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def delete_proveedor(self):
        try:
            if not self.prov_list.selectedItems():
                raise ValueError("Seleccione al menos un proveedor para eliminar.")

            for item in self.prov_list.selectedItems():
                self.proveedor_service.eliminar(item.data(1))

            self.refresh_lists()

        except ValueError as ve:
            QMessageBox.warning(self, "Validación requerida", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    # =========================
    # GESTIÓN DE IMAGEN
    # =========================
    def select_image(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar imagen", "", "Images (*.png *.jpg *.jpeg)"
        )
        if file:
            self.image_path = file
            self.lbl_img.setText(file.split("/")[-1])

    # =========================
    # VALIDACIONES Y GUARDADO
    # =========================
    def validate_inputs(self):
        nombre = self.nombre.text().strip()
        if not nombre:
            raise ValueError("Debe ingresar el nombre del producto.")

        # 1. Validación de Precio
        precio_str = self.precio.text().strip().replace(",", ".")
        if not precio_str:
            raise ValueError("Debe ingresar un precio base.")
        
        try:
            precio = float(precio_str)
        except ValueError:
            raise ValueError("El precio debe ser un número válido (ej: 14500.50).")

        if precio <= 0:
            raise ValueError("El precio debe ser mayor a 0.")

        # 2. Validación de Stock
        stock_str = self.stock.text().strip()
        if not stock_str:
            raise ValueError("Debe ingresar el stock.")
        
        try:
            stock = int(stock_str)
        except ValueError:
            raise ValueError("El stock debe ser un número entero (ej: 25).")

        # Regla: No permitir stock negativo
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")

        # Si tampoco querés permitir stock en 0 al dar de alta:
        if stock == 0:
            raise ValueError("El stock debe ser mayor a 0.")

        # 3. Asignación de Rubros y Proveedores
        rubros = self.get_selected_ids(self.rubros_list)
        if not rubros:
            raise ValueError("Debe asignar al menos un rubro al producto.")

        proveedores = self.get_selected_ids(self.prov_list)
        if not proveedores:
            raise ValueError("Debe asignar al menos un proveedor al producto.")

        return nombre, precio, stock, rubros, proveedores

    def save(self):
        file_obj = None
        try:
            nombre, precio, stock, rubros, proveedores = self.validate_inputs()

            data = {
                "nombre": nombre,
                "precio_base": precio,
                "stock": stock,
                "rubros": rubros,
                "proveedores": proveedores,
            }

            files = None
            if self.image_path:
                file_obj = open(self.image_path, "rb")
                files = {"img": file_obj}

            if self.producto:
                self.producto_service.actualizar(self.producto["id"], data, files)
                QMessageBox.information(self, "Operación Exitosa", "Producto actualizado correctamente.")
            else:
                self.producto_service.crear(data, files)
                QMessageBox.information(self, "Operación Exitosa", "Producto registrado correctamente.")

            self.on_success()
            self.close()

        except ValueError as ve:
            QMessageBox.warning(self, "Validación requerida", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        finally:
            if file_obj:
                file_obj.close()

    # =========================
    # EDICIÓN
    # =========================
    def load_producto(self):
        p = self.producto

        self.nombre.setText(p.get("nombre", ""))
        self.precio.setText(str(p.get("precio_base", "")))
        self.stock.setText(str(p.get("stock", "")))

        rubro_ids = [r["id"] for r in p.get("rubros", []) if isinstance(r, dict)]
        for i in range(self.rubros_list.count()):
            item = self.rubros_list.item(i)
            if item.data(1) in rubro_ids:
                item.setSelected(True)

        prov_ids = [pr["id"] for pr in p.get("proveedores", []) if isinstance(pr, dict)]
        for i in range(self.prov_list.count()):
            item = self.prov_list.item(i)
            if item.data(1) in prov_ids:
                item.setSelected(True)