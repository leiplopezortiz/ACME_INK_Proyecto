import time
from datetime import datetime
import json
import csv

productos = {} #Diccionario para guardar los productos globales
inventario_general = { #Diccionario en donde se encuentran las bodegas respectivas y en donde guardar los productos
    "bodega_norte":{},
    "bodega_centro":{},
    "bodega_oriente":{}
}

def leer_archivo_productos(): #Lee el archivo JSON de productos
    with open("productos.json") as file:
        productos = json.load(file)
    return productos
def leer_archivo_inventario(): #Lee el archivo JSON de pinventario
    with open("inventario.json") as file:
        inventario = json.load(file)
    return inventario
def agregar_data_archivo_productos(producto): #Agrega al archivo JSON de productos y recibe el parámetro de producto
    with open("productos.json", 'w') as outfile:
        json.dump(producto,outfile,indent=4)
def agregar_data_archivo_inventario(inventario): #Agrega al archivo JSON de inventario y recibe el parámetro de inventario
    with open("inventario.json", 'w') as outfile:
        json.dump(inventario,outfile,indent=4)

def menu(): #Función menú
    print("==================================================")
    print("=================== Bienvenido ===================")
    print("=== Estas son las acciones que puede realizar: ===")
    print("==================================================")
    print("1. Registrar producto")
    print("2. Ingresar producto al inventario")
    print("3. Retirar prodcto")
    print("4. Buscar producto")
    print("5. Historial de producto")
    print("6. Reporte")
    print("0. Salir")
    print("==================================================")

def registrar_producto(): #Función para registrar el producto
    print("")
    print("   RECUERDE QUE SI HAY PRODUCTOS CON EL MISMO NOMBRE ")
    print("DEBE REGISTRARSE CON DIFERENTE CÓDIGO Y ESPECIFICACIÓN CLARA")
    print("")
    codigo=input("Ingrese el código del producto:\n") #Pide el código
    nombre=input("Ingrese el nombre del producto:\n") #Pide el nombre del producto
    especificacion=input("Ingrese especificaciones del producto:\n") #Pide una especificación o detalle del producto (ej. codigo:1, nombre: lulo, especificación: lulo importado)
    proveedor=input("Ingrese el proveedor del producto:\n") #Pide el proveedor
    productos_json = leer_archivo_productos() #Trae la función de leer JSON de productos
    if codigo not in productos_json: #si código no está en el JSON entra acá
        produ={ #Diccionario que almacena la información solicitada previamente
                "nombre":nombre,
                "especificacion": especificacion,
                "proveedor": proveedor,
                "fecha": [datetime.now().strftime("%d/%m/%y, %H:%M:%S")]
        }
        print(f"El producto a ingresar es codigo:  {codigo}| {nombre}| {especificacion}| {proveedor}| creado el: {datetime.now().strftime("%d/%m/%y, %H:%M:%S")}") #Muestra lo que el usuario ingresó
        confirmacion=input("¿El articulo creado es correcto? s/n:\n") #Solicita confirmación para agregarlo correctamente
        if confirmacion=="s": #si la confirmación es afirmativa
            print("Agregando producto...")
            time.sleep(0.5)
            productos[codigo] = produ 
            agregar_data_archivo_productos(productos) #Agrega la informacion
            print("Poducto agregado correctamente")
        elif confirmacion == "n": #si la confirmación es negativa 
            print("Lo sentimos, intentalo de nuevo.")
            time.sleep(0.5)
            print("volviendo al menú principal")
        else:
            print("Debe escribir (s) o (n)") #ayuda a que sea solamene "s" o "n"
            time.sleep(0.5)
            print("volviendo al menú principal")
    else:
        print("Ya existe el producto") #si código está en el JSON
        
