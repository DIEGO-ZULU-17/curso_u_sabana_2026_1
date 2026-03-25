# proveedores.py
# ==============================================================================
# MÓDULO DE PROVEEDORES Y ABASTECIMIENTO
# ==============================================================================

class Proveedor:
    def __init__(self, nombre_empresa, nit, ciudad):
        # ENCAPSULAMIENTO: Protegemos los datos sensibles de la empresa
        self.__nombre_empresa = nombre_empresa
        self.__nit = str(nit) 
        self.__ciudad = ciudad

    # GETTER
    def get_nit(self):
        return self.__nit
        
    # SETTER CON VALIDACIÓN (Sanity Check)
    def set_nit(self, nuevo_nit):
        nuevo_nit_limpio = str(nuevo_nit).strip()
        
        if len(nuevo_nit_limpio) == 0:
            print("❌ Error: El NIT no puede estar vacío.")
        elif not nuevo_nit_limpio.isdigit():
            print("❌ Error: El NIT debe contener únicamente números.")
        else:
            self.__nit = nuevo_nit_limpio
            print(f"✅ NIT actualizado correctamente a: {self.__nit}")

    # INTERACCIÓN ENTRE OBJETOS: El proveedor modifica a un objeto 'Producto'
    def suministrar_producto(self, producto, cantidad):
        if cantidad <= 0:
            print("❌ Error: La cantidad a suministrar debe ser mayor a 0.")
            return

        # Llamamos al método seguro del objeto 'producto'
        if producto.aumentar_stock(cantidad):
            print(f"📦 PROVEEDOR: Se han añadido {cantidad} unidades de '{producto.nombre}'. Nuevo stock: {producto.get_stock()}")
        else:
            print("❌ Error interno al actualizar el inventario.")