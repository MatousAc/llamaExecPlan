import re
import pyperclip as clip

text = clip.paste()

def cleanPlan(query):
  # 1. rm square brackets
  query = re.sub(r'\[([^\]]+)\]', r'\1', query)
  # 2. rm unnecessary syntax
  query = re.sub(r'[ \t]*(\|(--)?)|(sauAttendance\.dbo\.)', '', query)
  query = re.sub(r'attendanceDB\.dbo\.([a-zA-Z]+)\.PK__?[a-zA-Z]+(?:__)?\w*', r'\1', query)
  query = re.sub(r'attendanceDB\.dbo\.(\w+) as (\w+)', r'\1 as \2', query)

  # 3. remove unnecessary entities
  query = re.sub(r',? *residual:.*?define:.*?\)', '', query, flags = re.I)
  query = re.sub(r',? *opt_bitmap\d+,?', '', query, flags = re.I)
  query = re.sub(r'object:', r'', query, flags = re.I)
  # 4. clean up 'N' in front of strings
  query = re.sub(r"N('[^']+')", r'\1', query, flags = re.I)
  # 5. rm multiple parentheses
  query = re.sub(r'\(\(([^)]+)\)\)', r'(\1)', query)
  # 6. rm empty f(x)s
  query = re.sub(r',?[a-zA-Z]+:\(\)', r'', query)
  
  # 7. reverse and rm line breaks
  steps = query.split('\r\n')[::-1]
  steps = [f'{num + 1}: {q}' for num, q in enumerate(steps)]
  query = '\\n# '.join(steps)
  query = '# ' + query

  # 8. rm extra specifiers
  return query

# cleaned output
out = cleanPlan(text)
print(out)

clip.copy(out)
