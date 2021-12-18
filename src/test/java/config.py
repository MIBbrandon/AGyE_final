import math
import random
import numpy as np
from datetime import datetime


set_seeds = False
np_seed = random_seed = 2319
if set_seeds:
    np.random.seed(np_seed)
    random.seed(random_seed)

num_genes = 10
num_genes_str = str(num_genes)

# Nickname para que cada experimento hecho tenga un nombre más identificativo
nickname = 'online'

# Tipo de población
tipo_poblacion = "mu+lambda"

"""
Cada individuo nuevo sin padres tiene que partir de algún punto. No ayudará mucho en 1+1, pero en las estrategias
con poblaciones mayores, los individuos estarán más esparcidos en el espacio de búsqueda, incrementando la probabilidad
de encontrar una solución y con menos generaciones.
"""
rango_de_inicializacion = (0, 360)

now = datetime.now().strftime('%y-%m-%d_%H-%M-%S')

if tipo_poblacion == "mu+lambda":
    common_path = f'resultados/mu_mas_lambda/{nickname}/{now}/'

    # Path a donde se guardará el archivo con los datos relevantes
    config_filepath = common_path + 'config.csv'

    # Path a donde se guardará la evolución de la población
    evolucion_filepath = common_path + 'evolucion.csv'

    max_generaciones = 30

    size_poblacion = 5
    lambda_ = 1

    media = 0
    sd = 180

    # Selección
    size_torneo = 2
    size_familia = 1

    # Mutación
    b = 1
    tau = b / math.sqrt(2 * math.sqrt(num_genes))
    escalar_vector_resultante = False
    if escalar_vector_resultante:
        tau_null = b / math.sqrt(2 * num_genes)
