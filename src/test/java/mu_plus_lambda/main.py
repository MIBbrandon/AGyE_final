# P2 - Estrategias evolutivas
import copy
import time

from objetos import Individuo, Poblacion_1_mas_1, Poblacion_mu_lambda, Poblacion_mu_mas_lambda
import config
import saver


def main():
    # Primero queremos recordar la configuración usada (será ajustado para la estrategia elegida)
    saver.config_saver(config.config_filepath)
    # También abriremos un archivo en el que se guardará la evolución de la población
    saver.guardar_evolucion(config.evolucion_filepath)
    # Queremos el tiempo de ejecución
    start_time = time.time()

    if config.tipo_poblacion == "mu+lambda":
        # Estrategia (mu+lambda)

        mejor_individuo_global = Individuo()

        # 1) Generar aleatoriamente un vector de números reales y sus varianzas. Las varianzas tomarán valores grandes
        poblacion = Poblacion_mu_mas_lambda()

        # EXTRA) Hacer una evaluación inicial
        for i, individuo in enumerate(poblacion.individuos):
            poblacion.individuos[i].evaluarse()

        # 2) Repetir hasta cumplir criterio de convergencia
        generacion = 1
        convergencia = False
        while not convergencia and generacion <= config.max_generaciones:
            print(f"Generación {generacion}:")
            print(f"Mejor individuo global: {mejor_individuo_global}")
            # 2.2-2.3) Crear lambda individuos y añadir
            poblacion.crear_mutar_y_anadir_lambda()

            # EXTRA2) Evaluamos la población entera
            for i, individuo in enumerate(poblacion.individuos):
                poblacion.individuos[i].evaluarse()

            # Ordenamos la población
            poblacion.ordenar_poblacion()

            # Si el mejor de población es mejor que el mejor global, sustituir
            mejor_individuo_poblacion = poblacion.get_mejor_individuo()

            print(poblacion, "\n")

            # Guardamos la información de la población
            saver.guardar_generacion_en_evolucion(config.evolucion_filepath, generacion, poblacion,
                                                  mejor_individuo_global)

            if mejor_individuo_poblacion.fitness < mejor_individuo_global.fitness:
                print("Nuevo mejor individuo global")
                mejor_individuo_global = copy.deepcopy(mejor_individuo_poblacion)
                mejor_individuo_global.generacion_creada = generacion

            # 2.4) Eliminar los lambda peores individuos
            poblacion.eliminar_lambda_peores()

            # Pasamos a una nueva generación
            generacion += 1

        # 3) Producir como resultado el mejor individuo de la población resultante
        print(mejor_individuo_global)

    end_time = time.time()
    saver.adjuntar_resultado(config.config_filepath, mejor_individuo_global.fitness, mejor_individuo_global.motores,
                             mejor_individuo_global.generacion_creada, end_time - start_time)


if __name__ == '__main__':
    main()
