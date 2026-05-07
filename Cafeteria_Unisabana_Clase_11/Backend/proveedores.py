# proveedores.py

import sqlite3
import pandas as pd

class ProveedorManager:
    def __init__(self, db_name):
        self.db_name = db_name

    def create(self, nit_proveedor, contacto, telefono, email, nombre_empresa, ciudad):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO proveedores (nit_proveedor, contacto, telefono, email, Nombre_Empresa, Ciudad)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nit_proveedor, contacto, telefono, email, nombre_empresa, ciudad))
            conn.commit()
            print(f"✅ Proveedor '{nombre_empresa}' creado.")

    def read(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM proveedores")
            return cursor.fetchall()


# Actualizaciones individuales para cada campo (para evitar romper las llaves foráneas en otras tablas)
    def update_ciudad(self, nit_proveedor, nueva_ciudad):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE proveedores SET Ciudad = ? WHERE nit_proveedor = ?", (nueva_ciudad, nit_proveedor))
            conn.commit()
            print(f"🔄 Ciudad del proveedor {nit_proveedor} actualizada.")

    def update_contacto(self, nit_proveedor, nuevo_contacto):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE proveedores SET contacto = ? WHERE nit_proveedor = ?", (nuevo_contacto, nit_proveedor))
            conn.commit()
            print(f"🔄 Contacto del proveedor {nit_proveedor} actualizado.")

    def update_telefono(self, nit_proveedor, nuevo_telefono):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE proveedores SET telefono = ? WHERE nit_proveedor = ?", (nuevo_telefono, nit_proveedor))
            conn.commit()
            print(f"🔄 Teléfono del proveedor {nit_proveedor} actualizado.")

    def update_email(self, nit_proveedor, nuevo_email):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE proveedores SET email = ? WHERE nit_proveedor = ?", (nuevo_email, nit_proveedor))
            conn.commit()
            print(f"🔄 Email del proveedor {nit_proveedor} actualizado.")

    def update_nombre_empresa(self, nit_proveedor, nuevo_nombre):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE proveedores SET Nombre_Empresa = ? WHERE nit_proveedor = ?", (nuevo_nombre, nit_proveedor))
            conn.commit()
            print(f"🔄 Nombre de la empresa del proveedor {nit_proveedor} actualizado.")




    def delete(self, nit_proveedor):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM proveedores WHERE nit_proveedor = ?", (nit_proveedor,))
            conn.commit()
            print(f"❌ Proveedor {nit_proveedor} eliminado.")


class ProveedorDataCleaner:
    """
    Clase encargada de extraer datos de proveedores, normalizar nombres,
    limpiar teléfonos/emails y rellenar contactos vacíos en la BD.
    """
    def __init__(self, db_name):
        self.db_name = db_name

    def limpiar_datos(self):
        with sqlite3.connect(self.db_name) as conn:
            df = pd.read_sql_query("SELECT * FROM proveedores", conn)

            # 1. LIMPIEZA DE NOMBRES Y CIUDADES
            df['Nombre_Empresa'] = df['Nombre_Empresa'].astype(str).str.strip().str.title()
            df['Ciudad'] = df['Ciudad'].astype(str).str.strip().str.title()

            # 2. LIMPIEZA DE CONTACTO (Rellenar vacíos con un área por defecto)
            df['contacto'] = df['contacto'].astype(str).str.strip().str.title()
            df.loc[df['contacto'].isin(['Nan', 'None', '', 'Null']), 'contacto'] = 'Departamento De Ventas'

            # 3. LIMPIEZA DE TELÉFONO (Quitar .0 y rellenar nulos)
            df['telefono'] = df['telefono'].astype(str).str.replace('.0', '', regex=False).str.strip()
            df.loc[df['telefono'].isin(['Nan', 'None', '', 'Null']), 'telefono'] = 'No Registra'

            # 4. LIMPIEZA DE EMAIL
            df['email'] = df['email'].astype(str).str.strip().str.lower()
            df.loc[df['email'].isin(['nan', 'none', '', 'null']), 'email'] = 'contacto@empresa.com'

            # 5. ACTUALIZACIÓN EN BASE DE DATOS
            cursor = conn.cursor()
            for index, row in df.iterrows():
                cursor.execute('''
                    UPDATE proveedores 
                    SET contacto = ?, telefono = ?, email = ?, Nombre_Empresa = ?, Ciudad = ?
                    WHERE nit_proveedor = ?
                ''', (
                    row['contacto'], 
                    row['telefono'], 
                    row['email'], 
                    row['Nombre_Empresa'], 
                    row['Ciudad'], 
                    row['nit_proveedor']
                ))
            
            conn.commit()
            print("✨ Pandas: Tabla 'proveedores' auditada, limpiada y normalizada exitosamente.")


class ProveedorInteractivo:
    """
    Clase encargada de interactuar con el usuario mediante la consola (inputs),
    capturar los datos del nuevo proveedor, validarlos estrictamente, insertarlos 
    en la base de datos y limpiarlos automáticamente usando Pandas.
    """
    def __init__(self, db_name):
        self.db_name = db_name
        self.manager = ProveedorManager(db_name)
        self.cleaner = ProveedorDataCleaner(db_name)

    def registrar_proveedor_consola(self):
        print("\n" + "="*50)
        print("🏢 REGISTRO INTERACTIVO DE NUEVO PROVEEDOR")
        print("="*50)
        try:
            # Capturamos los datos como texto (.strip() elimina espacios en blanco accidentales)
            nit_input = input("Ingrese el NIT del proveedor (numérico): ").strip()
            nombre_empresa = input("Ingrese el nombre de la empresa: ").strip()
            ciudad = input("Ingrese la ciudad: ").strip()
            contacto = input("Ingrese el nombre del contacto principal: ").strip()
            telefono = input("Ingrese el teléfono del contacto: ").strip()
            email = input("Ingrese el correo electrónico: ").strip()

            # ------------------------------------------------------------------
            # VALIDACIONES LEVANTANDO ERRORES (RAISE VALUEERROR)
            # ------------------------------------------------------------------
            
            # 1. Validación de campos vacíos
            if not all([nit_input, nombre_empresa, ciudad, contacto, telefono, email]):
                raise ValueError("Ningún dato puede quedar vacío. Debe completar todos los campos.")

            # 2. Validación de formato de NIT
            if not nit_input.isdigit():
                raise ValueError("El NIT del proveedor debe contener únicamente números.")
            nit_proveedor = int(nit_input)

            # 3. Validación de formato de Teléfono
            if not telefono.isdigit():
                raise ValueError("El teléfono debe contener únicamente números (sin espacios ni guiones).")

            # 4. Validación de formato de Email
            if "@" not in email or "." not in email:
                raise ValueError("El formato del correo electrónico es inválido.")

            # 5. Validaciones directamente contra la Base de Datos
            import sqlite3
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                
                # Validación: ¿El NIT de proveedor ya existe?
                cursor.execute("SELECT 1 FROM proveedores WHERE nit_proveedor = ?", (nit_proveedor,))
                if cursor.fetchone():
                    raise ValueError(f"El NIT '{nit_proveedor}' ya se encuentra registrado en el sistema.")
                
                # Validación: ¿El Nombre de la Empresa ya existe? (COLLATE NOCASE ignora mayúsculas/minúsculas)
                cursor.execute("SELECT 1 FROM proveedores WHERE Nombre_Empresa = ? COLLATE NOCASE", (nombre_empresa,))
                if cursor.fetchone():
                    raise ValueError(f"La empresa con el nombre '{nombre_empresa}' ya está registrada.")
                
                # Validación: ¿El Email ya existe?
                cursor.execute("SELECT 1 FROM proveedores WHERE email = ? COLLATE NOCASE", (email,))
                if cursor.fetchone():
                    raise ValueError(f"El correo electrónico '{email}' ya se encuentra registrado por otro proveedor.")

            # ------------------------------------------------------------------
            # EJECUCIÓN SI PASA TODAS LAS VALIDACIONES
            # ------------------------------------------------------------------
            self.manager.create(
                nit_proveedor=nit_proveedor, 
                contacto=contacto, 
                telefono=telefono, 
                email=email, 
                nombre_empresa=nombre_empresa, 
                ciudad=ciudad
            )
            
            # Llamamos al limpiador de Pandas para normalizar el texto inmediatamente
            self.cleaner.limpiar_datos()
            print("✅ Proveedor registrado y datos normalizados correctamente desde consola.")

        # ------------------------------------------------------------------
        # CAPTURA DE ERRORES (EXCEPTIONS)
        # ------------------------------------------------------------------
        except ValueError as ve:
            # Atrapa de forma controlada todos los 'raise ValueError' de la sección superior
            print(f"❌ Error de Validación: {ve}")
            
        except sqlite3.IntegrityError as ie:
            # Atrapa errores de violaciones de integridad a nivel de SQL
            print(f"❌ Error de Integridad en la BD: {ie}")
            
        except Exception as e:
            # Captura general (Fallback) para evitar que el programa colapse ante un error no mapeado
            print(f"❌ Error inesperado durante el registro del proveedor: {e}")