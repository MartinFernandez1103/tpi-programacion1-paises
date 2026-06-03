#Trabajo Practico Integrador - Programacion 1
#Grupo 67 - Integrantes: Fernandez Martin (Comision 4) - Fernandez Facundo (Comision 14)
#D.N.I: 48.400.007 - 45.456.939
#Fecha: 03/06/2026

import os

#FASE 1:PERSISTENCIA DE ARCHIVOS (CSV)
def cargar_paises_csv(nombre_archivo):
    """
    Lee el archivo CSV, valida su formato y devuelve una lista de diccionarios.
    Maneja la excepcion obligatoria si el archivo no existe en el disco.
    """
    lista_paises = []
    
    try:
        with open(nombre_archivo, mode="r", encoding="utf-8") as archivo:
            encabezado = archivo.readline()  # Descartar la linea del encabezado
            
            linea_nro = 1
            for linea in archivo:
                linea_nro += 1
                linea = linea.strip()
                
                if not linea:
                    continue
                
                partes = linea.split(",")
                
                # Validacion de formato: cada linea debe tener exactamente 4 campos
                if len(partes) != 4:
                    print(f"Error de formato en linea {linea_nro}: Se esperaban 4 campos. Linea omitida.")
                    continue
                
                nombre = partes[0].strip()
                poblacion_str = partes[1].strip()
                superficie_str = partes[2].strip()
                continente = partes[3].strip()
                
                # Validacion de campos vacios
                if nombre == "" or poblacion_str == "" or superficie_str == "" or continente == "":
                    print(f"Error en linea {linea_nro}: Hay campos vacios. Linea omitida.")
                    continue
                
                # Validacion y conversion de tipos numericos de manera logica
                if poblacion_str.isdigit() and superficie_str.isdigit():
                    poblacion = int(poblacion_str)
                    superficie = int(superficie_str)
                else:
                    print(f"Error de tipo en linea {linea_nro}: Poblacion o Superficie no son enteros validos. Linea omitida.")
                    continue
                
                # Armamos el diccionario del pais
                pais = {
                    "nombre": nombre,
                    "poblacion": poblacion,
                    "superficie": superficie,
                    "continente": continente
                }
                lista_paises.append(pais)
                
    except FileNotFoundError:
        print(f"Aviso: El archivo '{nombre_archivo}' no fue encontrado. Se iniciara con una lista vacia.")
        # Se genera un archivo base para evitar errores futuros
        with open(nombre_archivo, mode="w", encoding="utf-8") as archivo:
            archivo.write("nombre,poblacion,superficie,continente\n")
            
    return lista_paises


def guardar_paises_csv(nombre_archivo, lista_paises):
    """
    Guarda la lista de diccionarios de paises de vuelta en el archivo CSV.
    """
    try:
        with open(nombre_archivo, mode="w", encoding="utf-8") as archivo:
            archivo.write("nombre,poblacion,superficie,continente\n")
            
            for pais in lista_paises:
                linea = f"{pais['nombre']},{pais['poblacion']},{pais['superficie']},{pais['continente']}\n"
                archivo.write(linea)
        print("Datos guardados exitosamente en el archivo CSV.")
    except Exception as e:
        print(f"Error: Ocurrio un error al intentar guardar los datos: {e}")



#HERRAMIENTAS DE VALIDACION AUXILIARES
def solicitar_entero_positivo(mensaje):
    """
    Solicita un numero entero por consola de manera repetitiva hasta que el ingreso
    sea un numero valido y mayor que cero. Evita campos vacios y textos.
    """
    while True:
        entrada = input(mensaje).strip()
        if entrada == "":
            print("Error: El campo no puede estar vacio. Por favor, ingrese un numero.")
            continue
        
        if entrada.isdigit():
            numero = int(entrada)
            if numero > 0:
                return numero
            else:
                print("Error: El numero debe ser mayor a cero.")
        else:
            print("Error: Entrada invalida. Debe ingresar un numero entero (solo digitos).")



