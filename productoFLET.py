import flet as ft
import mysql.connector

def producto_view(page: ft.Page):
    conn = mysql.connector.connect(host="localhost", port="3310", user="root", password="mario19", database="modelorama")
    cursor = conn.cursor()

    codigo = ft.TextField(label="Código",max_length=13, width=130)
    nombre = ft.TextField(label="Nombre", width=150)
    precio = ft.TextField(label="Precio", width=100)
    stock = ft.TextField(label="Stock", width=100)
    id_categoria = ft.TextField(label="ID Categoría", width=100)
    id_unidad = ft.TextField(label="ID Unidad", width=100)

    tabla = ft.DataTable(columns=[
        ft.DataColumn(ft.Text("Código")),
        ft.DataColumn(ft.Text("Nombre")),
        ft.DataColumn(ft.Text("Precio")),
        ft.DataColumn(ft.Text("Stock")),
        ft.DataColumn(ft.Text("Categoría")),
        ft.DataColumn(ft.Text("Unidad"))
    ], rows=[])

    def cargar():
        tabla.rows.clear()
        cursor.execute("SELECT * FROM producto")
        for fila in cursor.fetchall():
            tabla.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(str(c))) for c in fila]))
        page.update()

    def añadir(e):
        cursor.execute("INSERT INTO producto VALUES (%s, %s, %s, %s, %s, %s)",
                       (codigo.value, nombre.value, precio.value, stock.value, id_categoria.value, id_unidad.value))
        conn.commit()
        cargar()

    def buscar(e):
        cursor.execute("SELECT * FROM producto WHERE codigo = %s", (codigo.value,))
        fila = cursor.fetchone()
        if fila:
            nombre.value, precio.value, stock.value, id_categoria.value, id_unidad.value = fila[1:]
        page.update()

    def actualizar(e):
        cursor.execute("UPDATE producto SET nombre_producto=%s, precio_producto=%s, stock=%s, idCategoria=%s, idUnidad=%s WHERE codigo=%s",
                       (nombre.value, precio.value, stock.value, id_categoria.value, id_unidad.value, codigo.value))
        conn.commit()
        cargar()

    def eliminar(e):
        cursor.execute("DELETE FROM producto WHERE codigo = %s", (codigo.value,))
        conn.commit()
        cargar()

    cargar()
    return ft.Column([
        ft.Text("Gestión de Productos", size=24, weight="bold"),
        ft.Row([codigo, nombre, precio, stock, id_categoria, id_unidad], spacing=10),
        ft.Row([
            ft.ElevatedButton("Añadir", on_click=añadir),
            ft.ElevatedButton("Buscar", on_click=buscar),
            ft.ElevatedButton("Actualizar", on_click=actualizar),
            ft.ElevatedButton("Eliminar", on_click=eliminar),
        ]),
        tabla
    ])
