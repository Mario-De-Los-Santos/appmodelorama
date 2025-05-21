import flet as ft
import mysql.connector

def venta_view(page: ft.Page):
    conn = mysql.connector.connect(host="localhost", port="3310", user="root", password="mario19", database="modelorama")
    cursor = conn.cursor()

    id_venta = ft.TextField(label="ID Venta", width=100)
    fecha = ft.TextField(label="Fecha (YYYY-MM-DD HH:MM:SS)", width=220)
    id_empleado = ft.TextField(label="ID Empleado", width=100)
    tel_cliente = ft.TextField(label="Teléfono Cliente", width=130)
    id_pago = ft.TextField(label="ID Método Pago", width=100)

    detalle_codigo = ft.TextField(label="Código Producto", width=180)
    detalle_cantidad = ft.TextField(label="Cantidad", width=100)
    detalles = []

    tabla_ventas = ft.DataTable(columns=[
        ft.DataColumn(ft.Text("ID")),
        ft.DataColumn(ft.Text("Fecha")),
        ft.DataColumn(ft.Text("Total")),
        ft.DataColumn(ft.Text("Empleado")),
        ft.DataColumn(ft.Text("Cliente")),
        ft.DataColumn(ft.Text("Pago"))
    ], rows=[])

    tabla_detalles = ft.DataTable(columns=[
        ft.DataColumn(ft.Text("Producto")),
        ft.DataColumn(ft.Text("Cantidad")),
        ft.DataColumn(ft.Text("Subtotal"))
    ], rows=[])

    def cargar():
        tabla_ventas.rows.clear()
        cursor.execute("SELECT * FROM venta")
        for fila in cursor.fetchall():
            tabla_ventas.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(str(c))) for c in fila]))
        page.update()

    def añadir_detalle(e):
        if detalle_codigo.value and detalle_cantidad.value:
            cursor.execute("SELECT precio_producto FROM producto WHERE codigo = %s", (detalle_codigo.value,))
            res = cursor.fetchone()
            if not res:
                page.snack_bar = ft.SnackBar(ft.Text("Código de producto no válido."), open=True)
                return
            precio = float(res[0])
            cantidad = int(detalle_cantidad.value)
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
        if not (id_venta.value and fecha.value and id_empleado.value and tel_cliente.value and id_pago.value):
            page.snack_bar = ft.SnackBar(ft.Text("Completa todos los campos de la venta."), open=True)
            return
        if not detalles:
            page.snack_bar = ft.SnackBar(ft.Text("Agrega al menos un detalle de venta."), open=True)
            return
        total = sum([d[2] for d in detalles])  # suma de subtotales
        cursor.execute("INSERT INTO venta VALUES (%s, %s, %s, %s, %s, %s)",
                       (id_venta.value, fecha.value, total, id_empleado.value, tel_cliente.value, id_pago.value))
        for codigo, cantidad, subtotal in detalles:
            cursor.execute("INSERT INTO detalles_venta (idVenta, codigo, total) VALUES (%s, %s, %s)",
                           (id_venta.value, codigo, cantidad))
        conn.commit()
        detalles.clear()
        tabla_detalles.rows.clear()
        cargar()
        page.snack_bar = ft.SnackBar(ft.Text("Venta registrada exitosamente."), open=True)
        page.update()

    cargar()
    return ft.Column([
        ft.Text("Gestión de Ventas", size=24, weight="bold"),
        ft.Row([id_venta, fecha], spacing=10),
        ft.Row([id_empleado, tel_cliente, id_pago], spacing=10),
        ft.Row([
            ft.ElevatedButton("Guardar Venta + Detalles", on_click=añadir_venta),
        ]),
        tabla_ventas,
        ft.Divider(),
        ft.Text("Añadir Detalles de Venta", size=20, weight="bold"),
        ft.Row([detalle_codigo, detalle_cantidad], spacing=10),
        ft.Row([
            ft.ElevatedButton("Añadir Detalle", on_click=añadir_detalle),
        ]),
        tabla_detalles
    ])