def ingreso_productos(): #Función ingresar producto
    codigo=input("Ingrese el código del producto\n") #Pide el código
    productos_json = leer_archivo_productos() #Trae la función de leer JSON de productos
    if codigo in productos_json: #si código está en el JSON entra acá
        stock=int(input("Ingrese la cantidad del producto que desee agregar\n")) #Solicita el stock
        if stock>=0: #Valida que el valor del stock sea mayor o igual que 0
            motivo = input('Escriba el motivo\n') #Solicita descripción o motivo por el cual ingresa el valor
            print("Nuestras bodegas son\n")
            print("- Bodega norte")
            print("- Bodega centro")
            print("- Bodega oriente\n")
            try: #Captura el error de escribir mal el nombre de la bodega
                bodega=input("ingrese la bodega que desea de la siguiente manera (bodega_norte, bodega_centro, bodega_oriente)\n")
                inventario = leer_archivo_inventario() #Trae la función de leer JSON de inventario
                if codigo in inventario[bodega]: #si codigo esta en inventario en la llave de bodega
                    inventario[bodega][codigo]['stock'] += stock #entra a inventario en la llave de bodega, en la llave de código y la llave de stock y se suma con el valor que estaba anteriormente
                    inventario[bodega][codigo]['Historial'].append({'mensaje': f'Entrada de producto, cantidad: {stock} por concepto de: {motivo}, Fecha: {datetime.now().strftime("%d/%m/%y, %H:%M:%S")}'}) #se agrega al historial
                    agregar_data_archivo_inventario(inventario) #Agrega la informacion
                    print("En proceso...")
                    time.sleep(0.5)
                    print("Stock agregado correctamente")
                else: #si codigo no esta en inventario en la llave de bodega
                    bodega_producto={ #Diccionario que almacena la información en la bodega ingresada
                        "stock":stock,
                        "producto":productos_json[codigo],
                        "Historial":[],
                        "Detalle": motivo
                    }
                    bodega_producto["Historial"].append({'mensaje': f'Entrada de producto, codigo: {codigo}, nombre: {productos_json[codigo]['nombre']}, cantidad {stock}, por concepto de: {motivo}, Fecha: {datetime.now().strftime("%d/%m/%y, %H:%M:%S")}'}) #se agrega al historial
                    inventario[bodega][codigo] = bodega_producto 
                    agregar_data_archivo_inventario(inventario) #Agrega la informacion
                    print("En proceso...")
                    time.sleep(0.5)
                    print("Stock agregado correctamente")
            except KeyError: #Recoge el error por escribir mal la bodega
                    print("Ups! Ingreso errado de la bodega, revisa la escritura e intentalo de nuevo")
                    time.sleep(0.5)
                    print("Volviendo al menú principal...")
        else:
            print("Lo sentimos, no se puede agregar un valor menor a 0") #si el valor de stock es menor a 0
            time.sleep(0.5)
            print("Volviendo al menú principal...")
    else:
        print("Codigo no encontrado") #si no encuentra el código
        time.sleep(0.5)
        print("Regresando al menú principal...")

def retirar_producto(): #Función retirar producto
    codigo=input("Ingrese el código del producto\n")
    productos_json = leer_archivo_productos() #Trae la función de leer JSON de productos
    if codigo in productos_json:
        motivo = input('Escriba el motivo\n')
        print("Estas son las bodegas disponibles")
        print("- Bodega norte")
        print("- Bodega centro")
        print("- Bodega oriente\n")
        try:
            bodega=input("ingrese la bodega (bodega_norte, bodega_centro, bodega_oriente)\n")
            inventario = leer_archivo_inventario() #Trae la función de leer JSON de inventario
            if codigo in inventario[bodega]: #si código está en el JSON
                retiro=int(input("Ingrese el valor a retirar\n")) #Solicita valor de retiro
                if retiro>=0: #Valida que el valor del retiro sea mayor o igual que 0
                    if retiro<=inventario[bodega][codigo]['stock']: #valida que el valor del retiro sea menor que lo que hay en stock
                        inventario[bodega][codigo]['stock'] -= retiro #entra a inventario en la llave de bodega, en la llave de código y la llave de stock y se suma con el valor que estaba anteriormente
                        inventario[bodega][codigo]['Historial'].append({'mensaje': f'Salida de producto, cantidad: {retiro}, por concepto de: {motivo}, Fecha: {datetime.now().strftime("%d/%m/%y, %H:%M:%S")}'}) #agrega a historial
                        agregar_data_archivo_inventario(inventario) #Agrega la información
                        print("En proceso...")
                        time.sleep(0.5)
                        print("Retiro de bodega exitoso")
                    else:
                        time.sleep(0.5)
                        print("Lo sentimos, stock insuficiente, verifique e intente de nuevo")
                        inventario[bodega][codigo]['Historial'].append({'mensaje':f'se intenta retirar producto por {motivo}, cantidad: {retiro} en la fecha {datetime.now().strftime("%d/%m/%y, %H:%M:%S")}'}) #Se agrega el movimiento pero no se altera el stock
                else:
                        print("No puede ingresar valores negativos") #si ingresn valores menores a 0
                        time.sleep(0.5)
                        print("Volviendo al menú principal...")
        except KeyError:
            print("Ups! Ingreso errado de la bodega, revisa la escritura e intentalo de nuevo") #si escriben mal la bodega
            time.sleep(0.5)
            print("Volviendo al menú principal...")
    else:
        print("No existe el producto")
        time.sleep(0.5)
        print("Volviendo al menú principal...")
        