#FASE 2:OPERACIONES CRUD (ALTA, ACTUALIZACION Y BUSQUEDA)
def agregar_pais(lista_paises):
    """
    Solicita los datos de un nuevo pais, valida que no este vacio, 
    controla duplicados y lo añade a la lista en memoria.
    """
    print("\n--- AGREGAR NUEVO PAIS ---")
    
    while True:
        nombre = input("Ingrese el nombre del pais: ").strip()
        if nombre == "":
            print("Error: El nombre no puede estar vacio.")
            continue
        break
        
    # Control de duplicados (insensible a mayusculas/minusculas)
    for pais in lista_paises:
        if pais["nombre"].lower() == nombre.lower():
            print(f"Error: El pais '{pais['nombre']}' ya se encuentra registrado.")
            return

    poblacion = solicitar_entero_positivo("Ingrese la cantidad de poblacion: ")
    superficie = solicitar_entero_positivo("Ingrese la superficie en km2: ")
    
    while True:
        continente = input("Ingrese el continente: ").strip()
        if continente == "":
            print("Error: El continente no puede estar vacio.")
            continue
        break
        
    nuevo_pais = {
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente
    }
    
    lista_paises.append(nuevo_pais)
    print(f"Exito: Pais '{nombre}' agregado exitosamente en memoria.")


def actualizar_pais(lista_paises):
    """
    Busca un pais por nombre exacto y permite modificar su poblacion 
    y superficie en memoria.
    """
    print("\n--- ACTUALIZAR DATOS DE PAIS ---")
    nombre_buscar = input("Ingrese el nombre exacto del pais a actualizar: ").strip()
    
    if nombre_buscar == "":
        print("Error: El nombre no puede estar vacio.")
        return
    
    encontrado = None
    for pais in lista_paises:
        if pais["nombre"].lower() == nombre_buscar.lower():
            encontrado = pais
            break
            
    if encontrado is None:
        print(f"Error: El pais '{nombre_buscar}' no se encuentra registrado en el sistema.")
        return
        
    print(f"Pais encontrado: {encontrado['nombre']} ({encontrado['continente']})")
    print(f"Datos actuales -> Poblacion: {encontrado['poblacion']} | Superficie: {encontrado['superficie']} km2")
    
    nueva_poblacion = solicitar_entero_positivo("Ingrese la NUEVA cantidad de poblacion: ")
    nueva_superficie = solicitar_entero_positivo("Ingrese la NUEVA superficie en km2: ")
    
    encontrado["poblacion"] = nueva_poblacion
    encontrado["superficie"] = nueva_superficie
    
    print(f"Exito: Datos de '{encontrado['nombre']}' actualizados con exito en memoria.")


def buscar_pais(lista_paises):
    """
    Permite buscar paises por una coincidencia parcial o exacta con su nombre.
    """
    print("\n--- BUSCAR PAIS ---")
    termino = input("Ingrese el nombre (o parte del nombre) a buscar: ").strip()
    
    if termino == "":
        print("Error: El termino de busqueda no puede estar vacio.")
        return
        
    coincidencias = []
    for pais in lista_paises:
        if termino.lower() in pais["nombre"].lower():
            coincidencias.append(pais)
            
    if len(coincidencias) == 0:
        print(f"Error: No se encontraron paises que coincidan con '{termino}'.")
        return
        
    print(f"\nSe encontraron {len(coincidencias)} coincidencia(s):")
    print("-" * 75)
    for pais in coincidencias:
        print(f"{pais['nombre']:<15} | Continente: {pais['continente']:<10} | Poblacion: {pais['poblacion']:<12} | Superficie: {pais['superficie']} km2")
    print("-" * 75)



