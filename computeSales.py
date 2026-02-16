# pylint: disable=invalid-name
"""
Módulo para el cálculo de ventas totales a partir de catálogos JSON.
Actividad 5.2 - Programación y Análisis Estático.
"""

import sys
import json
import time


def load_json(file_path):
    """
    Carga y decodifica un archivo JSON.
    Maneja errores de archivo no encontrado o formato inválido.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as error:
        print(f"ERROR: No se pudo procesar el archivo {file_path}: {error}")
        return None


def calculate_total(catalogue, sales):
    """
    Cruza los datos de ventas con el catálogo de precios.
    Retorna el costo total acumulado.
    """
    # Mapeo de precios basado en TC1.ProductList.json (usa 'title')
    price_map = {item.get('title'): item.get('price') for item in catalogue
                 if 'title' in item and 'price' in item}

    total_cost = 0.0
    for sale in sales:
        # Basado en los archivos TC (usa 'Product' y 'Quantity')
        product = sale.get('Product')
        quantity = sale.get('Quantity', 0)

        if product in price_map:
            total_cost += price_map[product] * quantity
        else:
            # Req 3: Informar productos no encontrados
            print(f"ADVERTENCIA: Producto '{product}' no encontrado.")

    return total_cost


def main():
    """Función principal: Orquestación del programa."""
    start_time = time.time()

    # Req 5: Verificar parámetros de línea de comandos
    if len(sys.argv) != 3:
        print("Uso: python computeSales.py catálogo.json ventas.json")
        return

    # Carga de datos
    catalogue_data = load_json(sys.argv[1])
    sales_data = load_json(sys.argv[2])

    if catalogue_data is None or sales_data is None:
        return

    # Proceso de cálculo
    total = calculate_total(catalogue_data, sales_data)
    elapsed_time = time.time() - start_time

    # Formateo de resultados (Req 2 y Req 7)
    results = (
        f"--- RESULTADOS DE EJECUCIÓN ---\n"
        f"Catálogo: {sys.argv[1]}\n"
        f"Ventas: {sys.argv[2]}\n"
        f"Costo Total: {total:,.2f}\n"
        f"Tiempo de ejecución: {elapsed_time:.4f} segundos\n"
        f"{'-' * 31}\n"
    )

    # Imprimir en consola y guardar en archivo (Req 2)
    print(results)
    try:
        with open("SalesResults.txt", "a", encoding="utf-8") as out_file:
            out_file.write(results)
    except IOError as error:
        print(f"Error escribiendo el archivo de resultados: {error}")


if __name__ == "__main__":
    main()
