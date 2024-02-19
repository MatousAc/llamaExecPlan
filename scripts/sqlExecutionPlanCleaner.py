import re
import pyperclip as clip

text = clip.paste()

def cleanPlan(query):
  # rm unnecessary syntax
  query = re.sub(r'[ \t]*(\|(--)?)|(\[sauAttendance\]\.\[dbo\]\.)', '', query)
  # rm square brackets
  query = re.sub(r'\[([^\]]+)\]', r'\1', query)

  # remove unnecessary entities
  query = re.sub(r',? *RESIDUAL:.*?DEFINE:.*?\)', '', query)
  # query = re.sub(r',? *WHERE:\(PROBE\([^\)]*\)[^\)]*\)', '', query)
  query = re.sub(r',? *OPT_Bitmap\d+', '', query)
  query = re.sub(r'OBJECT:', '', query)
  # rm multiple parentheses
  query = re.sub(r'\(\(([^)]+)\)\)', r'(\1)', query)
  # collapse multiple \n
  print(query)
  query = query.replace('\n\n', '\n')
  query = query.replace('\n\n', '\n')
  print(query)
  # reverse and rm newlines
  steps = query.split('\n')[::-1]
  steps = [f'{num + 1}: {q}' for num, q in enumerate(steps)]
  query = ' # '.join(steps)
  return query

# cleaned output
out = cleanPlan(text)
print(out)

clip.copy(out)
