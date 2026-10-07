# desktop/app/style/components/compra_card_styles.py
QSS_STYLE = """
    QFrame#card_frame {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 6px;
    }
    QLabel {
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 13px;
        color: #495057;
    }
    QLabel#lbl_id {
        font-size: 15px;
        font-weight: bold;
        color: #1a1a1a;
    }
    QLabel#lbl_estado_recibida {
        font-weight: bold;
        color: #198754;
        background-color: #d1e7dd;
        padding: 3px 8px;
        border-radius: 4px;
    }
    QLabel#lbl_estado_pendiente {
        font-weight: bold;
        color: #dc3545;
        background-color: #f8d7da;
        padding: 3px 8px;
        border-radius: 4px;
    }
    QLabel#lbl_total {
        font-size: 16px;
        font-weight: bold;
        color: #1a1a1a;
    }
    QPushButton#btn_recibir {
        background-color: #dc3545;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 6px 12px;
        font-weight: bold;
    }
    QPushButton#btn_recibir:hover {
        background-color: #bd2130;
    }
    QPushButton#btn_recibir:disabled {
        background-color: #e9ecef;
        color: #adb5bd;
        border: 1px solid #ced4da;
    }
"""