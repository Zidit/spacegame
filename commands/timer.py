class timer():
   def __init__(self):
      self.time = 0

   def simulate(self, dt, power_factor):
      self.time += dt

   def parse(self,args):
      return str(self.time)
