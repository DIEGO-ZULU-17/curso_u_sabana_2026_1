# clientes.py

# Este archivo solo se encarga de la lógica de los usuarios y sus descuentos.

class Cliente:
    def __init__(self, nombre, id_cliente):
        self.nombre = nombre
        self.id_cliente = id_cliente

    def obtener_descuento(self):
        return 0.0 

class Estudiante(Cliente):
    def __init__(self, nombre, id_cliente):
        super().__init__(nombre, id_cliente)
        
    def obtener_descuento(self):
        return 0.10 

class Profesor(Cliente):
    def __init__(self, nombre, id_cliente):
        super().__init__(nombre, id_cliente)
        
    def obtener_descuento(self):
        return 0.05