#FASE 3:CONSULTAS AVANZADAS (FILTRADO Y ORDENAMIENTO)
def filtrar_paises(lista_paises):
    """
    Permite filtrar los paises segun continente, rangos de poblacion o superficie.
    Asegura robustez repitiendo el menu de criterios ante ingresos invalidos.
    """
    if len(lista_paises) == 0:
        print("Error: No hay paises registrados para filtrar.")
        return

    print("\n--- MODULO DE FILTRADO ---")
    print("1. Filtrar por Continente")
    print("2. Filtrar por Rango de Poblacion")
    print("3. Filtrar por Rango de Superficie")
    
    while True:
        sub_opcion = input("Seleccione el criterio de filtrado: ").strip()
        if sub_opcion in ["1", "2", "3"]:
            break
        print("Error: Opcion de filtrado invalida. Ingrese un numero del 1 al 3.")

    resultados = []

    if sub_opcion == "1":
        continente_buscar = input("Ingrese el nombre del continente a filtrar: ").strip()
        for pais in lista_paises:
            if pais["continente"].lower() == continente_buscar.lower():
                resultados.append(pais)
                
    elif sub_opcion == "2":
        print("\n--- Filtro por Poblacion ---")
        pob_min = solicitar_entero_positivo("Ingrese la poblacion MINIMA: ")
        while True:
            pob_max = solicitar_entero_positivo("Ingrese la poblacion MAXIMA: ")
            if pob_max >= pob_min:
                break
            print("Error: La poblacion maxima no puede ser menor que la minima.")
            
        for pais in lista_paises:
            if pob_min <= pais["poblacion"] <= pob_max:
                resultados.append(pais)

    elif sub_opcion == "3":
        print("\n--- Filtro por Superficie ---")
        sup_min = solicitar_entero_positivo("Ingrese la superficie MINIMA (km2): ")
        while True:
            sup_max = solicitar_entero_positivo("Ingrese la superficie MAXIMA (km2): ")
            if sup_max >= sup_min:
                break
            print("Error: La superficie maxima no puede ser menor que la minima.")
            
        for pais in lista_paises:
            if sup_min <= pais["superficie"] <= sup_max:
                resultados.append(pais)

    if len(resultados) == 0:
        print("Error: No se encontraron paises que cumplan con el criterio ingresado.")
    else:
        print(f"\nSe encontraron {len(resultados)} pais(es) que coinciden:")
        print("-" * 75)
        for pais in resultados:
            print(f"{pais['nombre']:<15} | Continente: {pais['continente']:<10} | Poblacion: {pais['poblacion']:<12} | Superficie: {pais['superficie']} km2")
        print("-" * 75)


def ordenar_paises(lista_paises):
    """
    Ordena una copia de la lista de paises utilizando el algoritmo Bubble Sort.
    Implementa bucles para garantizar que la seleccion de criterio y sentido sean robustas.
    """
    if len(lista_paises) == 0:
        print("Error: No hay paises registrados para ordenar.")
        return

    print("\n--- MODULO DE ORDENAMIENTO MANUAL ---")
    print("1. Ordenar por Nombre")
    print("2. Ordenar por Cantidad de Poblacion")
    print("3. Ordenar por Superficie (km2)")
    
    # Bucle robusto para el criterio
    while True:
        criterio = input("Seleccione el criterio de ordenamiento: ").strip()
        if criterio == "1":
            campo = "nombre"
            break
        elif criterio == "2":
            campo = "poblacion"
            break
        elif criterio == "3":
            campo = "superficie"
            break
        else:
            print("Error: Opcion de criterio invalida. Seleccione 1, 2 o 3.")

    print("\n¿En que sentido desea ordenar?")
    print("1. Ascendente (Menor a Mayor / A-Z)")
    print("2. Descendente (Mayor a Menor / Z-A)")
    
    # Bucle robusto para el sentido
    while True:
        sentido = input("Seleccione el sentido: ").strip()
        if sentido == "1" or sentido == "2":
            break
        print("Error: Opcion de sentido invalida. Seleccione 1 o 2.")

    # Creamos una copia de la lista para proteger los datos originales
    lista_ordenada = []
    for pais in lista_paises:
        lista_ordenada.append(pais)

    # Algoritmo Bubble Sort Manual
    n = len(lista_ordenada)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            
            val1 = lista_ordenada[j][campo]
            val2 = lista_ordenada[j+1][campo]
            
            if campo == "nombre":
                val1 = val1.lower()
                val2 = val2.lower()
                
            intercambiar = False
            if sentido == "1" and val1 > val2:      # Ascendente
                intercambiar = True
            elif sentido == "2" and val1 < val2:    # Descendente
                intercambiar = True
                
            if intercambiar:
                lista_ordenada[j], lista_ordenada[j+1] = lista_ordenada[j+1], lista_ordenada[j]

    # Mostrar la lista ordenada
    sentido_texto = "ASCENDENTE" if sentido == "1" else "DESCENDENTE"
    print(f"\nLista ordenada por [{campo.upper()}] de forma {sentido_texto}:")
    print("-" * 75)
    for pais in lista_ordenada:
        print(f"{pais['nombre']:<15} | Continente: {pais['continente']:<10} | Poblacion: {pais['poblacion']:<12} | Superficie: {pais['superficie']} km2")
    print("-" * 75)



