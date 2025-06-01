import flet as ft
from proveedoresFLET import proveedores_view
from categoriasFLET import categorias_view
from clientesFLET import clientes_view
from empleadosFLET import empleados_view
from unidadFLET import unidad_view
from productoFLET import producto_view
from ventaFLET import venta_view
from pedidoFLET import pedido_view
from listaventasFLET import listaventas_view
from listapedidosFLET import listapedidos_view

def main(page: ft.Page):
    page.title = "Modelorama"
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.window_width = 1000
    page.window_height = 700

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        expand=True,
        tabs=[
            ft.Tab(text="Proveedores", content=proveedores_view(page)),
            ft.Tab(text="Categorías", content=categorias_view(page)),
            ft.Tab(text="Clientes", content=clientes_view(page)),
            ft.Tab(text="Empleados", content=empleados_view(page)),
            ft.Tab(text="Realizar Venta", content=venta_view(page)),
            ft.Tab(text="Lista de ventas", content=listaventas_view(page)),
            ft.Tab(text="Pedidos", content=pedido_view(page)),
            ft.Tab(text="Lista de Pedidos", content=listapedidos_view(page)),
            ft.Tab(text="Producto", content=producto_view(page)),
            ft.Tab(text="Unidades", content=unidad_view(page))
        ]
    )

    page.add(tabs)
    
ft.app(target=main)