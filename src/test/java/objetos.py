from typing import Union
import json
import config
import random
import subprocess
from math import isclose
import numpy as np

PARAMETER_RANGES = (
(0.3, 1.2), (90, 110), (0.1, 5.0), (0.0001, 0.01), (1000, 3000), (400, 800), (0.1, 5.0), (0.0001, 0.01), (0, 400),
(150, 210))

# TODO Fit paths to each computer or if need other configs
command_line = '/usr/bin/env /usr/lib/jvm/java-11-openjdk-amd64/bin/java @/tmp/cp_7c0lmj2jd1cq9jhk4phi5edyk.argfile SkeletonMain'
cwd = '/home/cesar/Uni/AGE/e3/AGyE_final'

# Files' paths
rules_size = 10
files_config_path = "./individuals_configurations/ag1.txt"
files_result_path = "./experiments/ag1.json"

def save_individual(individual, sigmas, output_path):
    with open(output_path, "w+") as output_fd:
        for i, val in enumerate(individual):
            output_fd.write(str(float(val)))
            if i != len(individual) - 1:
                output_fd.write(", ")
        output_fd.write("\n")
        for j, sd in enumerate(sigmas):
            output_fd.write(str(sd))
            if j != len(sigmas) - 1:
                output_fd.write(", ")


def fit_individual(result_path):
    agent = open(result_path)
    agentData = json.load(agent)

    fitness = np.sum(agentData['times'])
    return fitness


class Individuo:
    
    def __init__(self, motores=None):
        if motores is None:
            # Queremos que el individuo nuevo creado empieze en un punto aleatorio de los
            self.motores = [[np.random.normal(random.uniform(*config.rango_de_inicializacion), config.sd), config.sd] for _ in range(config.num_motores)]
        else:
            self.motores = motores
            for i, (val, var) in enumerate(self.motores):
                self.motores[i] = [np.random.normal(val, var), var]

        self.fitness = float('inf')
        self.generacion_creada = -1  # Guarda la generación en la que se creó

    def __repr__(self):
        return "Fitness: " + str(self.fitness) + " | " + str(self.motores)


    def limitador(self, x, limits):
        toReturn = max(x,limits[0])
        toReturn = min(toReturn,limits[1])
        return toReturn

    def evaluarse(self):
        # Save individual
        angulos = []
        vars_ = []

        for i, (angulo, var) in enumerate(self.motores):
            angulos.append(angulo)
            vars_.append(var)
        save_individual(angulos, vars_, files_config_path)

        s = subprocess.check_output(command_line, shell=True, cwd=cwd)
        self.fitness = fit_individual(files_result_path)
    

    def update_motores(self):
        for i, (motor) in enumerate(self.motores):
            self.motores[i][0] = self.limitador(self.motores[i][0] + np.random.normal(0, self.motores[i][1]),PARAMETER_RANGES[i])


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

            nueva_var = escalar * var * np.exp(np.random.normal(0, config.tau))
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


class Poblacion_mu_lambda:
    def _init_(self):
        self.individuos = [Individuo() for _ in range(config.size_poblacion)]
        self.torneo = Torneo(self)
        self.lambda_ = config.lambda_

    def _str_(self):
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

    def crear_mutar_y_sustituir_lambda(self):
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
                motores_padres = [padre.motores[indice_motor][0] for padre in familia]
                nuevo_val = np.average(motores_padres)
                vars_padres = [padre.motores[indice_motor][1] for padre in familia]
                nuevo_var = random.choice(vars_padres)
                nuevos_motores.append([nuevo_val, nuevo_var])

            nuevo_individuo.motores = nuevos_motores

            # MUTACIÓN
            nuevo_individuo.update_motores()  # Motores se mutan según la distribución Gaussiana
            nuevo_individuo.update_vars_gauss()

            lambdas.append(nuevo_individuo)

        # lambdas está lleno de individuos nuevos
        # 2.5-2.6) Sustituir los lambda peores de la población original por la población lambda obtenida
        self.individuos = lambdas + self.individuos[self.lambda_:]


class Poblacion_mu_mas_lambda:
    def __init__(self):
        self.individuos = [Individuo(motores=self.get_starting_individual()) for _ in range(config.size_poblacion)]
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

    def get_starting_individual(self):
        with open('./individuals_configurations/ag_starting.txt', 'r') as f:
            read = f.readlines()
        read_split = read[0].split(', ')
        read_var_split = read[1].split(', ')
        starting_values = [[self.limitador(float(val), PARAMETER_RANGES[i]), float(var)] for i, (val, var) in enumerate(zip(read_split, read_var_split))]
        return starting_values

    def ordenar_poblacion(self):
        self.individuos.sort(key=lambda individuo: individuo.fitness, reverse=True)

    def get_mejor_individuo(self):
        return self.individuos[-1]

    def get_media_fitness(self):
        return np.average([individuo.fitness for individuo in self.individuos])

    def eliminar_lambda_peores(self):
        self.ordenar_poblacion()  # Se ordenan primero de peor a mejor
        self.individuos = self.individuos[self.lambda_:]


    def limitador(self, x, limits):
        toReturn = max(x,limits[0])
        toReturn = min(toReturn,limits[1])
        return toReturn
        
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
                nuevo_val = self.limitador(np.average([padre.motores[indice_motor][0] for padre in familia]), PARAMETER_RANGES[indice_motor])
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
