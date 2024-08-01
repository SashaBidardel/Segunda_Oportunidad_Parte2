import mysql.connector
from config.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
from salesforce.salesforce_operations import query_productos_usados, query_segunda_oportunidad
import pandas as pd
import logging
from decimal import Decimal, ROUND_HALF_UP

# Configurar el logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def connec_mysql():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        print("Conexión a MySQL exitosa")
        return conn
    except mysql.connector.Error as e:
        print(f"Error al conectar con MySQL: {e}")
        return None

def resetear_columnas_usuarios(conn):
    try:
        with conn.cursor() as cursor:
            sql = """
                UPDATE usuarios 
                SET beneficios_anio = 0.00, 
                    cantidad_a_pagar = 0.00, 
                    impuesto_transmisiones = 0.00,
                    total_compras = 0.00
            """
            cursor.execute(sql)
        conn.commit()
        print("Columnas reseteadas en MySQL")
    except mysql.connector.Error as e:
        print(f"Error al resetear columnas en MySQL: {e}")

def procesar_productos_usados(sf, year):
    try:
        productos_usados = query_productos_usados(sf, year)
        
        registros_actualizar = []
        beneficios_vendedor = {}
        impuestos_comprador = {}
        total_compras_comprador = {}

        for producto in productos_usados:
            precio_compra = round(float(producto['Precio_Compra__c']), 2)
            precio_venta = round(float(producto['Precio_Venta__c']), 2)
            beneficio = round(precio_venta - precio_compra, 2)
            logger.info(f"Precio de venta: {precio_venta}, 4% impuesto: {round(precio_venta * 0.04, 2)}")
            vendedor_info = query_segunda_oportunidad(sf, producto['Segunda_Oportunidad__c'])
            comprador_info = query_segunda_oportunidad(sf, producto['Comprador__c']) if producto.get('Comprador__c') else None
            
            if vendedor_info and len(vendedor_info) > 0:
                vendedor_dni = vendedor_info[0]['DNI__c']
                vendedor_nombre = vendedor_info[0]['Name']
                vendedor_email = vendedor_info[0]['Email__c']
            else:
                print(f"Error: No se encontró información del vendedor para el producto {producto['Name']}")
                continue
            
            if comprador_info and len(comprador_info) > 0:
                comprador_dni = comprador_info[0]['DNI__c']
                comprador_nombre = comprador_info[0]['Name']
                comprador_email = comprador_info[0]['Email__c']
            else:
                comprador_dni = None
            
            # Calcular beneficios para el vendedor
            if beneficio > 0:
                if vendedor_dni in beneficios_vendedor:
                    beneficios_vendedor[vendedor_dni]['beneficio'] += beneficio
                else:
                    beneficios_vendedor[vendedor_dni] = {
                        'nombre': vendedor_nombre,
                        'email': vendedor_email,
                        'beneficio': beneficio
                    }
            
            # Calcular impuestos para el comprador
            if comprador_dni:
                impuesto_transmisiones = calcular_impuesto_transmisiones_prueba(precio_venta) 
                if comprador_dni in impuestos_comprador:
                    impuestos_comprador[comprador_dni]['impuesto'] += impuesto_transmisiones
                    total_compras_comprador[comprador_dni] += precio_venta
                else:
                    impuestos_comprador[comprador_dni] = {
                        'nombre': comprador_nombre,
                        'email': comprador_email,
                        'impuesto': impuesto_transmisiones
                    }
                    total_compras_comprador[comprador_dni] = precio_venta
        
        # Preparar registros para actualizar
        for dni, data in beneficios_vendedor.items():
            registros_actualizar.append({
                'DNI__c': dni,
                'Name': data['nombre'],
                'Email__c': data['email'],
                'Beneficio': round(data['beneficio'], 2),
                'Impuesto_Transmisiones': 0.00,
                'Cantidad_A_Pagar': round(data['beneficio'] * 0.2, 2),
                'Total_Compras': 0.00
            })
        
        for dni, data in impuestos_comprador.items():
            registros_actualizar.append({
                'DNI__c': dni,
                'Name': data['nombre'],
                'Email__c': data['email'],
                'Beneficio': 0.00,
                'Impuesto_Transmisiones': round(data['impuesto'], 2),
                'Cantidad_A_Pagar': 0.00,
                'Total_Compras': total_compras_comprador[dni]
            })
          
        return registros_actualizar
    
    except Exception as e:
        print(f"Error durante el procesamiento de productos usados: {e}")
        return []

