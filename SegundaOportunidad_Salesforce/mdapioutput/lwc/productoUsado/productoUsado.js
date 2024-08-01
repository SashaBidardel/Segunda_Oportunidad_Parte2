import { LightningElement, track } from 'lwc';
import saveProduct from '@salesforce/apex/ProductoUsadoController.saveProduct';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';

export default class ProductoUsado extends LightningElement {
    @track productName = '';
    @track fechaVenta = '';
    @track imagenUrl = '';
    @track precioCompra = '';
    @track precioVenta = '';
    @track segundaOportunidadId = '';

    handleInputChange(event) {
        const field = event.target.label;
        if (field === 'Nombre') {
            this.productName = event.target.value;
        } else if (field === 'Fecha de Venta') {
            this.fechaVenta = event.target.value;
        } else if (field === 'Imagen URL') {
            this.imagenUrl = event.target.value;
        } else if (field === 'Precio de Compra') {
            this.precioCompra = event.target.value;
        } else if (field === 'Precio de Venta') {
            this.precioVenta = event.target.value;
        } else if (field === 'Segunda Oportunidad') {
            this.segundaOportunidadId = event.target.value;
        }
    }

    handleSave() {
        saveProduct({
            name: this.productName,
            fechaVenta: this.fechaVenta,
            imagenUrl: this.imagenUrl,
            precioCompra: this.precioCompra,
            precioVenta: this.precioVenta,
            segundaOportunidadId: this.segundaOportunidadId
        })
        .then(() => {
            this.showToast('Success', 'Producto guardado correctamente', 'success');
            this.clearFields();
        })
        .catch(error => {
            this.showToast('Error', error.body.message, 'error');
        });
    }

    showToast(title, message, variant) {
        const event = new ShowToastEvent({
            title,
            message,
            variant,
        });
        this.dispatchEvent(event);
    }

    clearFields() {
        this.productName = '';
        this.fechaVenta = '';
        this.imagenUrl = '';
        this.precioCompra = '';
        this.precioVenta = '';
        this.segundaOportunidadId = '';
    }
}
