import pandas as pd
from arm import get_areas_by_diameters
import numpy as np
from drawiso import draw_hatches_from_dataframe
niz_x_fon= 5.65
diam=[12, 16,20]
lanker={12:0.5,16:0.65,20:0.95}
df=pd.read_csv("full.csv", index_col=0)
df=df[df["direction"]=="niz_x"]
df['type_arm']=0 
df['value'] = (df['value'] - niz_x_fon).clip(lower=0)
positive_mask = df['value'] > 0
df_pos = df[positive_mask].copy()
df_areas = get_areas_by_diameters(diam)
areas_sorted = df_areas['S'].sort_values().values
nums_sorted = df_areas.index[df_areas['S'].argsort()]
masks = [df_pos['value'].values < area for area in areas_sorted]
result = np.select(masks, nums_sorted, default=0)


df.loc[positive_mask, 'type_arm'] = result
df['type_arm'] = df['type_arm'].astype('Int64') 
# print(df)
# draw_hatches_from_dataframe(df,"df.dxf")
def extend_reinforcement_zones(df_cells, df_areas, lanker):
    # Сортируем типы армирования по убыванию площади
    sorted_areas = df_areas.sort_values('S', ascending=False)
    df_mod = df_cells.copy()
    
    # Определяем границы всей сетки
    global_x_min = df_mod[['vt_1_x', 'vt_2_x', 'vt_3_x', 'vt_4_x']].min().min()
    global_x_max = df_mod[['vt_1_x', 'vt_2_x', 'vt_3_x', 'vt_4_x']].max().max()
    
    for _, row in sorted_areas.iterrows():
        num = row.name
        d = row['d']
        l_anchor = lanker[d]
        
        current_cells = df_mod[df_mod['type_arm'] == num]
        
        for idx in current_cells.index:
            x_coords = df_mod.loc[idx, ['vt_1_x', 'vt_2_x', 'vt_3_x', 'vt_4_x']].values
            y_coords = df_mod.loc[idx, ['vt_1_y', 'vt_2_y', 'vt_3_y', 'vt_4_y']].values
            
            x_min, x_max = min(x_coords), max(x_coords)
            y_min, y_max = min(y_coords), max(y_coords)
            
            # Расширение вправо
            right_bound = min(x_max + l_anchor, global_x_max)  # Не выходим за границы сетки
            right_cells = df_mod[
                (df_mod['vt_1_y'] == y_min) & 
                (df_mod['vt_4_y'] == y_max) &
                (df_mod['vt_1_x'] >= x_max) &
                (df_mod['vt_1_x'] <= right_bound)
            ].sort_values('vt_1_x')
            
            for n_idx in right_cells.index:
                if df_mod.loc[n_idx, 'type_arm'] > num:
                    continue  # Пропускаем ячейку, но продолжаем проверять дальше
                df_mod.loc[n_idx, 'type_arm'] = num
            
            # Расширение влево
            left_bound = max(x_min - l_anchor, global_x_min)  # Не выходим за границы сетки
            left_cells = df_mod[
                (df_mod['vt_1_y'] == y_min) & 
                (df_mod['vt_4_y'] == y_max) &
                (df_mod['vt_2_x'] <= x_min) &
                (df_mod['vt_2_x'] >= left_bound)
            ].sort_values('vt_2_x', ascending=False)
            
            for n_idx in left_cells.index:
                if df_mod.loc[n_idx, 'type_arm'] > num:
                    continue  # Пропускаем ячейку, но продолжаем проверять дальше
                df_mod.loc[n_idx, 'type_arm'] = num
    
    return df_mod
# print(extend_reinforcement_zones(df,df_areas,lanker))
draw_hatches_from_dataframe(extend_reinforcement_zones(df,df_areas,lanker),"with_anker.dxf")