import math
from typing import Union
import json
import config
import random
import requests
from math import isclose
import numpy as np

files_result_path = [
    "./experiments/ag1.json",
    "./experiments/ag2.json"
    ]

def fit_individual(result_path):
    agent = open(result_path)
    agentData = json.load(agent)

    fitness = np.sum(agentData['times'])
    return fitness


def limitador(val):
    while val > 360:
        val -= 360
    while val < 0:
        val += 360
    return val

def angulo_medio(angulos):
    assert all([0 <= angulo <= 360 for angulo in angulos])

    # Primero convertimos los ángulos a radianes
    rad_angulos = [math.radians(angulo) for angulo in angulos]

    media_sen = np.average([np.sin(rad_angulo) for rad_angulo in rad_angulos])
    media_cos = np.average([np.cos(rad_angulo) for rad_angulo in rad_angulos])

    to_return = limitador(math.degrees(np.arctan2(media_sen, media_cos)))
    return to_return


def funcion_local(motores):
    res = float('inf')
    if config.version == 1:
        res = 0
        for i, (angulo, var) in enumerate(motores):
            if config.num_motores == 4:
                angulo_objetivo = config.angulos_optimos_4[i]
            elif config.num_motores == 10:
                angulo_objetivo = config.angulos_optimos_10[i]
            res += (angulo - angulo_objetivo)**2
    elif config.version == 2:
        res = abs(sum([angulo for angulo, var in motores]) - config.suma_total)
    elif config.version == 3:
        res = abs(np.prod([angulo for angulo, var in motores]) - config.prod_total)
    if config.ruido:
        res += abs(np.random.normal(0, config.sd_ruido))
    return res


class Individuo:
    def __init__(self, motores=None):
        if motores is None:
            # Queremos que el individuo nuevo creado empieze en un punto aleatorio de los
            self.motores = [[limitador(np.random.normal(random.uniform(*config.rango_de_inicializacion), config.sd)), config.sd] for _ in range(config.num_motores)]
        else:
            self.motores = motores
        self.fitness = float('inf')
        self.generacion_creada = -1  # Guarda la generación en la que se creó

    def __repr__(self):
        return "Fitness: " + str(self.fitness) + " | " + str(self.motores)

    def evaluarse(self):
        result = fit_individual(files_result_path[0])
        r = result
        self.fitness = r

    def update_motores(self):
        # Damos nuevos valores a los motores según una distribución Gaussiana alrededor del valor que ya tienen
        for i, motor in enumerate(self.motores):
            self.motores[i][0] = limitador(self.motores[i][0] + np.random.normal(0, self.motores[i][1]))
        # pass

    def update_vars_un_quinto(self, incrementar: bool):
        for i, (angulo, var) in enumerate(self.motores):
            if not incrementar:
                # Varianza decrece
                new_var = var * config.c
            else:
                # Varianza crece
                new_var = var / config.c
            self.motores[i] = [angulo, new_var]

    def update_vars_gauss(self):
        # Nuevas varianzas obtenidas según esquema Gaussiano
        for i, (angulo, var) in enumerate(self.motores):
            escalar = 1
            if config.escalar_vector_resultante:
                escalar = np.exp(np.random.normal(0, config.tau_null))

            # Aplicaremos un limitador a las varianzas, pues sin ella salen varianzas exageradas
            nueva_var = limitador(escalar * var * np.exp(np.random.normal(0, config.tau)))
            self.motores[i] = [angulo, nueva_var]

    def varianzas_nulas(self):
        """
        Determina si las varianzas son nulas (es decir, que ya está muy cerca de la solución)
        :return:
        """
        for angulo, var in self.motores:
            if not isclose(var, 0, abs_tol=0.01):
                return False
        return True

    def boost_varianzas(self):
        for i, (angulo, var) in enumerate(self.motores):
            self.motores[i] = [angulo, config.sd * config.boost_proporcion]



class Poblacion_mu_mas_lambda:
    def __init__(self):
        self.individuos = [Individuo() for _ in range(config.size_poblacion)]
        self.torneo = Torneo(self)
        self.lambda_ = config.lambda_

    def __str__(self):
        return f"\tPeor individuo: {self.individuos[0]}\n" \
               f"\t75%: {self.individuos[int(len(self.individuos)*0.25)]}\n" \
               f"\t50%: {self.individuos[int(len(self.individuos) * 0.5)]}\n" \
               f"\t25%: {self.individuos[int(len(self.individuos) * 0.75)]}\n" \
               f"\tTop 5:\n" \
                    f"\t\t{self.individuos[-5]}\n" \
                    f"\t\t{self.individuos[-4]}\n" \
                    f"\t\t{self.individuos[-3]}\n" \
                    f"\t\t{self.individuos[-2]}\n" \
                    f"\t\t{self.individuos[-1]}\n" \
               f"\tMejor individuo: {self.individuos[-1]}"

    def ordenar_poblacion(self):
        self.individuos.sort(key=lambda individuo: individuo.fitness, reverse=True)

    def get_mejor_individuo(self):
        return self.individuos[-1]

    def get_media_fitness(self):
        return np.average([individuo.fitness for individuo in self.individuos])

    def eliminar_lambda_peores(self):
        self.ordenar_poblacion()  # Se ordenan primero de peor a mejor
        self.individuos = self.individuos[self.lambda_:]

    def crear_mutar_y_anadir_lambda(self):
        # 2.3-2.4) Crear lambda individuos
        lambdas = []  # Guardamos los individuos lambda
        while len(lambdas) < self.lambda_:
            # CREACIÓN
            nuevo_individuo = Individuo()  # Nuevo individuo al que le daremos nuevos valores de motores y varianzas
            familia = []  # Individuos que compondrán la familia
            for _ in range(config.size_familia):
                familia.append(self.torneo.obtener_ganador())

            # Ahora calculamos los nuevos valores de los motores del hijo con la media de los padres y las varianzas
            nuevos_motores = []
            for indice_motor in range(config.num_motores):
                nuevo_val = angulo_medio([padre.motores[indice_motor][0] for padre in familia])
                nuevo_var = random.choice([padre.motores[indice_motor][1] for padre in familia])
                nuevos_motores.append([nuevo_val, nuevo_var])

            nuevo_individuo.motores = nuevos_motores

            # MUTACIÓN
            nuevo_individuo.update_motores()  # Motores se mutan según la distribución Gaussiana
            nuevo_individuo.update_vars_gauss()

            lambdas.append(nuevo_individuo)

        # lambdas está lleno de individuos nuevos
        # 2.5-2.6) Añadir los lambda peores de la población original por la población lambda obtenida
        self.individuos += lambdas




class Torneo:
    def __init__(self, poblacion: Union[Poblacion_mu_lambda, Poblacion_mu_mas_lambda]):
        self.poblacion = poblacion  # Referencia a la población, no copia
        self.size_torneo = config.size_torneo

    def obtener_ganador(self):
        participantes = [random.choice(self.poblacion.individuos) for _ in range(self.size_torneo)]
        ganador = min(participantes, key=lambda x: x.fitness)
        return ganador