def buscar_producto(): #Función buscar producto
    codigo=input("Ingrese el código del producto que desea buscar\n") #solicita código para buscarlo
    productos_json = leer_archivo_productos() #Trae la función de leer JSON de productos
    inventario = leer_archivo_inventario() #Trae la función de leer JSON de inventario
    if codigo in productos_json:
        if codigo in inventario["bodega_norte"] != {}: #Si codigo en el diccionario inventario en la llave de bodega norte NO esta vacio
            print(inventario["bodega_norte"][codigo]) #imprime el inventario en la llave bodega_norte en la llave código
        else:
            print("no hay producto en la bodega norte") #Si está vacío se imprime
        if codigo in inventario["bodega_centro"] != {} :  #Si codigo en el diccionario inventario en la llave de bodega centro NO esta vacio
            print(inventario["bodega_centro"][codigo]) #imprime el inventario en la llave bodega_centro en la llave código
        else:
            print("no hay producto en la bodega centro")#Si está vacío se imprime
        if codigo in inventario["bodega_oriente"] != {} :  #Si codigo en el diccionario inventario en la llave de bodega oriente NO esta vacio
            print(inventario["bodega_oriente"][codigo]) #imprime el inventario en la llave bodega_oriente en la llave código
        else:
            print("no hay producto en la bodega oriente")#Si está vacío se imprime
            
    else:
        time.sleep(0.5)
        print("Lo sentimos, código no encontrado") #si el producto no existe
        time.sleep(0.5)
        print("Volviendo al menú principal...")

def historial_producto(): #Función historial de producto
    codigo=input("Ingresa el código del producto que desea conocer\n")
    productos_json = leer_archivo_productos() #Trae la función de leer JSON de productos
    if codigo in productos_json:
        print("Estas son las bodegas disponibles\n")
        print("- Bodega norte")
        print("- Bodega centro")
        print("- Bodega oriente\n")
        try: #Recoge el error de mala escritura de bodega
            bodega=input("ingrese la bodega (bodega_norte, bodega_centro, bodega_oriente)\n")
            inventario = leer_archivo_inventario() #Trae la función de leer JSON de inventario
            if codigo in inventario[bodega]: #si codigo está en inventario en la llave de bodega(segun la que se agregara anteriormente)
                print(inventario[bodega][codigo]['Historial']) #Imprime inventario en la llave de bodega en la llave de código en la llave de historial
            else:
                time.sleep(0.5)
                print('producto no esta en bodega, verifica e intenta de nuevo') #si el producto no se agrego en bodega
                time.sleep(0.5)
                print("Volviendo al menú principal...")
        except KeyError:
            print("Ups! Ingreso errado de la bodega, revisa la escritura e intentalo de nuevo")#error de mala escritura de bodega
            time.sleep(0.5)
            print("Volviendo al menú principal...")
    else:
        time.sleep(0.5)
        print("producto no existe, verifica e intenta de nuevo") #si el producto no fue registrado en la opcion 1
        time.sleep(0.5)
        print("Volviendo al menú principal...")

