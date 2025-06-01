import flet as ft
import mysql.connector
from conexionmysql import conecta

def unidad_view(page: ft.Page):
    conn = conecta()
    cursor = conn.cursor()

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("ID")),
            ft.DataColumn(label=ft.Text("Tipo de Unidad")),
        ],
        rows=[]
    )

    def cargar():
        tabla.rows.clear()
        cursor.execute("SELECT * FROM unidad")
        for fila in cursor.fetchall():
            tabla.rows.append(
                ft.DataRow(cells=[ft.DataCell(ft.Text(str(col))) for col in fila])
            )
        page.update()

    cargar()

    return ft.Column([
        ft.Text("Unidades existentes", size=24, weight="bold"),
        tabla
    ])
