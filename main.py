# import matplotlib
# matplotlib.use('TkAgg') # <--- Agrega esta línea ANTES de importar pyplot

import matplotlib.pyplot as plt
import pandas as pd
import io

# Cargar datos
df = pd.read_csv('acme-export.csv')

# Convertir fecha
# df['Date_Time'] = pd.to_datetime(df['Date_Time'])
df['Date_Time'] = pd.to_datetime(df['Date_Time'], format='%m/%d/%Y %I:%M:%S %p')

# Filtrar por "B3 DPT B"
df_b3 = df[df['Button_Name'] == 'B3 DPT B'].copy()

# Extraer día del mes
df_b3['Day'] = df_b3['Date_Time'].dt.day

# Agrupar por día
daily_stats = df_b3.groupby('Day')['Response_Time'].agg(['count', 'mean']).sort_index()

# Crear gráfico
fig, ax1 = plt.subplots(figsize=(12, 6))

# Eje 1: Llamadas Totales (Barras para mejor visibilidad dada la uniformidad)
color = 'tab:blue'
ax1.set_xlabel('Día del Mes (Noviembre)')
ax1.set_ylabel('Llamadas Totales', color=color)
ax1.plot(daily_stats.index, daily_stats['count'], color=color, marker='o', linestyle='-', label='Llamadas Totales')
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_ylim(0, 5) # Ajustar escala para ver claramente la línea en 2

# Eje 2: Tiempo Promedio (Línea)
ax2 = ax1.twinx()
color = 'tab:orange'
ax2.set_ylabel('Tiempo Promedio (segundos)', color=color)
ax2.plot(daily_stats.index, daily_stats['mean'], color=color, marker='s', linestyle='--', label='Tiempo Promedio')
ax2.tick_params(axis='y', labelcolor=color)

# Título y Grid
plt.title('B3 DPT B: Llamadas y Tiempo de Respuesta por Día del Mes')
plt.grid(True, alpha=0.3)
fig.tight_layout()

# Mostrar gráfico
plt.show()
