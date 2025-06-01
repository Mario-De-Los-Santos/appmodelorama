1. El primer paso sería crear la base de datos con el archivo .sql incluído de nombre; 'db23270621.sql'
    dentro del cliente de mysql, indicar el comando 'source' seguido de la dirección del archivo .sql incluído

2. Generar el entorno virtual (si ya existe, saltar)
    python -m venv "nombre del entorno"

3. Activar el entorno virtual
    "nombre del entorno"\Scripts\activate
    usar el la versión recomendada del interprete

4. Crear el archivo .gitignore
    dentro del archivo incluir el nombre del entorno virtual para que no se suba al repositorio

5. Instalar los requerimientos con utilizando el archivo incluído llamado requirements.txt con el siguiente comando:
    pip install -r requirements.txt

6. Después de eso se puede ejecutar el archivo 'menubase.py'

    Recomendaciones
        - Para visualizar los detalles de las ventas y pedidos en la pestaña 'lista ventas/pedidos' solo hace falta darle clic a la
          venta/pedido para poder visualizarlas
        
        - Si un detalle de venta o pedido no aparece en las ventanas anteriormente mencionadas, solo hace falta presionar
          el botón 'limpiar' y la página se actualizará
