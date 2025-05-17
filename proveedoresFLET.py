import flet as ft
import mysql.connector

def proveedores_view(page: ft.Page):
    conn = mysql.connector.connect(
        host="localhost",
        port="3310",  
        user="root",
        password="mario19",
        database="modelorama"
    )
    cursor = conn.cursor()

    txt_id = ft.TextField(label="ID Proveedor", width=150)
    txt_nombre = ft.TextField(label="Nombre del Proveedor", width=200)
    txt_direccion = ft.TextField(label="Dirección", width=250)
    txt_telefono = ft.TextField(label="Teléfono", max_length=10, width=150)

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("ID")),
            ft.DataColumn(label=ft.Text("Nombre")),
            ft.DataColumn(label=ft.Text("Dirección")),
            ft.DataColumn(label=ft.Text("Teléfono")),
        ],
        rows=[]
    )

    def cargar():
        tabla.rows.clear()
        cursor.execute("SELECT * FROM proveedor")
        for row in cursor.fetchall():
            tabla.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(col))) for col in row
                ])
            )
        page.update()

    def registrar(e):
        if all([txt_id.value, txt_nombre.value, txt_direccion.value, txt_telefono.value]):
            try:
                cursor.execute(
                    "INSERT INTO proveedor VALUES (%s, %s, %s, %s)",
                    (txt_id.value, txt_nombre.value, txt_direccion.value, txt_telefono.value)
                )
                conn.commit()
                cargar()
                page.snack_bar = ft.SnackBar(ft.Text("Proveedor registrado."), open=True)
            except Exception as err:
                page.snack_bar = ft.SnackBar(ft.Text(f"Error: {err}"), open=True)
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Completa todos los campos."), open=True)
        page.update()

    def buscar(e):
        cursor.execute("SELECT * FROM proveedor WHERE idproveedor = %s", (txt_id.value,))
        row = cursor.fetchone()
        if row:
            txt_nombre.value = row[1]
            txt_direccion.value = row[2]
            txt_telefono.value = row[3]
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Proveedor no encontrado."), open=True)
        page.update()

    def eliminar(e):
        cursor.execute("DELETE FROM proveedor WHERE idproveedor = %s", (txt_id.value,))
        conn.commit()
        cargar()
        page.snack_bar = ft.SnackBar(ft.Text("Proveedor eliminado."), open=True)
        page.update()

    # Cargar datos al iniciar
    cargar()

    return ft.Column([
        ft.Text("Gestión de Proveedores", size=24, weight="bold"),
        ft.Row([txt_id, txt_nombre, txt_direccion, txt_telefono], spacing=10),
        ft.Row([
            ft.ElevatedButton("Registrar", on_click=registrar),
            ft.ElevatedButton("Buscar", on_click=buscar),
            ft.ElevatedButton("Eliminar", on_click=eliminar)
        ], spacing=10),
        tabla
    ])
