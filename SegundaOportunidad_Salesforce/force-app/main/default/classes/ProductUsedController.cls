public with sharing class ProductUsedController {
    
    @AuraEnabled(cacheable=true)
    public static List<Producto_Usado__c> getProductsUsed(Integer pageNumber, Integer pageSize) {
        Integer offset = (pageNumber - 1) * pageSize;
        return [SELECT Id, Name, Fecha_Venta__c, imagen2__c, Precio_Compra__c, Precio_Venta__c, Segunda_Oportunidad__c, Vendido__c, Comprador__c
                FROM Producto_Usado__c
                ORDER BY Name
                LIMIT :pageSize
                OFFSET :offset];
    }

    @AuraEnabled(cacheable=true)
    public static Integer getProductsUsedCount() {
        return [SELECT COUNT() FROM Producto_Usado__c];
    }

    @AuraEnabled
    public static void comprarProducto(Id productId, Id compradorId) {
        Producto_Usado__c product = [SELECT Id, Vendido__c, Fecha_Venta__c, Comprador__c FROM Producto_Usado__c WHERE Id = :productId LIMIT 1];

        product.Vendido__c = true;
        product.Fecha_Venta__c = Date.today();
        product.Comprador__c = compradorId;

        update product;
    }

    @AuraEnabled(cacheable=true)
    public static List<Segunda_Oportunidad__c> getSegundaOportunidadOptions(Id currentSegundaOportunidadId) {
        return [SELECT Id, Name FROM Segunda_Oportunidad__c WHERE Id != :currentSegundaOportunidadId];
    }
}
