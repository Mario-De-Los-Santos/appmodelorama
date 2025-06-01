import flet as ft
import mysql.connector
from datetime import datetime
from conexionmysql import conecta

def pedido_view(page: ft.Page):
    conn = conecta()
    cursor = conn.cursor()

    id_proveedor = ft.TextField(label="ID Proveedor", width=150)
    detalle_cantidad = ft.TextField(label="Cantidad", width=100)

    producto_dropdown = ft.Dropdown(label="Producto", width=300, options=[])

    detalles = []
    total_text = ft.Text("Total: $0.00", size=20, weight="bold", text_align="right")
    tabla_detalles = ft.DataTable(columns=[
        ft.DataColumn(ft.Text("Producto")),
        ft.DataColumn(ft.Text("Cantidad")),
        ft.DataColumn(ft.Text("Subtotal")),
        ft.DataColumn(ft.Text("Acciones"))
    ], rows=[])
    mensaje_resultado = ft.Text("", size=16, weight="bold")

    def cargar_productos():
        producto_dropdown.options.clear()
        cursor.execute("SELECT codigo, nombre_producto, precio_producto FROM producto WHERE stock >= 0")
        for codigo, nombre, precio in cursor.fetchall():
            producto_dropdown.options.append(
                ft.dropdown.Option(codigo, f"{nombre} (${precio:.2f})")
            )
        page.update()

    def actualizar_total():
        total = sum([d[3] for d in detalles])
        total_text.value = f"Total: ${total:.2f}"
        page.update()

    def eliminar_detalle(index):
        detalles.pop(index)
        tabla_detalles.rows.pop(index)
        actualizar_total()

    def añadir_detalle(e):
        if not producto_dropdown.value:
            return

        try:
            cantidad = int(detalle_cantidad.value)
            if cantidad <= 0:
                raise ValueError()
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Cantidad inválida."), open=True)
            return

        cursor.execute("SELECT nombre_producto, precio_producto FROM producto WHERE codigo = %s", (producto_dropdown.value,))
        res = cursor.fetchone()
        if not res:
            page.snack_bar = ft.SnackBar(ft.Text("Producto no válido."), open=True)
            return

        nombre, precio = res
        subtotal = precio * cantidad
        detalles.append((producto_dropdown.value, nombre, cantidad, subtotal))

        idx = len(tabla_detalles.rows)
        eliminar_btn = ft.IconButton(icon=ft.icons.DELETE, tooltip="Eliminar", on_click=lambda e, i=idx: eliminar_detalle(i))

        tabla_detalles.rows.append(ft.DataRow(cells=[
            ft.DataCell(ft.Text(nombre)),
            ft.DataCell(ft.Text(str(cantidad))),
            ft.DataCell(ft.Text(f"{subtotal:.2f}")),
            ft.DataCell(eliminar_btn)
        ]))

        producto_dropdown.value = None
        detalle_cantidad.value = ""
        producto_dropdown.focus()
        actualizar_total()

    def registrar_pedido(e):
        if not id_proveedor.value:
            page.snack_bar = ft.SnackBar(ft.Text("Completa el ID del proveedor."), open=True)
            return
        if not detalles:
            page.snack_bar = ft.SnackBar(ft.Text("Agrega al menos un producto al pedido."), open=True)
            return

        total = sum([d[3] for d in detalles])
        try:
            cursor.execute("INSERT INTO pedido (idProveedor, precio_total) VALUES (%s, %s)", (id_proveedor.value, total))
            id_pedido = cursor.lastrowid

            for codigo, _, cantidad, _ in detalles:
                cursor.execute("INSERT INTO detalles_pedido (idPedido, codigo, cantidad) VALUES (%s, %s, %s)", (id_pedido, codigo, cantidad))
                cursor.execute("UPDATE producto SET stock = stock + %s WHERE codigo = %s", (cantidad, codigo))

            conn.commit()
            detalles.clear()
            tabla_detalles.rows.clear()
            total_text.value = "Total: $0.00"
            mensaje_resultado.value = "✅ Pedido registrado y stock actualizado exitosamente."
            page.update()

        except mysql.connector.Error as err:
            conn.rollback()
            mensaje_resultado.value = f"❌ Error al registrar el pedido: {err}"
            page.update()

    cargar_productos()

    return ft.Column([
        ft.Text("Registrar Pedido", size=24, weight="bold"),
        ft.Row([id_proveedor], spacing=10),
        ft.Divider(),
        ft.Row([
            ft.Text("Añadir Producto", size=20, weight="bold"),
            ft.Container(content=total_text, expand=True, alignment=ft.alignment.center_right)
        ]),
        ft.Row([producto_dropdown, detalle_cantidad], spacing=10),
        ft.Row([ft.ElevatedButton("Añadir Detalle", on_click=añadir_detalle)]),
        tabla_detalles,
        ft.Container(
            content=ft.Row([
                ft.Container(expand=True),
                ft.ElevatedButton("Registrar Pedido", on_click=registrar_pedido),
            ]),
            padding=10
        ),
        mensaje_resultado
    ])
