"""
Aquí tienes el paso a paso estructurado y el código exacto para transicionar de un archivo .ipynb 
(ideal para exploración y ciencia de datos) a una arquitectura de software real con 
múltiples archivos .py (ideal para desarrollo de aplicaciones y despliegue).

El concepto clave es la Modularidad: separar el código por "dominios de negocio" 
para que el proyecto sea escalable, fácil de leer y permita el trabajo en equipo 
en GitHub sin generar conflictos masivos.

## Paso 1: Crear la estructura de carpetas en VS Code

Creen una carpeta nueva llamada Cafeteria_U_Sabana_Clase_6 y, dentro de ella, creen exactamente estos 4 archivos vacíos:

    productos.py (Módulo de inventario)

    clientes.py (Módulo de CRM / Usuarios)

    ventas.py (Módulo de facturación)

    main.py (El archivo orquestador / punto de entrada)

## Paso 2: Construir el módulo productos.py

Este archivo solo se encarga de saber qué es un producto y cómo calcular sus impuestos.

## Paso 3: Construir el módulo clientes.py

Este archivo solo se encarga de la lógica de los usuarios y sus descuentos.

## Paso 4: Construir el módulo ventas.py

Este archivo maneja la lógica de negocio (el carrito y la factura).

## Paso 5: Construir el Orquestador main.py

Aquí usamos la importación (import). 
El archivo main.py actúa como el gerente de la empresa: 
no hace el trabajo operativo, pero llama a los demás módulos para que trabajen juntos.

### Paso 6: Ejecución y Pruebas
Para demostrar que funciona:
    Abran una nueva Terminal en VS Code (Ctrl + ñ o Terminal -> New Terminal).
    Aseguren estar dentro de la carpeta Cafeteria_U_Sabana_Clase_6.
    Escriban el siguiente comando y presionen Enter:
    # python main.py

"""

# main.py

# Aquí se aplica la importación (import). 
# El archivo main.py actúa como el gerente de la empresa: 
# no hace el trabajo operativo, pero llama a los demás módulos para que trabajen juntos.

# 1. IMPORTACIONES: Traemos las piezas de nuestros otros archivos
from productos import Bebida, Snack
from clientes import Estudiante, Profesor
from ventas import CarritoDeCompras

def main():

    print("Iniciando Sistema Cafeteria_U_Sabana...\n")

    # 1. Creamos nuestro inventario
    cafe_tostao = Bebida(nombre="Café de Origen Tostao", precio=5000, stock=50, tamano="Mediano")
    chocolate_jet = Snack(nombre="Chocolatina Jet", precio=1200, stock=100, gramos=12)

    # 2. Creamos al cliente (Prueba cambiando 'Estudiante' por 'Profesor' para ver cómo cambia el descuento)
    cliente_actual_1 = Estudiante(nombre="Diego Zuluaga", id_cliente="00012345") # Prueba con un estudiante para ver el descuento del 10%
    cliente_actual_2 = Profesor(nombre="Yeimy Castillo", id_cliente="00067890") # Prueba con un profesor para ver el cambio en el descuento

    # 3. Inicializamos el sistema de ventas INYECTANDO al cliente
    caja_registradora_1 = CarritoDeCompras(cliente=cliente_actual_1) # Inyectamos el cliente estudiante
    caja_registradora_2 = CarritoDeCompras(cliente=cliente_actual_2) # Inyectamos el cliente profesor

    # 4. Simulamos transacciones
    caja_registradora_1.agregar_producto(cafe_tostao, 2)    
    caja_registradora_2.agregar_producto(chocolate_jet, 5)  

    # 5. Generamos el reporte final
    caja_registradora_1.generar_factura()
    caja_registradora_2.generar_factura()

# Punto de entrada estándar en Python
if __name__ == "__main__":
    main()


""" 
Paso final: Ejecución desde la Terminal

Para demostrar que funciona:

    Abran una nueva Terminal en VS Code (Ctrl + ñ o Terminal -> New Terminal).

    Aseguren estar dentro de la carpeta Cafeteria_U_Sabana_Clase_6.

    Escriban el siguiente comando y presionen Enter:

python main.py

(Si usan Mac, probablemente deban escribir python3 main.py).

Reflexión:
Miren sus carpetas. Si mañana el Departamento de Marketing quiere cambiar la lógica de los descuentos, solo modifican clientes.py. Si Inventario quiere cambiar el IVA, solo modifican productos.py. 
Nadie se estorba, el código es limpio y profesional. 
Así es como se estructuran los proyectos en la industria.
"""