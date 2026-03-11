# ventas.py

# Este archivo maneja la lógica de negocio (el carrito y la factura).

class CarritoDeCompras:
    def __init__(self, cliente):
        self.cliente = cliente 
        self.items =[] 
        self.subtotal = 0.0
        self.total_impuestos = 0.0

    def agregar_producto(self, producto, cantidad):
        if producto.reducir_stock(cantidad):
            self.items.append({
                "producto": producto, 
                "cantidad": cantidad
            })
            
            precio_base = producto.get_precio() * cantidad
            impuesto = producto.calcular_impuesto() * cantidad

            self.subtotal += precio_base
            self.total_impuestos += impuesto
            
            print(f"✅ Agregado: {cantidad}x {producto.nombre} al carrito.")
        else:
            print(f"❌ Error: Stock insuficiente para {producto.nombre}.")

    def generar_factura(self):
        print("\n" + "="*45)
        print("🧾 FACTURA ELECTRÓNICA - CAFETERÍA U. SABANA")
        print(f"👤 Cliente: {self.cliente.nombre} | ID: {self.cliente.id_cliente}")
        print("="*45)
        
        if len(self.items) == 0:
            print("El carrito está vacío.")
        else:
            for item in self.items:
                prod = item["producto"] 
                cant = item["cantidad"]
                total_linea = prod.get_precio() * cant
                print(f"🛒 {prod.nombre.ljust(20)} (x{cant}) : ${total_linea:,.2f}")

            total_bruto = self.subtotal + self.total_impuestos
            porcentaje_desc = self.cliente.obtener_descuento()
            valor_descuento = total_bruto * porcentaje_desc
            total_pagar = total_bruto - valor_descuento
            
            print("-" * 45)
            print(f"Subtotal:      ${self.subtotal:,.2f} COP")
            print(f"Impuestos:     ${self.total_impuestos:,.2f} COP")
            
            if porcentaje_desc > 0:
                print(f"Descuento ({(porcentaje_desc*100):.0f}%): -${valor_descuento:,.2f} COP")
                
            print(f"TOTAL A PAGAR: ${total_pagar:,.2f} COP")
        print("="*45 + "\n")