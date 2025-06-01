import flet as ft
import mysql.connector
from conexionmysql import conecta

def empleados_view(page: ft.Page):
    conn = conecta()
    cursor = conn.cursor()

    txt_id = ft.TextField(label="ID", width=100)
    txt_nombre = ft.TextField(label="Nombre", width=150)
    txt_apellido = ft.TextField(label="Apellido", width=150)
    txt_numero = ft.TextField(label="Número", max_length=10, width=100)
    txt_puesto = ft.TextField(label="Puesto", width=150)

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("ID")),
            ft.DataColumn(label=ft.Text("Nombre")),
            ft.DataColumn(label=ft.Text("Apellido")),
            ft.DataColumn(label=ft.Text("Número")),
            ft.DataColumn(label=ft.Text("Puesto")),
        ],
        rows=[]
    )

    def cargar():
        tabla.rows.clear()
        cursor.execute("SELECT * FROM empleado")
        for emp in cursor.fetchall():
            tabla.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(str(col))) for col in emp]))
        page.update()

    def añadir(e):
        if all([txt_nombre.value, txt_apellido.value, txt_numero.value, txt_puesto.value]):
            cursor.execute(
                "INSERT INTO empleado (nombre_empleado, apellido_empleado, numero_empleado, puesto) VALUES (%s, %s, %s, %s)",
                (txt_nombre.value, txt_apellido.value, txt_numero.value, txt_puesto.value)
            )
            conn.commit()
            cargar()
            page.snack_bar = ft.SnackBar(ft.Text("Empleado añadido correctamente."), open=True)
            page.update()

    def buscar(e):
        if txt_id.value:
            cursor.execute("SELECT * FROM empleado WHERE idEmpleado = %s", (txt_id.value,))
            resultado = cursor.fetchone()
            if resultado:
                txt_nombre.value = resultado[1]
                txt_apellido.value = resultado[2]
                txt_numero.value = resultado[3]
                txt_puesto.value = resultado[4]
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Empleado no encontrado."), open=True)
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Ingresa un ID para buscar."), open=True)
        page.update()

    def eliminar(e):
        if txt_id.value:
            cursor.execute("DELETE FROM empleado WHERE idEmpleado = %s", (txt_id.value,))
            conn.commit()
            cargar()
            page.snack_bar = ft.SnackBar(ft.Text("Empleado eliminado."), open=True)
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Ingresa un ID para eliminar."), open=True)
        page.update()

    def actualizar(e):
        if all([txt_id.value, txt_nombre.value, txt_apellido.value, txt_numero.value, txt_puesto.value]):
            cursor.execute(
                "UPDATE empleado SET nombre_empleado = %s, apellido_empleado = %s, numero_empleado = %s, puesto = %s WHERE idEmpleado = %s",
                (txt_nombre.value, txt_apellido.value, txt_numero.value, txt_puesto.value, txt_id.value)
            )
            conn.commit()
            cargar()
            page.snack_bar = ft.SnackBar(ft.Text("Empleado actualizado."), open=True)
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Completa todos los campos."), open=True)
        page.update()

    # Cargar al inicio
    cargar()

    return ft.Column([
        ft.Text("Gestión de Empleados", size=24, weight="bold"),
        ft.Row([txt_id, txt_nombre, txt_apellido, txt_numero, txt_puesto], spacing=10),
        ft.Row([
            ft.ElevatedButton("Añadir", on_click=añadir),
            ft.ElevatedButton("Buscar", on_click=buscar),
            ft.ElevatedButton("Actualizar", on_click=actualizar),
            ft.ElevatedButton("Eliminar", on_click=eliminar),
        ], spacing=10),
        tabla
    ])
