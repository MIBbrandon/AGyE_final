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
        f.write(f'Numero de motores={config.num_motores}\n')
        if config.test_function:
            if config.version == 1 and config.num_motores == 4:
                f.write(f'Funcion usada=local:v{config.version}_{config.angulos_optimos_4}\n')
            elif config.version == 1 and config.num_motores == 10:
                f.write(f'Funcion usada=local:v{config.version}_{config.angulos_optimos_10}\n')
            elif config.version == 2:
                f.write(f'Funcion usada=local:v{config.version}_{config.suma_total}\n')
            elif config.version == 3:
                f.write(f'Funcion usada=local:v{config.version}_{config.prod_total}\n')
        else:
            f.write(f'Funcion usada=online\n')
        f.write(f'Rango de inicializacion={config.rango_de_inicializacion}\n')
        if config.tipo_poblacion == '1+1':
            # Si la estrategia es 1+1, guardamos solo lo relevante a esa estrategia
            f.write(f'Maximo numero de generaciones={config.max_generaciones}\n')
            f.write(f'S={config.s}\n')
            f.write(f'C={config.c}\n')
            f.write(f'Media={config.media}\n')
            f.write(f'Desviacion estandard={config.sd}\n')
            if config.hacer_boost:
                f.write(f'Boost usado=True:{config.boost_proporcion}\n')
            else:
                f.write(f'Boost usado=False\n')
            f.write(f'Epsilon={config.epsilon}\n')
        elif config.tipo_poblacion == 'mu_lambda' or config.tipo_poblacion == 'mu+lambda':
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


def adjuntar_resultado(filepath: str, fitness_final: float, motores: List[List[int]], generacion: int, tiempo: float):
    with open(filepath, 'a+') as f:
        f.write(f'Mejor fitness final={fitness_final}\n')
        f.write(f'Mejor individuo final={motores}\n')
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
            f.write('Iteracion;Padre fitness;Hijo fitness;Padre motores;Hijo motores\n')  # Header del archivo
        elif config.tipo_poblacion == 'mu_lambda' or config.tipo_poblacion == 'mu+lambda':
            f.write('Iteracion;Mejor global fitness;Mejor poblacion fitness;Media fitness;Mejor global motores;Mejor poblacion motores\n')


def guardar_generacion_en_evolucion(filepath: str, generacion: int, poblacion, mejor_global=None):
    """
    Adjuntamos al archivo creado por guardar_evolucion() para añadir la información de la población
    """
    with open(filepath, 'a+') as f:
        if config.tipo_poblacion == '1+1':
            f.write(f'{generacion};{poblacion.individuos[0].fitness};{poblacion.individuos[1].fitness};{poblacion.individuos[0].motores};{poblacion.individuos[1].motores}\n')
        elif config.tipo_poblacion == 'mu_lambda' or config.tipo_poblacion == 'mu+lambda':
            mejor_poblacion = poblacion.get_mejor_individuo()
            f.write(f'{generacion};{mejor_global.fitness};{mejor_poblacion.fitness};{poblacion.get_media_fitness()};{mejor_global.motores};{mejor_poblacion.motores}\n')
            print("blablabla\n\n")
