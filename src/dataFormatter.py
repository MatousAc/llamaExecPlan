from datasets import load_dataset
from configBase import ConfigBase

class DataFormatter(ConfigBase):
  def configure(self):
    self.dfCf = self.cp['dataFormatter']
    self.delim = self.dfCf['delim']
    self.inputTemplate = self.dfCf['inputTemplate']
    self.fxMux()
    self.load()

  def load(self):
    if not self.quiet: print('Loading Data . . .')
    dsDict = load_dataset(self.paths['data'])
    if not self.quiet: print(f'Results:\n{dsDict}')
  
  def getInferenceInput(self):
    '''returns a prompt for inference'''
    sampleMode = self.dfCf['sampleMode']
    match sampleMode:
      case 'generate':
        input()
        template = self.inputTemplate
      case 'manual':
        template = input(f'> ')
        print('↓')
    template = template.replace('<query>', self.getRandomQuery())
    template = template.replace('<execPlan>', '')
    return template.strip()

if __name__ == '__main__':
  df = DataFormatter()
  df.printHeader('Testing DataFormatter')
  print(df.getInputSample())
