import pandas as pd
import math

# Создаем таблицу
# diameters = [3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 25, 28, 32, 36, 40]
diameters=[6, 8, 10, 12, 14, 16, 18, 20, 22, 25, 28, 32, 36]
# num_bars = range(1, 11)
num_bars=[5,10]
# Рассчитываем площади
data=[]
for d in diameters:
    area_per_bar = math.pi * (d/10)**2 / 4  # Площадь в см²
    for n in num_bars:
        data.append({
            'S': round(area_per_bar * n, 3),
            'd': d,
            'n': n
        })
df = pd.DataFrame(data).sort_values('S')
df.insert(0, 'Num', range(1, len(df)+1))  # Добавляем порядковый номер
df.set_index('Num', inplace=True)
df.to_csv("square_diam.csv")
# Функция фильтрации
def get_areas_by_diameters(selected_diameters):
    return df[df['d'].isin(selected_diameters)]

