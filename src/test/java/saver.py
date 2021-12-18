from typing import List

import config
import os

# CONFIG.CSV
def config_saver(filepath: str):
    """
    Guarda todos los parametros relevantes cuando se ejecuta
    """
    # Primero creamos el directorio si no existe ya
    path = '/'.join(os.path.split(filepath)[:-1])
    if not os.path.exists(path):
        os.makedirs(path, 0o777)
    # Creamos el archivo y empezamos a escribir
    with open(filepath, 'w+') as f:
        f.write(f'Tipo de poblacion={config.tipo_poblacion}\n')
        if config.set_seeds:
            f.write(f'Seeds usadas={config.set_seeds}:np{config.np_seed}_rnd{config.random_seed}\n')
        else:
            f.write(f'Seeds usadas=False\n')
        f.write(f'Numero de genes={config.num_genes}\n')
        f.write(f'Funcion usada=online\n')
        f.write(f'Maximo numero de generaciones={config.max_generaciones}\n')
        f.write(f'Poblacion={config.size_poblacion}\n')
        f.write(f'Lambda={config.lambda_}\n')
        f.write(f'Torneo={config.size_torneo}\n')
        f.write(f'Familia={config.size_familia}\n')
        f.write(f'B={config.b}\n')
        f.write(f'Tau={config.tau}\n')
        if config.escalar_vector_resultante:
            f.write(f'Escalar usado=True:{config.tau_null}\n')
        else:
            f.write(f'Escalar usado=False\n')


def adjuntar_resultado(filepath: str, fitness_final: float, genes: List[List[int]], generacion: int, tiempo: float):
    with open(filepath, 'a+') as f:
        f.write(f'Mejor fitness final={fitness_final}\n')
        f.write(f'Mejor individuo final={genes}\n')
        f.write(f'Generacion de mejor individuo final={generacion}\n')
        f.write(f'Tiempo de ejecucion={tiempo}\n')

# EVOLUCION.CSV
def guardar_evolucion(filepath: str):
    """
    Creamos un archivo donde se van a guardar la evolución
    """
    # El directorio debería existir, pues antes se habrá guardado la config.csv
    with open(filepath, 'w+') as f:
        if config.tipo_poblacion == '1+1':
            f.write('Iteracion;Padre fitness;Hijo fitness;Padre genes;Hijo genes\n')  # Header del archivo
        elif config.tipo_poblacion == 'mu_lambda' or config.tipo_poblacion == 'mu+lambda':
            f.write('Iteracion;Mejor global fitness;Mejor poblacion fitness;Media fitness;Mejor global genes;Mejor poblacion genes\n')


def guardar_generacion_en_evolucion(filepath: str, generacion: int, poblacion, mejor_global=None):
    """
    Adjuntamos al archivo creado por guardar_evolucion() para añadir la información de la población
    """
    with open(filepath, 'a+') as f:
        if config.tipo_poblacion == '1+1':
            f.write(f'{generacion};{poblacion.individuos[0].fitness};{poblacion.individuos[1].fitness};{poblacion.individuos[0].genes};{poblacion.individuos[1].genes}\n')
        elif config.tipo_poblacion == 'mu_lambda' or config.tipo_poblacion == 'mu+lambda':
            mejor_poblacion = poblacion.get_mejor_individuo()
            f.write(f'{generacion};{mejor_global.fitness};{mejor_poblacion.fitness};{poblacion.get_media_fitness()};{mejor_global.genes};{mejor_poblacion.genes}\n')
