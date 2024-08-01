# Proyecto de Gestión de Productos Usados y Segundas Oportunidades

## Descripción

Este proyecto integra Salesforce y MySQL con un API en Python para gestionar productos usados y segundas oportunidades, realizando cálculos financieros y generando informes en formato Excel. La aplicación consta de las siguientes partes principales:

- [Parte de Python](#SegundaOportunidad_Python)
- [Parte de Salesforce](#SegundaOportunidad_Salesforce)


## Estructura del Proyecto

### Parte de Python

El código Python se encarga de la conexión con Salesforce y MySQL, el procesamiento de datos y la generación de informes en Excel. Para más detalles, consulte el [README de la parte de Python](SegundaOportunidad_Python\README.md).

### Parte de Salesforce

En Salesforce se gestionan los objetos `Producto_Usado__c` y `Segunda_Oportunidad__c`, con reglas de validación y triggers para asegurar la integridad de los datos. Para más detalles, consulte el [README de la parte de Salesforce](SegundaOportunidad_Salesforce\README.md).


## Instalación y Configuración

### Requisitos

- Python 3.8 o superior
- MySQL 5.7 o superior
- Cuenta de Salesforce

### Configuración

#### Configuración de Salesforce

1. Configure las credenciales de Salesforce en el archivo `config.py`.
2. Importe los objetos `Producto_Usado__c` y `Segunda_Oportunidad__c` en Salesforce.

#### Configuración de MySQL

1. Cree la base de datos y las tablas en MySQL utilizando el archivo `schema.sql`.
2. Configure las credenciales de MySQL en el archivo `config.py`.

### Instalación de Dependencias

Instale las dependencias de Python:

```bash
pip install -r requirements.txt

```

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


