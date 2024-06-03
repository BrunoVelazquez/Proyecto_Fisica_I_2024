def reformat_values(input_file, output_file):
    try:
        # Leer el contenido del archivo de entrada
        with open(input_file, 'r') as infile:
            data = infile.read()
        
        # Separar los valores por comas y eliminar cualquier espacio en blanco alrededor de ellos
        values = data.strip().split(',')

        # Escribir los valores en el archivo de salida, uno por línea
        with open(output_file, 'w') as outfile:
            for value in values:
                outfile.write(value.strip() + '\n')
                
        print(f"Datos reformateados y guardados en {output_file}")
    
    except Exception as e:
        print(f"Se produjo un error: {e}")


def write_values_to_file(values, output_file):
    try:
        with open(output_file, 'w') as outfile:
            for value in values:
                outfile.write(f"{value}\n")
        print(f"Valores guardados en {output_file}")
    except Exception as e:
        print(f"Se produjo un error: {e}")


# Uso de la función
input_file = 'Datos_Extraidos_Marca\\Datos_Video_1\\posicionX_1.txt'  # Nombre del archivo de entrada
output_file = 'Datos_Extraidos_Marca\\Datos_Video_1\\posicionX_1_2.txt'   # Nombre del archivo de salida
reformat_values(input_file, output_file)

input_file = 'Datos_Extraidos_Marca\\Datos_Video_1\\posicionY_1.txt'  # Nombre del archivo de entrada
output_file = 'Datos_Extraidos_Marca\\Datos_Video_1\\posicionY_1_2.txt'   # Nombre del archivo de salida
reformat_values(input_file, output_file)

input_file = 'Datos_Extraidos_Marca\\Datos_Video_1\\velocidadX_1.txt'  # Nombre del archivo de entrada
output_file = 'Datos_Extraidos_Marca\\Datos_Video_1\\velocidadX_1_2.txt'   # Nombre del archivo de salida
reformat_values(input_file, output_file)

input_file = 'Datos_Extraidos_Marca\\Datos_Video_1\\velocidadY_1.txt'  # Nombre del archivo de entrada
output_file = 'Datos_Extraidos_Marca\\Datos_Video_1\\velocidadY_1_2.txt'   # Nombre del archivo de salida
reformat_values(input_file, output_file)



t = []

with open(f'Datos_Extraidos_Marca\\Datos_Video_1\\datosRuedaX_1.txt', 'r') as f:
            for linea in f:
                partes = linea.split()
                t.append(float(partes[0].replace(',', '.')))

# Ejemplo de uso

output_file = 'Datos_Extraidos_Marca\\Datos_Video_1\\tiempo_1.txt'  # Nombre del archivo de salida
write_values_to_file(t, output_file)