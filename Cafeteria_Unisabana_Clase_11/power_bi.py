import sqlite3
import pandas as pd

# 1. Definir la ruta EXACTA donde está el archivo .db en su computador.
# OJO: Usar doble barra invertida (\\) o barra normal (/) para evitar errores en Windows.
ruta_bd = r"C:\Users\diego\OneDrive\Documentos\Clase_Python_U_Sabana\2026-1\Cafeteria_Unisabana_Clase_10\cafeteria_unisabana.db"

# 2. Crear la conexión
conexion = sqlite3.connect(ruta_bd)

# 3. Usar Pandas para leer las tablas y convertirlas en DataFrames.
# (Deben hacer esto por cada tabla que quieran importar)
df_clientes = pd.read_sql_query("SELECT * FROM clientes", conexion)
df_productos = pd.read_sql_query("SELECT * FROM productos", conexion)
df_proveedor = pd.read_sql_query("SELECT * FROM proveedores", conexion)
df_ventas = pd.read_sql_query("SELECT * FROM ventas", conexion)

# 4. Cerrar la conexión
conexion.close()

# Power BI detectará automáticamente todas las variables que empiecen con 'df_' y las mostrará como tablas.