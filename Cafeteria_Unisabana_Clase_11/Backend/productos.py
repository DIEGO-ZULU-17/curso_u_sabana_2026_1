# productos.py

import sqlite3
import pandas as pd

class ProductoManager:
    def __init__(self, db_name):
        self.db_name = db_name

    def create(self, id_producto, precio, stock, fecha_vencimiento, nombre, categoria):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO productos (id_producto, precio, stock, fecha_vencimiento, Nombre_Producto, Categoria)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (id_producto, precio, stock, fecha_vencimiento, nombre, categoria))
            conn.commit()
            print(f"✅ Producto '{nombre}' creado.")

    def read(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos")
            return cursor.fetchall()


# Actualizaciones individuales para cada campo (para evitar romper las llaves foráneas en otras tablas)
    def update_precio(self, id_producto, nuevo_precio):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE productos SET precio = ? WHERE id_producto = ?", (nuevo_precio, id_producto))
            conn.commit()
            print(f"🔄 Precio del producto {id_producto} actualizado.")


    def update_stock(self, id_producto, nuevo_stock):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE productos SET stock = ? WHERE id_producto = ?", (nuevo_stock, id_producto))
            conn.commit()
            print(f"🔄 Stock del producto {id_producto} actualizado.")

    def update_fecha_vencimiento(self, id_producto, nueva_fecha):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE productos SET fecha_vencimiento = ? WHERE id_producto = ?", (nueva_fecha, id_producto))
            conn.commit()
            print(f"🔄 Fecha de vencimiento del producto {id_producto} actualizada.")

    def update_nombre(self, id_producto, nuevo_nombre):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE productos SET Nombre_Producto = ? WHERE id_producto = ?", (nuevo_nombre, id_producto))
            conn.commit()
            print(f"🔄 Nombre del producto {id_producto} actualizado.")

    def update_categoria(self, id_producto, nueva_categoria):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE productos SET Categoria = ? WHERE id_producto = ?", (nueva_categoria, id_producto))
            conn.commit()
            print(f"🔄 Categoría del producto {id_producto} actualizada.")




    def delete(self, id_producto):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM productos WHERE id_producto = ?", (id_producto,))
            conn.commit()
            print(f"❌ Producto {id_producto} eliminado.")


class ProductoDataCleaner:
    """
    Clase encargada de extraer los datos de productos, limpiar nulos, 
    estandarizar textos, castear precios y stocks, y actualizar la BD.
    """
    def __init__(self, db_name):
        self.db_name = db_name

    def limpiar_datos(self):
            with sqlite3.connect(self.db_name) as conn:
                df = pd.read_sql_query("SELECT * FROM productos", conn)

                # 1. LIMPIEZA DE NOMBRES Y CATEGORÍAS (Formato Título y sin espacios)
                df['Nombre_Producto'] = df['Nombre_Producto'].astype(str).str.strip().str.title()
                df['Categoria'] = df['Categoria'].astype(str).str.strip().str.title()

                # 2. LIMPIEZA DE PRECIO Y STOCK (Casting a numérico y relleno de nulos con 0)
                df['precio'] = pd.to_numeric(df['precio'], errors='coerce').fillna(0.0)
                df['stock'] = pd.to_numeric(df['stock'], errors='coerce').fillna(0).astype(int)

                # 3. LIMPIEZA DE FECHAS (Convertir a datetime, rellenar nulos con fecha antigua y luego formatear a texto)
                # Primero: Convertimos a formato datetime (errores pasan a NaT)
                df['fecha_vencimiento'] = pd.to_datetime(df['fecha_vencimiento'], errors='coerce')
                
                # Segundo: Rellenamos los NaT AHORA, mientras son objetos de fecha reales
                df['fecha_vencimiento'] = df['fecha_vencimiento'].fillna(pd.to_datetime('1999-01-01'))
                
                # Tercero: pasamos todo a texto seguro para SQLite (YYYY-MM-DD)
                df['fecha_vencimiento'] = df['fecha_vencimiento'].dt.strftime('%Y-%m-%d')

                # 4. ACTUALIZACIÓN EN BASE DE DATOS
                cursor = conn.cursor()
                for index, row in df.iterrows():
                    cursor.execute('''
                        UPDATE productos 
                        SET precio = ?, stock = ?, fecha_vencimiento = ?, Nombre_Producto = ?, Categoria = ?
                        WHERE id_producto = ?
                    ''', (
                        row['precio'], 
                        row['stock'], 
                        row['fecha_vencimiento'], 
                        row['Nombre_Producto'], 
                        row['Categoria'], 
                        row['id_producto']
                    ))
                
                conn.commit()
                print("✨ Pandas: Tabla 'productos' auditada, limpiada y normalizada exitosamente.")


class ProductoInteractivo:
    """
    Clase encargada de interactuar con el usuario mediante la consola (inputs),
    capturar los datos del nuevo producto, validarlos estrictamente, insertarlos 
    en la base de datos y limpiarlos automáticamente usando Pandas.
    """
    def __init__(self, db_name):
        self.db_name = db_name
        self.manager = ProductoManager(db_name)
        self.cleaner = ProductoDataCleaner(db_name)

    def registrar_producto_consola(self):

        print("\n" + "="*50)
        print("📦 REGISTRO INTERACTIVO DE NUEVO PRODUCTO")
        print("="*50)

        try:
            # Capturamos los datos como texto (.strip() elimina espacios en blanco accidentales)
            id_input = input("Ingrese el ID del producto (numérico): ").strip()
            nombre = input("Ingrese el nombre del producto: ").strip()
            precio_input = input("Ingrese el precio del producto: ").strip()
            stock_input = input("Ingrese el stock inicial (numérico): ").strip()
            fecha_vencimiento = input("Ingrese la fecha de vencimiento (YYYY-MM-DD): ").strip()
            categoria = input("Ingrese la categoría del producto: ").strip()

            # ------------------------------------------------------------------
            # VALIDACIONES LEVANTANDO ERRORES (RAISE VALUEERROR)
            # ------------------------------------------------------------------
            
            # 1. Validación de campos vacíos
            if not all([id_input, nombre, precio_input, stock_input, fecha_vencimiento, categoria]):
                raise ValueError("Ningún dato puede quedar vacío. Debe completar todos los campos.")

            # 2. Validación de formato de ID
            if not id_input.isdigit():
                raise ValueError("El ID del producto debe contener únicamente números.")
            id_producto = int(id_input)

            # 3. Validación de formato de Precio
            try:
                precio = float(precio_input)
                if precio < 0:
                    raise ValueError("El precio no puede ser negativo.")
            except ValueError: # Atrapa el error si float() falla al convertir letras a números
                raise ValueError("El precio debe ser un valor numérico válido.")

            # 4. Validación de formato de Stock
            if not stock_input.isdigit():
                raise ValueError("El stock debe contener únicamente números enteros positivos.")
            stock = int(stock_input)

            # 5. Validaciones directamente contra la Base de Datos
            import sqlite3
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                
                # Validación: ¿El ID de producto ya existe?
                cursor.execute("SELECT 1 FROM productos WHERE id_producto = ?", (id_producto,))
                if cursor.fetchone():
                    raise ValueError(f"El ID '{id_producto}' ya se encuentra registrado para otro producto.")
                
                # Validación: ¿El Nombre del producto ya existe? (COLLATE NOCASE ignora mayúsculas/minúsculas)
                cursor.execute("SELECT 1 FROM productos WHERE Nombre_Producto = ? COLLATE NOCASE", (nombre,))
                if cursor.fetchone():
                    raise ValueError(f"El producto con el nombre '{nombre}' ya existe en el inventario.")

            # ------------------------------------------------------------------
            # EJECUCIÓN SI PASA TODAS LAS VALIDACIONES
            # ------------------------------------------------------------------
            self.manager.create(
                id_producto=id_producto, 
                precio=precio, 
                stock=stock, 
                fecha_vencimiento=fecha_vencimiento, 
                nombre=nombre, 
                categoria=categoria
            )
            
            # Llamamos al limpiador de Pandas para normalizar el texto inmediatamente
            self.cleaner.limpiar_datos()
            print("✅ Producto registrado y datos normalizados correctamente desde consola.")

            with sqlite3.connect(self.db_name) as conn:
                df_verif = pd.read_sql_query("SELECT * FROM productos", conn)
                print(f"Total de productos: {len(df_verif)}")

        # ------------------------------------------------------------------
        # CAPTURA DE ERRORES (EXCEPTIONS)
        # ------------------------------------------------------------------
        except ValueError as ve: # ve es el alias que le damos al error capturado, para luego imprimir su mensaje
            # Atrapa de forma controlada todos los 'raise ValueError' de la sección superior
            print(f"❌ Error de Validación: {ve}")
            
        except sqlite3.IntegrityError as ie:
            # Atrapa errores de violaciones de integridad a nivel de SQL
            print(f"❌ Error de Integridad en la BD: {ie}")
            
        except Exception as e:
            # Captura general (Fallback) para evitar que el programa colapse ante un error no mapeado
            print(f"❌ Error inesperado durante el registro del producto: {e}")