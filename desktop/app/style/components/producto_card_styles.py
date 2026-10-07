# desktop/app/style/components/producto_card_styles.py
def get_producto_card_style(object_name: str, tiene_promocion: bool) -> str:
    """Devuelve la hoja de estilos de la tarjeta según su estado de promoción."""
    border_style = "2px solid #e53935;" if tiene_promocion else "2px solid #3a3a4a;"

    return f"""
        QWidget#{object_name} {{
            background-color: #ffffff;
            border: {border_style};
            border-radius: 8px;
        }}

        QLabel {{
            border: none;
            background-color: transparent;
            font-family: 'Segoe UI', Arial, sans-serif;
        }}

        QLabel#product_title {{
            font-size: 15px;
            font-weight: bold;
            color: #1e1e24;
            padding-top: 5px;
        }}

        QLabel#product_id {{
            font-size: 11px;
            color: #7f8c8d;
            font-weight: bold;
        }}

        QLabel#product_price {{
            font-size: 17px;
            font-weight: bold;
            color: #e53935;
        }}

        QLabel#product_stock {{
            font-size: 12px;
            color: #475569;
            font-weight: 600;
        }}

        QLabel#promo_tag {{
            background-color: #e53935;
            color: #ffffff;
            font-size: 10px;
            font-weight: bold;
            padding: 4px;
            border-radius: 4px;
        }}

        QPushButton {{
            border: none;
            border-radius: 4px;
            padding: 6px 10px;
            font-size: 11px;
            font-weight: bold;
            color: #ffffff;
        }}

        QPushButton#btn_edit {{ background-color: #2ecc71; }}
        QPushButton#btn_edit:hover {{ background-color: #27ae60; }}

        QPushButton#btn_promo {{ background-color: #ff9800; }}
        QPushButton#btn_promo:hover {{ background-color: #e68a00; }}

        QPushButton#btn_remove {{ background-color: #9c27b0; }}
        QPushButton#btn_remove:hover {{ background-color: #8e24aa; }}

        QPushButton#btn_delete {{ background-color: #e74c3c; }}
        QPushButton#btn_delete:hover {{ background-color: #c0392b; }}
    """


ESTILO_CONFIRM_DIALOG = """
    QMessageBox {
        background-color: #f5f6f8;
    }
    QLabel {
        color: #1e1e24;
        font-size: 13px;
    }
    QPushButton {
        background-color: #e2e8f0;
        color: #1e1e24;
        border: 1px solid #cbd5e1;
        border-radius: 4px;
        padding: 6px 15px;
        font-weight: bold;
        min-width: 65px;
    }
    QPushButton:hover {
        background-color: #cbd5e1;
    }
"""