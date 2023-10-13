import sys
from math import *
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def define_D_H(manipulator)
  joints = manipulator[0]
  links = manipulator[1]
  d = []
  th = []
  a = []
  al = []
  