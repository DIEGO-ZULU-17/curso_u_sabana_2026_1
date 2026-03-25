# clientes.py
# ==============================================================================
# MÓDULO DE CLIENTES Y DESCUENTOS
# ==============================================================================

class Cliente:
    def __init__(self, nombre, id_cliente):
        self.nombre = nombre
        self.id_cliente = id_cliente

    # Método base que será sobreescrito (Polimorfismo)
    def obtener_descuento(self):
        return 0.0 # 0% de descuento por defecto para clientes genéricos

class Estudiante(Cliente):
    def __init__(self, nombre, id_cliente):
        super().__init__(nombre, id_cliente)
        
    # POLIMORFISMO: 10% de descuento
    def obtener_descuento(self):
        return 0.10 

class Profesor(Cliente):
    def __init__(self, nombre, id_cliente):
        super().__init__(nombre, id_cliente)
        
    # POLIMORFISMO: 5% de descuento
    def obtener_descuento(self):
        return 0.05