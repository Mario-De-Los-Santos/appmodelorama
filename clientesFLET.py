import flet as ft

def main(page: ft.Page):
    page.title = "Registro de Cliente"
    page.window_width = 400
    page.window_height = 400

    # Campos de entrada
    txt_telefono = ft.TextField(label="Teléfono", max_length=10, width=300, keyboard_type=ft.KeyboardType.NUMBER)
    txt_nombre = ft.TextField(label="Nombre del Cliente", max_length=45, width=300)
    txt_rfc = ft.TextField(label="RFC", max_length=13, width=300)

    # Función para manejar el botón guardar
    def guardar_datos(e):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Cliente registrado:\nTel: {txt_telefono.value}\nNombre: {txt_nombre.value}\nRFC: {txt_rfc.value}"),
            open=True
        )
        page.update()

    # Botón de guardar
    btn_guardar = ft.ElevatedButton(text="Guardar Cliente", on_click=guardar_datos)

    # Layout
    page.add(
        ft.Column(
            [
                ft.Text("Formulario de Cliente", size=24, weight="bold"),
                txt_telefono,
                txt_nombre,
                txt_rfc,
                btn_guardar
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START
        )
    )

ft.app(target=main)
