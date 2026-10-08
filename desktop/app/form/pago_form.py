# desktop/app/form/pago_form.py
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QDoubleSpinBox
)
from style.form.pago_form_styles import QSS_STYLE


class PagoForm(QDialog):

    def __init__(self, parent=None, factura_id=None, pago=None, monto_sugerido=0.0):
        super().__init__(parent)

        self.pago = pago
        self.factura_id = factura_id

        self.setWindowTitle("Registrar Cobro")
        self.resize(380, 260)
        self.setStyleSheet(QSS_STYLE)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header destacado con el número de factura
        self.lbl_factura = QLabel(f"Factura #{self.factura_id}")
        self.lbl_factura.setObjectName("lbl_factura")
        main_layout.addWidget(self.lbl_factura)

        form_layout = QFormLayout()
        form_layout.setSpacing(12)

        # Monto a cobrar
        self.monto_input = QDoubleSpinBox()
        self.monto_input.setMaximum(9999999.99)
        self.monto_input.setDecimals(2)
        self.monto_input.setPrefix("$ ")
        if not self.pago and monto_sugerido > 0:
            self.monto_input.setValue(float(monto_sugerido))
        form_layout.addRow("Monto a Cobrar:", self.monto_input)

        # Método de Pago
        self.metodo_combo = QComboBox()
        self.metodo_combo.addItems(["efectivo", "transferencia", "tarjeta"])
        form_layout.addRow("Método:", self.metodo_combo)

        # Referencia
        self.referencia_input = QLineEdit()
        self.referencia_input.setPlaceholderText("Ej. Nº de transacción o recibo")
        form_layout.addRow("Referencia:", self.referencia_input)

        main_layout.addLayout(form_layout)

        # Botón rojo de acción principal
        self.btn_guardar = QPushButton("Guardar Cobro")
        self.btn_guardar.clicked.connect(self.accept)
        main_layout.addWidget(self.btn_guardar)

        self.setLayout(main_layout)

        if self.pago:
            self.monto_input.setValue(float(self.pago["monto"]))
            self.metodo_combo.setCurrentText(str(self.pago["metodo_pago"]).lower())
            self.referencia_input.setText(str(self.pago.get("referencia") or ""))

    def obtener_datos(self):
        ref_text = self.referencia_input.text().strip()

        return {
            "factura": self.factura_id,
            "monto": self.monto_input.value(),
            "metodo_pago": self.metodo_combo.currentText(),
            "estado": "completado",
            "referencia": ref_text if ref_text else ""
        }
    
    