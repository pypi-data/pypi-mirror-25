def validate_json_entry_types(types, entry):
  floats = types['floats']
  ints = types['ints']
  strs = types['strs']

  for k, v in entry.items():
    if v == None:
      if k in floats:
        entry[k] = 0.0
      elif k in ints:
        entry[k] = 0
      elif k in strs:
        entry[k] = ""

    if k in floats:
      entry[k] = float(entry[k])
    elif k in ints:
      entry[k] = int(entry[k])
    elif k in strs:
      entry[k] = str(entry[k])

  return entry

def format_date(t):
  return t.strftime("%Y-%m-%d")

def format_time(d):
  return d.strftime("%I:%M:%S %p")