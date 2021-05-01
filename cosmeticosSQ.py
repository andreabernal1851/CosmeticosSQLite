import sys
import sqlite3
from sqlite3 import Error
import time
import datetime
import os

try:
    listaproductos = []
    listaprecio = []
    r = 1
    folio = 0
    while True:
        print("*****COSMETICOS*****")
        print("1. REGISTRAR VENTA")
        print("2. CONSULTAR VENTA")
        print("3. REPORTE POR FECHA")
        print("4. SALIR")
        op = int(input("¿Que opcion desea consultar? >>> "))
        if op == 1:
            print("*****REGISTRAR VENTA*****")
            print("*" * 50)
            while r == 1:
                db = "CosmeticosSQLite.db"
                ex = os.path.isfile(db)
                if ex:
                    if folio == 0:
                        with sqlite3.connect("CosmeticosSQLite.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
                            c = conn.cursor()
                            c.execute("SELECT MAX(folio) FROM ventas;")
                            registros = c.fetchall()
                        n = registros[0][0]
                        folio = n+1
                else:
                    folio = 1
                nombre = input("Ingrese el nombre del producto >>> ")
                cantidad = int(input("Ingrese la cantidad >>> "))
                precio = int(input("Ingrese el precio >>> "))
                precio_total = cantidad * precio
                precio_total = int(precio_total)
                fecha = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
                fechalista = (time.strftime("%Y-%m-%d"))

                datos = [[(folio), (nombre), (cantidad), (precio), (precio_total), (fechalista)]]
                listaproductos.append(datos)
                listaprecio.append(precio_total)
                with sqlite3.connect("CosmeticosSQLite.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
                    c = conn.cursor()
                    c.execute("CREATE TABLE IF NOT EXISTS ventas (folio INTEGER NOT NULL, nombre TEXT NOT NULL, cantidad INTEGER NOT NULL, precio INTEGER NOT NULL, precio_total INTEGER NOT NULL, fecha timestamp);")
                    valores = {"folio":folio, "nombre":nombre, "cantidad": cantidad, "precio":precio, "precio_total":precio_total, "fecha":fecha}
                    c.execute("INSERT INTO ventas VALUES(:folio,:nombre,:cantidad,:precio,:precio_total,:fecha)", valores)
                conn.close()
                print("¿Desea registrar otro producto?")
                print("1. SI\t2.NO")
                r = int(input())
            print(f"El numero de folio es >>> {folio}")
            for lista_primer_nivel in listaproductos:
                for elemento in lista_primer_nivel:
                    print(f"{elemento}")
            Suma = 0
            for i in listaprecio:
                Suma = Suma + i
            print(f"El total a pagar es {Suma}")
        if op == 2:
            print("*****CONSULTAR VENTA*****")
            print("*" * 50)
            foliob = int(input("Ingresa el folio >>> "))
            with sqlite3.connect("CosmeticosSQLite.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
                c = conn.cursor()
                valores = {"folio":foliob}
                c.execute("SELECT * FROM ventas WHERE folio = :folio", valores)
                registros = c.fetchall()
            conn.close()
        
            for registro in registros:
                print(registro)
               
        if op == 3:
            print("*****REPORTE POR FECHAS*****")
            print("*" * 50)
            fecha_consultar = input("Ingresa la fecha (AAAA-MM-DD): ")
            fecha_consultar = datetime.datetime.strptime(fecha_consultar, "%Y-%m-%d").date()
            with sqlite3.connect("CosmeticosSQLite.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
                c = conn.cursor()
                criterios = {"fecha":fecha_consultar}
                c.execute("SELECT * FROM ventas WHERE DATE(fecha) = :fecha;", criterios)
                registros = c.fetchall()
            conn.close()
            for registro in registros:
                print(registro)

        if op == 4:
            break
except Error as e:
    print (e)
    
finally:
    conn.close()