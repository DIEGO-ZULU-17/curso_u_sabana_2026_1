# main.py

# ==============================================================================
# ARCHIVO ORQUESTADOR: INICIALIZACIÓN Y SIMULACIÓN PARA POWER BI
# ==============================================================================

import sqlite3
import pandas as pd
import io # Para convertir strings CSV a DataFrames

# Importamos las variables de datos y las clases Manager
from Backend.datos import csv_clientes, csv_productos, csv_proveedores, csv_ventas
from Backend.clientes import ClienteManager, ClienteDataCleaner, ClienteInteractivo
from Backend.productos import ProductoManager, ProductoDataCleaner, ProductoInteractivo
from Backend.proveedores import ProveedorManager, ProveedorDataCleaner, ProveedorInteractivo
from Backend.ventas import VentasManager, VentasInteractivo

# Se debe ubicar en la terminar en esta carpeta y ejecutar: python main.py.
# Así la ubicación relativa de la base de datos funcionará correctamente 
# sin importar el computador o usuario que lo ejecute, siempre y cuando 
# mantengan la misma estructura de carpetas del proyecto.
DB_NAME = "cafeteria_unisabana.db"

"""

# Para garantiza que cafeteria_unisabana.db siempre se cree y se lea dentro de Cafeteria_Unisabana_Clase_10.
# Se ejecuta el siguiente código para obtener la ruta absoluta del archivo main.py, 
# luego se extrae la carpeta y se une con el nombre del archivo .db.
  
import os # <-- NUEVA IMPORTACIÓN: Para manejar rutas del sistema operativo
# ==============================================================================
# CONFIGURACIÓN DINÁMICA DE LA RUTA DE LA BASE DE DATOS
# ==============================================================================
# 1. os.path.abspath(__file__) obtiene la ruta completa de este script (main.py)
# 2. os.path.dirname() extrae solo la carpeta donde está este script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 3. os.path.join() une la ruta de la carpeta con el nombre del archivo .db
DB_NAME = os.path.join(BASE_DIR, "cafeteria_unisabana.db")

print(f"📂 Ruta configurada de la BD: {DB_NAME}\n")
# ==============================================================================
"""


