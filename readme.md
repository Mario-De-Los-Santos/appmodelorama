1. El primer paso sería crear la base de datos con el archivo .sql incluído de nombre; 'db23270621.sql'
    dentro del cliente de mysql, indicar el comando 'source' seguido de la dirección del archivo .sql incluído

2. Generar el entorno virtual (si ya existe, saltar)
    python -m venv "nombre del entorno"

3. Activar el entorno virtual
    "nombre del entorno"\Scripts\activate
    usar el la versión recomendada del interprete

4. Crear el archivo .gitignore
    dentro del archivo incluir el nombre del entorno virtual para que no se suba al repositorio

5. Instalar la biblioteca flet con el comando:
    pip install flet

6. Después de eso se puede ejecutar el archivo menubase.py