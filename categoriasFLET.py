import flet as ft

def main(page: ft.Page):
    page.title = "Formulario de Categoría"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # Esto centra horizontalmente


   # Título principal
    titulo = ft.Text(
        value="Categorías de productos",
        size=24,
        weight="bold",
        text_align="center"
    )

    # Campos de entrada
    id_categoria = ft.TextField(label="ID Categoría", keyboard_type="number")
    nombre_categoria = ft.TextField(label="Nombre de la categoría")
    descripcion_categoria = ft.TextField(label="Descripción", multiline=True)

    # Área para mostrar los datos ingresados
    resultado = ft.Text()

    def guardar_categoria(e):
        resultado.value = f"ID: {id_categoria.value}\nNombre: {nombre_categoria.value}\nDescripción: {descripcion_categoria.value}"
        page.update()

    # Botón
    btn_guardar = ft.ElevatedButton(text="Guardar", on_click=guardar_categoria)

    # Agregamos los controles dentro de un contenedor centrado
    page.add(
        ft.Container(
            content=ft.Column([
                titulo,
                id_categoria,
                nombre_categoria,
                descripcion_categoria,
                btn_guardar,
                resultado
            ], width=400, alignment=ft.MainAxisAlignment.CENTER),
            alignment=ft.alignment.center
        )
    )

ft.app(target=main)
