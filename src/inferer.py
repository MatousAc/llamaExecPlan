# import libraries we need
import torch, re, sys, pandas as pd
from transformers import AutoModelForCausalLM, BitsAndBytesConfig, AutoTokenizer
from configBase import ConfigBase
from dataFormatter import DataFormatter
from timeLogger import TimeLogger

class Inferer(ConfigBase):
  # a srtring variable that holds the conversation throughout inference
  conversation = ''
  
  def configure(self):
    self.timer = TimeLogger()

  def loadModel(self):
    # quantized LoRA (QLoRA) - uses 4-bit normal float to lighten GPU/CPU load
    self.bnbConfig = BitsAndBytesConfig(
      load_in_4bit = True,
      # we leave the model quantized in 4 bits
      bnb_4bit_quant_type = 'nf4',
      bnb_4bit_compute_dtype = torch.float16
    )
    # load our model
    self.model = AutoModelForCausalLM.from_pretrained(
      pretrained_model_name_or_path=self.paths['model'],
      quantization_config=self.bnbConfig,
      device_map='auto'
    )
    self.model.config.use_cache = False

    # load our tokenizer
    self.tokenizer = AutoTokenizer.from_pretrained(self.paths['model'])
    self.tokenizer.pad_token = self.tokenizer.eos_token

  def detokenize(self, tokens):
    with torch.no_grad():
      return self.tokenizer.decode(tokens, skip_special_tokens=True)
  
  def extendConversation(self, nextPrompt):
    # initial prompt
    if not self.conversation:
      self.systemPrompt = open('sysPrompt.txt').read()
      self.conversation = f'<s>[INST] <<SYS>>\n{self.systemPrompt}\n<</SYS>>\n\n{nextPrompt} [/INST]'
    else: self.conversation += f'\n</s><s>[INST] {nextPrompt} [/INST]'
  
  def clearConverstaion(self):
    self.conversation = ''
  
  # testing the models
  def inference(self, prompt):
    self.extendConversation(prompt)
    modelInput = self.tokenizer(self.conversation, return_tensors='pt').to('cuda')

    self.timer.start()
    self.model.eval()
    with torch.no_grad(): # grad only used in training
      tokens = self.model.generate(**modelInput, max_new_tokens=100)[0]
      response = self.detokenize(tokens).split('[/INST]')[-1]
      self.timer.stop()
      self.conversation += response
      if not self.quiet: print(f'Llama: {response}')
    return response
  
  def inferenceLoop(self):
    self.printHeader('Testing Loop')
    print('Ctrl+C to exit')
    try:
      while True: self.inference(self.dataFormatter.getPrompt())
    except KeyboardInterrupt: self.printHeader('Closing')
    except: raise # rethrow
  
  def evalGen(self):
    output = pd.DataFrame(columns = ['query', 'sqlPlan', 'llamaPlan'])
    resultsRe = r'Return(\sResults)?'
    stepRe = r'\n(?P<stepNum>\d{1,2}).?\s(?P<stepText>[^-\n]*)'
    templ = self.dataFormatter.inputTemplate
    for _, row in self.dataFormatter.data.iterrows():
      nextPrompt = self.dataFormatter.fillTemplate(templ, row['query'])
      fullLlamaOutput = ''
      latestOutput = self.inference(nextPrompt)
      
      maxStepNum = 0
      runsLeft = 7 # prompt the model to continue up to 7 times
      while re.search(resultsRe, latestOutput) == None and runsLeft > 0:
        # don't continue if the model is not producing further steps
        stepNums = [int(m[0]) for m in re.findall(stepRe, latestOutput)]
        if len(stepNums) == 0: break # model is not doing hot, abort
        currMaxStep = max(stepNums)
        # ensure we keep increasing with steps
        if maxStepNum >= currMaxStep: break
        else:
          maxStepNum = currMaxStep
          fullLlamaOutput += latestOutput
        nextPrompt = self.dataFormatter.continuationPrompt.replace('<nextStep>', f'{maxStepNum + 1}')
        latestOutput = self.inference(nextPrompt)
        runsLeft -= 1
      matches = [f'#{m[0]} {m[1]}' for m in re.findall(stepRe, fullLlamaOutput)]
      matches = [m.split('):')[0] if m.find('):') != -1 else m for m in matches]
      steps = ' '.join(matches)
      output.loc[len(output)] = [row['query'], row['sqlPlan'], steps]
      self.clearConverstaion() # start over
    output.to_csv(self.basePath + '/data/out/generatedPlans.csv', index = False)

if __name__ == '__main__':
  df = DataFormatter()
  inferer = Inferer(dataFormatter=df)
  # must first loadModel()
  inferer.loadModel()
  if len(sys.argv) <= 1: inferer.inferenceLoop()
  else:
    cmd = sys.argv[1].lower().replace('-', '')
    if cmd == 'evalgen':
      inferer.evalGen()
