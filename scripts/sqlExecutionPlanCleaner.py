import re
import pyperclip as clip

text = clip.paste()

def cleanPlan(query):
  # rm unnecessary syntax
  query = re.sub(r'[ \t]*(\|--)|(\[sauAttendance\]\.\[dbo\]\.)', '', query)
  # rm square brackets
  query = re.sub(r'\[([^\]]+)\]', r'\1', query)

  # remove unnecessary entities
  query = re.sub(r',? *RESIDUAL:.*?DEFINE:.*?\)', '', query)
  query = re.sub(r',? *WHERE:\(PROBE\([^\)]*\)[^\)]*\)', '', query)
  query = re.sub(r',? *OPT_Bitmap\d+', '', query)
  query = re.sub(r'OBJECT:', '', query)
  # rm multiple parentheses
  query = re.sub(r'\(\(([^)]+)\)\)', r'(\1)', query)

  return query

# cleaned output
out = cleanPlan(text)
print(out)

clip.copy(out)
