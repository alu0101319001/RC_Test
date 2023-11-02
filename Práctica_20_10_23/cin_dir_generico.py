#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Robótica Computacional
# Grado en Ingeniería Informática (Cuarto)
# Práctica: Resolución de la cinemática directa mediante Denavit-Hartenberg.

# Ejemplo:
# ./cdDH.py 30 45

import sys
import argparse
from math import *
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import file_reader as fr
import process_manipulator as pm

# ******************************************************************************
# Declaración de funciones

def ramal(I, prev=[], base=0):
    # Convierte el robot a una secuencia de puntos para representar
    O = []
    if I:
        if isinstance(I[0][0], list):
            for j in range(len(I[0])):
                O.extend(ramal(I[0][j], prev, base or j < len(I[0]) - 1))
        else:
            O = [I[0]]
            O.extend(ramal(I[1:], I[0], base))
            if base:
                O.append(prev)
    return O

def muestra_robot(O, ef=[]):
    # Pinta en 3D
    OR = ramal(O)
    OT = np.array(OR).T
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # Bounding box cúbico para simular el ratio de aspecto correcto
    max_range = np.array([OT[0].max() - OT[0].min(),
                          OT[1].max() - OT[1].min(),
                          OT[2].max() - OT[2].min()
                          ]).max()
    Xb = (0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][0].flatten()
          + 0.5 * (OT[0].max() + OT[0].min()))
    Yb = (0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][1].flatten()
          + 0.5 * (OT[1].max() + OT[1].min()))
    Zb = (0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][2].flatten()
          + 0.5 * (OT[2].max() + OT[2].min()))
    for xb, yb, zb in zip(Xb, Yb, Zb):
        ax.plot([xb], [yb], [zb], 'w')
    ax.plot3D(OT[0], OT[1], OT[2], marker='s')
    ax.plot3D([0], [0], [0], marker='o', color='k', ms=10)
    if not ef:
        ef = OR[-1]
    ax.plot3D([ef[0]], [ef[1]], [ef[2]], marker='s', color='r')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()
    return

def arbol_origenes(O, base=0, sufijo=''):
    # Da formato a los orígenes de coordenadas para mostrarlos por pantalla
    if isinstance(O[0], list):
        for i in range(len(O)):
            if isinstance(O[i][0], list):
                for j in range(len(O[i])):
                    arbol_origenes(O[i][j], i + base, sufijo + str(j + 1))
            else:
                print('(O' + str(i + base) + sufijo + ')0\t= ' + str([round(j, 3) for j in O[i]]))
    else:
        print('(O' + str(base) + sufijo + ')0\t= ' + str([round(j, 3) for j in O]))

def muestra_origenes(O, final=0):
    # Muestra los orígenes de coordenadas para cada articulación
    print('Orígenes de coordenadas:')
    arbol_origenes(O)
    if final:
        print('E.Final = ' + str([round(j, 3) for j in final]))

def matriz_T(d, theta, a, alpha):
    # Calcula la matriz T (ángulos de entrada en grados)
    th = theta * pi / 180
    al = alpha * pi / 180
    return [[cos(th), -sin(th) * cos(al), sin(th) * sin(al), a * cos(th)],
            [sin(th), cos(th) * cos(al), -sin(al) * cos(th), a * sin(th)],
            [0, sin(al), cos(al), d],
            [0, 0, 0, 1]
            ]

# ******************************************************************************
# Automatización de la introducción de los valores de las articulaciones
# Recibir manipulador por fichero
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=str, nargs='?', default='dh_1.txt')
args = parser.parse_args()
file_name = args.file
dh = fr.read_DH_file(file_name)
nvar = dh[0] # Número de variables

d, th, a, al = fr.replace_variables_with_values(dh[1], dh[2], dh[3], dh[4], dh[5])
print("d =", d)
print("th =", th)
print("a =", a)
print("al =", al)

# Valores D-H (d, theta, a, alpha)
dh_parameters = [
    [2, 0, 0, 0],
    [0, 45, 2, -90],
    [0, 0, 2, -90],
    [5, 0, 0, 0],
    [0, 0, 0, 0]
]

# Cálculo de matrices de transformación y orígenes
o00 = [0, 0, 0, 1]
o_prev = o00
o = []

for i in range(dh[6]):
    cd = d[i]
    cth = th[i]
    ca = a[i]
    cal = al[i]
    T = matriz_T(cd, cth, ca, cal)
    o_next = np.dot(T, o_prev)
    o.append(o_next.tolist())
    o_prev = o_next

print(o)
# Mostrar resultado de la cinemática directa
muestra_origenes([o00, o[0], o[1], o[2]])
muestra_robot([o00, o[0], o[1], o[2]])