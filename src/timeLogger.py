# import libraries we need
from configBase import ConfigBase
import time

class TimeLogger(ConfigBase):
  def configure(self):
    self.logDir = self.paths['log']
    self.startTime = None
    self.stopTime = None
    self.timing = False
    
  def start(self):
    if self.timing:
      print('Already timing')
      return
    
    self.timing = True
    self.startTime = time.time()
    
  # stops timer, logs by default
  def stop(self, log = True):
    if not self.timing:
      print('Not timing')
      return
    
    self.stopTime = time.time()
    self.timing = False
    elapsedSeconds = self.stopTime - self.startTime
    model = self.paths["model"].split("/")[-1]
    if log:
      f = open(f'{self.logDir}/ExecutionTime.txt', "a")
      f.write(f'{model}, {round(elapsedSeconds, 3)}\n')
      f.close()
    return elapsedSeconds
    
if __name__ == '__main__':
  TimeLogger()
