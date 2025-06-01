import flet as ft
import mysql.connector
from datetime import date

def listaventas_view(page: ft.Page):
    page.title = "Consulta de Ventas"

    # Filtros
    filtro_id = ft.TextField(label="Buscar por ID de Venta", width=200)
    filtro_fecha = ft.TextField(label="Buscar por Fecha", width=200, read_only=True)

    def actualizar_fecha(e):
        if date_picker.value:
            filtro_fecha.value = str(date_picker.value)
            page.update()

    def abrir_calendario():
        date_picker.open = True
        page.update()

    date_picker = ft.DatePicker(
        on_change=actualizar_fecha,
        first_date=date(2023, 1, 1),
        last_date=date(2030, 12, 31)
    )
    page.overlay.append(date_picker)

    tabla_ventas = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID Venta")),
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Total")),
            ft.DataColumn(ft.Text("ID Empleado")),
            ft.DataColumn(ft.Text("Tel. Cliente")),
            ft.DataColumn(ft.Text("ID Pago")),
        ],
        rows=[]
    )

    tabla_detalles = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Código")),
            ft.DataColumn(ft.Text("Producto")),
            ft.DataColumn(ft.Text("Cantidad")),
            ft.DataColumn(ft.Text("Precio c/u"))  
        ],
        rows=[]
    )

    contenedor_detalles = ft.Column(visible=False)

    def mostrar_detalles(id_venta):
        conn = mysql.connector.connect(
            host="localhost", port="3310", user="root", password="mario19", database="modelorama"
        )
        cursor = conn.cursor()
        tabla_detalles.rows.clear()

        cursor.execute("""
            SELECT dv.codigo, p.nombre_producto, dv.cantidad, p.precio_producto
            FROM detalles_venta dv
            JOIN producto p ON dv.codigo = p.codigo
            WHERE dv.idVenta = %s
        """, (id_venta,))
        for codigo, nombre, cantidad, precio in cursor.fetchall():
            tabla_detalles.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(codigo)),
                    ft.DataCell(ft.Text(nombre)),
                    ft.DataCell(ft.Text(str(cantidad))),
                    ft.DataCell(ft.Text(f"${precio:.2f}"))
                ])
            )

        conn.close()
        contenedor_detalles.visible = True
        tabla_ventas.visible = False
        page.update()

    def cargar_ventas(filtro_id_val="", filtro_fecha_val=""):
        tabla_ventas.rows.clear()
        conn = mysql.connector.connect(
            host="localhost", port="3310", user="root", password="mario19", database="modelorama"
        )
        cursor = conn.cursor()

        query = "SELECT * FROM venta"
        condiciones = []
        valores = []

        if filtro_id_val:
            condiciones.append("idVenta LIKE %s")
            valores.append(f"%{filtro_id_val}%")
        if filtro_fecha_val:
            condiciones.append("DATE(fecha_venta) = %s")
            valores.append(filtro_fecha_val)

        if condiciones:
            query += " WHERE " + " AND ".join(condiciones)

        cursor.execute(query, valores)

        for fila in cursor.fetchall():
            id_venta, fecha, total, id_empleado, tel_cliente, id_pago = fila
            tabla_ventas.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(id_venta))),
                        ft.DataCell(ft.Text(str(fecha))),
                        ft.DataCell(ft.Text(f"${total:.2f}")),
                        ft.DataCell(ft.Text(str(id_empleado))),
                        ft.DataCell(ft.Text(tel_cliente)),
                        ft.DataCell(ft.Text(str(id_pago))),
                    ],
                    on_select_changed=lambda e, idv=id_venta: mostrar_detalles(idv)
                )
            )

        conn.close()
        page.update()

    # Acciones de los botones
    def buscar(e):
        cargar_ventas(filtro_id.value, filtro_fecha.value)

    def limpiar(e):
        filtro_id.value = ""
        filtro_fecha.value = ""
        cargar_ventas()

    def cerrar_detalles(e):
        contenedor_detalles.visible = False
        tabla_ventas.visible = True
        page.update()

    # Definición del contenedor de detalles
    contenedor_detalles.controls = [
        ft.Text("Detalles de Venta", size=20, weight="bold"),
        tabla_detalles,
        ft.ElevatedButton("Cerrar Detalles", on_click=cerrar_detalles)
    ]

    cargar_ventas()

    return ft.Column([
        ft.Text("Consulta de Ventas", size=24, weight="bold"),
        ft.Row([
            filtro_id,
            filtro_fecha,
            ft.IconButton(icon=ft.icons.CALENDAR_MONTH, on_click=lambda _: abrir_calendario())
        ]),
        ft.Row([
            ft.ElevatedButton("Buscar", on_click=buscar),
            ft.OutlinedButton("Limpiar", on_click=limpiar)
        ]),
        ft.Divider(),
        tabla_ventas,
        contenedor_detalles
    ])