#FASE 4:INDICADORES Y ESTADISTICAS
def mostrar_estadisticas(lista_paises):
    """
    Calcula de manera estrictamente manual la cantidad de registros, totales,
    promedios y valores maximos/minimos del dataset de paises.
    """
    total_paises = len(lista_paises)
    if total_paises == 0:
        print("Error: No hay paises registrados para procesar estadisticas.")
        return

    print("\n--- MODULO DE ESTADISTICAS GENERALES ---")

    # Inicializacion de acumuladores y extremos
    total_poblacion = 0
    total_superficie = 0
    
    pais_mas_poblado = lista_paises[0]
    pais_menos_poblado = lista_paises[0]
    pais_mayor_superficie = lista_paises[0]
    pais_menor_superficie = lista_paises[0]

    # Recorrido unico para calcular todos los indicadores de forma eficiente
    for pais in lista_paises:
        total_poblacion += pais["poblacion"]
        total_superficie += pais["superficie"]

        # Evaluacion manual de extremos de poblacion
        if pais["poblacion"] > pais_mas_poblado["poblacion"]:
            pais_mas_poblado = pais
        if pais["poblacion"] < pais_menos_poblado["poblacion"]:
            pais_menos_poblado = pais

        # Evaluacion manual de extremos de superficie
        if pais["superficie"] > pais_mayor_superficie["superficie"]:
            pais_mayor_superficie = pais
        if pais["superficie"] < pais_menor_superficie["superficie"]:
            pais_menor_superficie = pais

    # Calculo de promedios generales
    promedio_poblacion = total_poblacion / total_paises
    promedio_superficie = total_superficie / total_paises

    # Impresion formal de resultados por pantalla
    print(f"Cantidad total de paises registrados: {total_paises}")
    print("-" * 60)
    print("INDICADORES DE POBLACION:")
    print(f"  Poblacion total global       : {total_poblacion} habitantes")
    print(f"  Promedio de poblacion x pais : {promedio_poblacion:.2f} habitantes")
    print(f"  Pais mas poblado             : {pais_mas_poblado['nombre']} ({pais_mas_poblado['poblacion']} habitantes)")
    print(f"  Pais menos poblado           : {pais_menos_poblado['nombre']} ({pais_menos_poblado['poblacion']} habitantes)")
    print("-" * 60)
    print("INDICADORES DE SUPERFICIE:")
    print(f"  Superficie total global      : {total_superficie} km2")
    print(f"  Promedio de superficie x pais: {promedio_superficie:.2f} km2")
    print(f"  Pais con mayor superficie    : {pais_mayor_superficie['nombre']} ({pais_mayor_superficie['superficie']} km2)")
    print(f"  Pais con menor superficie    : {pais_menor_superficie['nombre']} ({pais_menor_superficie['superficie']} km2)")
    print("-" * 60)



#BUCLE PRINCIPAL DEL SISTEMA
def ejecutar_sistema():
    """
    Funcion principal que coordina el menu de opciones en consola.
    """
    archivo_datos = "paises.csv"
    paises = cargar_paises_csv(archivo_datos)
    
    while True:
        print("\n========================================")
        print("SISTEMA DE GESTION DE DATOS DE PAISES")
        print("========================================")
        print("1. Agregar un pais")
        print("2. Actualizar Poblacion y Superficie")
        print("3. Buscar un pais por nombre")
        print("4. Filtrar paises")
        print("5. Ordenar paises")
        print("6. Mostrar estadisticas generales")
        print("0. Salir y Guardar Cambios")
        print("========================================")
        
        opcion = input("Seleccione una opcion: ").strip()
        
        if opcion == "1":
            agregar_pais(paises)
        elif opcion == "2":
            actualizar_pais(paises)
        elif opcion == "3":
            buscar_pais(paises)
        elif opcion == "4":
            filtrar_paises(paises)
        elif opcion == "5":
            ordenar_paises(paises)
        elif opcion == "6":
            mostrar_estadisticas(paises)
        elif opcion == "0":
            print("\nGuardando cambios antes de cerrar...")
            guardar_paises_csv(archivo_datos, paises)
            print("Gracias por usar el sistema. Programa finalizado.")
            break
        else:
            print("Error: Opcion invalida. Por favor, seleccione un numero del menu.")

if __name__ == "__main__":
    ejecutar_sistema()