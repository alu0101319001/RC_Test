import sys
from math import cos, sin, pi
import numpy as np

def forward_kinematics(dh_parameters):
    # Número de articulaciones
    num_joints = dh_parameters[0]
    # Parametros D-H:
    all_d = dh_parameters[1]
    all_th = dh_parameters[2]
    all_a = dh_parameters[3]
    all_al = dh_parameters[4]
    
    # Inicializar la lista de coordenadas de articulaciones
    joint_coordinates = []
    
    # Inicializar la matriz de transformación homogénea
    T = np.identity(4)
    
    for i in range(1, num_joints + 1):
        d = all_d[i - 1]
        theta = all_th[i - 1]
        a = all_a[i - 1]
        alpha = all_al[i - 1]
        
        # Convertir ángulos de grados a radianes
        theta = theta * pi / 180
        alpha = alpha * pi / 180
        
        # Matriz de transformación homogénea para la articulación i
        A = np.array([
            [cos(theta), -sin(theta) * cos(alpha), sin(theta) * sin(alpha), a * cos(theta)],
            [sin(theta), cos(theta) * cos(alpha), -cos(theta) * sin(alpha), a * sin(theta)],
            [0, sin(alpha), cos(alpha), d],
            [0, 0, 0, 1]
        ])
        
        # Multiplicar la matriz actual por la matriz de transformación de la articulación i
        T = np.dot(T, A)
        
        # Guardar las coordenadas de la articulación en el sistema de coordenadas 0
        joint_coordinates.append(T[:3, 3])
    
    return joint_coordinates
  