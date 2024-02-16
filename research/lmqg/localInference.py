# this does not work with the current model
from pprint import pprint
from lmqg import TransformersQG

model_location = "/home/ac/code/aqg/models/llama-hf/7b"


# initialize model
model = TransformersQG(model_location)
# paragraph to generate pairs of question and answer
context = "William Turner was an English painter who specialised in watercolour landscapes. He is often known " \
          "as William Turner of Oxford or just Turner of Oxford to distinguish him from his contemporary, " \
          "J. M. W. Turner. Many of Turner's paintings depicted the countryside around Oxford. One of his " \
          "best known pictures is a view of the city of Oxford from Hinksey Hill."
# model prediction
question_answer = model.generate_qa(context)
# the output is a list of tuple (question, answer)
pprint(question_answer)
[
    ('Who was an English painter who specialised in watercolour landscapes?', 'William Turner'),
    ('What is another name for William Turner?', 'William Turner of Oxford'),
    ("What did many of William Turner's paintings depict around Oxford?", 'the countryside'),
    ('From what hill is a view of the city of Oxford taken?', 'Hinksey Hill.')
]