def Cargar_DB():
    """
    1. Se conecta al archivo .db (o lo crea si no existe).
    2. Crea las estructuras de las tablas SOLO si no existen (IF NOT EXISTS).
    3. Verifica si las tablas están vacías. Si lo están, carga los datos del 
       archivo datos.py. Si ya tienen datos (ej. un cliente nuevo que ingresaste 
       ayer), NO los sobrescribe y respeta la persistencia.
    """

    print("⚙️ Verificando y cargando la base de datos...")
    
    # Abrimos conexión a SQLite
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        
        # Activamos obligatoriamente el soporte para Llaves Foráneas (FK)
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        # ----------------------------------------------------------------------
        # CREACIÓN SEGURA DE TABLAS (Sin usar DROP TABLE)
        # ----------------------------------------------------------------------
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id_cliente INTEGER PRIMARY KEY,
                email TEXT, 
                telefono TEXT, 
                fecha_nacimiento TEXT, 
                Nombre_Cliente TEXT, 
                Tipo_Cliente TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id_producto INTEGER PRIMARY KEY,
                precio REAL, 
                stock INTEGER, 
                fecha_vencimiento TEXT, 
                Nombre_Producto TEXT, 
                Categoria TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS proveedores (
                nit_proveedor INTEGER PRIMARY KEY,
                contacto TEXT, 
                telefono TEXT, 
                email TEXT, 
                Nombre_Empresa TEXT, 
                Ciudad TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ventas (
                id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
                id_cliente INTEGER,
                id_producto INTEGER,
                nit_proveedor INTEGER,
                cantidad INTEGER,
                total_venta REAL,
                fecha_venta TEXT,
                FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
                FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
                FOREIGN KEY (nit_proveedor) REFERENCES proveedores(nit_proveedor)
            )
        ''')

        # ----------------------------------------------------------------------
        # CARGA DE DATOS SEMILLA (Solo si la base de datos está vacía)
        # ----------------------------------------------------------------------
        
        # CLIENTES
        cursor.execute("SELECT COUNT(*) FROM clientes")
        # fetchone()[0] extrae el número de registros. Si es 0, la tabla está vacía.
        if cursor.fetchone()[0] == 0:
            print("📊 Insertando datos iniciales en 'clientes'...")
            df_c = pd.read_csv(io.StringIO(csv_clientes))
            df_c.to_sql('clientes', conn, if_exists='append', index=False)

        # PRODUCTOS
        cursor.execute("SELECT COUNT(*) FROM productos")
        if cursor.fetchone()[0] == 0:
            print("📊 Insertando datos iniciales en 'productos'...")
            df_p = pd.read_csv(io.StringIO(csv_productos))
            df_p.to_sql('productos', conn, if_exists='append', index=False)

        # PROVEEDORES
        cursor.execute("SELECT COUNT(*) FROM proveedores")
        if cursor.fetchone()[0] == 0:
            print("📊 Insertando datos iniciales en 'proveedores'...")
            df_pr = pd.read_csv(io.StringIO(csv_proveedores))
            df_pr.to_sql('proveedores', conn, if_exists='append', index=False)

        # VENTAS
        cursor.execute("SELECT COUNT(*) FROM ventas")
        if cursor.fetchone()[0] == 0:
            print("📊 Insertando datos iniciales en 'ventas'...")
            df_v = pd.read_csv(io.StringIO(csv_ventas))
            df_v.to_sql('ventas', conn, if_exists='append', index=False)
            
    print("✅ Base de datos lista. Los datos ingresados manualmente se han preservado exitosamente.\n")


def simulacion_power_bi():
    """
    Simula la inserción de nuevos datos en todas las tablas mediante POO. 
    Una vez ejecutada esta función, si vas a Power BI y presionas 'Actualizar', 
    las gráficas cambiarán reflejando estos nuevos registros en tiempo real.
    """
    print("🚀 SIMULACIÓN DE NUEVOS DATOS (Para actualizar en Power BI)\n")
    
    # Instanciamos los gestores (Managers) que contienen la lógica CRUD
    mgr_clientes = ClienteManager(DB_NAME)
    mgr_productos = ProductoManager(DB_NAME)
    mgr_proveedores = ProveedorManager(DB_NAME)
    mgr_ventas = VentasManager(DB_NAME)
    
    # 1. Agregamos un NUEVO PROVEEDOR
    mgr_proveedores.create(
        nit_proveedor=888000, 
        contacto="",                               # Error: Vacío
        telefono="3009998877.0",                   # Error: Formato float
        email=" VENTAS@NuevoProveedor.com   ",     # Error: Mayúsculas y espacios
        nombre_empresa="suministros power bi",     # Error: Todo en minúsculas
        ciudad="bogota"                            # Error: Todo en minúsculas
    )

    # 2. Agregamos un NUEVO CLIENTE
    mgr_clientes.create(
        id_cliente=999, 
        email=" NUEVO_Estudiante@Sabana.edu.co  ",  # Error: Espacios y mayúsculas
        telefono="3000000000.0",                   # Error: Formato float con .0
        fecha_nacimiento="01/01/2005",             # Error: Formato de fecha incorrecto
        nombre="nuevo estudiante prueba",          # Error: Todo en minúsculas
        tipo=" ESTUDIANTE "                        # Error: Espacios y todo mayúsculas
    )
    
    # 3. Agregamos un NUEVO PRODUCTO
    mgr_productos.create(
        id_producto=99, 
        precio="8000",                             # Error: Enviado como string
        stock=None,                                # Error: Nulo/Vacío
        fecha_vencimiento="31-12-2026",            # Error: Formato de fecha invertido
        nombre=" combo especial bi ",              # Error: Minúsculas y espacios extra
        categoria=" ALMUERZO "                     # Error: Mayúsculas y espacios extra
    )
    
    # 4. Registramos NUEVAS VENTAS conectando los datos recién creados

    # Consultamos el precio del producto directamente desde la base de datos
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT precio FROM productos WHERE id_producto = ?", (99,))
        precio_producto = cursor.fetchone()[0]

    # Venta 1: El cliente nuevo compra el producto nuevo suministrado por el proveedor nuevo
    cantidad_venta_1 = 2  # Definimos la cantidad antes de usarla
    mgr_ventas.create(
        id_cliente=999, 
        id_producto=99, 
        nit_proveedor=888000, 
        cantidad=cantidad_venta_1, 
        total_venta=(cantidad_venta_1 * precio_producto)
    )
    
    # Venta 2: Un cliente antiguo (101 - Diego) también compra el producto nuevo del proveedor nuevo
    cantidad_venta_2 = 3  # Definimos una cantidad diferente para la segunda venta
    mgr_ventas.create(
        id_cliente=101, 
        id_producto=99, 
        nit_proveedor=888000, 
        cantidad=cantidad_venta_2, 
        total_venta=(cantidad_venta_2 * precio_producto)
    )

    # Venta 2: Un cliente antiguo (101 - Diego) también compra el producto nuevo del proveedor nuevo
    cantidad_venta_2 = 3  # Definimos una cantidad diferente para la segunda venta
    mgr_ventas.create(
        id_cliente=101, 
        id_producto=99, 
        nit_proveedor=888000, 
        cantidad=cantidad_venta_2, 
        total_venta=(cantidad_venta_2 * precio_producto)
    )

    # Venta 2: Un cliente antiguo (108 - Andrés Felipe) también compra el producto nuevo del proveedor nuevo
    cantidad_venta_2 = 5  # Definimos una cantidad diferente para la segunda venta
    mgr_ventas.create(
        id_cliente=108, 
        id_producto=99, 
        nit_proveedor=888000, 
        cantidad=cantidad_venta_2, 
        total_venta=(cantidad_venta_2 * precio_producto)
    )    

    print("\n🎉 ¡Nuevos registros insertados!")
    print("👉 Ve a Power BI y haz clic en 'Actualizar' para ver cómo aparecen:")
    print("   - El nuevo proveedor 'Suministros Power BI'")
    print("   - El nuevo producto 'Combo Especial BI'")
    print("   - Y el incremento en los ingresos por las nuevas ventas.")


    # 5. EJECUTAMOS LA LIMPIEZA CON PANDAS INMEDIATAMENTE DESPUÉS DE INSERTAR
    limpiador_proveedores = ProveedorDataCleaner(DB_NAME)
    limpiador_proveedores.limpiar_datos()

    limpiador_clientes = ClienteDataCleaner(DB_NAME)
    limpiador_clientes.limpiar_datos()

    limpiador_productos = ProductoDataCleaner(DB_NAME)
    limpiador_productos.limpiar_datos()


# FUNCIONES INTERACTIVAS PARA REGISTRO MANUAL POR CONSOLA

def Cliente_Interactivo():

    # ==========================================================================
    # PRUEBA DE INGRESO INTERACTIVO (CONSOLA)
    # ==========================================================================
    # Instanciamos la nueva clase interactiva

    registro_interactivo = ClienteInteractivo(DB_NAME)
    
    # Ejecutamos el método que pide los inputs y guarda la información
    registro_interactivo.registrar_cliente_consola()
    
    print("\n🎉 Proceso de registro manual finalizado. Si vas a Power BI y presionas 'Actualizar', verás a este nuevo cliente reflejado en tu dashboard.")    


def Producto_Interactivo():
    """
    Función orquestadora para lanzar el registro interactivo de un producto.
    """
    # Instanciamos la clase interactiva pasándole la constante global de la base de datos
    registro_producto = ProductoInteractivo(DB_NAME)
    
    # Ejecutamos el método que pide los inputs, valida y guarda la información
    registro_producto.registrar_producto_consola()
    
    print("\n🎉 Proceso interactivo de producto finalizado. Actualiza Power BI para ver el nuevo ítem en tu inventario.")


def Proveedor_Interactivo():
    """
    Función orquestadora para lanzar el registro interactivo de un proveedor.
    """
    # Instanciamos la clase interactiva pasándole la constante global de la base de datos
    registro_proveedor = ProveedorInteractivo(DB_NAME)
    
    # Ejecutamos el método que pide los inputs, valida y guarda la información
    registro_proveedor.registrar_proveedor_consola()
    
    print("\n🎉 Proceso interactivo de proveedor finalizado. Actualiza Power BI para ver el nuevo registro en tu modelo de datos.")


def Ventas_Interactivo():
    """
    Función orquestadora para lanzar el registro interactivo de una venta.
    """
    # Instanciamos la clase interactiva pasándole la constante global de la base de datos
    registro_venta = VentasInteractivo(DB_NAME)
    
    # Ejecutamos el método que pide los inputs, valida y guarda la información
    registro_venta.registrar_venta_consola()
    
    print("\n🎉 Proceso interactivo de ventas finalizado. Actualiza Power BI para ver la nueva venta y la reducción del stock en tu modelo de datos.")



# FUNCIONES INTERACTIVAS PARA ACTUALIZAR REGISTROS EXISTENTES POR CONSOLA 
# (NO SE CREAN NUEVOS REGISTROS, SOLO SE ACTUALIZAN LOS CAMPOS DE LOS REGISTROS YA EXISTENTES)

def Actualizar_Cliente_Interactivo():
    """Permite al usuario elegir qué campo del cliente desea actualizar."""
    print("\n" + "="*50)
    print("🔄 ACTUALIZACIÓN INTERACTIVA DE CLIENTE")
    print("="*50)
    try:
        id_cliente = int(input("Ingrese el ID del cliente a actualizar: ").strip())
        print("\n¿Qué dato desea actualizar?")
        print("1. Email")
        print("2. Teléfono")
        print("3. Fecha de Nacimiento")
        print("4. Nombre del Cliente")
        print("5. Tipo de Cliente")
        opcion = input("Seleccione una opción (1-5): ").strip()

        manager = ClienteManager(DB_NAME)
        cleaner = ClienteDataCleaner(DB_NAME)
        nuevo_dato = input("Ingrese el nuevo valor: ").strip()

        if opcion == "1":
            manager.update_email(id_cliente, nuevo_dato)
        elif opcion == "2":
            manager.update_telefono(id_cliente, nuevo_dato)
        elif opcion == "3":
            manager.update_fecha_nacimiento(id_cliente, nuevo_dato)
        elif opcion == "4":
            manager.update_nombre(id_cliente, nuevo_dato)
        elif opcion == "5":
            manager.update_tipo(id_cliente, nuevo_dato)
        else:
            print("❌ Opción inválida.")
            return

        # Limpiamos y normalizamos los datos automáticamente
        cleaner.limpiar_datos()
        print("✅ Cliente actualizado y normalizado correctamente.")

    except ValueError:
        print("❌ Error: El ID debe ser un número entero.")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")


def Actualizar_Producto_Interactivo():
    """Permite al usuario elegir qué campo del producto desea actualizar."""
    print("\n" + "="*50)
    print("🔄 ACTUALIZACIÓN INTERACTIVA DE PRODUCTO")
    print("="*50)
    try:
        id_producto = int(input("Ingrese el ID del producto a actualizar: ").strip())
        print("\n¿Qué dato desea actualizar?")
        print("1. Precio")
        print("2. Stock")
        print("3. Fecha de Vencimiento")
        print("4. Nombre del Producto")
        print("5. Categoría")
        opcion = input("Seleccione una opción (1-5): ").strip()

        manager = ProductoManager(DB_NAME)
        cleaner = ProductoDataCleaner(DB_NAME)
        nuevo_dato = input("Ingrese el nuevo valor: ").strip()

        if opcion == "1":
            manager.update_precio(id_producto, float(nuevo_dato))
        elif opcion == "2":
            manager.update_stock(id_producto, int(nuevo_dato))
        elif opcion == "3":
            manager.update_fecha_vencimiento(id_producto, nuevo_dato)
        elif opcion == "4":
            manager.update_nombre(id_producto, nuevo_dato)
        elif opcion == "5":
            manager.update_categoria(id_producto, nuevo_dato)
        else:
            print("❌ Opción inválida.")
            return

        cleaner.limpiar_datos()
        print("✅ Producto actualizado y normalizado correctamente.")

    except ValueError:
        print("❌ Error: Validar que el ID o los campos numéricos (precio, stock) sean números válidos.")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")


def Actualizar_Proveedor_Interactivo():
    """Permite al usuario elegir qué campo del proveedor desea actualizar."""
    print("\n" + "="*50)
    print("🔄 ACTUALIZACIÓN INTERACTIVA DE PROVEEDOR")
    print("="*50)
    try:
        nit_proveedor = int(input("Ingrese el NIT del proveedor a actualizar: ").strip())
        print("\n¿Qué dato desea actualizar?")
        print("1. Contacto")
        print("2. Teléfono")
        print("3. Email")
        print("4. Nombre de la Empresa")
        print("5. Ciudad")
        opcion = input("Seleccione una opción (1-5): ").strip()

        manager = ProveedorManager(DB_NAME)
        cleaner = ProveedorDataCleaner(DB_NAME)
        nuevo_dato = input("Ingrese el nuevo valor: ").strip()

        if opcion == "1":
            manager.update_contacto(nit_proveedor, nuevo_dato)
        elif opcion == "2":
            manager.update_telefono(nit_proveedor, nuevo_dato)
        elif opcion == "3":
            manager.update_email(nit_proveedor, nuevo_dato)
        elif opcion == "4":
            manager.update_nombre_empresa(nit_proveedor, nuevo_dato)
        elif opcion == "5":
            manager.update_ciudad(nit_proveedor, nuevo_dato)
        else:
            print("❌ Opción inválida.")
            return

        cleaner.limpiar_datos()
        print("✅ Proveedor actualizado y normalizado correctamente.")

    except ValueError:
        print("❌ Error: El NIT debe ser un número entero.")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")


# FUNCIONES INTERACTIVAS PARA ELIMINAR REGISTROS EXISTENTES POR CONSOLA (BORRAR REGISTROS COMPLETAMENTE DE LA BASE DE DATOS)

def Eliminar_Cliente_Interactivo():
    """Permite al usuario eliminar un cliente ingresando su ID."""
    print("\n" + "="*50)
    print("🗑️ ELIMINACIÓN INTERACTIVA DE CLIENTE")
    print("="*50)
    try:
        id_cliente = int(input("Ingrese el ID del cliente a eliminar: ").strip())
        
        manager = ClienteManager(DB_NAME)
        manager.delete(id_cliente)
        
        print("\n🎉 Proceso finalizado. Si vas a Power BI y presionas 'Actualizar', el cliente desaparecerá de tu reporte.")

    except ValueError:
        print("❌ Error: El ID debe ser un número entero.")
    except sqlite3.IntegrityError:
        # Esto ocurre si las Llaves Foráneas (FK) están activas y el cliente tiene ventas registradas
        print("⚠️ Error de Integridad: No puedes eliminar este cliente porque tiene compras asociadas en la tabla de Ventas.")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")


def Eliminar_Producto_Interactivo():
    """Permite al usuario eliminar un producto ingresando su ID."""
    print("\n" + "="*50)
    print("🗑️ ELIMINACIÓN INTERACTIVA DE PRODUCTO")
    print("="*50)
    try:
        id_producto = int(input("Ingrese el ID del producto a eliminar: ").strip())
        
        manager = ProductoManager(DB_NAME)
        manager.delete(id_producto)
        
        print("\n🎉 Proceso finalizado. Actualiza Power BI para ver los cambios en el inventario.")

    except ValueError:
        print("❌ Error: El ID debe ser un número entero.")
    except sqlite3.IntegrityError:
        print("⚠️ Error de Integridad: No puedes eliminar este producto porque ya tiene transacciones en la tabla de Ventas.")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")


def Eliminar_Proveedor_Interactivo():
    """Permite al usuario eliminar un proveedor ingresando su NIT."""
    print("\n" + "="*50)
    print("🗑️ ELIMINACIÓN INTERACTIVA DE PROVEEDOR")
    print("="*50)
    try:
        nit_proveedor = int(input("Ingrese el NIT del proveedor a eliminar: ").strip())
        
        manager = ProveedorManager(DB_NAME)
        manager.delete(nit_proveedor)
        
        print("\n🎉 Proceso finalizado. Actualiza Power BI para ver los cambios en tus proveedores.")

    except ValueError:
        print("❌ Error: El NIT debe ser un número entero.")
    except sqlite3.IntegrityError:
        print("⚠️ Error de Integridad: No puedes eliminar este proveedor porque está vinculado a ventas o productos activos.")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")


def Eliminar_Venta_Interactivo():
    """Permite al usuario eliminar un registro de venta ingresando su ID."""
    print("\n" + "="*50)
    print("🗑️ ELIMINACIÓN INTERACTIVA DE VENTA")
    print("="*50)
    try:
        id_venta = int(input("Ingrese el ID de la venta a eliminar: ").strip())
        
        manager = VentasManager(DB_NAME)
        manager.delete(id_venta)
        
        print("\n🎉 Proceso finalizado. Actualiza Power BI y verás cómo el ingreso total disminuye al borrar esta transacción.")

    except ValueError:
        print("❌ Error: El ID de la venta debe ser un número entero.")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")





#if __name__ == "__main__":
    # 1. Creamos la base de datos a partir del archivo datos.py
    #Cargar_DB()
    
    # 2. Hacemos operaciones CRUD para simular la inserción de nuevos datos y su limpieza automática,
    # para luego ir a Power BI y actualizar el dashboard viendo cómo se reflejan estos cambios en tiempo real.
    #simulacion_power_bi()

    # 3. Prueba de ingreso interactivo por consola
    #Cliente_Interactivo()
    #Producto_Interactivo()
    #Proveedor_Interactivo()
    #Ventas_Interactivo()

    # 4. Prueba de actualización interactiva por consola
    #Actualizar_Cliente_Interactivo()
    #Actualizar_Producto_Interactivo() 
    #Actualizar_Proveedor_Interactivo()

    # 5. Prueba de eliminación interactiva por consola
    #Eliminar_Cliente_Interactivo()
    #Eliminar_Producto_Interactivo()
    #Eliminar_Proveedor_Interactivo()
    #Eliminar_Venta_Interactivo()



# Importamos tkinter para mostrar mensajes emergentes (pop-ups) en la interfaz gráfica
# Permite mostrar alertas de éxito o error al usuario sin necesidad de imprimir en consola, 
# lo cual es útil especialmente cuando se integre con la interfaz gráfica (Frontend).

# Debería ir al inicio del archivo main.py para que esté disponible en toda la aplicación,
# pero lo dejamos aquí para no interferir con la lógica de la base de datos y las simulaciones, 
# ya que esta importación es principalmente para la parte de la interfaz gráfica (Frontend).
import tkinter as tk
import os

# 1. Manejo dinámico de rutas (Asegurando que encuentre la carpeta backend)
# Este código aplica si ubican el archivo .db en la carpeta Backend, pero si lo dejan en la raíz del proyecto, no es necesario.

#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#DB_NAME = os.path.join(BASE_DIR, "backend", "cafeteria_unisabana.db")

# Base de datos global para todo el proyecto
DB_NAME = "cafeteria_unisabana.db"

# 2. Importamos la clase de la Interfaz Gráfica desde la carpeta frontend
from Frontend.app_central import AppCentral

def iniciar_app():
    """
    Punto de arranque de la aplicación.
    Inicializa Tkinter, carga la clase principal y ejecuta el loop de eventos.
    """
    print("🚀 Iniciando Sistema Central ERP (GUI)...")
    print(f"📂 Base de datos configurada: {DB_NAME}")
    
    # 1. Instanciamos el "lienzo" base de Tkinter
    root = tk.Tk()
    
    # 2. Le pasamos el lienzo y la constante de la BD a nuestra clase orquestadora visual
    app = AppCentral(root, DB_NAME)
    
    # 3. Iniciamos el "Loop" Principal de eventos. 
    # El programa se queda "escuchando" interacciones del usuario.
    root.mainloop()

# Ejecución estándar en Python
if __name__ == "__main__":
    iniciar_app()


