# import libraries we need
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from configBase import ConfigBase
from dataFormatter import DataFormatter
from timeLogger import TimeLogger

class Inferer(ConfigBase):
  def configure(self):
    self.timer = TimeLogger()

  def loadModel(self):
    # load our model
    self.model = AutoModelForCausalLM.from_pretrained(
      pretrained_model_name_or_path=self.paths['model'],
      device_map='auto'
    )
    self.model.config.use_cache = False

    # load our tokenizer
    self.tokenizer = AutoTokenizer.from_pretrained(self.paths['model'])
    self.tokenizer.pad_token = self.tokenizer.eos_token

  def detokenize(self, tokens):
    with torch.no_grad():
      return self.tokenizer.decode(tokens, skip_special_tokens=True)
    
  # testing the models
  def inference(self):
    inferenceInput = self.dataFormatter.getInferenceInput()
    modelInput = self.tokenizer(inferenceInput, return_tensors='pt').to('cuda')

    self.timer.start()
    self.model.eval()
    with torch.no_grad(): # grad only used in training
      tokens = self.model.generate(**modelInput, max_new_tokens=100)[0]
      print(self.detokenize(tokens))
    self.timer.stop()
    
    print('~' * int(self.vw * 1.3))
  
  def inferenceLoop(self):
    self.printHeader('Testing Loop')
    print('Ctrl+C to exit')
    self.df = DataFormatter()
    try:
      while True: self.inference()
    except KeyboardInterrupt: print('\rClosing\n')
    except: raise # rethrow


if __name__ == '__main__':
  df = DataFormatter()
  trainer = Inferer(dataFormatter=df)
  # must first loadModel()
  trainer.loadModel()
  trainer.inferenceLoop()
