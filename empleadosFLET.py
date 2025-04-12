import flet as ft

def main(page: ft.Page):
    page.title = "Registro de Empleados"
    page.window_width = 400
    page.window_height = 300

    # Título
    titulo = ft.Text("Registro de Empleados", size=30, weight="bold", text_align="center")

    # Campos de entrada
    txt_nombre = ft.TextField(label="Nombre Empleado", width=300)
    txt_apellido = ft.TextField(label="Apellido Empleado", width=300)
    txt_numero = ft.TextField(label="Número Empleado", width=300)
    txt_puesto = ft.TextField(label="Puesto", width=300)

    # Función al hacer clic en el botón
    def añadir_empleado(e):
        if all([txt_nombre.value, txt_apellido.value, txt_numero.value, txt_puesto.value]):
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Empleado añadido:\n"
                                f"Nombre: {txt_nombre.value} {txt_apellido.value}\n"
                                f"Número: {txt_numero.value}\n"
                                f"Puesto: {txt_puesto.value}"),
                open=True
            )
        else:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Por favor, completa todos los campos."),
                open=True
            )
        page.update()

    # Botón para añadir empleado
    btn_añadir = ft.ElevatedButton(text="Añadir Empleado", on_click=añadir_empleado)

    # Layout principal
    page.add(
        ft.Column(
            [
                titulo,
                txt_nombre,
                txt_apellido,
                txt_numero,
                txt_puesto,
                btn_añadir
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=15,
            expand=True
        )
    )

ft.app(target=main)

