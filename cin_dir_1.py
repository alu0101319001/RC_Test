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
import lectura_fichero as lf

# ******************************************************************************
# Declaración de funciones

def ramal(I,prev=[],base=0):
  # Convierte el robot a una secuencia de puntos para representar
  O = []
  if I:
    if isinstance(I[0][0],list):
      for j in range(len(I[0])):
        O.extend(ramal(I[0][j], prev, base or j < len(I[0])-1))
    else:
      O = [I[0]]
      O.extend(ramal(I[1:],I[0],base))
      if base:
        O.append(prev)
  return O

def muestra_robot(O,ef=[]):
  # Pinta en 3D
  OR = ramal(O)
  OT = np.array(OR).T
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')
  # Bounding box cúbico para simular el ratio de aspecto correcto
  max_range = np.array([OT[0].max()-OT[0].min()
                       ,OT[1].max()-OT[1].min()
                       ,OT[2].max()-OT[2].min()
                       ]).max()
  Xb = (0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten()
     + 0.5*(OT[0].max()+OT[0].min()))
  Yb = (0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten()
     + 0.5*(OT[1].max()+OT[1].min()))
  Zb = (0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten()
     + 0.5*(OT[2].max()+OT[2].min()))
  for xb, yb, zb in zip(Xb, Yb, Zb):
     ax.plot([xb], [yb], [zb], 'w')
  ax.plot3D(OT[0],OT[1],OT[2],marker='s')
  ax.plot3D([0],[0],[0],marker='o',color='k',ms=10)
  if not ef:
    ef = OR[-1]
  ax.plot3D([ef[0]],[ef[1]],[ef[2]],marker='s',color='r')
  ax.set_xlabel('X')
  ax.set_ylabel('Y')
  ax.set_zlabel('Z')
  plt.show()
  return

def arbol_origenes(O,base=0,sufijo=''):
  # Da formato a los origenes de coordenadas para mostrarlos por pantalla
  if isinstance(O[0],list):
    for i in range(len(O)):
      if isinstance(O[i][0],list):
        for j in range(len(O[i])):
          arbol_origenes(O[i][j],i+base,sufijo+str(j+1))
      else:
        print('(O'+str(i+base)+sufijo+')0\t= '+str([round(j,3) for j in O[i]]))
  else:
    print('(O'+str(base)+sufijo+')0\t= '+str([round(j,3) for j in O]))

def muestra_origenes(O,final=0):
  # Muestra los orígenes de coordenadas para cada articulación
  print('Orígenes de coordenadas:')
  arbol_origenes(O)
  if final:
    print('E.Final = '+str([round(j,3) for j in final]))

def matriz_T(d,theta,a,alpha):
  # Calcula la matriz T (ángulos de entrada en grados)
  th=theta*pi/180;
  al=alpha*pi/180;
  return [[cos(th), -sin(th)*cos(al),  sin(th)*sin(al), a*cos(th)]
         ,[sin(th),  cos(th)*cos(al), -sin(al)*cos(th), a*sin(th)]
         ,[      0,          sin(al),          cos(al),         d]
         ,[      0,                0,                0,         1]
         ]
# ******************************************************************************
"""
# Recibir manipulador por fichero
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=str, nargs='?', default='manipulador_1.txt')
parser.add_argument("-ft", "--file_type", type=str, nargs='?', default='manipulator')
args = parser.parse_args()

file_name = args.file
file_type = args.file_type
if file_type == "manipulator":
  manipulator = lf.read_manipulator_file(file_name)
  print(manipulator)
elif file_type == "dh":
  dh = lf.read_DH_file(file_name)
  print(dh)

# Parametros D-H:
d = dh[1]
th = dh[2]
a = dh[3]
al = dh[4]

# Orígenes para cada articulacion
origins = []
for i in range(dh[0] + 1):
  point_name = "o" + str(i) + str(i)
  p = [point_name, [0,0,0,1]]
  origins.append(p)
print(origins)

# Calculo matrices transformacion
matrix_T = np.array()
for i in range(dh[0]):
  matrix_name = "T" + str(i) + str(i+1)
  matrix_T.append([matrix_name, matriz_T(d[i],th[i],a[i],al[i])])
for j in range(dh[0] - 1):
   
"""
  

# Introducción de los valores de las articulaciones
nvar=3 # Número de variables
print(sys.argv)
if len(sys.argv) != nvar+1:
  sys.exit('El número de articulaciones no es el correcto ('+str(nvar)+')')
p=[float(i) for i in sys.argv[1:nvar+1]]

# Parámetros D-H:
#        1     2      3
d  = [   5,    0,     0]
th = [p[0],   90, -p[2]]
a  = [   0, p[1],     2]
al = [   0,  -90,     0]

# Orígenes para cada articulación
o00=[0,0,0,1]
o11=[0,0,0,1]
o22=[0,0,0,1]
o33=[0,0,0,1]
# Cálculo matrices transformación
T01=matriz_T(d[0],th[0],a[0],al[0])
T12=matriz_T(d[1],th[1],a[1],al[1])
T23=matriz_T(d[2],th[2],a[2],al[2])
T13=np.dot(T12, T23)
T02=np.dot(T01,T12)
T03=np.dot(T01,T13)

# Transformación de cada articulación
o10 =np.dot(T01, o11).tolist()
o20 =np.dot(T02, o22).tolist()
o30 =np.dot(T03, o33).tolist()

# Mostrar resultado de la cinemática directa
muestra_origenes([o00,o10,o20,o30])
muestra_robot   ([o00,o10,o20,o30])
input()


