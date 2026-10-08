# desktop/app/views/pago_view.py
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QLabel,
    QAbstractItemView,
    QHeaderView,
    QScrollArea,
    QFrame
)
from form.pago_form import PagoForm
from style.views.pago_view_style import QSS_STYLE_CLARO

class PagoView(QWidget):

    def __init__(self, factura=None, pago_service=None):
        """
        Constructor de la vista de pagos.
        Puede recibir una factura específica (diccionario/objeto) o None (Vista General).
        """
        super().__init__()

        self.factura = factura
        self.service = pago_service
        self.pendiente_actual = 0.0
        # Extrae el ID limpio de la factura si fue provista
        self.factura_id = self._obtener_id_factura(self.factura)

        # Configura el título y tamaño de la ventana según el modo de apertura
        if self.factura_id is not None:
            self.setWindowTitle(f"Pagos - Factura #{self.factura_id}")
            self.resize(750, 480)
        else:
            self.setWindowTitle("Cobranzas - Panel General")
            self.resize(900, 650)
            
        self.setStyleSheet(QSS_STYLE_CLARO)

        # Inicializa el layout vertical principal
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(15)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Etiqueta informativa superior para saldos y títulos
        self.info = QLabel("")
        self.info.setObjectName("infoLabel")
        self.main_layout.addWidget(self.info)

        if self.factura:
            # === VISTA INDIVIDUAL DESDE UNA FACTURA ESPECÍFICA ===
            buttons_layout = QHBoxLayout()
            self.btn_crear = QPushButton("Crear")
            self.btn_editar = QPushButton("Editar")
            self.btn_eliminar = QPushButton("Eliminar")
            self.btn_recargar = QPushButton("Recargar")

            self.btn_crear.clicked.connect(self.crear_pago)
            self.btn_editar.clicked.connect(self.editar_pago)
            self.btn_eliminar.clicked.connect(self.eliminar_pago)
            self.btn_recargar.clicked.connect(self.cargar_pagos)

            buttons_layout.addWidget(self.btn_crear)
            buttons_layout.addWidget(self.btn_editar)
            buttons_layout.addWidget(self.btn_eliminar)
            buttons_layout.addStretch()
            buttons_layout.addWidget(self.btn_recargar)
            self.main_layout.addLayout(buttons_layout)

            # Configuración de la tabla única de pagos para la factura seleccionada
            self.table = QTableWidget()
            self.table.setColumnCount(5)
            self.table.setHorizontalHeaderLabels(["ID", "Monto", "Método", "Estado", "Referencia"])
            self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
            self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
            self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.main_layout.addWidget(self.table)
        else:
            # === VISTA GENERAL DE COBRANZAS (DISEÑO POR TARJETAS CLARAS) ===
            top_actions = QHBoxLayout()
            self.btn_recargar_global = QPushButton("Recargar Panel")
            self.btn_recargar_global.setObjectName("btn_recargar_global")
            self.btn_recargar_global.clicked.connect(self.cargar_pagos)
            top_actions.addStretch()
            top_actions.addWidget(self.btn_recargar_global)
            self.main_layout.addLayout(top_actions)

            self.scroll_area = QScrollArea()
            self.scroll_area.setWidgetResizable(True)
            self.scroll_widget = QWidget()
            self.scroll_layout = QVBoxLayout(self.scroll_widget)
            self.scroll_layout.setSpacing(15)
            self.scroll_layout.setContentsMargins(0, 0, 0, 0)
            self.scroll_area.setWidget(self.scroll_widget)
            self.main_layout.addWidget(self.scroll_area)

        self.setLayout(self.main_layout)
        self.cargar_pagos()

    def _obtener_id_factura(self, factura):
        """Helper para extraer el ID de factura de forma segura si viene como dict o modelo."""
        if isinstance(factura, dict):
            return factura.get("id")
        return getattr(factura, "id", None)

    def _obtener_total_factura(self):
        """Helper para extraer el importe total de la factura actual."""
        if isinstance(self.factura, dict):
            return self.factura.get("total")
        return getattr(self.factura, "total", None)

    def cargar_pagos(self):
        """Método central que recupera los datos desde la API y repobla la interfaz gráfica."""
        try:
            if self.factura_id is not None:
                id_factura_actual = int(self.factura_id)
                response = self.service.listar_por_factura(id_factura_actual)
                
                pagos_filtrados = response.get("results", response) if isinstance(response, dict) else response
                
                total_f = float(self._obtener_total_factura() or 0)
                total_p = sum(float(p["monto"]) for p in pagos_filtrados if str(p["estado"]).lower() == "completado")
                self.pendiente_actual = max(0.0, total_f - total_p)

                self.info.setText(
                    f"Factura #{id_factura_actual}  |  Total: ${total_f:.2f}  |  "
                    f"Pagado: ${total_p:.2f}  |  Pendiente: ${self.pendiente_actual:.2f}"
                )

                self.table.clearContents()
                self.table.setRowCount(0)
                self.table.setRowCount(len(pagos_filtrados))
                
                for row, p in enumerate(pagos_filtrados):
                    self.table.setItem(row, 0, QTableWidgetItem(str(p["id"])))
                    self.table.setItem(row, 1, QTableWidgetItem(f"$ {float(p['monto']):.2f}"))
                    self.table.setItem(row, 2, QTableWidgetItem(str(p["metodo_pago"]).upper()))
                    self.table.setItem(row, 3, QTableWidgetItem(str(p["estado"]).upper()))
                    self.table.setItem(row, 4, QTableWidgetItem(str(p["referencia"]) if p["referencia"] else "-"))
            else:
                self.info.setText("Listado General de Cobranzas — Control de Comprobantes")
                
                while self.scroll_layout.count():
                    item = self.scroll_layout.takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()

                response = self.service.listar()
                todos_los_pagos = response["results"] if isinstance(response, dict) else response

                pagos_por_factura = {}
                for p in todos_los_pagos:
                    factura_campo = p.get("factura")
                    f_id = factura_campo.get("id") if isinstance(factura_campo, dict) else factura_campo
                    
                    if f_id not in pagos_por_factura:
                        pagos_por_factura[f_id] = []
                    pagos_por_factura[f_id].append(p)

                for f_id, lista_pagos in pagos_por_factura.items():
                    card = QFrame()
                    card.setObjectName("cardFactura")
                    card_layout = QVBoxLayout(card)
                    card_layout.setContentsMargins(15, 15, 15, 15)
                    card_layout.setSpacing(12)

                    header_layout = QHBoxLayout()
                    lbl_titulo = QLabel(f"Factura #{f_id}")
                    lbl_titulo.setObjectName("cardTitle")
                    header_layout.addWidget(lbl_titulo)

                    total_pagado = sum(float(p["monto"]) for p in lista_pagos if str(p["estado"]).lower() == "completado")
                    
                    lbl_resumen = QLabel(f"Total Cobrado: ${total_pagado:.2f}  |  Transacciones: {len(lista_pagos)}")
                    lbl_resumen.setObjectName("cardSummaryText")
                    header_layout.addWidget(lbl_resumen)
                    header_layout.addStretch()

                    card_buttons = QHBoxLayout()
                    btn_edit = QPushButton("Editar")
                    btn_delete = QPushButton("Eliminar")
                    
                    btn_edit.clicked.connect(lambda checked, fid=f_id: self.editar_pago_general(fid))
                    btn_delete.clicked.connect(lambda checked, fid=f_id: self.eliminar_pago_general(fid))
                    
                    card_buttons.addWidget(btn_edit)
                    card_buttons.addWidget(btn_delete)
                    header_layout.addLayout(card_buttons)
                    card_layout.addLayout(header_layout)

                    sub_table = QTableWidget()
                    sub_table.setObjectName(f"table_factura_{f_id}")
                    sub_table.setColumnCount(5)
                    sub_table.setHorizontalHeaderLabels(["ID Pago", "Monto", "Método", "Estado", "Referencia"])
                    sub_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
                    sub_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
                    sub_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
                    sub_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
                    sub_table.setFixedHeight(110)
                    
                    sub_table.setRowCount(len(lista_pagos))
                    for row, p in enumerate(lista_pagos):
                        sub_table.setItem(row, 0, QTableWidgetItem(str(p["id"])))
                        sub_table.setItem(row, 1, QTableWidgetItem(f"$ {float(p['monto']):.2f}"))
                        sub_table.setItem(row, 2, QTableWidgetItem(str(p["metodo_pago"]).upper()))
                        sub_table.setItem(row, 3, QTableWidgetItem(str(p["estado"]).upper()))
                        sub_table.setItem(row, 4, QTableWidgetItem(str(p["referencia"]) if p["referencia"] else "-"))
                    
                    card_layout.addWidget(sub_table)
                    self.scroll_layout.addWidget(card)
                
                self.scroll_layout.addStretch()

        except Exception as e:
            QMessageBox.critical(self, "Error al Cargar", str(e))

    # === CONTROLES DE EDICIÓN PARA LA ENTRADA GENERAL ===
    def obtener_id_desde_subtabla(self, factura_id):
        tabla = self.findChild(QTableWidget, f"table_factura_{factura_id}")
        if tabla:
            fila = tabla.currentRow()
            if fila >= 0:
                return int(tabla.item(fila, 0).text())
        return None

    def editar_pago_general(self, factura_id):
        pago_id = self.obtener_id_desde_subtabla(factura_id)
        if not pago_id:
            QMessageBox.warning(self, "Atención", "Seleccione una fila en la tabla de la factura correspondiente.")
            return
        try:
            pago = self.service.obtener(pago_id)
            dialog = PagoForm(self, factura_id=factura_id, pago=pago)
            if dialog.exec():
                self.service.actualizar(pago_id, dialog.obtener_datos())
                self.cargar_pagos()
        except Exception as e:
            QMessageBox.warning(self, "Límite de Cobro / Error", str(e))

    def eliminar_pago_general(self, factura_id):
        pago_id = self.obtener_id_desde_subtabla(factura_id)
        if not pago_id:
            QMessageBox.warning(self, "Atención", "Seleccione una fila en la tabla de la factura correspondiente.")
            return
        if QMessageBox.question(self, "Confirmar", "¿Desea eliminar el pago seleccionado?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            try:
                self.service.eliminar(pago_id)
                self.cargar_pagos()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    # === CONTROLES DE EDICIÓN PARA VISTA INDIVIDUAL (DESDE FACTURAS) ===
    def obtener_id_seleccionado(self):
        if not self.table:
            return None
        fila = self.table.currentRow()
        return int(self.table.item(fila, 0).text()) if fila >= 0 else None

    def crear_pago(self):
        """Instancia el formulario para registrar un nuevo cobro sugerido."""
        if self.factura_id is None:
            return

        dialog = PagoForm(self, factura_id=self.factura_id, monto_sugerido=self.pendiente_actual)
        if dialog.exec():
            try:
                self.service.crear(dialog.obtener_datos())
                self.cargar_pagos()
            except Exception as e:
                # Muestra el error formateado enviado por el backend
                QMessageBox.warning(self, "Validación de Cobro", str(e))

    def editar_pago(self):
        pago_id = self.obtener_id_seleccionado()
        if not pago_id:
            QMessageBox.warning(self, "Atención", "Seleccione un pago de la lista.")
            return
        try:
            pago = self.service.obtener(pago_id)
            dialog = PagoForm(self, factura_id=self.factura_id, pago=pago)
            if dialog.exec():
                self.service.actualizar(pago_id, dialog.obtener_datos())
                self.cargar_pagos()
        except Exception as e:
            QMessageBox.warning(self, "Validación de Cobro", str(e))

    def eliminar_pago(self):
        pago_id = self.obtener_id_seleccionado()
        if not pago_id or QMessageBox.question(self, "Confirmar", "¿Eliminar pago?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) != QMessageBox.StandardButton.Yes:
            return
        try:
            self.service.eliminar(pago_id)
            self.cargar_pagos()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))