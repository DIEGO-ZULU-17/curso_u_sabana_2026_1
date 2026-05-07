# Archivo de la Interfaz Gráfica (GUI)

# Para procesar imágenes en la interfaz, 
# deben instalar la librería estándar de imágenes en Python ejecutando en su terminal:
# pip install Pillow

# frontend/app_ventas.py
# ==============================================================================
# MÓDULO FRONTEND: INTERFAZ GRÁFICA DE USUARIO (GUI)
# Tema: Eventos, Excepciones e Imágenes
# ==============================================================================

import tkinter as tk
from tkinter import messagebox # Para mostrar ventanas emergentes (Pop-ups de error/éxito)
from PIL import Image, ImageTk # Para procesar el logo (.png / .jpg)
import sqlite3
import os
import sys

# Agregamos la carpeta 'backend' a la ruta del sistema para poder importar sus clases
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from Backend.ventas import VentasManager

class PantallaVentas:
    """
    Clase que construye la interfaz gráfica para registrar ventas.
    Aplica programación orientada a eventos.
    """
    def __init__(self, root, db_path):
        self.root = root
        self.db_path = db_path
        self.manager_ventas = VentasManager(self.db_path)
        
        # 1. CONFIGURACIÓN DE LA VENTANA PRINCIPAL
        self.root.title("Cafetería U. Sabana - Punto de Venta (POS)")
        self.root.geometry("450x600") # Ancho x Alto en píxeles
        self.root.configure(bg="#f4f5f9") # Color de fondo (Gris claro)
        self.root.resizable(False, False) # Evita que el usuario cambie el tamaño de la ventana

        # 2. PROCESAMIENTO DE IMÁGENES (Cargar el Logo)
        try:
            # Buscamos el logo en la carpeta frontend/assets/
            ruta_logo = os.path.join(os.path.dirname(__file__), "Logo_ventas.png")
            # Abrimos la imagen y la redimensionamos a 150x150 píxeles
            img_original = Image.open(ruta_logo)
            img_redimensionada = img_original.resize((150, 150))
            self.logo = ImageTk.PhotoImage(img_redimensionada)
            
            # Colocamos la imagen dentro de una "Etiqueta" (Label)
            lbl_logo = tk.Label(self.root, image=self.logo, bg="#f4f4f9")
            lbl_logo.pack(pady=10) # pack() la ubica en la ventana con una separación de 10px arriba y abajo
        except Exception as e:
            # Si el logo no existe, mostramos un texto alternativo en lugar de colapsar
            tk.Label(self.root, text="☕ CAFETERÍA UNISABANA", font=("Arial", 16, "bold"), bg="#f4f4f9").pack(pady=20)

        # 3. DISEÑO DE FORMULARIO (Ingreso de información)
        # Título del formulario
        tk.Label(self.root, text="Registro de Nueva Venta", font=("Arial", 14), bg="#f4f4f9").pack(pady=10)

        # Campo: ID Cliente
        tk.Label(self.root, text="ID Cliente:", bg="#f4f4f9").pack()
        self.entry_cliente = tk.Entry(self.root, font=("Arial", 12), justify="center")
        self.entry_cliente.pack(pady=5)

        # Campo: ID Producto
        tk.Label(self.root, text="ID Producto:", bg="#f4f4f9").pack()
        self.entry_producto = tk.Entry(self.root, font=("Arial", 12), justify="center")
        self.entry_producto.pack(pady=5)

        # Campo: NIT Proveedor
        tk.Label(self.root, text="NIT Proveedor:", bg="#f4f4f9").pack()
        self.entry_proveedor = tk.Entry(self.root, font=("Arial", 12), justify="center")
        self.entry_proveedor.pack(pady=5)

        # Campo: Cantidad
        tk.Label(self.root, text="Cantidad a vender:", bg="#f4f4f9").pack()
        self.entry_cantidad = tk.Entry(self.root, font=("Arial", 12), justify="center")
        self.entry_cantidad.pack(pady=5)

        # 4. BOTONES Y EVENTOS (Clics)
        # El parámetro 'command' enlaza el clic del botón a una función (Evento)
        btn_registrar = tk.Button(self.root, text="💳 Registrar Venta", font=("Arial", 12, "bold"), 
                                  bg="#4CAF50", fg="white", cursor="hand2",
                                  command=self.procesar_venta_evento) # <-- EVENTO
        btn_registrar.pack(pady=20, fill="x", padx=50) # fill="x" hace que el botón se estire a lo ancho

        btn_limpiar = tk.Button(self.root, text="🧹 Limpiar Campos", font=("Arial", 10), 
                                bg="#f44336", fg="white", cursor="hand2",
                                command=self.limpiar_formulario)
        btn_limpiar.pack(fill="x", padx=100)


    # ==============================================================================
    # 5. MANEJO DE EVENTOS Y EXCEPCIONES (Lógica de la Interfaz)
    # ==============================================================================
    def procesar_venta_evento(self):
        """
        Esta función se ejecuta al hacer clic en 'Registrar Venta'.
        Atrapa los datos de la interfaz visual, los valida mediante try-except 
        y los envía al backend (SQLite).
        """
        # Extraemos el texto escrito por el usuario en las cajas de texto (Entry)
        str_cliente = self.entry_cliente.get().strip()
        str_producto = self.entry_producto.get().strip()
        str_proveedor = self.entry_proveedor.get().strip()
        str_cantidad = self.entry_cantidad.get().strip()

        # BLOQUE TRY-EXCEPT: Protección de la Interfaz Gráfica
        try:
            # 1. Validación de campos vacíos
            if not all([str_cliente, str_producto, str_proveedor, str_cantidad]):
                raise ValueError("Por favor, complete todos los campos del formulario.")

            # 2. Validación de tipos de datos (Casting a enteros)
            # Si el usuario escribe "Dos" en vez de "2", int() fallará y lanzará ValueError
            id_cliente = int(str_cliente)
            id_producto = int(str_producto)
            nit_proveedor = int(str_proveedor)
            cantidad = int(str_cantidad)

            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a cero.")

            # 3. Lógica de Negocio (Consulta a Base de Datos)
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Verificamos si el producto existe y tenemos stock
                cursor.execute("SELECT nombre_producto, precio, stock FROM productos WHERE id_producto = ?", (id_producto,))
                resultado = cursor.fetchone()

                if not resultado:
                    raise ValueError(f"El Producto con ID {id_producto} no existe en el inventario.")

                nombre_prod, precio, stock = resultado

                if stock < cantidad:
                    raise ValueError(f"Stock insuficiente. Solo hay {stock} unidades de '{nombre_prod}'.")

                # Calculamos el total
                total_venta = precio * cantidad

                # Actualizamos el stock
                nuevo_stock = stock - cantidad
                cursor.execute("UPDATE productos SET stock = ? WHERE id_producto = ?", (nuevo_stock, id_producto))
                conn.commit()

            # 4. Enviamos los datos al Backend (VentasManager)
            self.manager_ventas.create(id_cliente, id_producto, nit_proveedor, cantidad, total_venta)

            # 5. SALIDA DE INFORMACIÓN: Mensaje de Éxito (Pop-up)
            messagebox.showinfo("Venta Exitosa", f"Se han vendido {cantidad}x '{nombre_prod}'.\n\nTotal: ${total_venta:,.2f} COP\n\n(Actualice Power BI para ver los cambios)")
            
            # Limpiamos el formulario automáticamente tras el éxito
            self.limpiar_formulario()

        except ValueError as ve:
            # SALIDA DE INFORMACIÓN: Mensaje de Error Lógico/Digitación
            messagebox.showwarning("Error de Validación", str(ve))
            
        except sqlite3.IntegrityError:
            # SALIDA DE INFORMACIÓN: Mensaje de Error de Llaves Foráneas (FK)
            messagebox.showerror("Error de Integridad", "El Cliente o el Proveedor ingresado NO existen en la base de datos.")
            
        except Exception as e:
            # SALIDA DE INFORMACIÓN: Mensaje de Error Crítico (Fallo del sistema)
            messagebox.showerror("Error Crítico", f"Ha ocurrido un error inesperado:\n{str(e)}")


    def limpiar_formulario(self):
        """Borra el contenido de las cajas de texto de la interfaz."""
        # delete(0, tk.END) borra desde el primer carácter (0) hasta el final
        self.entry_cliente.delete(0, tk.END)
        self.entry_producto.delete(0, tk.END)
        self.entry_proveedor.delete(0, tk.END)
        self.entry_cantidad.delete(0, tk.END)