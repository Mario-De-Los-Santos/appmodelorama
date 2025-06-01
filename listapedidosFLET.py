import flet as ft
import mysql.connector
from datetime import date
from conexionmysql import conecta

def listapedidos_view(page: ft.Page):
    page.title = "Consulta de Pedidos"

    # Filtros
    filtro_id = ft.TextField(label="Buscar por ID de Pedido", width=200)

    tabla_pedidos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID Pedido")),
            ft.DataColumn(ft.Text("Proveedor")),
            ft.DataColumn(ft.Text("Total")),
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

    def mostrar_detalles(id_pedido):
        conn = conecta()
        cursor = conn.cursor()
        tabla_detalles.rows.clear()

        cursor.execute("""
            SELECT dp.codigo, p.nombre_producto, dp.cantidad, p.precio_producto
            FROM detalles_pedido dp
            JOIN producto p ON dp.codigo = p.codigo
            WHERE dp.idPedido = %s
        """, (id_pedido,))
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
        tabla_pedidos.visible = False
        page.update()

    def cargar_pedidos(filtro_id_val=""):
        tabla_pedidos.rows.clear()
        conn = mysql.connector.connect(
            host="localhost", port="3310", user="root", password="mario19", database="modelorama"
        )
        cursor = conn.cursor()

        query = """
            SELECT pe.idPedido, pr.nombre_proveedor, pe.precio_total
            FROM pedido pe
            JOIN proveedor pr ON pe.idProveedor = pr.idProveedor
        """
        condiciones = []
        valores = []

        if filtro_id_val:
            condiciones.append("pe.idPedido LIKE %s")
            valores.append(f"%{filtro_id_val}%")

        if condiciones:
            query += " WHERE " + " AND ".join(condiciones)

        cursor.execute(query, valores)

        for id_pedido, proveedor, total in cursor.fetchall():
            tabla_pedidos.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(id_pedido))),
                        ft.DataCell(ft.Text(proveedor)),
                        ft.DataCell(ft.Text(f"${total:.2f}")),
                    ],
                    on_select_changed=lambda e, idp=id_pedido: mostrar_detalles(idp)
                )
            )

        conn.close()
        page.update()

    # Acciones de los botones
    def buscar(e):
        cargar_pedidos(filtro_id.value)

    def limpiar(e):
        filtro_id.value = ""
        cargar_pedidos()

    def cerrar_detalles(e):
        contenedor_detalles.visible = False
        tabla_pedidos.visible = True
        page.update()

    # Definición del contenedor de detalles
    contenedor_detalles.controls = [
        ft.Text("Detalles del Pedido", size=20, weight="bold"),
        tabla_detalles,
        ft.ElevatedButton("Cerrar Detalles", on_click=cerrar_detalles)
    ]

    cargar_pedidos()

    return ft.Column([
        ft.Text("Consulta de Pedidos", size=24, weight="bold"),
        ft.Row([filtro_id]),
        ft.Row([
            ft.ElevatedButton("Buscar", on_click=buscar),
            ft.OutlinedButton("Limpiar", on_click=limpiar)
        ]),
        ft.Divider(),
        tabla_pedidos,
        contenedor_detalles
    ])
