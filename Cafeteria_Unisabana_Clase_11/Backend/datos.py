# datos.py
# ==============================================================================
# MÓDULO DE DATOS INICIALES (SEMILLA)
# ==============================================================================

csv_clientes = """id_cliente,email,telefono,fecha_nacimiento,Nombre_Cliente,Tipo_Cliente
101,diego@correo.com,3001112233.0,1985-05-10,Diego Zuluaga,Profesor
102,sin_correo@cafeteria.com,No Registra,2004-01-15,Ana Gomez,Estudiante
103,carlos@correo.com,3109998877.0,1989-08-20,Carlos Ruiz,Profesor
104,sin_correo@cafeteria.com,3204445566.0,1995-11-30,Maria Lopez,Estudiante
105,luis@correo.com,No Registra,1976-02-14,Luis Perez,Externo
106,sofia@correo.com,3112223344.0,2006-03-22,Sofia Ramirez,Estudiante
107,juan@correo.com,No Registra,2002-07-11,Juan Camilo,Estudiante
108,sin_correo@cafeteria.com,3156667788.0,1996-09-05,Andres Felipe,Externo
109,valeria@correo.com,3009991122.0,1981-12-01,Valeria Morales,Profesor
110,isa@correo.com,No Registra,2005-04-18,Isabella Carranza,Estudiante
111,sin_correo@cafeteria.com,3105556677.0,2003-02-28,Matias Mondragon,Estudiante
112,arianne@correo.com,3201112233.0,1999-06-15,Arianne Amorocho,Externo
113,mariana@correo.com,No Registra,2004-08-08,Mariana Peña,Estudiante
114,nico@correo.com,3114445566.0,1988-10-10,Nicolas Torres,Profesor
115,sin_correo@cafeteria.com,3007778899.0,2001-11-25,Juan Leyton,Estudiante
116,cristian@correo.com,No Registra,1994-01-05,Cristian Bermudez,Externo
117,paula@correo.com,3152223344.0,2006-09-14,Paula Arciniegas,Estudiante
118,sin_correo@cafeteria.com,3206667788.0,2002-05-30,Samuel Lozano,Estudiante
119,gabi@correo.com,No Registra,1984-07-07,Gabriela Ruiz,Profesor
120,lucas@correo.com,3103334455.0,1995-03-12,Lucas Blanco,Externo"""

csv_productos = """id_producto,precio,stock,fecha_vencimiento,Nombre_Producto,Categoria
1,5000,50,2026-12-01,Café Tostao,Bebida
2,1200,0,2027-01-15,Chocolatina Jet,Snack
3,3000,20,2026-05-10,Empanada,Snack
4,2500,0,2026-08-22,Jugo Hit,Bebida
5,1500,100,2026-11-30,Galletas Festival,Snack
6,2000,30,2026-10-10,Agua Cristal,Bebida
7,7500,15,2026-04-20,Sandwich De Pavo,Almuerzo
8,3500,0,2026-04-25,Brownie,Postre
9,3000,40,2026-07-11,Té Helado,Bebida
10,2200,60,2026-09-05,Papas Margarita,Snack
11,2800,0,2026-05-15,Croissant,Panaderia
12,2600,25,2026-06-20,Avena Alpina,Bebida
13,3200,35,2026-07-30,Yogurt Finesse,Bebida
14,4000,0,2026-08-10,Muffin De Arandanos,Postre
15,2500,45,2026-05-05,Dedito De Queso,Snack
16,5500,10,2026-04-18,Ensalada De Frutas,Postre
17,8000,0,2026-04-19,Wrap De Pollo,Almuerzo
18,1000,80,2026-12-20,Gomitas Trululu,Snack
19,1500,100,2026-04-30,Tinto,Bebida
20,2000,0,2026-05-01,Aromatica,Bebida"""

csv_proveedores = """nit_proveedor,contacto,telefono,email,Nombre_Empresa,Ciudad
900111,Carlos Perez,3005551122.0,carlos@coop.com,CoopCafe,Bogota
800222,Departamento de Ventas,3114445566.0,contacto@empresa.com,Insumos Panaderos,Medellin
700333,Ana Rojas,No Registra,ana@prado.com,Lacteos El Prado,Cali
600444,Luis Gomez,3208889900.0,luis@sabana.com,Distribuidora Sabana,Chia
500555,Departamento de Ventas,3157778899.0,contacto@empresa.com,Salsas y Especias,Bogota
400666,Marta Diaz,3001112233.0,marta@empaques.com,Empaques de Carton,Barranquilla
300777,Departamento de Ventas,No Registra,ventas@granos.com,Granos y Cereales,Bucaramanga
200888,Jorge Silva,3109998877.0,contacto@empresa.com,Bebidas Refrescantes,Bogota
100999,Elena Castro,3204445566.0,elena@dulces.com,Dulces y Postres,Medellin
999000,Departamento de Ventas,3112223344.0,frutas@cali.com,Frutas Frescas,Cali"""

csv_ventas = """id_venta,id_cliente,id_producto,nit_proveedor,cantidad,total_venta,fecha_venta
1,101,1,900111,3,15000.0,2026-04-20 02:25:51
2,102,2,800222,5,6000.0,2026-04-20 02:25:51
4,104,4,700333,1,2500.0,2026-04-20 02:25:51
5,105,1,900111,4,20000.0,2026-04-20 02:25:51
6,101,1,900111,2,10000.0,2026-04-20 02:32:15
7,102,2,800222,5,6000.0,2026-04-20 02:32:15
8,103,3,900111,3,9000.0,2026-04-20 02:32:15
9,104,4,700333,1,2500.0,2026-04-20 02:32:15
10,105,1,900111,4,20000.0,2026-04-20 02:32:15
11,101,1,900111,2,10000.0,2026-04-22 21:17:00
12,102,2,800222,5,6000.0,2026-04-22 21:17:00
13,103,3,900111,3,9000.0,2026-04-22 21:17:00
14,104,4,700333,1,2500.0,2026-04-22 21:17:00
15,105,1,900111,4,20000.0,2026-04-22 21:17:00
16,101,1,900111,2,10000.0,2026-04-24 01:27:19
17,102,2,800222,5,6000.0,2026-04-24 01:27:19
18,103,3,900111,3,9000.0,2026-04-24 01:27:19
19,104,4,700333,1,2500.0,2026-04-24 01:27:19
20,105,1,900111,4,20000.0,2026-04-24 01:27:19"""