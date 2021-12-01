import math
import random
import numpy as np
from datetime import datetime


WEBSITE = 'http://163.117.164.219/age/robot'
# WEBSITE = f'http://memento.evannai.inf.uc3m.es/age/robot'
set_seeds = False
np_seed = random_seed = 2319
if set_seeds:
    np.random.seed(np_seed)
    random.seed(random_seed)

num_motores = 3  # 4, 6, 10
num_motores_str = str(num_motores)  # 4, 6, 10, 10b

# Nickname para que cada experimento hecho tenga un nombre más identificativo
nickname = 'online'

# Tipo de población
tipo_poblacion = "mu+lambda"  # "1+1", "mu_lambda", "mu+lambda"

# Usar función local de prueba
test_function = False
version = 3

# Añadir ruido
ruido = False
sd_ruido = 5

if test_function:
    if version == 1:  # Cada ángulo afecta el fitness individualmente
        angulos_optimos_4 = [13.4, 49.2, 126, 355.8]
        angulos_optimos_10 = [13.4, 49.2, 126, 355.8, 13.4, 49.2, 126, 355.8, 13.4, 49.2]
    elif version == 2:  # Los ángulos en conjunto afectan el fitness por la suma
        suma_total = 420
    elif version == 3:  # Los ángulos en conjunto afectan el fitness por la multiplicación
        prod_total = 2319

"""
Cada individuo nuevo sin padres tiene que partir de algún punto. No ayudará mucho en 1+1, pero en las estrategias
con poblaciones mayores, los individuos estarán más esparcidos en el espacio de búsqueda, incrementando la probabilidad
de encontrar una solución y con menos generaciones.
"""
rango_de_inicializacion = (0, 360)

now = datetime.now().strftime('%y-%m-%d_%H-%M-%S')

if tipo_poblacion == "1+1":
    common_path = f'resultados/uno_mas_uno/{nickname}/{now}/'

    # Path a donde se guardará el archivo con los datos relevantes
    config_filepath = common_path + 'config.csv'

    # Path a donde se guardará la evolución de la población
    evolucion_filepath = common_path + 'evolucion.csv'

    max_generaciones = 1000

    s = 5
    c = 0.92

    media = 0
    sd = 180

    hacer_boost = False
    if hacer_boost:
        boost_proporcion = 0.01  # El nuevo boost asignado es una proporción de sd

    # Para que no se cuente como una mejora si es así de pequeño o menos, para que se incrementen las varianzas
    epsilon = 0.001

elif tipo_poblacion == "mu_lambda":
    common_path = f'resultados/mu_lambda/{nickname}/{now}/'

    # Path a donde se guardará el archivo con los datos relevantes
    config_filepath = common_path + 'config.csv'

    # Path a donde se guardará la evolución de la población
    evolucion_filepath = common_path + 'evolucion.csv'

    max_generaciones = 10

    size_poblacion = 50
    lambda_ = 10

    media = 0
    sd = 180

    # Selección
    size_torneo = 5
    size_familia = 3

    # Mutación
    b = 1
    tau = b/math.sqrt(2*math.sqrt(num_motores))
    escalar_vector_resultante = False
    if escalar_vector_resultante:
        tau_null = b/math.sqrt(2*num_motores)

elif tipo_poblacion == "mu+lambda":
    common_path = f'resultados/mu_mas_lambda/{nickname}/{now}/'

    # Path a donde se guardará el archivo con los datos relevantes
    config_filepath = common_path + 'config.csv'

    # Path a donde se guardará la evolución de la población
    evolucion_filepath = common_path + 'evolucion.csv'

    max_generaciones = 10

    size_poblacion = 5
    lambda_ = 3

    media = 0
    sd = 180

    # Selección
    size_torneo = 3
    size_familia = 2

    # Mutación
    b = 1
    tau = b / math.sqrt(2 * math.sqrt(num_motores))
    escalar_vector_resultante = False
    if escalar_vector_resultante:
        tau_null = b / math.sqrt(2 * num_motores)
