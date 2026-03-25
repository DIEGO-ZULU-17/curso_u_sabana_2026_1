# productos.py
# ==============================================================================
# MÓDULO DE INVENTARIO Y PRODUCTOS
# ==============================================================================

class Producto:
    def __init__(self, nombre, precio, stock):
        self.nombre = nombre
        # ENCAPSULAMIENTO: Atributos privados para evitar modificaciones directas
        self.__precio = precio 
        self.__stock = stock   
        
    # GETTERS: Métodos seguros para leer datos privados
    def get_precio(self):
        return self.__precio
        
    def get_stock(self):
        return self.__stock
        
    # SETTERS: Métodos seguros para modificar el stock (Ventas)
    def reducir_stock(self, cantidad):
        if cantidad > 0 and cantidad <= self.__stock:
            self.__stock -= cantidad
            return True
        return False

    # SETTERS: Métodos seguros para modificar el stock (Proveedores)
    def aumentar_stock(self, cantidad):
        if cantidad > 0:
            self.__stock += cantidad
            return True
        return False

# HERENCIA: Bebida hereda de Producto
class Bebida(Producto):
    def __init__(self, nombre, precio, stock, tamano):
        super().__init__(nombre, precio, stock) 
        self.tamano = tamano
        
    # POLIMORFISMO: Impoconsumo del 8% para bebidas preparadas
    def calcular_impuesto(self):
        return self.get_precio() * 0.08 

# HERENCIA: Snack hereda de Producto
class Snack(Producto):
    def __init__(self, nombre, precio, stock, gramos):
        super().__init__(nombre, precio, stock)
        self.gramos = gramos
        
    # POLIMORFISMO: IVA del 19% para snacks procesados
    def calcular_impuesto(self):
        return self.get_precio() * 0.19