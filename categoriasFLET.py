import flet as ft
import mysql.connector

def categorias_view(page: ft.Page):
    conn = mysql.connector.connect(
        host="localhost",
        port="3310",
        user="root",
        password="mario19",
        database="modelorama"
    )
    cursor = conn.cursor()

    id_categoria = ft.TextField(label="ID Categoría", width=150)
    nombre_categoria = ft.TextField(label="Nombre", width=250)
    descripcion_categoria = ft.TextField(label="Descripción", multiline=True, min_lines=2, max_lines=3, width=300)

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("ID")),
            ft.DataColumn(label=ft.Text("Nombre")),
            ft.DataColumn(label=ft.Text("Descripción")),
        ],
        rows=[]
    )

    def cargar():
        tabla.rows.clear()
        cursor.execute("SELECT * FROM categoria")
        for cat in cursor.fetchall():
            tabla.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(str(col))) for col in cat]))
        page.update()

    def guardar(e):
        if all([id_categoria.value, nombre_categoria.value, descripcion_categoria.value]):
            cursor.execute("INSERT INTO categoria VALUES (%s, %s, %s)",
                           (id_categoria.value, nombre_categoria.value, descripcion_categoria.value))
            conn.commit()
            cargar()
        page.update()

    def buscar(e):
        cursor.execute("SELECT * FROM categoria WHERE idCategoria = %s", (id_categoria.value,))
        resultado = cursor.fetchone()
        if resultado:
            nombre_categoria.value = resultado[1]
            descripcion_categoria.value = resultado[2]
        page.update()

    def eliminar(e):
        cursor.execute("DELETE FROM categoria WHERE idCategoria = %s", (id_categoria.value,))
        conn.commit()
        cargar()
        page.update()

    return ft.Column([
        ft.Text("Categorías de Productos", size=24, weight="bold"),
        ft.Row([id_categoria, nombre_categoria, descripcion_categoria], spacing=10),
        ft.Row([
            ft.ElevatedButton("Guardar", on_click=guardar),
            ft.ElevatedButton("Buscar", on_click=buscar),
            ft.ElevatedButton("Eliminar", on_click=eliminar),
        ], spacing=10),
        tabla
    ])
