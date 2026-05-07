# Frontend/app_productos.py
# ==============================================================================
# MÓDULO FRONTEND: REGISTRO Y GESTIÓN DE PRODUCTOS (CRUD COMPLETO)
# Tema: GUI, Combobox, Calendarios, Treeview (Tablas) y Validaciones
# ==============================================================================

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry # Librería para el calendario interactivo
from PIL import Image, ImageTk
import sqlite3
import os
import sys

# Agregamos la ruta del sistema para poder importar el Backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Backend.productos import ProductoManager, ProductoDataCleaner

class PantallaProductos:
    """
    Clase que construye la interfaz gráfica para gestionar el inventario de productos (CRUD).
    """
    def __init__(self, root, db_path):
        self.root = root
        self.db_path = db_path
        
        # Instanciamos la lógica de negocio (Backend)
        self.manager_productos = ProductoManager(self.db_path)
        self.cleaner_productos = ProductoDataCleaner(self.db_path)
        
        # 1. CONFIGURACIÓN DE LA VENTANA
        self.root.title("Cafetería U. Sabana - Gestión de Inventario")
        self.root.geometry("480x780") # Ventana un poco más alta para acomodar todos los campos
        self.root.configure(bg="#f4f5f9")
        self.root.resizable(False, False)

        # 2. PROCESAMIENTO DEL LOGO
        try:
            ruta_logo = os.path.join(os.path.dirname(__file__), "Logo_productos.png")
            img_original = Image.open(ruta_logo)
            img_redimensionada = img_original.resize((120, 120))
            self.logo = ImageTk.PhotoImage(img_redimensionada)
            tk.Label(self.root, image=self.logo, bg="#f4f5f9").pack(pady=10)
        except Exception:
            # Plan B si no encuentran la imagen
            tk.Label(self.root, text="📦 MÓDULO PRODUCTOS", font=("Arial", 16, "bold"), bg="#f4f5f9").pack(pady=10)

        tk.Label(self.root, text="Gestión Integral de Productos", font=("Arial", 14, "bold"), bg="#f4f5f9").pack(pady=5)

        # 3. FORMULARIO DE INGRESO DE DATOS
        
        tk.Label(self.root, text="ID Producto (Numérico):", bg="#f4f5f9").pack()
        self.entry_id = tk.Entry(self.root, font=("Arial", 12), justify="center")
        self.entry_id.pack(pady=5)

        tk.Label(self.root, text="Nombre del Producto:", bg="#f4f5f9").pack()
        self.entry_nombre = tk.Entry(self.root, font=("Arial", 12), justify="center")
        self.entry_nombre.pack(pady=5)

        tk.Label(self.root, text="Precio (COP):", bg="#f4f5f9").pack()
        self.entry_precio = tk.Entry(self.root, font=("Arial", 12), justify="center")
        self.entry_precio.pack(pady=5)

        tk.Label(self.root, text="Stock Inicial:", bg="#f4f5f9").pack()
        self.entry_stock = tk.Entry(self.root, font=("Arial", 12), justify="center")
        self.entry_stock.pack(pady=5)

        tk.Label(self.root, text="Fecha de Vencimiento:", bg="#f4f5f9").pack()
        self.cal_fecha = DateEntry(self.root, width=15, background='darkgreen',
                                   foreground='white', borderwidth=2, 
                                   date_pattern='yyyy-mm-dd', font=("Arial", 12), justify="center")
        self.cal_fecha.pack(pady=5)

        tk.Label(self.root, text="Categoría:", bg="#f4f5f9").pack()
        opciones_categoria =["Bebida", "Snack", "Almuerzo", "Postre", "Panaderia", "Insumo"]
        self.combo_categoria = ttk.Combobox(self.root, values=opciones_categoria, state="readonly", font=("Arial", 12), justify="center")
        self.combo_categoria.pack(pady=5)

        # 4. CONTENEDOR DE BOTONES (FRAME)
        frame_botones = tk.Frame(self.root, bg="#f4f5f9")
        frame_botones.pack(pady=20)

        # Fila 0: Crear y Actualizar
        btn_registrar = tk.Button(frame_botones, text="💾 Registrar", font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", cursor="hand2", width=15, command=self.procesar_registro_evento)
        btn_registrar.grid(row=0, column=0, padx=10, pady=5)

        btn_actualizar = tk.Button(frame_botones, text="🔄 Actualizar", font=("Arial", 11, "bold"), bg="#2196F3", fg="white", cursor="hand2", width=15, command=self.procesar_actualizacion_evento)
        btn_actualizar.grid(row=0, column=1, padx=10, pady=5)

        # Fila 1: Eliminar y Ver Tabla
        btn_eliminar = tk.Button(frame_botones, text="🗑️ Eliminar", font=("Arial", 11, "bold"), bg="#f44336", fg="white", cursor="hand2", width=15, command=self.procesar_eliminacion_evento)
        btn_eliminar.grid(row=1, column=0, padx=10, pady=5)

        btn_ver = tk.Button(frame_botones, text="📊 Ver Inventario", font=("Arial", 11, "bold"), bg="#9C27B0", fg="white", cursor="hand2", width=15, command=self.ver_productos_evento)
        btn_ver.grid(row=1, column=1, padx=10, pady=5)

        # Fila 2: Limpiar Formulario
        btn_limpiar = tk.Button(frame_botones, text="🧹 Limpiar Campos", font=("Arial", 10), bg="#7F8C8D", fg="white", cursor="hand2", width=33, command=self.limpiar_formulario)
        btn_limpiar.grid(row=2, column=0, columnspan=2, padx=10, pady=10)


    # ==============================================================================
    # 5. LÓGICA DE EVENTOS (CRUD) Y VALIDACIONES
    # ==============================================================================
    
    def procesar_registro_evento(self):
        """[CREATE] Valida los datos numéricos y de texto, y registra un producto."""
        str_id, nombre, str_precio, str_stock, fecha, categoria = self._obtener_datos_formulario()
        try:
            if not all([str_id, nombre, str_precio, str_stock, fecha, categoria]):
                raise ValueError("Todos los campos son obligatorios para registrar el producto.")
            
            if not str_id.isdigit():
                raise ValueError("El ID del producto debe ser un número entero.")
            
            # Validación estricta de números (Casting)
            try:
                precio = float(str_precio)
                if precio < 0: raise ValueError("El precio no puede ser negativo.")
            except ValueError:
                raise ValueError("El precio debe ser un valor numérico válido.")

            if not str_stock.isdigit():
                raise ValueError("El stock debe ser un número entero positivo.")
            
            id_producto = int(str_id)
            stock = int(str_stock)

            # Inserción en la base de datos
            self.manager_productos.create(id_producto, precio, stock, fecha, nombre, categoria)
            # Normalización automática con Pandas
            self.cleaner_productos.limpiar_datos()

            messagebox.showinfo("Registro Exitoso", f"Producto '{nombre}' agregado al inventario.")
            self.limpiar_formulario()

        except ValueError as ve:
            messagebox.showwarning("Error de Validación", str(ve))
        except sqlite3.IntegrityError:
            messagebox.showerror("Error de Integridad", "El ID del producto ya existe en la base de datos.")
        except Exception as e:
            messagebox.showerror("Error Crítico", str(e))

    def procesar_actualizacion_evento(self):
        """[UPDATE] Actualiza un producto existente si el ID coincide."""
        str_id, nombre, str_precio, str_stock, fecha, categoria = self._obtener_datos_formulario()
        try:
            if not str_id.isdigit():
                raise ValueError("Debe ingresar un ID numérico válido para actualizar el producto.")
            
            id_producto = int(str_id)
            
            # Validamos que el producto exista en la base de datos
            if not self._producto_existe(id_producto):
                raise ValueError(f"No existe ningún producto con el ID {id_producto}.")

            # Ejecutamos las actualizaciones individuales si los campos no están vacíos
            if nombre: self.manager_productos.update_nombre(id_producto, nombre)
            if str_precio: self.manager_productos.update_precio(id_producto, float(str_precio))
            if str_stock: self.manager_productos.update_stock(id_producto, int(str_stock))
            if fecha: self.manager_productos.update_fecha_vencimiento(id_producto, fecha)
            if categoria: self.manager_productos.update_categoria(id_producto, categoria)

            # Normalizamos
            self.cleaner_productos.limpiar_datos()

            messagebox.showinfo("Actualización Exitosa", f"Inventario del producto ID {id_producto} actualizado.")
            self.limpiar_formulario()

        except ValueError as ve:
            messagebox.showwarning("Error de Validación", str(ve))
        except Exception as e:
            messagebox.showerror("Error Crítico", str(e))

    def procesar_eliminacion_evento(self):
        """[DELETE] Elimina un producto pidiendo confirmación de seguridad."""
        str_id = self.entry_id.get().strip()
        try:
            if not str_id.isdigit():
                raise ValueError("Debe ingresar el ID numérico del producto a eliminar.")
            
            id_producto = int(str_id)

            if not self._producto_existe(id_producto):
                raise ValueError(f"No existe ningún producto con el ID {id_producto}.")

            confirmacion = messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de que desea eliminar el producto ID {id_producto}?\nPerderá el registro histórico de este ítem.")
            
            if confirmacion:
                self.manager_productos.delete(id_producto)
                messagebox.showinfo("Eliminación Exitosa", "El producto ha sido eliminado del catálogo.")
                self.limpiar_formulario()

        except ValueError as ve:
            messagebox.showwarning("Error de Validación", str(ve))
        except sqlite3.IntegrityError:
            messagebox.showerror("Error de Integridad", "No se puede eliminar el producto porque ya tiene ventas registradas asociadas a él.")
        except Exception as e:
            messagebox.showerror("Error Crítico", str(e))

    def ver_productos_evento(self):
        """[READ] Abre una tabla interactiva para mostrar el inventario."""
        ventana_tabla = tk.Toplevel(self.root)
        ventana_tabla.title("Base de Datos - Inventario de Productos")
        ventana_tabla.geometry("950x400")
        ventana_tabla.configure(bg="#f4f5f9")
        ventana_tabla.grab_set()

        tk.Label(ventana_tabla, text="Catálogo Actual de Productos", font=("Arial", 14, "bold"), bg="#f4f5f9").pack(pady=10)

        # Definimos las columnas a mostrar
        columnas = ("ID", "Nombre", "Precio (COP)", "Stock", "Vencimiento", "Categoría")
        tabla = ttk.Treeview(ventana_tabla, columns=columnas, show="headings", height=15)

        # Formateamos las columnas
        for col in columnas:
            tabla.heading(col, text=col)
            # Le damos más ancho a la columna del nombre del producto
            tabla.column(col, anchor="center", width=200 if col == "Nombre" else 120)

        tabla.pack(pady=10, padx=10, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tabla, orient="vertical", command=tabla.yview)
        tabla.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Rellenamos la tabla con los datos de SQLite
        try:
            registros = self.manager_productos.read()
            for r in registros:
                # El orden del tuple devuelto por SQLite es: 
                # (id_producto, precio, stock, fecha_vencimiento, Nombre_Producto, Categoria)
                # Lo reordenamos visualmente: ID, Nombre, Precio, Stock, Vencimiento, Categoría
                precio_formateado = f"${r[1]:,.2f}"
                tabla.insert("", "end", values=(r[0], r[4], precio_formateado, r[2], r[3], r[5]))
        except Exception as e:
            messagebox.showerror("Error al cargar datos", str(e))

    # ==============================================================================
    # 6. MÉTODOS AUXILIARES
    # ==============================================================================
    def _obtener_datos_formulario(self):
        """Extrae el texto de todos los campos de entrada."""
        return (
            self.entry_id.get().strip(),
            self.entry_nombre.get().strip(),
            self.entry_precio.get().strip(),
            self.entry_stock.get().strip(),
            self.cal_fecha.get(),
            self.combo_categoria.get()
        )

    def _producto_existe(self, id_producto):
        """Verifica en la BD si el producto ya existe mediante un SELECT."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM productos WHERE id_producto = ?", (id_producto,))
            return cursor.fetchone() is not None

    def limpiar_formulario(self):
        """Reinicia la interfaz borrando las cajas de texto y el combobox."""
        self.entry_id.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)
        self.combo_categoria.set('')