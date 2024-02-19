import os
from transformers import AutoModelForCausalLM, AutoTokenizer

# get base directory path
repo = 'llamaExecPlan'
basePath = f'{os.getcwd().split(repo)[0]}{repo}'
basePath = os.path.normpath(basePath)
print(basePath)

# get model source and dest from user
modelSource = input('hf model name: ')
modelDestination = os.path.normpath(basePath + '/' + input("model folder name: "))
print(f'saving {modelSource} to {modelDestination}')

# download and save models
model = AutoModelForCausalLM.from_pretrained(modelSource)
tokenizer = AutoTokenizer.from_pretrained(modelSource)
model.save_pretrained(modelDestination)
tokenizer.save_pretrained(modelDestination)
