import flet as ft
import mysql.connector
from datetime import datetime

def venta_view(page: ft.Page):
    conn = mysql.connector.connect(
        host="localhost", port="3310",
        user="root",
        password="mario19",
        database="modelorama"
    )
    cursor = conn.cursor()

    id_empleado = ft.TextField(label="ID Empleado", width=100)
    tel_cliente = ft.TextField(label="Teléfono Cliente", max_length=10, width=130)

    metodo_pago_dropdown = ft.Dropdown(
        label="Método de Pago",
        width=150,
        options=[
            ft.dropdown.Option("1", "Efectivo"),
            ft.dropdown.Option("2", "Tarjeta")
        ]
    )

    detalle_cantidad = ft.TextField(label="Cantidad", width=100)

    detalles = []
    total_text = ft.Text("Total: $0.00", size=20, weight="bold", text_align="right")

    tabla_detalles = ft.DataTable(columns=[
        ft.DataColumn(ft.Text("Producto")),
        ft.DataColumn(ft.Text("Cantidad")),
        ft.DataColumn(ft.Text("Subtotal")),
        ft.DataColumn(ft.Text("Acciones"))
    ], rows=[])

    mensaje_resultado = ft.Text("", size=16, weight="bold")

    def actualizar_total():
        total = sum([d[3] for d in detalles])
        total_text.value = f"Total: ${total:.2f}"
        page.update()

    def eliminar_detalle(index):
        detalles.pop(index)
        tabla_detalles.rows.pop(index)
        actualizar_total()

    def añadir_detalle(e):
        if not detalle_codigo.value:
            return

        try:
            cantidad = int(detalle_cantidad.value) if detalle_cantidad.value else 1
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Cantidad inválida."), open=True)
            return

        cursor.execute("SELECT nombre_producto, precio_producto, stock FROM producto WHERE codigo = %s", (detalle_codigo.value,))
        res = cursor.fetchone()

        if not res:
            page.snack_bar = ft.SnackBar(ft.Text("Código de producto no válido."), open=True)
            return

        nombre, precio, stock_disponible = res

        if cantidad > stock_disponible:
            page.snack_bar = ft.SnackBar(ft.Text(f"❌ Stock insuficiente (disponible: {stock_disponible})"), open=True)
            return

        subtotal = precio * cantidad
        detalles.append((detalle_codigo.value, nombre, cantidad, subtotal))

        idx = len(tabla_detalles.rows)

        eliminar_btn = ft.IconButton(
            icon=ft.icons.DELETE,
            tooltip="Eliminar",
            on_click=lambda e, i=idx: eliminar_detalle(i)
        )

        tabla_detalles.rows.append(ft.DataRow(cells=[
            ft.DataCell(ft.Text(nombre)),
            ft.DataCell(ft.Text(str(cantidad))),
            ft.DataCell(ft.Text(f"{subtotal:.2f}")),
            ft.DataCell(eliminar_btn)
        ]))

        detalle_codigo.value = ""
        detalle_cantidad.value = ""
        detalle_codigo.focus()  # ← vuelve a enfocar para siguiente escaneo
        actualizar_total()

    # Se declara después de añadir_detalle para evitar error
    detalle_codigo = ft.TextField(
        label="Código Producto",
        autofocus=True,
        max_length=13,
        width=180,
        on_submit=añadir_detalle  # ← importante: ya está definida
    )

    def añadir_venta(e):
        if not (id_empleado.value and tel_cliente.value and metodo_pago_dropdown.value):
            page.snack_bar = ft.SnackBar(ft.Text("Completa todos los campos de la venta."), open=True)
            return
        if not detalles:
            page.snack_bar = ft.SnackBar(ft.Text("Agrega al menos un detalle de venta."), open=True)
            return

        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        total = sum([d[3] for d in detalles])

        try:
            cursor.execute("INSERT INTO venta (fecha_venta, total, idEmpleado, telefono_cliente, idMetodo_pago) VALUES (%s, %s, %s, %s, %s)",
                           (fecha_actual, total, id_empleado.value, tel_cliente.value, metodo_pago_dropdown.value))
            venta_id = cursor.lastrowid

            for codigo, nombre, cantidad, subtotal in detalles:
                cursor.execute("INSERT INTO detalles_venta (idVenta, codigo, cantidad) VALUES (%s, %s, %s)",
                               (venta_id, codigo, cantidad))
                cursor.execute("UPDATE producto SET stock = stock - %s WHERE codigo = %s", (cantidad, codigo))

            conn.commit()
            detalles.clear()
            tabla_detalles.rows.clear()
            total_text.value = "Total: $0.00"
            mensaje_resultado.value = "✅ Venta registrada y stock actualizado exitosamente."
            page.update()

        except mysql.connector.Error as err:
            conn.rollback()
            mensaje_resultado.value = f"❌ Error al registrar la venta: {err}"
            page.update()

    return ft.Column([
        ft.Text("Registrar Venta", size=24, weight="bold"),
        ft.Row([id_empleado, tel_cliente, metodo_pago_dropdown], spacing=10),
        ft.Divider(),
        ft.Row([
            ft.Text("Añadir Producto", size=20, weight="bold"),
            ft.Container(content=total_text, expand=True, alignment=ft.alignment.center_right)
        ]),
        ft.Row([detalle_codigo, detalle_cantidad], spacing=10),
        ft.Row([ft.ElevatedButton("Añadir Detalle", on_click=añadir_detalle)]),
        tabla_detalles,
        ft.Container(
            content=ft.Row([
                ft.Container(expand=True),
                ft.ElevatedButton("Realizar venta", on_click=añadir_venta),
            ]),
            padding=10
        ),
        mensaje_resultado
    ])
