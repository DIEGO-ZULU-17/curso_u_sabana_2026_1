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
# ==============================================================================
# ARCHIVO PRINCIPAL (ORQUESTADOR Y BATERÍA DE PRUEBAS)
# ==============================================================================

# 1. IMPORTACIONES: Traemos todas las clases de nuestros módulos
from productos import Bebida, Snack
from clientes import Estudiante, Profesor
from proveedores import Proveedor
from ventas import CarritoDeCompras

def main():
    print("☕ INICIANDO BATERÍA DE PRUEBAS 'CAFETERÍA U. SABANA' ☕\n")

    # ==========================================================================
    # PRUEBA 1: MÓDULO DE PRODUCTOS (Herencia y Polimorfismo)
    # ==========================================================================
    print("--- 1. PRUEBAS DE PRODUCTOS ---")
    
    # Instanciamos los objetos
    cafe_tostao = Bebida(nombre="Café de Origen Tostao", precio=5000, stock=50, tamano="Mediano")
    chocolate_jet = Snack(nombre="Chocolatina Jet", precio=1200, stock=100, gramos=12)

    # Probamos lectura de atributos públicos y privados (Getters)
    print(f"Nombre Bebida: {cafe_tostao.nombre}")                # Café de Origen Tostao
    print(f"Precio Bebida: ${cafe_tostao.get_precio():,.0f}")    # 5000 (Viene de atributo privado)
    print(f"Stock Bebida:  {cafe_tostao.get_stock()} unds")      # 50 (Viene de atributo privado)
    print(f"Tamaño Bebida: {cafe_tostao.tamano}")                # Mediano (Atributo propio de Bebida)

    print("\n") # Salto de línea

    print(f"Nombre Snack: {chocolate_jet.nombre}")               # Chocolatina Jet
    print(f"Precio Snack: ${chocolate_jet.get_precio():,.0f}")   # 1200
    print(f"Stock Snack:  {chocolate_jet.get_stock()} unds")     # 100
    print(f"Peso Snack:   {chocolate_jet.gramos}g")              # 12 (Atributo propio de Snack)

    print("\n")

    # Probamos el Polimorfismo (Mismo método, diferente cálculo matemático)
    print(f"Impuesto Café (8%):  ${cafe_tostao.calcular_impuesto():,.1f}")    # 400.0
    print(f"Impuesto Snack (19%): ${chocolate_jet.calcular_impuesto():,.1f}") # 228.0
    print("\n")


    # ==========================================================================
    # PRUEBA 2: MÓDULO DE CLIENTES (Polimorfismo en Descuentos)
    # ==========================================================================
    print("--- 2. PRUEBAS DE CLIENTES ---")
    
    estudiante_ana = Estudiante(nombre="Ana Gómez", id_cliente="1001")
    profesor_carlos = Profesor(nombre="Carlos Ruiz", id_cliente="2002")
    
    print(f"Descuento Estudiante ({estudiante_ana.nombre}): {estudiante_ana.obtener_descuento() * 100}%") # 10.0%
    print(f"Descuento Profesor ({profesor_carlos.nombre}): {profesor_carlos.obtener_descuento() * 100}%") # 5.0%
    print("\n")


    # ==========================================================================
    # PRUEBA 3: MÓDULO DE PROVEEDORES (Encapsulamiento y Validaciones)
    # ==========================================================================
    print("--- 3. PRUEBAS DE PROVEEDORES ---")
    
    proveedor_cafe = Proveedor(nombre_empresa="CoopCafé", nit="900123456", ciudad="Bogotá")
    
    # Probamos el Setter del NIT con errores intencionales (Sanity Check)
    print("\n[Prueba de Seguridad NIT]")
    proveedor_cafe.set_nit("")          # Error: Vacío
    proveedor_cafe.set_nit("900ABC")    # Error: Contiene letras
    proveedor_cafe.set_nit("800987654") # Éxito: Formato válido
    
    # Probamos la interacción entre objetos (Proveedor abastece Producto)
    print("\n[Prueba de Abastecimiento]")
    # Intento fallido (Cantidad 0 o negativa)
    proveedor_cafe.suministrar_producto(producto=cafe_tostao, cantidad=0) 
    # Intento exitoso (Suma 20 al stock actual de 50 -> Queda en 70)
    proveedor_cafe.suministrar_producto(producto=cafe_tostao, cantidad=20) 
    print("\n")


    # ==========================================================================
    # PRUEBA 4: MÓDULO DE VENTAS (Carrito e Integración Total)
    # ==========================================================================
    print("--- 4. PRUEBAS DE CARRITO DE COMPRAS ---")
    
    # IMPORTANTE: En la nueva arquitectura, el Carrito EXIGE un objeto Cliente.
    # Creamos un carrito para la estudiante Ana
    carrito_ana = CarritoDeCompras(cliente=estudiante_ana)

    # Agregamos productos (Caminos de éxito)
    print("\n[Agregando productos válidos]")
    carrito_ana.agregar_producto(cafe_tostao, 2)     # Agrega 2 cafés
    carrito_ana.agregar_producto(chocolate_jet, 3)   # Agrega 3 snacks

    # Agregamos productos (Caminos de error por falta de stock)
    print("\n[Prueba de Seguridad: Exceso de Stock]")
    # El stock del café es 70 (50 iniciales + 20 del proveedor - 2 de la compra anterior = 68 restantes)
    carrito_ana.agregar_producto(cafe_tostao, 100)   # Error: Supera los 68 disponibles
    carrito_ana.agregar_producto(chocolate_jet, 101) # Error: Supera los 97 disponibles

    # Generamos la factura de Ana (Debe aplicar 10% de descuento)
    carrito_ana.generar_factura()


    # ==========================================================================
    # PRUEBA 5: ESCENARIOS ADICIONALES (Profesor y Carrito Vacío)
    # ==========================================================================
    print("--- 5. PRUEBAS ADICIONALES ---")
    
    # Prueba: Factura de un Profesor (Debe aplicar 5% de descuento)
    carrito_carlos = CarritoDeCompras(cliente=profesor_carlos)
    carrito_carlos.agregar_producto(cafe_tostao, 1)
    carrito_carlos.generar_factura()

    # Prueba: Generar factura con carrito vacío (Manejo de errores de UX)
    print("\n[Prueba: Carrito Vacío]")
    carrito_vacio = CarritoDeCompras(cliente=estudiante_ana)
    carrito_vacio.generar_factura()

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