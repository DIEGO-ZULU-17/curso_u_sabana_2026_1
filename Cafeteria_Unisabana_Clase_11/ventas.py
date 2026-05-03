# ventas.py

import sqlite3
from datetime import datetime

class VentasManager:
    def __init__(self, db_name):
        self.db_name = db_name

    def create(self, id_cliente, id_producto, nit_proveedor, cantidad, total_venta):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;") # Aseguramos validación de FK
            fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            try:
                cursor.execute('''
                    INSERT INTO ventas (id_cliente, id_producto, nit_proveedor, cantidad, total_venta, fecha_venta)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (id_cliente, id_producto, nit_proveedor, cantidad, total_venta, fecha_actual))
                conn.commit()
                print(f"✅ Venta registrada exitosamente. Total: ${total_venta}")
            except sqlite3.IntegrityError:
                print("⚠️ Error: Violación de llave foránea. Cliente, Producto o Proveedor no existe.")

    def read(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ventas")
            return cursor.fetchall()

    def update_cantidad(self, id_venta, nueva_cantidad, nuevo_total):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE ventas SET cantidad = ?, total_venta = ? WHERE id_venta = ?
            ''', (nueva_cantidad, nuevo_total, id_venta))
            conn.commit()
            print(f"🔄 Venta {id_venta} actualizada.")

    def delete(self, id_venta):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ventas WHERE id_venta = ?", (id_venta,))
            conn.commit()
            print(f"❌ Venta {id_venta} eliminada.")


class VentasInteractivo:
    """
    Clase encargada de interactuar con el usuario mediante la consola (inputs),
    capturar los datos de la nueva venta, validar la existencia de las llaves 
    foráneas (Cliente, Producto, Proveedor), validar el stock disponible, 
    calcular el total de la venta matemáticamente y guardar todo en la base de datos.
    """
    def __init__(self, db_name):
        # Guardamos el nombre de la base de datos
        self.db_name = db_name
        # Instanciamos el manager de ventas que ya contiene la función 'create'
        self.manager = VentasManager(db_name)

    def registrar_venta_consola(self):
        print("\n" + "="*50)
        print("🛒 REGISTRO INTERACTIVO DE NUEVA VENTA")
        print("="*50)

        try:
            # 1. Capturamos los datos como texto (.strip() elimina espacios en blanco accidentales)
            id_cliente_input = input("Ingrese el ID del cliente: ").strip()
            id_producto_input = input("Ingrese el ID del producto: ").strip()
            nit_proveedor_input = input("Ingrese el NIT del proveedor: ").strip()
            cantidad_input = input("Ingrese la cantidad a comprar: ").strip()

            # ------------------------------------------------------------------
            # VALIDACIONES LEVANTANDO ERRORES (RAISE VALUEERROR)
            # ------------------------------------------------------------------
            
            # Validación 1: Campos vacíos
            # all() verifica que todos los elementos de la lista tengan algún contenido
            if not all([id_cliente_input, id_producto_input, nit_proveedor_input, cantidad_input]):
                raise ValueError("Ningún dato puede quedar vacío. Debe completar todos los campos.")

            # Validación 2: Formatos numéricos de IDs
            if not id_cliente_input.isdigit():
                raise ValueError("El ID del cliente debe ser un número entero.")
            id_cliente = int(id_cliente_input)

            if not id_producto_input.isdigit():
                raise ValueError("El ID del producto debe ser un número entero.")
            id_producto = int(id_producto_input)

            if not nit_proveedor_input.isdigit():
                raise ValueError("El NIT del proveedor debe ser un número entero.")
            nit_proveedor = int(nit_proveedor_input)

            # Validación 3: Formato numérico y lógico de la Cantidad
            if not cantidad_input.isdigit() or int(cantidad_input) <= 0:
                raise ValueError("La cantidad debe ser un número entero mayor a 0.")
            cantidad = int(cantidad_input)

            # ------------------------------------------------------------------
            # VALIDACIONES CONTRA LA BASE DE DATOS Y LÓGICA DE NEGOCIO
            # ------------------------------------------------------------------
            import sqlite3
            
            # Usamos 'with' para abrir la base de datos y que se cierre sola al terminar el bloque
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                
                # Validación 4: ¿El Cliente existe?
                cursor.execute("SELECT 1 FROM clientes WHERE id_cliente = ?", (id_cliente,))
                if not cursor.fetchone():
                    raise ValueError(f"El cliente con ID '{id_cliente}' no se encuentra registrado en el sistema.")

                # Validación 5: ¿El Proveedor existe?
                cursor.execute("SELECT 1 FROM proveedores WHERE nit_proveedor = ?", (nit_proveedor,))
                if not cursor.fetchone():
                    raise ValueError(f"El proveedor con NIT '{nit_proveedor}' no se encuentra registrado.")

                # Validación 6: ¿El Producto existe? ¿Tiene Stock suficiente? Extraer Precio.
                # Consultamos el precio, el stock y el nombre del producto en una sola consulta
                cursor.execute("SELECT precio, stock, Nombre_Producto FROM productos WHERE id_producto = ?", (id_producto,))
                producto_info = cursor.fetchone()
                
                # Si 'producto_info' es None, significa que no encontró el ID del producto
                if not producto_info:
                    raise ValueError(f"El producto con ID '{id_producto}' no existe en el inventario.")
                
                # Desempaquetamos la tupla devuelta por la consulta
                precio_producto = producto_info[0]
                stock_actual = producto_info[1]
                nombre_producto = producto_info[2]

                # Validación de Stock (Sanity Check vital para el negocio)
                if stock_actual < cantidad:
                    raise ValueError(f"Stock insuficiente. Intentas vender {cantidad}, pero solo hay {stock_actual} unidades disponibles de '{nombre_producto}'.")

                # CÁLCULO FINANCIERO: Calculamos el total de la venta matemáticamente
                total_venta = cantidad * precio_producto

                # ACTUALIZACIÓN DE INVENTARIO: Restamos el stock vendido del inventario disponible
                nuevo_stock = stock_actual - cantidad
                cursor.execute("UPDATE productos SET stock = ? WHERE id_producto = ?", (nuevo_stock, id_producto))
                
                # Confirmamos el descuento del inventario en la base de datos
                conn.commit()

            # ------------------------------------------------------------------
            # EJECUCIÓN SI PASA TODAS LAS VALIDACIONES (REGISTRAR LA VENTA)
            # ------------------------------------------------------------------
            # Usamos el manager para insertar la venta en la tabla 'ventas'
            self.manager.create(
                id_cliente=id_cliente,
                id_producto=id_producto,
                nit_proveedor=nit_proveedor,
                cantidad=cantidad,
                total_venta=total_venta
            )
            
            print(f"✅ Venta registrada exitosamente. El inventario de '{nombre_producto}' ha bajado a {nuevo_stock} unidades.")

        # ------------------------------------------------------------------
        # CAPTURA DE ERRORES (EXCEPTIONS)
        # ------------------------------------------------------------------
        except ValueError as ve:
            # Atrapa de forma controlada todos los 'raise ValueError' y los de conversión (int)
            print(f"❌ Error de Validación: {ve}")
            
        except sqlite3.IntegrityError as ie:
            # Atrapa errores de violaciones de integridad de SQL (ej. llaves foráneas rotas a nivel de motor)
            print(f"❌ Error de Integridad en la BD: {ie}")
            
        except Exception as e:
            # Captura general (Fallback) para evitar que el programa colapse ante un error inesperado
            print(f"❌ Error inesperado durante el registro de la venta: {e}")