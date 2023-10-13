"""
Funciones para lectura de fichero que procese una entrada concreta
de un manipulador

Formato: 
  Numero articulaciones
  Numero elementos rigidos

  Lista Articulaciones
    [tipo, valor]
      ar = articulacion de revolucion --> valor = tita
      ap = articulacion prismatica --> valor: distancia

  Lista Elementos Rigidos
    [nombre, valor]
      nombre: lx
      valor: numero >= 0                  
"""

def read_manipulator_file(file_name):
  with open(file_name, 'r') as f:
    num_joints = int(f.readline())
    num_links = int(f.readline())
    joints = []
    links = []
    for i in range(num_joints):
      line = f.readline()
      line = line.split()
      if line[0] == 'ar':
        joint_type = 'r'
        joint_value = float(line[1])
      elif line[0] == 'ap':
        joint_type = 'p'
        joint_value = float(line[1])
      else:
        sys.exit('Error: articulacion no reconocida')
      joints.append([joint_type, joint_value])
    for j in range(num_links):
      line = f.readline()
      line = line.split()
      link_name = line[0]
      link_value =  line[1]
      links.append([link_name, link_value])

  manipulator = [joints, links]
  return manipulator

def read_DH_file(file_name):
  with open(file_name, 'r') as f:
    num_joints = int(f.readline())
    line = f.readline()
    d = line.split()
    d = [float(i) for i in d]
    line = f.readline()
    th = line.split()
    th = [float(i) for i in th]
    line = f.readline()
    a = line.split()
    a = [float(i) for i in a]
    line = f.readline()
    al = line.split()
    al = [float(i) for i in al]
  D_H = [num_joints, d, th, a, al]
  return D_H
    

