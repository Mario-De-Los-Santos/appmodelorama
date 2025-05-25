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

    id_venta = ft.TextField(label="ID Venta", width=100)
    id_empleado = ft.TextField(label="ID Empleado",width=100)
    tel_cliente = ft.TextField(label="Teléfono Cliente", max_length=10 , width=130)
    id_pago = ft.TextField(label="ID Método Pago", width=100)

    detalle_codigo = ft.TextField(label="Código Producto", autofocus=True, max_length=13 , width=180)
    detalle_cantidad = ft.TextField(label="Cantidad", width=100)
    detalles = []

    tabla_detalles = ft.DataTable(columns=[
        ft.DataColumn(ft.Text("Producto")),
        ft.DataColumn(ft.Text("Cantidad")),
        ft.DataColumn(ft.Text("Subtotal"))
    ], rows=[])

    # Etiqueta para mostrar confirmación
    mensaje_resultado = ft.Text("", size=16, weight="bold")

    def añadir_detalle(e):
        if not detalle_codigo.value:
            return

        try:
            cantidad = int(detalle_cantidad.value) if detalle_cantidad.value else 1
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Cantidad inválida."), open=True)
            return

        cursor.execute("SELECT precio_producto, stock FROM producto WHERE codigo = %s", (detalle_codigo.value,))
        res = cursor.fetchone()

        if not res:
            page.snack_bar = ft.SnackBar(ft.Text("Código de producto no válido."), open=True)
            return

        precio, stock_disponible = res
        if cantidad > stock_disponible:
            page.snack_bar = ft.SnackBar(ft.Text(f"❌ Stock insuficiente (disponible: {stock_disponible})"), open=True)
            return

        subtotal = precio * cantidad
        detalles.append((detalle_codigo.value, cantidad, subtotal))
        tabla_detalles.rows.append(ft.DataRow(cells=[
            ft.DataCell(ft.Text(detalle_codigo.value)),
            ft.DataCell(ft.Text(str(cantidad))),
            ft.DataCell(ft.Text(f"{subtotal:.2f}"))
        ]))

        detalle_codigo.value = ""
        detalle_cantidad.value = ""
        page.update()


    def añadir_venta(e):
        if not (id_venta.value and id_empleado.value and tel_cliente.value and id_pago.value):
            page.snack_bar = ft.SnackBar(ft.Text("Completa todos los campos de la venta."), open=True)
            return
        if not detalles:
            page.snack_bar = ft.SnackBar(ft.Text("Agrega al menos un detalle de venta."), open=True)
            return

        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        total = sum([d[2] for d in detalles])

        try:
            cursor.execute("INSERT INTO venta VALUES (%s, %s, %s, %s, %s, %s)",
                        (id_venta.value, fecha_actual, total, id_empleado.value, tel_cliente.value, id_pago.value))

            for codigo, cantidad, subtotal in detalles:
                cursor.execute("INSERT INTO detalles_venta (idVenta, codigo, cantidad) VALUES (%s, %s, %s)",
                            (id_venta.value, codigo, cantidad))
                cursor.execute("UPDATE producto SET stock = stock - %s WHERE codigo = %s", (cantidad, codigo))

            conn.commit()
            detalles.clear()
            tabla_detalles.rows.clear()

            mensaje_resultado.value = "✅ Venta registrada y stock actualizado exitosamente."
            page.update()

        except mysql.connector.Error as err:
            conn.rollback()
            mensaje_resultado.value = f"❌ Error al registrar la venta: {err}"
            page.update()

    return ft.Column([
        ft.Text("Registrar Venta", size=24, weight="bold"),
        ft.Row([id_venta], spacing=10),
        ft.Row([id_empleado, tel_cliente, id_pago], spacing=10),
        ft.Row([
            ft.ElevatedButton("Guardar Venta + Detalles", on_click=añadir_venta),
        ]),
        mensaje_resultado,
        ft.Divider(),
        ft.Text("Añadir Detalles de Venta", size=20, weight="bold"),
        ft.Row([detalle_codigo, detalle_cantidad], spacing=10),
        ft.Row([
            ft.ElevatedButton("Añadir Detalle", on_click=añadir_detalle),
        ]),
        tabla_detalles
    ])
