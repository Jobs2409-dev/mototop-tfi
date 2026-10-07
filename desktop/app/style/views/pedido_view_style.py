# desktop/app/style/views/pedido_view_style.py
ESTILO_ADMIN_PEDIDOS = """
    QWidget#main_view {
        background-color: #f5f6f8;                 /* Gris claro moderno de fondo general */
        font-family: 'Segoe UI', Arial, sans-serif;
    }

    /* Área de Scroll donde viven las tarjetas */
    QScrollArea {
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        background-color: #ffffff;
    }

    QWidget#scroll_container {
        background-color: #ffffff;                 /* Blanco limpio para el contenedor interno */
    }

    /* Botón Nuevo Pedido (Rojo Administrativo) */
    QPushButton#btn_nuevo_pedido {
        background-color: #e53935;                 /* Rojo destacado */
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
        font-size: 13px;
    }

    QPushButton#btn_nuevo_pedido:hover {
        background-color: #d32f2f;                 /* Rojo más oscuro al pasar el mouse */
    }

    QPushButton#btn_nuevo_pedido:pressed {
        background-color: #b71c1c;                 /* Rojo profundo al hacer clic */
    }

    /* Botón Refrescar (Azul para contrastar) */
    QPushButton#btn_refrescar {
        background-color: #1976d2;                 /* Azul profesional */
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
        font-size: 13px;
    }

    QPushButton#btn_refrescar:hover {
        background-color: #1565c0;                 /* Azul más oscuro al pasar el mouse */
    }

    QPushButton#btn_refrescar:pressed {
        background-color: #0d47a1;                 /* Azul profundo al hacer clic */
    }

    /* Botón Limpiar (Naranja para advertencia) */
    QPushButton#btn_limpiar {
        background-color: #f57c00;                 /* Naranja profesional */
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
        font-size: 13px;
    }

    QPushButton#btn_limpiar:hover {
        background-color: #e65100;                 /* Naranja más oscuro al pasar el mouse */
    }

    QPushButton#btn_limpiar:pressed {
        background-color: #bf360c;                 /* Naranja profundo al hacer clic */
    }

    /* Contenedor de botones horizontales */
    QWidget#botones_container {
        background-color: #f5f6f8;
    }
"""