def reporte(): #Función para el reporte
    suma_total = 0 #Variables iniciadas en 0 para poder realizar la suma correspondiente
    suma_norte = 0
    suma_centro = 0
    suma_oriente = 0
    inventario = leer_archivo_inventario() #Trae la función de leer JSON de inventario
    for codigo in inventario["bodega_norte"]: #para codigo en diccionario inventari en llave bodega norte
        if inventario["bodega_norte"] != {}: #si inventario en la llave bodega norte NO está vacio
            suma_norte +=  inventario["bodega_norte"][codigo]['stock'] #Suma diccionario inventario en la llave bodega norte en la llave código y en la llave stock para poder sumar el stock existente
    for codigo in inventario["bodega_centro"]: #para codigo en diccionario inventari en llave bodega centro
        if inventario["bodega_centro"] != {} : #si inventario en la llave bodega centro NO está vacio
            suma_centro += inventario["bodega_centro"][codigo]['stock'] #Suma diccionario inventario en la llave bodega centro en la llave código y en la llave stock para poder sumar el stock existente
    for codigo in inventario["bodega_oriente"]: #para codigo en diccionario inventari en llave bodega centro
        if inventario["bodega_oriente"] != {} : #si inventario en la llave bodega centro NO está vacio
            suma_oriente += inventario["bodega_oriente"][codigo]['stock'] #Suma diccionario inventario en la llave bodega oriente en la llave código y en la llave stock para poder sumar el stock existente
    suma_total = suma_norte + suma_centro + suma_oriente #Suma el total de cada bodega para el valor total de todas las bodegas
    print(f'La bodega norte cuenta con una cantidad total de productos de {suma_norte}')
    print(f'La bodega centro cuenta con una cantidad total de productos de {suma_centro}')
    print(f'La bodega oriente cuenta con una cantidad total de productos de {suma_oriente}')
    print(f'La suma total de todo el inventario general de productos es de  {suma_total}')
    guardar=input("¿Desea guardar este reporte? s/n\n") #Pregunta si quiere guardar el reporte
    if guardar=="s": #Si es afirmativo
        reporte_csv = 'reporte.csv' #Definimos el archivo csv
        with open(reporte_csv, mode='w' , newline="")as archivo: #Se abre o se crea, según sea el caso
            escrito = csv.writer(archivo) #Para escribir en el archivo
            escrito.writerow(['bodega', 'stock']) #Lo que va a entrar (2 objetos)
            escrito.writerow([inventario["bodega_norte"], suma_norte]) #Información de la bodega (todo lo que contiene y la sumatoria total)
            escrito.writerow([inventario["bodega_centro"], suma_centro]) #Información de la bodega (todo lo que contiene y la sumatoria total)
            escrito.writerow([inventario["bodega_oriente"], suma_oriente]) #Información de la bodega (todo lo que contiene y la sumatoria total)
            escrito.writerow(["El stock total es: " + str(suma_total)]) #El total de todas las bodegas
        print("Archivo guardado correctamente, volviendo al menú principal...")
        time.sleep(0.5)
    elif guardar=="n": #Si es negativo no guarda
        print("Archivo no guardado")
        time.sleep(0.5)
        print("Volviendo al menú principal...")
        
        
while True: #Bucle de regresar o imprimir el menú
    print(menu()) #función menú
    try:
        opc=int(input("Ingrese la opción que desea:\n")) #solicita el número de la opción
        #Según la opción se llama una función
        if opc ==1:
            registrar_producto()
            time.sleep(1) #Tiempo de espera para el usuario
        elif opc ==2:
            ingreso_productos()
            time.sleep(1)
        elif opc ==3:
            retirar_producto()
            time.sleep(1)
        elif opc ==4:
            buscar_producto()
            time.sleep(1)
        elif opc ==5:
            historial_producto()
            time.sleep(1)
        elif opc ==6:
            reporte()
            time.sleep(1)
        elif opc ==0:
            print("Cerrando programa, Gracias")
            time.sleep(1.5)
            agregar_data_archivo_productos({
                "nombre": "",
                "especificacion": "",
                "proveedor": "",
                "fecha": []})
            agregar_data_archivo_inventario({
                "bodega_norte": {},
                "bodega_centro":{},
                "bodega_oriente": {}
            })
            #Cuando se oprime 0 se reinicia la información de los JSON de lo contrario al verrar e iniciar nuevamente el valor de lo que contienen será reemplazado en caso de que se escriba el mismo código
            print("regresa pronto")
            break #Termina el programa
        else:
            print("Ups! La opción no se encuentra en nuestro menú, por favor intentalo de nuevo") #Si agrega un número distinto a las opciones del 0 al 6
            time.sleep(1)
    except ValueError:
        print("ups! ha ocurrido un error, asegurate que la opción sea un número valido") #Recoge el error en caso de ingresar un dato incorrecto en la opcion
        time.sleep(1)