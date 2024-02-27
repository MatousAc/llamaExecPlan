# import libraries we need
import torch
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
      systemPrompt = open('sysPrompt.txt').read()
      self.conversation = f'<s>[INST] <<SYS>>\n{systemPrompt}\n<</SYS>>\n\n{nextPrompt} [/INST]'
    else: self.conversation += f' </s><s>[INST] {nextPrompt} [/INST]'
  
  # testing the models
  def inference(self):
    nextPrompt = self.dataFormatter.getPrompt()
    self.extendConversation(nextPrompt)
    modelInput = self.tokenizer(self.conversation, return_tensors='pt').to('cuda')

    self.timer.start()
    self.model.eval()
    with torch.no_grad(): # grad only used in training
      tokens = self.model.generate(**modelInput, max_new_tokens=100)[0]
      response = self.detokenize(tokens).split('[/INST]')[-1]
      self.timer.stop()
      self.conversation += response
      print(f'Llama: {response}')
  
  def inferenceLoop(self):
    self.printHeader('Testing Loop')
    print('Ctrl+C to exit')
    try:
      while True: self.inference()
    except KeyboardInterrupt: self.printHeader('Closing')
    except: raise # rethrow


if __name__ == '__main__':
  df = DataFormatter()
  trainer = Inferer(dataFormatter=df)
  # must first loadModel()
  trainer.loadModel()
  trainer.inferenceLoop()
