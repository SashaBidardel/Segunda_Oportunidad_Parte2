import { LightningElement, wire, track } from 'lwc';
import getProductsUsed from '@salesforce/apex/ProductUsedController.getProductsUsed';
import getProductsUsedCount from '@salesforce/apex/ProductUsedController.getProductsUsedCount';
import getSegundaOportunidadOptions from '@salesforce/apex/ProductUsedController.getSegundaOportunidadOptions';
import { updateRecord } from 'lightning/uiRecordApi';
import { refreshApex } from '@salesforce/apex'; 
import PRODUCT_OBJECT from '@salesforce/schema/Producto_Usado__c';
import COMPRADOR_FIELD from '@salesforce/schema/Producto_Usado__c.Comprador__c';
import VENDIDO_FIELD from '@salesforce/schema/Producto_Usado__c.Vendido__c';
import FECHA_VENTA_FIELD from '@salesforce/schema/Producto_Usado__c.Fecha_Venta__c';

export default class ProductList extends LightningElement {
    @track products = [];
    @track displayedProducts = [];
    @track currentPage = 1;
    @track pageSize = 15;
    @track totalPages = 1;
    @track isModalOpen = false;
    @track selectedProductId;
    @track segundaOportunidadOptions = [];
    @track selectedCompradorId;

    @wire(getProductsUsed, { pageNumber: '$currentPage', pageSize: '$pageSize' })
    wiredProducts(result) {
        this.productsResult = result;
        const { error, data } = result;
        if (data) {
            this.displayedProducts = data;
            this.updatePagination();
        } else if (error) {
            this.displayedProducts = [];
            console.error('Error fetching products used:', error);
        }
    }

    @wire(getProductsUsedCount)
    wiredProductsCount(result) {
        this.productsCountResult = result;
        const { error, data } = result;
        if (data) {
            this.totalPages = Math.ceil(data / this.pageSize);
            this.updatePagination();
        } else if (error) {
            console.error('Error fetching products count:', error);
        }
    }

    openModal(event) {
        this.selectedProductId = event.target.dataset.id;
        this.isModalOpen = true;

        const selectedProduct = this.displayedProducts.find(
            product => product.Id === this.selectedProductId
        );

        getSegundaOportunidadOptions()
            .then((result) => {
                this.segundaOportunidadOptions = result
                    .filter(option => option.Id !== selectedProduct.Segunda_Oportunidad__c)
                    .map(option => ({
                        label: option.Name,
                        value: option.Id
                    }));
            })
            .catch((error) => {
                console.error('Error fetching segunda oportunidad options:', error);
            });
    }

    closeModal() {
        this.isModalOpen = false;
        this.selectedCompradorId = null;
    }
    
    handleComboboxChange(event) {
        this.selectedCompradorId = event.detail.value;
    }

    handleSave() {
        if (!this.selectedCompradorId) {
            return;
        }

        const fields = {};
        fields.Id = this.selectedProductId;
        fields[COMPRADOR_FIELD.fieldApiName] = this.selectedCompradorId;
        fields[VENDIDO_FIELD.fieldApiName] = true;
        fields[FECHA_VENTA_FIELD.fieldApiName] = new Date().toISOString();

        const recordInput = { fields };

        updateRecord(recordInput)
            .then(() => {
                this.isModalOpen = false;
                this.selectedCompradorId = null;
                return refreshApex(this.productsResult);
            })
            .catch((error) => {
                console.error('Error updating product:', error);
            });
    }

    handlePageChange(event) {
        const action = event.target.dataset.action;
        switch(action) {
            case 'first':
                this.currentPage = 1;
                break;
            case 'prev':
                if (this.currentPage > 1) {
                    this.currentPage--;
                }
                break;
            case 'next':
                if (this.currentPage < this.totalPages) {
                    this.currentPage++;
                }
                break;
            case 'last':
                this.currentPage = this.totalPages;
                break;
        }
        this.updatePagination();
    }

    updatePagination() {
        this.currentPage = Math.min(this.currentPage, this.totalPages);
    }

    get hasPrevPage() {
        return this.currentPage > 1;
    }

    get hasNextPage() {
        return this.currentPage < this.totalPages;
    }

    handleSoldClick(event) {
        //  maneja la lógica cuando se hace clic en un producto ya vendido
        alert('Producto Vendido');
    }
}
