# **Proyecto: Gestión de Productos Usados y Segundas Oportunidades (Segunda Parte)**

## **1. Descripción del Proyecto**

El objetivo de este proyecto es poder desde la agencia tributaria pedir los datos fiscales de venta de un año determinado de una app de ventas de segunda mano(Segunda Oportunida)cuyos datos tenemos alojados en una org de Salesforce para ver los beneficios de ese año,si los hubiese,con su correspondiente carga fiscal(20% de los beneficios). <br>
Se pide un año fiscal desde la api de python que simula a la agencia tributaria y se obtienen los datos de la org de salesforce en donde están los usuarios de la aplicación Segunda Oportunidad, se actualizan y calculan beneficios, y se generan reportes en formato Excel. Además, se gestionan las ventas y se aplican validaciones específicas sobre los datos.
En esta segunda parte también calculamos el impuesto de trasmisiones que es el 4% de cualquier compra,y en este caso siempre se tiene que pagar.En el excel saldrá ahora cualquier usuario que haya tenido ventas con beneficios o una compra al menos en ese año fiscal

## **2. Requisitos**

### **2.1. Requisitos del Sistema**

- Python 3.7 o superior
- Salesforce
- MySQL
- Herramientas de desarrollo:
  - Visual Studio Code
  - Postman (para pruebas de API)

  
### **2.2. Requisitos de Bibliotecas**

- `simple_salesforce`
- `mysql-connector-python`
- `openpyxl`
- `pytest` (para pruebas unitarias)

## **3. Configuración del Entorno**

### **3.1. Creación del Entorno Virtual**

```bash
python -m venv venv
source venv/bin/activate (En Windows: venv\Scripts\activate)
```
### **3.2. Instalación de Dependencias**

```bash
pip install -r requirements.txt
pip install simple-salesforce mysql-connector-python pandas openpyxl

```
### **3.3. Variables de Conexión**

```python
USERNAME=tu_usuario_salesforce
PASSWORD=tu_contraseña_salesforce
SECURITY_TOKEN=tu_token_de_seguridad_salesforce
DB_USER=tu_usuario_mysql
DB_HOST=tu_host_mysql
DB_PASSWORD=tu_contraseña_mysql
DB_NAME=nombre_base_datos
```
## **4. Implementación**

```sql
CREATE DATABASE segundoportunidad;

USE segundoportunidad;

CREATE TABLE usuarios (
    nombre VARCHAR(255) NOT NULL,
    dni_hash VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    beneficios_anio DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    cantidad_a_pagar DECIMAL(10,2) NOT NULL DEFAULT 0.00
    impuesto_transmisiones	DECIMAL(10,2)			
	total_compras	DECIMAL(10,2)
);
```
## **5 Scripts de Python**
### **5.1 Ejecución del proyecto**

- Configure las credenciales de Salesforce y MySQL como se explicó anteriormente.
- Asegúrese de que todas las dependencias estén instaladas.
- Ejecute el script principal(main.py):
```bash
python main.py
```
- Esto realizará las siguientes acciones:

    - Conectará a Salesforce y MySQL.
    - Reseteará las columnas relevantes en la base de datos MySQL.
    - Procesará los productos usados obtenidos de Salesforce.
    - Insertará o actualizará los registros de usuarios en MySQL.
    - Calculará la cuota a pagar y el impuesto de transmisiones para cada usuario.
    - Eliminará los registros de usuarios con beneficios, cuota y transmisiones en cero.
    - Exportará los datos actualizados a un archivo Excel llamado usuarios_data.xlsx



## **6. Pruebas**
### **6.1. Ejecución de Pruebas Unitarias**

Para ejecutar las pruebas unitarias, utilice el siguiente comando:
```bash
pytest tests/
```

## **7. Generación de Reportes**
### **7.1. Generación de Excel**

El script principal genera un archivo Excel con los datos de usuarios y beneficios calculados:

```python

generar_excel(conn)

```