def insert_update_usuarios(conn, registros):
    try:
        with conn.cursor() as cursor:
            for registro in registros:
                nombre = registro['Name']
                email = registro['Email__c']
                dni = registro['DNI__c']
                beneficio = round(float(registro['Beneficio']), 2)
                impuesto_transmisiones = round(float(registro['Impuesto_Transmisiones']), 2)
                cantidad_a_pagar = round(float(registro['Cantidad_A_Pagar']), 2)
                total_compras = round(float(registro['Total_Compras']), 2)
                
                # Verificar si el DNI existe en la base de datos
                sql_select = "SELECT * FROM usuarios WHERE dni_hash = %s"
                cursor.execute(sql_select, (dni,))
                result = cursor.fetchone()
                
                if result:
                    # Actualizar registro existente
                    sql_update = """
                        UPDATE usuarios 
                        SET nombre = %s,
                            email = %s,
                            beneficios_anio = beneficios_anio + %s, 
                            impuesto_transmisiones = impuesto_transmisiones + %s,
                            cantidad_a_pagar = cantidad_a_pagar + %s,
                            total_compras = total_compras + %s
                        WHERE dni_hash = %s
                    """
                    cursor.execute(sql_update, (nombre, email, beneficio, impuesto_transmisiones, cantidad_a_pagar, total_compras, dni))
                else:
                    # Insertar nuevo registro
                    sql_insert = """
                        INSERT INTO usuarios (dni_hash, nombre, email, beneficios_anio, impuesto_transmisiones, cantidad_a_pagar, total_compras) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql_insert, (dni, nombre, email, beneficio, impuesto_transmisiones, cantidad_a_pagar, total_compras))
            
            conn.commit()
            print("Inserción o actualización de Usuarios en MySQL completada")
    except mysql.connector.Error as e:
        print(f"Error al insertar o actualizar Usuarios en MySQL: {e}")

def calcular_cuotas_pagar(conn):
    try:
        with conn.cursor() as cursor:
            # Calcular el 20% de beneficios_anio y actualizar cantidad_a_pagar
            sql_update = """
                UPDATE usuarios
                SET cantidad_a_pagar = ROUND(beneficios_anio * 0.2, 2)
            """
            cursor.execute(sql_update)
        
        conn.commit()
        print("Cuota a pagar calculada y actualizada en MySQL")
    except mysql.connector.Error as e:
        print(f"Error al calcular cuota a pagar en MySQL: {e}")

def calcular_impuesto_transmisiones(conn):
    try:
        with conn.cursor() as cursor:
            # El cálculo del impuesto ya se hace en procesar_productos_usados
            pass
        
        conn.commit()
        print("Impuesto de transmisiones calculado y actualizado en MySQL")
    except mysql.connector.Error as e:
        print(f"Error al calcular impuesto de transmisiones en MySQL: {e}")

def eliminar_registros_cero_beneficio(conn):
    try:
        with conn.cursor() as cursor:
            # Eliminar registros donde beneficios_anio, impuesto_transmisiones y total_compras sean cero
            sql_delete = "DELETE FROM usuarios WHERE beneficios_anio = 0.00 AND impuesto_transmisiones = 0.00 AND total_compras = 0.00"
            cursor.execute(sql_delete)
        
        conn.commit()
        print("Registros con beneficios cero, impuesto de transmisiones cero y total de compras cero eliminados en MySQL")
    except mysql.connector.Error as e:
        print(f"Error al eliminar registros con beneficios cero en MySQL: {e}")

def calcular_impuesto_transmisiones_prueba(precio_venta):
    return round(precio_venta * 0.04, 2)

def prueba_calculo_impuesto_transmisiones():
    precios_venta = [20.00, 21.00, 22.00, 23.00, 24.00, 25.00]
    for precio in precios_venta:
        impuesto = calcular_impuesto_transmisiones_prueba(precio)
        print(f"Precio de venta: {precio} euros - Impuesto de transmisiones: {impuesto} euros")

prueba_calculo_impuesto_transmisiones()


