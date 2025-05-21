import flet as ft
import mysql.connector

def pedido_view(page: ft.Page):
    conn = mysql.connector.connect(host="localhost", port="3310", user="root", password="mario19", database="modelorama")
    cursor = conn.cursor()

    id_pedido = ft.TextField(label="ID Pedido", width=150)
    codigo = ft.TextField(label="Código Producto", width=150)
    id_prov = ft.TextField(label="ID Proveedor", width=150)
    cantidad = ft.TextField(label="Cantidad", width=100)

    tabla = ft.DataTable(columns=[
        ft.DataColumn(ft.Text("ID Pedido")),
        ft.DataColumn(ft.Text("Código")),
        ft.DataColumn(ft.Text("Proveedor")),
        ft.DataColumn(ft.Text("Cantidad"))
    ], rows=[])

    def cargar():
        tabla.rows.clear()
        cursor.execute("SELECT * FROM pedido")
        for fila in cursor.fetchall():
            tabla.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(str(c))) for c in fila]))
        page.update()

    def añadir(e):
        cursor.execute("INSERT INTO pedido VALUES (%s, %s, %s, %s)",
                       (id_pedido.value, codigo.value, id_prov.value, cantidad.value))
        conn.commit()
        cargar()

    def buscar(e):
        cursor.execute("SELECT * FROM pedido WHERE idPedido=%s AND codigo=%s AND idProveedor=%s",
                       (id_pedido.value, codigo.value, id_prov.value))
        fila = cursor.fetchone()
        if fila:
            cantidad.value = str(fila[3])
        page.update()

    def actualizar(e):
        cursor.execute("UPDATE pedido SET cantidad=%s WHERE idPedido=%s AND codigo=%s AND idProveedor=%s",
                       (cantidad.value, id_pedido.value, codigo.value, id_prov.value))
        conn.commit()
        cargar()

    def eliminar(e):
        cursor.execute("DELETE FROM pedido WHERE idPedido=%s AND codigo=%s AND idProveedor=%s",
                       (id_pedido.value, codigo.value, id_prov.value))
        conn.commit()
        cargar()

    cargar()
    return ft.Column([
        ft.Text("Gestión de Pedidos", size=24, weight="bold"),
        ft.Row([id_pedido, codigo, id_prov, cantidad], spacing=10),
        ft.Row([
            ft.ElevatedButton("Añadir", on_click=añadir),
            ft.ElevatedButton("Buscar", on_click=buscar),
            ft.ElevatedButton("Actualizar", on_click=actualizar),
            ft.ElevatedButton("Eliminar", on_click=eliminar),
        ]),
        tabla
    ])
