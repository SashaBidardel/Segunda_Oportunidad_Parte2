import random
import string
from simple_salesforce import Salesforce
from config.config import USERNAME, PASSWORD, SECURITY_TOKEN

def get_segunda_oportunidad_ids(sf):
    """Obtener todos los IDs de Segunda_Oportunidad__c"""
    query = "SELECT Id FROM Segunda_Oportunidad__c"
    result = sf.query_all(query)
    return [record['Id'] for record in result['records']]

def generate_random_price():
    return round(random.uniform(10.00, 99999.99), 2)

def load_random_records(num_records):
    sf = Salesforce(username=USERNAME, password=PASSWORD, security_token=SECURITY_TOKEN)
    
    segunda_oportunidad_ids = get_segunda_oportunidad_ids(sf)
    
    if len(segunda_oportunidad_ids) < 2:
        raise ValueError("No hay suficientes registros de Segunda_Oportunidad__c para generar datos válidos.")
    
    records = []
    for _ in range(num_records):
        precio_compra = generate_random_price()
        precio_venta = generate_random_price()
        
        # Decidir si el producto está vendido
        vendido = random.choice([True, False])
        
        # Inicializar variables
        fecha_venta = None
        segunda_oportunidad = None
        comprador = None
        
        if vendido:
            fecha_venta = f"{random.randint(2020, 2024)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
            segunda_oportunidad = random.choice(segunda_oportunidad_ids)
            comprador = random.choice([id for id in segunda_oportunidad_ids if id != segunda_oportunidad])
        else:
            segunda_oportunidad = random.choice(segunda_oportunidad_ids)
        
        # Validaciones
        if vendido and not fecha_venta:
            raise ValueError("Fecha_Venta__c es obligatoria cuando Vendido__c es True.")
        
        if not vendido and fecha_venta:
            raise ValueError("Vendido__c debe ser True si Fecha_Venta__c está presente.")
        
        record = {
            'Name': generate_random_string(10).title(),
            'Precio_Compra__c': precio_compra,
            'Precio_Venta__c': precio_venta,
            'Vendido__c': vendido,
            'Fecha_Venta__c': fecha_venta,
            'Segunda_Oportunidad__c': segunda_oportunidad,
            'Comprador__c': comprador
        }
        records.append(record)
    
    result = sf.bulk.Producto_Usado__c.insert(records)
    return result

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

if __name__ == "__main__":
    num_records = int(input("Ingrese el número de registros aleatorios que desea cargar en Productos Usados: "))
    try:
        result = load_random_records(num_records)
        print(f"Se cargaron {len(result)} registros en Productos Usados.")
    except ValueError as e:
        print(f"Error: {e}")
