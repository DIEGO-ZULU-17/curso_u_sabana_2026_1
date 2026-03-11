# productos.py

# Este archivo solo se encarga de saber qué es un producto y cómo calcular sus impuestos.

class Producto:
    def __init__(self, nombre, precio, stock):
        self.nombre = nombre
        self.__precio = precio 
        self.__stock = stock   
        
    def get_precio(self):
        return self.__precio
        
    def get_stock(self):
        return self.__stock
        
    def reducir_stock(self, cantidad):
        if cantidad > 0 and cantidad <= self.__stock:
            self.__stock -= cantidad
            return True
        return False

class Bebida(Producto):
    def __init__(self, nombre, precio, stock, tamano):
        super().__init__(nombre, precio, stock) 
        self.tamano = tamano
        
    def calcular_impuesto(self):
        return self.get_precio() * 0.08 

class Snack(Producto):
    def __init__(self, nombre, precio, stock, gramos):
        super().__init__(nombre, precio, stock)
        self.gramos = gramos
        
    def calcular_impuesto(self):
        return self.get_precio() * 0.19