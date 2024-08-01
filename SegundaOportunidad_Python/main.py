from salesforce.salesforce_operations import authenticate_salesforce
from data_base.operations import (
    connec_mysql,
    resetear_columnas_usuarios,
    procesar_productos_usados,
    insert_update_usuarios,
    calcular_cuotas_pagar,
    eliminar_registros_cero_beneficio
)
from excel.generate_excel import generar_excel

def main():
    year = input("Ingrese el año fiscal que desea consultar: ")

    # Autenticación en Salesforce
    sf = authenticate_salesforce()

    if sf:
        print("Autenticación en Salesforce exitosa")
        
        # Conexión a MySQL
        conn = connec_mysql()

        if conn:
            try:
                # Reiniciar columnas relevantes en MySQL
                resetear_columnas_usuarios(conn)

                # Procesar productos usados de Salesforce
                registros = procesar_productos_usados(sf, year)

                # Insertar o actualizar registros en MySQL
                insert_update_usuarios(conn, registros)

                # Calcular cuotas a pagar en MySQL
                calcular_cuotas_pagar(conn)

                # Eliminar registros con beneficios, cuota y transmisiones en cero
                eliminar_registros_cero_beneficio(conn)
                
                # Generar archivo exel con los registros correspondientes
                generar_excel(conn)
            finally:
                conn.close()
                print("Conexión a MySQL cerrada")


if __name__ == "__main__":
    main()
