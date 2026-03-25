# ventas.py
# ==============================================================================
# MÓDULO DE VENTAS Y CARRITO DE COMPRAS
# ==============================================================================

class CarritoDeCompras:
    # INTEGRACIÓN: El carrito exige un objeto Cliente al inicializarse
    def __init__(self, cliente):
        self.cliente = cliente 
        self.items =[] 
        self.subtotal = 0.0
        self.total_impuestos = 0.0

    # INTEGRACIÓN: Recibe un objeto Producto
    def agregar_producto(self, producto, cantidad):
        # Intentamos reducir el stock usando el método seguro del producto
        if producto.reducir_stock(cantidad):
            self.items.append({
                "producto": producto, 
                "cantidad": cantidad
            })
            
            # Cálculos financieros leyendo los métodos del objeto
            precio_base = producto.get_precio() * cantidad
            impuesto = producto.calcular_impuesto() * cantidad

            self.subtotal += precio_base
            self.total_impuestos += impuesto
            
            print(f"🛒 VENTAS: Agregado {cantidad}x {producto.nombre} al carrito.")
        else:
            print(f"❌ VENTAS: Stock insuficiente para {producto.nombre}.")

    def generar_factura(self):
        print("\n" + "="*50)
        print("🧾 FACTURA ELECTRÓNICA - CAFETERÍA U. SABANA")
        print(f"👤 Cliente: {self.cliente.nombre} | ID: {self.cliente.id_cliente}")
        print("="*50)
        
        if len(self.items) == 0:
            print("El carrito está vacío.")
        else:
            # Recorremos los objetos guardados
            for item in self.items:
                prod = item["producto"] 
                cant = item["cantidad"]
                total_linea = prod.get_precio() * cant
                print(f"🔸 {prod.nombre.ljust(25)} (x{cant}) : ${total_linea:,.2f}")

            # Lógica financiera
            total_bruto = self.subtotal + self.total_impuestos
            
            # POLIMORFISMO: Python calcula el descuento según el tipo de cliente
            porcentaje_desc = self.cliente.obtener_descuento()
            valor_descuento = total_bruto * porcentaje_desc
            total_pagar = total_bruto - valor_descuento
            
            print("-" * 50)
            print(f"Subtotal:      ${self.subtotal:,.2f} COP")
            print(f"Impuestos:     ${self.total_impuestos:,.2f} COP")
            
            if porcentaje_desc > 0:
                print(f"Descuento ({(porcentaje_desc*100):.0f}%): -${valor_descuento:,.2f} COP")
                
            print(f"TOTAL A PAGAR: ${total_pagar:,.2f} COP")
        print("="*50 + "\n")
