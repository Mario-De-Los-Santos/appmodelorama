import flet as ft
import mysql.connector

def clientes_view(page: ft.Page):
    conn = mysql.connector.connect(
        host="localhost",
        port="3310",
        user="root",
        password="mario19",
        database="modelorama"
    )
    cursor = conn.cursor()

    txt_telefono = ft.TextField(label="Teléfono", max_length=10, width=150)
    txt_nombre = ft.TextField(label="Nombre", width=250)
    txt_rfc = ft.TextField(label="RFC", max_length=13, width=200)

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Teléfono")),
            ft.DataColumn(label=ft.Text("Nombre")),
            ft.DataColumn(label=ft.Text("RFC"))
        ],
        rows=[]
    )

    def cargar():
        tabla.rows.clear()
        cursor.execute("SELECT * FROM cliente")
        for cli in cursor.fetchall():
            tabla.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(str(col))) for col in cli]))
        page.update()

    def añadir(e):
        if all([txt_telefono.value, txt_nombre.value, txt_rfc.value]):
            cursor.execute("INSERT INTO cliente VALUES (%s, %s, %s)",
                           (txt_telefono.value, txt_nombre.value, txt_rfc.value))
            conn.commit()
            cargar()
        page.update()

    def buscar(e):
        cursor.execute("SELECT * FROM cliente WHERE telefono = %s", (txt_telefono.value,))
        resultado = cursor.fetchone()
        if resultado:
            txt_nombre.value = resultado[1]
            txt_rfc.value = resultado[2]
        page.update()

    def eliminar(e):
        cursor.execute("DELETE FROM cliente WHERE telefono = %s", (txt_telefono.value,))
        conn.commit()
        cargar()
        page.update()

    def actualizar(e):
        cursor.execute("UPDATE cliente SET nombre_cliente = %s, RFC = %s WHERE telefono = %s",
                       (txt_nombre.value, txt_rfc.value, txt_telefono.value))
        conn.commit()
        cargar()
        page.update()

    return ft.Column([
        ft.Text("Gestión de Clientes", size=24, weight="bold"),
        ft.Row([txt_telefono, txt_nombre, txt_rfc], spacing=10),
        ft.Row([
            ft.ElevatedButton("Añadir", on_click=añadir),
            ft.ElevatedButton("Buscar", on_click=buscar),
            ft.ElevatedButton("Eliminar", on_click=eliminar),
            ft.ElevatedButton("Actualizar", on_click=actualizar),
        ], spacing=10),
        tabla
    ])
