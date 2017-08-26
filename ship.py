#!/usr/bin/python3
import numpy as np
from pyquaternion import Quaternion

class ship():
   ##Ships physical properties
   #Mass in kg
   mass = 1000000.0
   #Thruster powers in N
   thruster_power_front = 100000.0
   thruster_power_back = 1000000.0

   #Ships current control settings
   thruster_front = 0.0
   thruster_back = 0.0

   #Ships position
   position = np.array([0.0, 0.0, 0.0])
   #Vector for telling where the ship is facing
   front = np.array([0.0, 0.0, 0.0])
   #Vector for telling  where ship is going
   velocity = np.array([0.0, 0.0, 0.0])

   def __init__(self):
      __init__(position)

   def __init__(self, position):
      self.commands = {
         'echo':self.echo,
         'thrust':self.thrust,
         'fthrust':self.fthrust
      }

      self.position = np.array(position)

   def simulate(self, dt):
      acceleration = np.array([0.0, 0.0, 0.0])
      acceleration[0] = (self.thruster_back * self.thruster_power_back - self.thruster_front * self.thruster_power_front) / self.mass
      self.velocity += acceleration * dt
      self.position += self.velocity * dt

   def echo(self,data):
      return str.join(' ', data)
