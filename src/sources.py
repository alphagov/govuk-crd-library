from yaml import safe_load

def load(path):
  f = open(path, "r")
  data = f.read()
  f.close()

  return safe_load(data)
