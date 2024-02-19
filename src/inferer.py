# import libraries we need
import torch
from transformers import AutoModelForCausalLM, BitsAndBytesConfig, AutoTokenizer
from configBase import ConfigBase
from dataFormatter import DataFormatter
from timeLogger import TimeLogger

class Inferer(ConfigBase):
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
    self.baseModel = AutoModelForCausalLM.from_pretrained(
      pretrained_model_name_or_path=self.paths['base'],
      quantization_config=self.bnbConfig,
      device_map='auto'
    )
    self.baseModel.config.use_cache = False

    # load our tokenizer
    self.tokenizer = AutoTokenizer.from_pretrained(self.paths['base'])
    self.tokenizer.pad_token = self.tokenizer.eos_token

  def detokenize(self, tokens):
    with torch.no_grad():
      return self.tokenizer.decode(tokens, skip_special_tokens=True)
    
  # testing the models
  def inference(self):
    inferenceInput = self.dataFormatter.getInferenceInput(self.df)
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
