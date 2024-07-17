from json import dumps

# Stolen from https://github.com/yannh/kubeconform/blob/master/scripts/openapi2jsonschema.py
def replace_int_or_string(data):
  new = {}
  try:
    for k, v in iter(data.items()):
      new_v = v
      if isinstance(v, dict):
        if "format" in v and v["format"] == "int-or-string":
          new_v = {"oneOf": [{"type": "string"}, {"type": "integer"}]}
        else:
          new_v = replace_int_or_string(v)
      elif isinstance(v, list):
        new_v = list()
        for x in v:
          new_v.append(replace_int_or_string(x))
      else:
        new_v = v
      new[k] = new_v
    return new
  except AttributeError:
    return data
    
def schema_to_json(data):
  data = replace_int_or_string(data)
  return dumps(data, indent=2)
