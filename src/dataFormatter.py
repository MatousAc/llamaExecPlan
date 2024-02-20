import pandas as pd, random
from configBase import ConfigBase

class DataFormatter(ConfigBase):
  def configure(self):
    self.dfCf = self.cp['dataFormatter']
    self.delim = self.dfCf['delim']
    self.inputTemplate = self.dfCf['inputTemplate']
    self.load()

  def load(self):
    if not self.quiet: print('Loading Data . . .')
    self.data = pd.read_csv(self.paths['data'])
    if not self.quiet: print(f'Results:\n{self.data.head()}')
  
  def getRow(self, row = None):
    if not row: row = random.randrange(len(self.data))
    return self.data.iloc[row]
  
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
    template = template.replace('<query>', self.getRow()['query'])
    template = template.replace('<execPlan>', '')
    return template.strip()

if __name__ == '__main__':
  df = DataFormatter()
  df.printHeader('Testing DataFormatter')
  print(df.getRow())
  print(df.getInferenceInput())
