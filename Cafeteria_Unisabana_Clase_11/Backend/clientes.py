# clientes.py

import sqlite3
import pandas as pd

class ClienteManager:
    def __init__(self, db_name):
        self.db_name = db_name

    def create(self, id_cliente, email, telefono, fecha_nacimiento, nombre, tipo):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO clientes (id_cliente, email, telefono, fecha_nacimiento, Nombre_Cliente, Tipo_Cliente)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (id_cliente, email, telefono, fecha_nacimiento, nombre, tipo))
            conn.commit()
            print(f"✅ Cliente '{nombre}' creado.")

    def read(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes")
            return cursor.fetchall()


    # Actualizaciones individuales para cada campo (para evitar romper las llaves foráneas en otras tablas)
    def update_telefono(self, id_cliente, nuevo_telefono):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE clientes SET telefono = ? WHERE id_cliente = ?", (nuevo_telefono, id_cliente))
            conn.commit()
            print(f"🔄 Teléfono del cliente {id_cliente} actualizado.")
    
    def update_email(self, id_cliente, nuevo_email):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE clientes SET email = ? WHERE id_cliente = ?", (nuevo_email, id_cliente))
            conn.commit()
            print(f"🔄 Email del cliente {id_cliente} actualizado.")

    def update_fecha_nacimiento(self, id_cliente, nueva_fecha):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE clientes SET fecha_nacimiento = ? WHERE id_cliente = ?", (nueva_fecha, id_cliente))
            conn.commit()
            print(f"🔄 Fecha de nacimiento del cliente {id_cliente} actualizada.")

    def update_nombre(self, id_cliente, nuevo_nombre):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE clientes SET Nombre_Cliente = ? WHERE id_cliente = ?", (nuevo_nombre, id_cliente))
            conn.commit()
            print(f"🔄 Nombre del cliente {id_cliente} actualizado.")

    def update_tipo(self, id_cliente, nuevo_tipo):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE clientes SET Tipo_Cliente = ? WHERE id_cliente = ?", (nuevo_tipo, id_cliente))
            conn.commit()
            print(f"🔄 Tipo del cliente {id_cliente} actualizado.")



    def delete(self, id_cliente):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clientes WHERE id_cliente = ?", (id_cliente,))
            conn.commit()
            print(f"❌ Cliente {id_cliente} eliminado.")

class ClienteDataCleaner:
    """
    Clase encargada de extraer los datos de SQLite a Pandas, limpiar y normalizar 
    posibles errores de digitación (nulos, formatos, mayúsculas) y actualizar 
    la base de datos de forma segura sin romper las llaves foráneas.
    """
    def __init__(self, db_name):
        self.db_name = db_name

    def limpiar_datos(self):
        with sqlite3.connect(self.db_name) as conn:
            # 1. Leer los datos crudos desde la Base de Datos a un DataFrame
            df = pd.read_sql_query("SELECT * FROM clientes", conn)

            # 2. LIMPIEZA DE NOMBRES Y TIPOS (Formato Título y eliminar espacios extras)
            df['Nombre_Cliente'] = df['Nombre_Cliente'].astype(str).str.strip().str.title()
            df['Tipo_Cliente'] = df['Tipo_Cliente'].astype(str).str.strip().str.title()

            # 3. LIMPIEZA DE EMAIL (Minúsculas, eliminar espacios y relleno de nulos)
            df['email'] = df['email'].astype(str).str.strip().str.lower()
            df.loc[df['email'].isin(['nan', 'none', '', 'null']), 'email'] = 'sin_correo@cafeteria.com'
            df['email'] = df['email'].fillna('sin_correo@cafeteria.com')

            # 4. LIMPIEZA DE TELÉFONO (Eliminar '.0' de los flotantes y rellenar vacíos)
            df['telefono'] = df['telefono'].astype(str).str.replace('.0', '', regex=False).str.strip()
            df.loc[df['telefono'].isin(['nan', 'none', '', 'null']), 'telefono'] = 'No Registra'
            df['telefono'] = df['telefono'].fillna('No Registra')

            # 5. LIMPIEZA DE FECHAS (Estandarización estricta a formato YYYY-MM-DD)
            df['fecha_nacimiento'] = pd.to_datetime(df['fecha_nacimiento'], errors='coerce').dt.strftime('%Y-%m-%d')
            df['fecha_nacimiento'] = df['fecha_nacimiento'].fillna('1999-01-01')  # Relleno de nulos con una fecha por defecto  

            # 6. ACTUALIZACIÓN EN BASE DE DATOS (Usamos UPDATE para proteger las Llaves Foráneas)
            cursor = conn.cursor()
            for index, row in df.iterrows():
                cursor.execute('''
                    UPDATE clientes 
                    SET email = ?, telefono = ?, fecha_nacimiento = ?, Nombre_Cliente = ?, Tipo_Cliente = ?
                    WHERE id_cliente = ?
                ''', (
                    row['email'], 
                    row['telefono'], 
                    row['fecha_nacimiento'], 
                    row['Nombre_Cliente'], 
                    row['Tipo_Cliente'], 
                    row['id_cliente']
                ))
            
            conn.commit()
            print("✨ Pandas: Tabla 'clientes' auditada, limpiada y normalizada exitosamente.")


class ClienteInteractivo:
    """
    Clase encargada de interactuar con el usuario mediante la consola (inputs),
    capturar los datos del nuevo cliente, insertarlos en la base de datos y 
    limpiarlos automáticamente usando Pandas.
    """
    def __init__(self, db_name):
        self.db_name = db_name
        self.manager = ClienteManager(db_name)
        self.cleaner = ClienteDataCleaner(db_name)

    def registrar_cliente_consola(self):
        
        print("\n" + "="*50)
        print("📝 REGISTRO INTERACTIVO DE NUEVO CLIENTE")
        print("="*50)
        
        try:
            # Capturamos los datos como texto (.strip() quita espacios vacíos al inicio y final)
            id_input = input("Ingrese el ID del cliente (numérico): ").strip()
            nombre = input("Ingrese el nombre completo: ").strip()
            email = input("Ingrese el correo electrónico: ").strip()
            telefono = input("Ingrese el teléfono: ").strip()
            fecha_nacimiento = input("Ingrese la fecha de nacimiento (YYYY-MM-DD): ").strip()
            tipo = input("Ingrese el tipo de cliente (Estudiante/Profesor/Externo): ").strip()

            # ------------------------------------------------------------------
            # VALIDACIONES LEVANTANDO ERRORES (RAISE VALUEERROR)
            # ------------------------------------------------------------------
            
            # 1. Validación de campos vacíos
            if not all([id_input, nombre, email, telefono, fecha_nacimiento, tipo]):
                raise ValueError("Ningún dato puede quedar vacío. Debe completar todos los campos.")

            # 2. Validación de formato de ID
            if not id_input.isdigit():
                raise ValueError("El ID del cliente debe contener únicamente números.")
            id_cliente = int(id_input)

            # 3. Validaciones directamente contra la Base de Datos
            import sqlite3
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                
                # Validación: ¿El ID ya existe?
                cursor.execute("SELECT 1 FROM clientes WHERE id_cliente = ?", (id_cliente,))
                if cursor.fetchone():
                    raise ValueError(f"El ID '{id_cliente}' ya se encuentra registrado.")
                
                # Validación: ¿El Email ya existe? (COLLATE NOCASE ignora mayúsculas/minúsculas)
                cursor.execute("SELECT 1 FROM clientes WHERE email = ? COLLATE NOCASE", (email,))
                if cursor.fetchone():
                    raise ValueError(f"El correo electrónico '{email}' ya se encuentra registrado por otro usuario.")
                
                # Validación: ¿El Nombre ya existe?
                cursor.execute("SELECT 1 FROM clientes WHERE Nombre_Cliente = ? COLLATE NOCASE", (nombre,))
                if cursor.fetchone():
                    raise ValueError(f"El cliente con el nombre '{nombre}' ya existe en el sistema.")

            # ------------------------------------------------------------------
            # EJECUCIÓN SI PASA TODAS LAS VALIDACIONES
            # ------------------------------------------------------------------
            self.manager.create(
                id_cliente=id_cliente, 
                email=email, 
                telefono=telefono, 
                fecha_nacimiento=fecha_nacimiento, 
                nombre=nombre, 
                tipo=tipo
            )
            
            self.cleaner.limpiar_datos()
            print("✅ Cliente registrado y datos normalizados correctamente desde consola.")

        # ------------------------------------------------------------------
        # CAPTURA DE ERRORES (EXCEPTIONS)
        # ------------------------------------------------------------------
        except ValueError as ve:
            # Atrapa todos los 'raise ValueError' que definimos arriba
            print(f"❌ Error de Validación: {ve}")
            
        except sqlite3.IntegrityError as ie:
            # Atrapa errores nativos de SQLite (Ej: Otra restricción UNIQUE violada)
            print(f"❌ Error de Integridad en la BD: {ie}")
            
        except Exception as e:
            # Atrapa cualquier otro error inesperado para que el programa no colapse
            print(f"❌ Error inesperado durante el registro: {e}")
