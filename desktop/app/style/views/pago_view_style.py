# desktop/app/style/views/informe_view_style.py
QSS_STYLE_CLARO = """
    QWidget {
        background-color: #f8f9fa;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 13px;
        color: #212529;
    }
    
    /* Indicador del Panel Principal */
    QLabel#infoLabel {
        background-color: #ffffff;
        border-left: 4px solid #dc3545;
        padding: 14px;
        font-size: 15px;
        font-weight: bold;
        border-radius: 4px;
        color: #212529;
        border: 1px solid #e9ecef;
    }
    
    /* Contenedor con scroll para las tarjetas */
    QScrollArea {
        border: none;
        background-color: #f8f9fa;
    }
    
    /* Diseño de la Tarjeta de cada Factura */
    QFrame#cardFactura {
        background-color: #ffffff;
        border: 1px solid #e9ecef;
        border-radius: 6px;
        margin-bottom: 15px;
    }
    
    QLabel#cardTitle {
        font-size: 14px;
        font-weight: bold;
        color: #1a1a1a;
    }
    
    QLabel#cardBadgePendiente {
        background-color: #fff3cd;
        color: #856404;
        padding: 3px 8px;
        font-weight: bold;
        border-radius: 4px;
        font-size: 11px;
    }
    
    QLabel#cardBadgePagada {
        background-color: #d4edda;
        color: #155724;
        padding: 3px 8px;
        font-weight: bold;
        border-radius: 4px;
        font-size: 11px;
    }
    
    QLabel#cardSummaryText {
        font-size: 12px;
        color: #495057;
        font-weight: 500;
    }
    
    /* Botones de acción dentro de la tarjeta */
    QPushButton {
        background-color: #212529;
        color: #ffffff;
        border: none;
        border-radius: 4px;
        padding: 6px 12px;
        font-weight: bold;
        min-width: 70px;
    }
    QPushButton:hover {
        background-color: #dc3545;
    }
    QPushButton:pressed {
        background-color: #b02a37;
    }
    QPushButton#btn_recargar_global {
        background-color: #ffffff;
        color: #212529;
        border: 1px solid #ced4da;
        padding: 8px 16px;
    }
    QPushButton#btn_recargar_global:hover {
        background-color: #e2e6ea;
        color: #212529;
    }
    
    /* Grilla de pagos interna de la tarjeta */
    QTableWidget {
        background-color: #ffffff;
        border: 1px solid #e9ecef;
        gridline-color: #f1f3f5;
        border-radius: 4px;
    }
    QTableWidget::item {
        padding: 5px;
        color: #495057;
    }
    QTableWidget::item:selected {
        background-color: #f1f3f5;
        color: #dc3545;
        font-weight: bold;
    }
    QHeaderView::section {
        background-color: #f1f3f5;
        color: #495057;
        padding: 6px;
        border: 1px solid #e9ecef;
        font-weight: bold;
        font-size: 11px;
    }
    
    QScrollBar:vertical {
        border: none;
        background: #f8f9fa;
        width: 8px;
    }
    QScrollBar::handle:vertical {
        background: #ced4da;
        border-radius: 4px;
    }
    QScrollBar::handle:vertical:hover {
        background: #adb5bd;
    }
"""