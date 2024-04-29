import pandas as pd, random
from configBase import ConfigBase

class DataFormatter(ConfigBase):
  def configure(self):
    self.dfCf = self.cp['dataFormatter']
    self.delim = self.dfCf['delim']
    self.inputTemplate = self.dfCf['inputTemplate']
    self.continuationPrompt = self.dfCf['continuationPrompt']
    self.load()

  def load(self):
    if not self.quiet: print('Loading Data . . .')
    self.data = pd.read_csv(self.paths['data'])
    if not self.quiet: print(f'Results:\n{self.data.head()}')
  
  def getRow(self, row = None):
    if not row: row = random.randrange(len(self.data))
    return self.data.iloc[row]

  def getPrompt(self):
    '''returns a prompt for inference'''
    sampleMode = self.dfCf['sampleMode']
    match sampleMode:
      case 'generate':
        template = input(f'Press enter to generate or type continue to prompt the model to continue: ')
        if template.lower() == 'continue':
          template = 'Please continue with the next step of the execution plan. When you feel that you are done with the execution plan, make your last step be "Return Results"'
        else: template = self.inputTemplate
      case 'manual':
        template = input(f'You: ')
    prompt = self.fillTemplate(template, query = self.getRow()['query'])
    if sampleMode == 'generate' and not self.quiet: print(f'\r{prompt}')
    return prompt

  def fillTemplate(self, prompt, query):
    '''fills out a prompt template'''
    prompt = prompt.replace('<query>', query)
    prompt = prompt.replace('<execPlan>', '')
    prompt = prompt.strip()
    return prompt

if __name__ == '__main__':
  df = DataFormatter()
  df.printHeader('Testing DataFormatter')
  print(df.getRow())
  print(df.getPrompt())
