public with sharing class ProductoUsadoController {
    @AuraEnabled
    public static void saveProduct(String name, Date fechaVenta, String imagenUrl, Decimal precioCompra, Decimal precioVenta, Id segundaOportunidadId) {
        // Usar el nombre correcto del objeto: Producto_Usado__c
        Producto_Usado__c productoUsado = new Producto_Usado__c();
        productoUsado.Name = name;
        productoUsado.Fecha_Venta__c = fechaVenta; // Asegúrate de que este campo existe en Producto_Usado__c
        productoUsado.Imagen__c = imagenUrl; // Asegúrate de que este campo existe en Producto_Usado__c
        productoUsado.Precio_Compra__c = precioCompra; // Asegúrate de que este campo existe en Producto_Usado__c
        productoUsado.Precio_Venta__c = precioVenta; // Asegúrate de que este campo existe en Producto_Usado__c
        productoUsado.Segunda_Oportunidad__c = segundaOportunidadId; // Asegúrate de que este campo existe en Producto_Usado__c
        insert productoUsado;
    }
}


