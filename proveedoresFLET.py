import flet as ft

def main(page: ft.Page):
    page.title = "Registro de Proveedor"
    page.window_width = 640
    page.window_height = 480

    # Título
    titulo = ft.Text("Registro de Proveedor", size=30, weight="bold", text_align="center")

    # Campos de entrada
    txt_id = ft.TextField(label="ID Proveedor", width=300, keyboard_type=ft.KeyboardType.NUMBER)
    txt_nombre = ft.TextField(label="Nombre del Proveedor", width=300)
    txt_direccion = ft.TextField(label="Dirección del Proveedor", width=300)
    txt_telefono = ft.TextField(label="Teléfono del Proveedor", width=300)

    # Función del botón
    def registrar_proveedor(e):
        if all([txt_id.value, txt_nombre.value, txt_direccion.value, txt_telefono.value]):
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Proveedor registrado:\n"
                                f"ID: {txt_id.value}\n"
                                f"Nombre: {txt_nombre.value}\n"
                                f"Dirección: {txt_direccion.value}\n"
                                f"Teléfono: {txt_telefono.value}"),
                open=True
            )
        else:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Por favor, completa todos los campos."),
                open=True
            )
        page.update()

    # Botón
    btn_registrar = ft.ElevatedButton(text="Registrar Proveedor", on_click=registrar_proveedor)

    # Layout
    page.add(
        ft.Column(
            [
                titulo,
                txt_id,
                txt_nombre,
                txt_direccion,
                txt_telefono,
                btn_registrar
            ],
            spacing=15,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START
        )
    )

ft.app(target=main)
