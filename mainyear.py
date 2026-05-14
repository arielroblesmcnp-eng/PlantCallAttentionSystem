# import matplotlib
# matplotlib.use('TkAgg') # <--- Agrega esta línea ANTES de importar pyplot

import matplotlib.pyplot as plt
import pandas as pd
import io

# --- 1. CONFIGURACIÓN ---
# Puedes cambiar esta ruta si el archivo .csv está en otra ubicación
FILE_PATH = 'acme-export.csv'
BUTTON_NAME_FILTER = 'B3 DPT B'

# --- 2. CARGAR Y PREPARAR DATOS ---
try:
    # Cargar datos desde el archivo
    df = pd.read_csv(FILE_PATH)
except FileNotFoundError:
    print(f"Error: No se encontró el archivo '{FILE_PATH}'. Asegúrate de que está en la misma carpeta.")
    exit()

# Convertir la columna de fecha y hora a formato datetime
# Asumo el mismo formato de tu script original: MM/DD/YYYY HH:MM:SS AM/PM
df['Date_Time'] = pd.to_datetime(df['Date_Time'], format='%m/%d/%Y %I:%M:%S %p')

# Filtrar por el nombre del botón específico
df_b3 = df[df['Button_Name'] == BUTTON_NAME_FILTER].copy()

# --- 3. AGRUPACIÓN POR MES Y AÑO ---

# Crear una columna de Año-Mes para agrupar y mantener el orden cronológico
# Esto resultará en un string como '2023-11', '2023-12', '2024-01', etc.
df_b3['Year_Month'] = df_b3['Date_Time'].dt.to_period('M')

# Crear una columna de Mes para la etiqueta del gráfico (Enero, Febrero, etc.)
# Usamos el nombre abreviado del mes: 'Jan', 'Feb', etc.
df_b3['Month_Label'] = df_b3['Date_Time'].dt.strftime('%b-%y')

# Agrupar por el identificador único (Year_Month)
# Calculamos el conteo (llamadas totales) y el promedio (tiempo de respuesta)
monthly_stats = df_b3.groupby('Year_Month').agg(
    count=('Response_Time', 'count'),
    mean=('Response_Time', 'mean'),
    # Extraemos la etiqueta del mes/año para usarla en el gráfico
    label=('Month_Label', 'first')
).sort_index()

# Convertir el índice de Year_Month a un simple rango numérico para Matplotlib
x_data = range(len(monthly_stats))
# Usar la columna 'label' como etiquetas para el eje X
x_labels = monthly_stats['label'].tolist()

# --- 4. CREAR GRÁFICO ---

fig, ax1 = plt.subplots(figsize=(12, 6))

# --- Eje 1: Llamadas Totales (Línea o Barras, como prefieras, aquí usamos línea como ejemplo)
color_calls = 'tab:blue'
ax1.set_xlabel('Mes del Año (y Año)', fontsize=12)
ax1.set_ylabel('Llamadas Totales', color=color_calls, fontsize=12)
# Trazar la línea de Llamadas Totales
ax1.plot(x_data, monthly_stats['count'], color=color_calls, marker='o', linestyle='-', label='Llamadas Totales')
ax1.tick_params(axis='y', labelcolor=color_calls)
# Opcional: Ajustar el límite superior del eje Y para llamadas
# max_calls = monthly_stats['count'].max()
# ax1.set_ylim(0, max_calls * 1.1)

# --- Eje 2: Tiempo Promedio (Línea)
ax2 = ax1.twinx()
color_time = 'tab:orange'
ax2.set_ylabel('Tiempo Promedio (segundos)', color=color_time, fontsize=12)
# Trazar la línea de Tiempo Promedio
ax2.plot(x_data, monthly_stats['mean'], color=color_time, marker='s', linestyle='--', label='Tiempo Promedio')
ax2.tick_params(axis='y', labelcolor=color_time)

# --- Configuración de Eje X ---
# Establecer las etiquetas del eje X con los nombres de los meses (Mes-Año)
ax1.set_xticks(x_data)
ax1.set_xticklabels(x_labels, rotation=45, ha='right') # Rotar para mejor legibilidad

# Título y Grid
plt.title(f'{BUTTON_NAME_FILTER}: Llamadas y Tiempo de Respuesta por Mes', fontsize=14)
plt.grid(True, alpha=0.5)
fig.tight_layout() # Ajustar el diseño para que no se corten las etiquetas

# --- 5. MOSTRAR GRÁFICO ---
plt.show() 

