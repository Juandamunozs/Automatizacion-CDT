import os
import json
from env.env import dir_res

def guardar_exito_json(res_investigacion):
    res_investigacion_ordenado = dict(res_investigacion)

    # Ruta al archivo JSON
    file_path = os.path.join(dir_res, "res.json")

        # Guardar el archivo JSON
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(res_investigacion_ordenado, json_file, ensure_ascii=False, indent=4)