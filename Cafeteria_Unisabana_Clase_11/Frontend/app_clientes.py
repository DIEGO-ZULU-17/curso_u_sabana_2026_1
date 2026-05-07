# Frontend/app_clientes.py
# ==============================================================================
# MÓDULO FRONTEND: REGISTRO Y GESTIÓN DE CLIENTES (CRUD COMPLETO)
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
from Backend.clientes import ClienteManager, ClienteDataCleaner

class PantallaClientes:
    """
    Clase que construye la interfaz gráfica para gestionar clientes (CRUD).
    """
    def __init__(self, root, db_path):
        self.root = root
        self.db_path = db_path
        
        # Instanciamos la lógica de negocio (Backend)
        self.manager_clientes = ClienteManager(self.db_path)
        self.cleaner_clientes = ClienteDataCleaner(self.db_path)
        
        # 1. CONFIGURACIÓN DE LA VENTANA
        self.root.title("Cafetería U. Sabana - Gestión de Clientes")
        self.root.geometry("480x750") # Ventana ajustada para los nuevos botones
        self.root.configure(bg="#f4f5f9")
        self.root.resizable(False, False)

        # 2. PROCESAMIENTO DEL LOGO
        try:
            ruta_logo = os.path.join(os.path.dirname(__file__), "Logo_clientes.png")
            img_original = Image.open(ruta_logo)
            img_redimensionada = img_original.resize((120, 120))
            self.logo = ImageTk.PhotoImage(img_redimensionada)
            tk.Label(self.root, image=self.logo, bg="#f4f5f9").pack(pady=10)
        except Exception:
            tk.Label(self.root, text="👥 MÓDULO CLIENTES", font=("Arial", 16, "bold"), bg="#f4f5f9").pack(pady=10)

        tk.Label(self.root, text="Gestión Integral de Clientes", font=("Arial", 14, "bold"), bg="#f4f5f9").pack(pady=5)

        # 3. FORMULARIO DE INGRESO DE DATOS
        tk.Label(self.root, text="ID Cliente (Numérico):", bg="#f4f5f9").pack()
        self.entry_id = tk.Entry(self.root, font=("Arial", 12), justify="center")
        self.entry_id.pack(pady=5)

        tk.Label(self.root, text="Nombre Completo:", bg="#f4f5f9").pack()
        self.entry_nombre = tk.Entry(self.root, font=("Arial", 12), justify="center")
        self.entry_nombre.pack(pady=5)

        tk.Label(self.root, text="Correo Electrónico:", bg="#f4f5f9").pack()
        self.entry_email = tk.Entry(self.root, font=("Arial", 12), justify="center")
        self.entry_email.pack(pady=5)

        tk.Label(self.root, text="Teléfono:", bg="#f4f5f9").pack()
        self.entry_telefono = tk.Entry(self.root, font=("Arial", 12), justify="center")
        self.entry_telefono.pack(pady=5)

        tk.Label(self.root, text="Fecha de Nacimiento:", bg="#f4f5f9").pack()
        self.cal_fecha = DateEntry(self.root, width=15, background='darkblue',
                                   foreground='white', borderwidth=2, 
                                   date_pattern='yyyy-mm-dd', font=("Arial", 12), justify="center")
        self.cal_fecha.pack(pady=5)

        tk.Label(self.root, text="Tipo de Cliente:", bg="#f4f5f9").pack()
        opciones_tipo = ["Estudiante", "Profesor", "Externo", "Administrativo"]
        self.combo_tipo = ttk.Combobox(self.root, values=opciones_tipo, state="readonly", font=("Arial", 12), justify="center")
        self.combo_tipo.pack(pady=5)

        # 4. CONTENEDOR DE BOTONES (FRAME)
        # Usamos un Frame para organizar los botones en forma de cuadrícula (Grid) y ahorrar espacio
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

        btn_ver = tk.Button(frame_botones, text="📊 Ver Clientes", font=("Arial", 11, "bold"), bg="#9C27B0", fg="white", cursor="hand2", width=15, command=self.ver_clientes_evento)
        btn_ver.grid(row=1, column=1, padx=10, pady=5)

        # Fila 2: Limpiar Formulario (Ocupa las dos columnas)
        btn_limpiar = tk.Button(frame_botones, text="🧹 Limpiar Campos", font=("Arial", 10), bg="#7F8C8D", fg="white", cursor="hand2", width=33, command=self.limpiar_formulario)
        btn_limpiar.grid(row=2, column=0, columnspan=2, padx=10, pady=10)


    # ==============================================================================
    # 5. LÓGICA DE EVENTOS (CRUD) Y VALIDACIONES
    # ==============================================================================
    
    def procesar_registro_evento(self):
        """[CREATE] Valida los datos y registra un cliente nuevo."""
        str_id, nombre, email, telefono, fecha, tipo = self._obtener_datos_formulario()
        try:
            if not all([str_id, nombre, email, telefono, fecha, tipo]):
                raise ValueError("Todos los campos son obligatorios para registrar.")
            if not str_id.isdigit():
                raise ValueError("El ID del cliente debe ser un número entero.")
            if "@" not in email or "." not in email:
                raise ValueError("Ingrese un correo electrónico válido.")

            # Inserción y normalización
            self.manager_clientes.create(int(str_id), email, telefono, fecha, nombre, tipo)
            self.cleaner_clientes.limpiar_datos()

            messagebox.showinfo("Registro Exitoso", f"Cliente {nombre} guardado y normalizado.")
            self.limpiar_formulario()
        except ValueError as ve:
            messagebox.showwarning("Error de Validación", str(ve))
        except sqlite3.IntegrityError:
            messagebox.showerror("Error de Integridad", "El ID o el Email ya existen en la base de datos.")
        except Exception as e:
            messagebox.showerror("Error Crítico", str(e))

    def procesar_actualizacion_evento(self):
        """[UPDATE] Actualiza un cliente existente basado en el ID."""
        str_id, nombre, email, telefono, fecha, tipo = self._obtener_datos_formulario()
        try:
            if not str_id.isdigit():
                raise ValueError("Debe ingresar un ID numérico válido para actualizar.")
            
            id_cliente = int(str_id)
            
            # Validamos que el cliente exista antes de intentar actualizarlo
            if not self._cliente_existe(id_cliente):
                raise ValueError(f"No existe ningún cliente con el ID {id_cliente}.")

            # Ejecutamos los updates individuales del manager
            if nombre: self.manager_clientes.update_nombre(id_cliente, nombre)
            if email: self.manager_clientes.update_email(id_cliente, email)
            if telefono: self.manager_clientes.update_telefono(id_cliente, telefono)
            if fecha: self.manager_clientes.update_fecha_nacimiento(id_cliente, fecha)
            if tipo: self.manager_clientes.update_tipo(id_cliente, tipo)

            # Normalizamos los nuevos datos con Pandas
            self.cleaner_clientes.limpiar_datos()

            messagebox.showinfo("Actualización Exitosa", f"Datos del cliente ID {id_cliente} actualizados.")
            self.limpiar_formulario()
        except ValueError as ve:
            messagebox.showwarning("Error de Validación", str(ve))
        except Exception as e:
            messagebox.showerror("Error Crítico", str(e))

    def procesar_eliminacion_evento(self):
        """[DELETE] Elimina un cliente pidiendo confirmación primero."""
        str_id = self.entry_id.get().strip()
        try:
            if not str_id.isdigit():
                raise ValueError("Debe ingresar el ID numérico del cliente a eliminar.")
            
            id_cliente = int(str_id)

            if not self._cliente_existe(id_cliente):
                raise ValueError(f"No existe ningún cliente con el ID {id_cliente}.")

            # Pedimos confirmación al usuario (Pop-up de Sí/No)
            confirmacion = messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de que desea eliminar al cliente con ID {id_cliente}?\nEsta acción no se puede deshacer.")
            
            if confirmacion:
                self.manager_clientes.delete(id_cliente)
                messagebox.showinfo("Eliminación Exitosa", "El cliente ha sido eliminado del sistema.")
                self.limpiar_formulario()

        except ValueError as ve:
            messagebox.showwarning("Error de Validación", str(ve))
        except sqlite3.IntegrityError:
            messagebox.showerror("Error de Integridad", "No se puede eliminar este cliente porque tiene compras registradas en Ventas.")
        except Exception as e:
            messagebox.showerror("Error Crítico", str(e))

    def ver_clientes_evento(self):
        """[READ] Abre una nueva ventana con una tabla (Treeview) de todos los clientes."""
        ventana_tabla = tk.Toplevel(self.root)
        ventana_tabla.title("Base de Datos - Clientes")
        ventana_tabla.geometry("900x400")
        ventana_tabla.configure(bg="#f4f5f9")
        ventana_tabla.grab_set() # Modal

        tk.Label(ventana_tabla, text="Registro Histórico de Clientes", font=("Arial", 14, "bold"), bg="#f4f5f9").pack(pady=10)

        # Creamos el Treeview (Tabla)
        columnas = ("ID", "Nombre", "Email", "Teléfono", "Nacimiento", "Tipo")
        tabla = ttk.Treeview(ventana_tabla, columns=columnas, show="headings", height=15)

        # Definimos los encabezados y el tamaño de las columnas
        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, anchor="center", width=140 if col != "Email" else 200)

        tabla.pack(pady=10, padx=10, fill="both", expand=True)

        # Agregamos barra de desplazamiento (Scrollbar)
        scrollbar = ttk.Scrollbar(tabla, orient="vertical", command=tabla.yview)
        tabla.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Rellenamos la tabla con los datos de SQLite
        try:
            registros = self.manager_clientes.read()
            for r in registros:
                # El orden de la tabla SQLite en backend es: id_cliente, email, telefono, fecha_nacimiento, Nombre_Cliente, Tipo_Cliente
                # Los reordenamos para la vista de la tabla: ID, Nombre, Email, Teléfono, Fecha, Tipo
                tabla.insert("", "end", values=(r[0], r[4], r[1], r[2], r[3], r[5]))
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
            self.entry_email.get().strip(),
            self.entry_telefono.get().strip(),
            self.cal_fecha.get(),
            self.combo_tipo.get()
        )

    def _cliente_existe(self, id_cliente):
        """Verifica en SQLite si un cliente ya existe antes de actualizarlo o borrarlo."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM clientes WHERE id_cliente = ?", (id_cliente,))
            return cursor.fetchone() is not None

    def limpiar_formulario(self):
        """Reinicia la interfaz borrando las cajas de texto."""
        self.entry_id.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.combo_tipo.set('')