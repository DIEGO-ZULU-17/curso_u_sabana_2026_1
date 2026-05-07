# Frontend/app_proveedores.py
# ==============================================================================
# MÓDULO FRONTEND: REGISTRO Y GESTIÓN DE PROVEEDORES (CRUD COMPLETO)
# Tema: GUI, Treeview (Tablas) y Validaciones
# ==============================================================================

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import os
import sys

# Agregamos la ruta del sistema para poder importar el Backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Backend.proveedores import ProveedorManager, ProveedorDataCleaner

class PantallaProveedores:
    """
    Clase que construye la interfaz gráfica para gestionar proveedores (CRUD).
    """
    def __init__(self, root, db_path):
        self.root = root
        self.db_path = db_path
        
        # Instanciamos la lógica de negocio (Backend)
        self.manager_proveedores = ProveedorManager(self.db_path)
        self.cleaner_proveedores = ProveedorDataCleaner(self.db_path)
        
        # 1. CONFIGURACIÓN DE LA VENTANA
        self.root.title("Cafetería U. Sabana - Gestión de Proveedores")
        self.root.geometry("480x780") 
        self.root.configure(bg="#f4f5f9")
        self.root.resizable(False, False)

        # 2. PROCESAMIENTO DEL LOGO
        try:
            ruta_logo = os.path.join(os.path.dirname(__file__), "Logo_proveedores.png")
            img_original = Image.open(ruta_logo)
            img_redimensionada = img_original.resize((120, 120))
            self.logo = ImageTk.PhotoImage(img_redimensionada)
            tk.Label(self.root, image=self.logo, bg="#f4f5f9").pack(pady=10)
        except Exception:
            tk.Label(self.root, text="🏢 MÓDULO PROVEEDORES", font=("Arial", 16, "bold"), bg="#f4f5f9").pack(pady=10)

        tk.Label(self.root, text="Gestión Integral de Proveedores", font=("Arial", 14, "bold"), bg="#f4f5f9").pack(pady=5)

        # 3. FORMULARIO DE INGRESO DE DATOS
        tk.Label(self.root, text="NIT Proveedor (Numérico):", bg="#f4f5f9").pack()
        self.entry_nit = tk.Entry(self.root, font=("Arial", 12), justify="center")
        self.entry_nit.pack(pady=5)

        tk.Label(self.root, text="Nombre de la Empresa:", bg="#f4f5f9").pack()
        self.entry_empresa = tk.Entry(self.root, font=("Arial", 12), justify="center")
        self.entry_empresa.pack(pady=5)

        tk.Label(self.root, text="Ciudad:", bg="#f4f5f9").pack()
        self.entry_ciudad = tk.Entry(self.root, font=("Arial", 12), justify="center")
        self.entry_ciudad.pack(pady=5)

        tk.Label(self.root, text="Contacto Principal:", bg="#f4f5f9").pack()
        self.entry_contacto = tk.Entry(self.root, font=("Arial", 12), justify="center")
        self.entry_contacto.pack(pady=5)

        tk.Label(self.root, text="Teléfono:", bg="#f4f5f9").pack()
        self.entry_telefono = tk.Entry(self.root, font=("Arial", 12), justify="center")
        self.entry_telefono.pack(pady=5)

        tk.Label(self.root, text="Correo Electrónico:", bg="#f4f5f9").pack()
        self.entry_email = tk.Entry(self.root, font=("Arial", 12), justify="center")
        self.entry_email.pack(pady=5)

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

        btn_ver = tk.Button(frame_botones, text="📊 Ver Proveedores", font=("Arial", 11, "bold"), bg="#9C27B0", fg="white", cursor="hand2", width=15, command=self.ver_proveedores_evento)
        btn_ver.grid(row=1, column=1, padx=10, pady=5)

        # Fila 2: Limpiar Formulario
        btn_limpiar = tk.Button(frame_botones, text="🧹 Limpiar Campos", font=("Arial", 10), bg="#7F8C8D", fg="white", cursor="hand2", width=33, command=self.limpiar_formulario)
        btn_limpiar.grid(row=2, column=0, columnspan=2, padx=10, pady=10)


    # ==============================================================================
    # 5. LÓGICA DE EVENTOS (CRUD) Y VALIDACIONES
    # ==============================================================================
    
    def procesar_registro_evento(self):
        """[CREATE] Valida los datos y registra un proveedor nuevo."""
        str_nit, empresa, ciudad, contacto, telefono, email = self._obtener_datos_formulario()
        try:
            if not all([str_nit, empresa, ciudad, contacto, telefono, email]):
                raise ValueError("Todos los campos son obligatorios para registrar.")
            if not str_nit.isdigit():
                raise ValueError("El NIT del proveedor debe ser un número entero.")
            if not telefono.isdigit():
                raise ValueError("El teléfono debe contener únicamente números.")
            if "@" not in email or "." not in email:
                raise ValueError("Ingrese un correo electrónico válido.")

            nit_proveedor = int(str_nit)

            # Inserción y normalización
            self.manager_proveedores.create(nit_proveedor, contacto, telefono, email, empresa, ciudad)
            self.cleaner_proveedores.limpiar_datos()

            messagebox.showinfo("Registro Exitoso", f"Proveedor '{empresa}' guardado y normalizado.")
            self.limpiar_formulario()
        except ValueError as ve:
            messagebox.showwarning("Error de Validación", str(ve))
        except sqlite3.IntegrityError:
            messagebox.showerror("Error de Integridad", "El NIT del proveedor ya existe en la base de datos.")
        except Exception as e:
            messagebox.showerror("Error Crítico", str(e))

    def procesar_actualizacion_evento(self):
        """[UPDATE] Actualiza un proveedor existente basado en el NIT."""
        str_nit, empresa, ciudad, contacto, telefono, email = self._obtener_datos_formulario()
        try:
            if not str_nit.isdigit():
                raise ValueError("Debe ingresar un NIT numérico válido para actualizar.")
            
            nit_proveedor = int(str_nit)
            
            if not self._proveedor_existe(nit_proveedor):
                raise ValueError(f"No existe ningún proveedor con el NIT {nit_proveedor}.")

            # Ejecutamos los updates individuales del manager si los campos no están vacíos
            if empresa: self.manager_proveedores.update_nombre_empresa(nit_proveedor, empresa)
            if ciudad: self.manager_proveedores.update_ciudad(nit_proveedor, ciudad)
            if contacto: self.manager_proveedores.update_contacto(nit_proveedor, contacto)
            if telefono: self.manager_proveedores.update_telefono(nit_proveedor, telefono)
            if email: self.manager_proveedores.update_email(nit_proveedor, email)

            # Normalizamos los nuevos datos con Pandas
            self.cleaner_proveedores.limpiar_datos()

            messagebox.showinfo("Actualización Exitosa", f"Datos del proveedor NIT {nit_proveedor} actualizados.")
            self.limpiar_formulario()
        except ValueError as ve:
            messagebox.showwarning("Error de Validación", str(ve))
        except Exception as e:
            messagebox.showerror("Error Crítico", str(e))

    def procesar_eliminacion_evento(self):
        """[DELETE] Elimina un proveedor pidiendo confirmación primero."""
        str_nit = self.entry_nit.get().strip()
        try:
            if not str_nit.isdigit():
                raise ValueError("Debe ingresar el NIT numérico del proveedor a eliminar.")
            
            nit_proveedor = int(str_nit)

            if not self._proveedor_existe(nit_proveedor):
                raise ValueError(f"No existe ningún proveedor con el NIT {nit_proveedor}.")

            confirmacion = messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de que desea eliminar al proveedor con NIT {nit_proveedor}?\nEsta acción no se puede deshacer.")
            
            if confirmacion:
                self.manager_proveedores.delete(nit_proveedor)
                messagebox.showinfo("Eliminación Exitosa", "El proveedor ha sido eliminado del sistema.")
                self.limpiar_formulario()

        except ValueError as ve:
            messagebox.showwarning("Error de Validación", str(ve))
        except sqlite3.IntegrityError:
            messagebox.showerror("Error de Integridad", "No se puede eliminar este proveedor porque tiene productos o ventas asociadas.")
        except Exception as e:
            messagebox.showerror("Error Crítico", str(e))

    def ver_proveedores_evento(self):
        """[READ] Abre una nueva ventana con una tabla (Treeview) de todos los proveedores."""
        ventana_tabla = tk.Toplevel(self.root)
        ventana_tabla.title("Base de Datos - Proveedores")
        ventana_tabla.geometry("900x400")
        ventana_tabla.configure(bg="#f4f5f9")
        ventana_tabla.grab_set()

        tk.Label(ventana_tabla, text="Registro Histórico de Proveedores", font=("Arial", 14, "bold"), bg="#f4f5f9").pack(pady=10)

        # Creamos el Treeview (Tabla)
        columnas = ("NIT", "Empresa", "Ciudad", "Contacto", "Teléfono", "Email")
        tabla = ttk.Treeview(ventana_tabla, columns=columnas, show="headings", height=15)

        # Definimos los encabezados y el tamaño de las columnas
        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, anchor="center", width=150 if col in ("Empresa", "Email") else 100)

        tabla.pack(pady=10, padx=10, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tabla, orient="vertical", command=tabla.yview)
        tabla.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Rellenamos la tabla con los datos de SQLite
        try:
            registros = self.manager_proveedores.read()
            for r in registros:
                # Orden en la BD: nit_proveedor, contacto, telefono, email, Nombre_Empresa, Ciudad
                # Reordenamos visualmente: NIT, Empresa, Ciudad, Contacto, Teléfono, Email
                tabla.insert("", "end", values=(r[0], r[4], r[5], r[1], r[2], r[3]))
        except Exception as e:
            messagebox.showerror("Error al cargar datos", str(e))

    # ==============================================================================
    # 6. MÉTODOS AUXILIARES
    # ==============================================================================
    def _obtener_datos_formulario(self):
        """Extrae el texto de todos los campos de entrada."""
        return (
            self.entry_nit.get().strip(),
            self.entry_empresa.get().strip(),
            self.entry_ciudad.get().strip(),
            self.entry_contacto.get().strip(),
            self.entry_telefono.get().strip(),
            self.entry_email.get().strip()
        )

    def _proveedor_existe(self, nit_proveedor):
        """Verifica en SQLite si un proveedor existe."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM proveedores WHERE nit_proveedor = ?", (nit_proveedor,))
            return cursor.fetchone() is not None

    def limpiar_formulario(self):
        """Reinicia la interfaz borrando las cajas de texto."""
        self.entry_nit.delete(0, tk.END)
        self.entry_empresa.delete(0, tk.END)
        self.entry_ciudad.delete(0, tk.END)
        self.entry_contacto.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)