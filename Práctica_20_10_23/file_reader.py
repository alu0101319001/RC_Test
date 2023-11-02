"""
Funciones para lectura de fichero que procese una entrada concreta
de un manipulador

Formato: 
  Numero Variables
  d ---> array
  th
  a
  al                  
"""
def read_DH_file(file_name):
  with open(file_name, 'r') as f:
    num_joints = int(f.readline())
    line = f.readline()
    d = line.split()
    d = [str(i) for i in d]
    line = f.readline()
    th = line.split()
    th = [str(i) for i in th]
    line = f.readline()
    a = line.split()
    a = [str(i) for i in a]
    line = f.readline()
    al = line.split()
    al = [str(i) for i in al]
    if not check_size(d, th, a, al):
      print("Error al leer el fichero DH: todas las filas no son del mismo tamaño")
      return -1
    p = []
    for i in range(num_joints):
       line = f.readline()
       p.append(float(line))

  dh_size = len(a)
  D_H = [num_joints, d, th, a, al, p, dh_size]
  return D_H

def check_size(d, th, a, al):
  return len(d) == len(th) == len(a) == len(al)
    
def replace_variables_with_values(d, th, a, al, p):
    # Itera a través de los cuatro arrays
    for i in range(len(d)):
        # Divide cada cadena en palabras
        d_words = d[i].split()
        th_words = th[i].split()
        a_words = a[i].split()
        al_words = al[i].split()
        
        # Reemplaza las variables "pX" por sus valores correspondientes de p
        for j in range(len(d_words)):
            if d_words[j].startswith("p"):
                variable_name = d_words[j]
                variable_index = int(variable_name[1:])  # Obtiene el número de la variable (p0, p1, etc.)
                d_words[j] = str(p[variable_index])
        
        for j in range(len(th_words)):
            if th_words[j].startswith("p"):
                variable_name = th_words[j]
                variable_index = int(variable_name[1:])
                th_words[j] = str(p[variable_index])
        
        for j in range(len(a_words)):
            if a_words[j].startswith("p"):
                variable_name = a_words[j]
                variable_index = int(variable_name[1:])
                a_words[j] = str(p[variable_index])
        
        for j in range(len(al_words)):
            if al_words[j].startswith("p"):
                variable_name = al_words[j]
                variable_index = int(variable_name[1:])
                al_words[j] = str(p[variable_index])
        
        # Reemplaza las cadenas originales por las cadenas modificadas
        d[i] = " ".join(d_words)
        th[i] = " ".join(th_words)
        a[i] = " ".join(a_words)
        al[i] = " ".join(al_words)
    
    # Convierte las cadenas a números float
    d = [float(value) for value in d]
    th = [float(value) for value in th]
    a = [float(value) for value in a]
    al = [float(value) for value in al]
    
    return d, th, a, al
