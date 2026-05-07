# Frontend/app_central.py
# ==============================================================================
# MÓDULO FRONTEND: PANEL DE CONTROL PRINCIPAL (LAUNCHER)
# Tema: Enrutamiento de ventanas, arquitectura visual y apertura de archivos externos
# ==============================================================================

import tkinter as tk
from tkinter import messagebox
import os  # Necesario para interactuar con los archivos del sistema operativo

# Importamos las pantallas secundarias desde el mismo módulo Frontend
from Frontend.app_ventas import PantallaVentas
from Frontend.app_clientes import PantallaClientes
from Frontend.app_productos import PantallaProductos
from Frontend.app_proveedores import PantallaProveedores

class AppCentral:
    """
    Clase que construye el menú principal (Dashboard) del sistema.
    Desde aquí se lanzan los demás módulos de la aplicación y herramientas externas.
    """
    def __init__(self, root, db_path):
        self.root = root
        self.db_path = db_path
        
        # 1. CONFIGURACIÓN DE LA VENTANA PRINCIPAL
        self.root.title("Cafetería U. Sabana - Panel de Control")
        # Aumentamos la altura a 620 para dar espacio al nuevo botón de Power BI
        self.root.geometry("400x620") 
        self.root.configure(bg="#2C3E50") # Color corporativo oscuro
        self.root.resizable(False, False)

        # 2. TÍTULO DEL DASHBOARD
        tk.Label(self.root, text="SISTEMA CENTRAL ERP", font=("Arial", 18, "bold"), 
                 bg="#2C3E50", fg="white").pack(pady=30)

        # 3. BOTONES DE NAVEGACIÓN A LOS MÓDULOS INTERNOS
        btn_ventas = tk.Button(self.root, text="🛒 Módulo de Ventas", font=("Arial", 14, "bold"), 
                               bg="#3498DB", fg="white", cursor="hand2", pady=10,
                               command=self.abrir_modulo_ventas)
        btn_ventas.pack(fill="x", padx=40, pady=10)

        btn_clientes = tk.Button(self.root, text="👥 Módulo de Clientes", font=("Arial", 14, "bold"), 
                                 bg="#2ECC71", fg="white", cursor="hand2", pady=10,
                                 command=self.abrir_modulo_clientes)
        btn_clientes.pack(fill="x", padx=40, pady=10)

        btn_productos = tk.Button(self.root, text="📦 Módulo de Productos", font=("Arial", 14, "bold"), 
                                  bg="#E67E22", fg="white", cursor="hand2", pady=10,
                                  command=self.abrir_modulo_productos)
        btn_productos.pack(fill="x", padx=40, pady=10)

        btn_proveedores = tk.Button(self.root, text="🏢 Módulo de Proveedores", font=("Arial", 14, "bold"), 
                                    bg="#9B59B6", fg="white", cursor="hand2", pady=10,
                                    command=self.abrir_modulo_proveedores)
        btn_proveedores.pack(fill="x", padx=40, pady=10)

        # 4. BOTÓN PARA HERRAMIENTA EXTERNA (POWER BI)
        # Usamos el clásico color amarillo/dorado de Power BI para distinguirlo visualmente
        btn_power_bi = tk.Button(self.root, text="📊 Abrir Dashboard Analítico", font=("Arial", 14, "bold"), 
                                 bg="#F2C811", fg="black", cursor="hand2", pady=10,
                                 command=self.abrir_power_bi)
        btn_power_bi.pack(fill="x", padx=40, pady=15)


    # ==============================================================================
    # 5. LÓGICA DE ENRUTAMIENTO (Apertura de Sub-ventanas y Archivos)
    # ==============================================================================
    
    def abrir_modulo_ventas(self):
        ventana_ventas = tk.Toplevel(self.root)
        ventana_ventas.grab_set() 
        app = PantallaVentas(ventana_ventas, self.db_path)

    def abrir_modulo_clientes(self):
        ventana_clientes = tk.Toplevel(self.root)
        ventana_clientes.grab_set()
        app = PantallaClientes(ventana_clientes, self.db_path)

    def abrir_modulo_productos(self):
        ventana_productos = tk.Toplevel(self.root)
        ventana_productos.grab_set()
        app = PantallaProductos(ventana_productos, self.db_path)

    def abrir_modulo_proveedores(self):
        ventana_proveedores = tk.Toplevel(self.root)
        ventana_proveedores.grab_set()
        app = PantallaProveedores(ventana_proveedores, self.db_path)

    def abrir_power_bi(self):
        """
        Intenta abrir el archivo .pbix usando la aplicación predeterminada del sistema operativo.
        """
        # La 'r' al inicio convierte el string a "raw", evitando que Windows interprete los '\' como caracteres de escape
        ruta_pbix = r"C:\Users\diego\OneDrive\Documentos\Clase_Python_U_Sabana\2026-1\Cafeteria_Unisabana_Clase_11\Power_BI\Cafeteria_Unisabana_Clase_11.pbix"
        
        try:
            # os.startfile() es una función nativa de Windows que equivale a hacer doble clic sobre un archivo
            os.startfile(ruta_pbix)
            print("📊 Abriendo Power BI...")
        except FileNotFoundError:
            # Capturamos el error si el archivo fue borrado, movido o la ruta es incorrecta
            messagebox.showerror("Archivo No Encontrado", f"No se pudo encontrar el Dashboard.\n\nVerifique la siguiente ruta:\n{ruta_pbix}")
        except Exception as e:
            # Capturamos cualquier otro error del sistema (Ej. No tener Power BI instalado)
            messagebox.showerror("Error del Sistema", f"Ocurrió un error al intentar abrir Power BI:\n\n{e}")