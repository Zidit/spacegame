import math
import numpy as np

#import server
import gameObject
import logging

#return received arguments excluding the first one
class radar():
   def __init__(self, ship):
      self.ship = ship
      
      #Scan distance of the radar 
      self.range = 30000
      self.sector = 180
      #Power usage when on in watts
      self.power_consumption = 1000000
      self.powered = False
      self.power_factor = 1

   def parse(self, args):
      commands = {
      "on":self.powerOn,
      "off":self.powerOff,
      "scan":self.scan,
      "sector":self.setSector,
      "identify":self.identify,
      }
      try:
         return commands[args[1]](args)
      except:
         logging.exception('Radar exception')
         return("Error. Usage: radar scan/sector/on/off/identify\n"
                "output format:\n"
                "identifier: <range>(meters) <elevation>(degrees) <azimuth>(degrees)\n")

   def simulate(self, dt, power_factor):
      self.power_factor = power_factor

   def scan(self, args):
      if not self.powered:
         return "Radar is turned off"

      found_objects = []

     # eff_range = self.range * (180 / self.sector) * self.power_factor

      for obj in gameObject.objects:
      #   if obj.getDistanceTo(self.ship) < eff_range and self.ship.getAngleTo(obj, True) < self.sector: 
         if self.isInRange(obj):
            if obj != self.ship:
               found_objects.append(obj) 

      found_objects.sort(key=lambda tup: tup.getDistanceTo(self.ship))

      result = ""
      for i in found_objects:
         dist, azimuth, inclination = self.ship.getSphericalCoordinateTo(i, inDeg = True)
         result += "{}: {:06.3E} {:+06.1f} {:+06.1f}\n".format(i.identifier, dist, azimuth, inclination)

      return result

   def setSector(self, args):
      try:
         self.sector = np.clip(float(args[2]), 1, 180)
         return "sector set to: {0}".format(self.sector)
      except IndexError:
         return "{0}".format(self.sector)
      except:
         logging.exception("exception when setting secotr value")
         return "Error. Usage: radar sector {float = 1.0 ... 180.0}"

   def powerOn(self, args):
      self.powered = True
      return " "
   
   def powerOff(self, args):
      self.powered = False
      return " "

   def getPowerNeeded(self):
      if self.powered:
         return self.power_consumption
      else:
         return 0

   def isInRange(self, obj):
      eff_range = self.range * (180 / self.sector) * self.power_factor
      return obj.getDistanceTo(self.ship) < eff_range and self.ship.getAngleTo(obj, True) < self.sector

   def identify(self, args):
      if not self.powered:
         return "Radar is turned off"

      target = None

      for obj in gameObject.objects:
         if self.isInRange(obj) and obj.identifier == args[2]: 
            target = obj
            break
      
      if isinstance(target, gameObject.gameObject):
         dist, azimuth, inclination = self.ship.getSphericalCoordinateTo(target, inDeg = True)
         result = "{}: {:06.3E} {:+06.1f} {:+06.1f}\n".format(target.identifier, dist, azimuth, inclination)
         result += "mass: {:06.3E}\n".format(target.mass)
         result += "heading: "+ str(target.getHeading())
      else:
         return " "

      return result
