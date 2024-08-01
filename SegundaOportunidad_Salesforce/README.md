## Configuración de Salesforce

### Objetos Customizados en Salesforce

#### Objeto Producto_Usado__c

El objeto `Producto_Usado__c` tiene los siguientes campos:

- **CreatedById**: Lookup(User)
- **Fecha_Venta__c**: Date
- **LastModifiedById**: Lookup(User)
- **OwnerId**: Lookup(User, Group)
- **Precio_Compra__c**: Currency(6, 2)
- **Precio_Venta__c**: Currency(6, 2)
- **Name**: Text(80)
- **Segunda_Oportunidad__c**: Lookup(Segunda_Oportunidad__c)
- **Vendido__c**: Checkbox
- **Comprador__c**: Lookup(Segunda_Oportunidad__c)

#### Objeto Segunda_Oportunidad__c

El objeto `Segunda_Oportunidad__c` tiene los siguientes campos:

- **CreatedById**: Lookup(User)
- **DNI__c**: Text(80) (Unique Case Insensitive)
- **Email__c**: Email
- **LastModifiedById**: Lookup(User)
- **OwnerId**: Lookup(User, Group)
- **Name**: Text(80)

### Configuración y Relaciones

- **Producto_Usado__c** tiene un campo de relación (`Segunda_Oportunidad__c`) que referencia a `Segunda_Oportunidad__c`.
- **Producto_Usado__c** también tiene un campo de relación (`Comprador__c`) que referencia a `Segunda_Oportunidad__c`.

### Diagrama de Relaciones

```plaintext
+------------------------+            +--------------------------+
|   Producto_Usado__c    |            |  Segunda_Oportunidad__c  |
+------------------------+            +--------------------------+
| - CreatedById          |            | - CreatedById            |
| - Fecha_Venta__c       |            | - DNI__c                 |
| - LastModifiedById     |            | - Email__c               |
| - OwnerId              |            | - LastModifiedById       |
| - Precio_Compra__c     |            | - OwnerId                |
| - Precio_Venta__c      |            | - Name                   |
| - Name                 |            +--------------------------+
| - Segunda_Oportunidad__c|                 ^          
| - Vendido__c           |                 |          
| - Comprador__c         |-----------------+         
+------------------------+
```
### Código SQL para la Base de Datos

```sql
CREATE TABLE usuarios (
    nombre VARCHAR(255),
    dni_hash VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255),
    beneficios_anio DECIMAL(10,2) DEFAULT 0.00,
    cantidad_a_pagar DECIMAL(10,2) DEFAULT 0.00,
    impuesto_transmisiones DECIMAL(10,2) DEFAULT 0.00
);

CREATE TABLE productos_usados (
    Id VARCHAR(18) PRIMARY KEY,
    CreatedById VARCHAR(18),
    Fecha_Venta DATE,
    LastModifiedById VARCHAR(18),
    OwnerId VARCHAR(18),
    Precio_Compra DECIMAL(10,2),
    Precio_Venta DECIMAL(10,2),
    Name VARCHAR(80),
    Segunda_Oportunidad_Id VARCHAR(18),
    Vendido BOOLEAN,
    Comprador_Id VARCHAR(18),
    FOREIGN KEY (Segunda_Oportunidad_Id) REFERENCES segunda_oportunidad(Id),
    FOREIGN KEY (Comprador_Id) REFERENCES segunda_oportunidad(Id)
);

CREATE TABLE segunda_oportunidad (
    Id VARCHAR(18) PRIMARY KEY,
    CreatedById VARCHAR(18),
    DNI VARCHAR(80) UNIQUE,
    Email VARCHAR(255),
    LastModifiedById VARCHAR(18),
    OwnerId VARCHAR(18),
    Name VARCHAR(80)
);
```