import ezdxf
from ezdxf import colors  # Импортируем модуль colors
from arm import get_areas_by_diameters
filenames=("niz_x",
           "niz_y",
           "verx_x",
           "verx_y"
           )
diam=[12, 16,20]
numbers_for_color=get_areas_by_diameters(diam).index.unique().tolist()
colors_rgb = [
    (255, 0, 0),    # Красный
    (0, 255, 0),    # Зелёный
    (0, 0, 255),    # Синий
    (255, 255, 0),  # Жёлтый
    (255, 0, 255),  # Пурпурный
    (0, 255, 255),  # Бирюзовый
    (255, 165, 0),  # Оранжевый
    (128, 0, 128),  # Фиолетовый
    (0, 128, 0),    # Тёмно-зелёный
    (255, 99, 71)   # Томатный
]
color_mapping = {
    idx: colors_rgb[i % len(colors_rgb)] 
    for i, idx in enumerate(numbers_for_color)
}
def draw_hatches_from_dataframe(df, output_dxf="hatches.dxf"):
    doc = ezdxf.new("R2018")
    msp = doc.modelspace()
    
    def get_color_by_value(value):

        return color_mapping.get(value)
    
    for _, row in df.iterrows():
        points = [
            (row['vt_1_x'], row['vt_1_y']),
            (row['vt_2_x'], row['vt_2_y']),
            (row['vt_3_x'], row['vt_3_y']),
            (row['vt_4_x'], row['vt_4_y']),
        ]
        
        # Создаём заливку
        hatch = msp.add_hatch()
        rgb_color = get_color_by_value(row['type_arm'])
        if rgb_color :
            hatch.paths.add_polyline_path(points, is_closed=True)
            hatch.set_solid_fill(rgb=rgb_color)  # Основной способ для RGB

    doc.saveas(output_dxf)