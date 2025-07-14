import ezdxf
from ezdxf import colors
from ezdxf.gfxattribs import GfxAttribs
from ezdxf.render import forms
import pandas as pd
import numpy as np
from pathlib import Path
base_dir = Path("zad")
filenames=("niz_x",
           "niz_y",
           "verx_x",
           "verx_y"
           )
filenames = [base_dir / f"{name}.dxf" for name in filenames]
full_table=pd.DataFrame()
data=[]
for file in filenames:
    doc = ezdxf.readfile(file)
    msp = doc.modelspace()
    faces=msp.query('3DFACE[layer=="layer_elements"]')
    values=msp.query('Text[layer=="layer_result_values"]')
    if len(faces) != len(values):
        print(f"Предупреждение: в файле {file.name} количество faces ({len(faces)}) "
                f"не совпадает с values ({len(values)})")
        break        
    for face, value in zip(faces,values):
        vertices = face.wcs_vertices()[:4]  # Берём 4 вершины
        xy_coords = []
        for vertex in vertices:
            x, y, _ = vertex  # Распаковываем Vec3 в x, y, z (z игнорируем)
            xy_coords.extend([
                round(round(x / 0.05) * 0.05, 2),
                round(round(y / 0.05) * 0.05, 2)
            ])
        data.append([file.stem] + xy_coords+[value.dxf.text]) 
columns = ['direction'] + [f'vt_{i+1}_{coord}' for i in range(4) for coord in ['x', 'y']]+["value"]
df = pd.DataFrame(data, columns=columns)
print(df)
df.to_csv("full.csv")
print(f"сохраняем в файл")