from yaml import load_all, SafeLoader

# This fixes pyyaml crashing when it attempts to parse an unquoted '='
# https://github.com/yaml/pyyaml/issues/89
class PatchedSafeLoader(SafeLoader):
  yaml_implicit_resolvers = SafeLoader.yaml_implicit_resolvers.copy()
  yaml_implicit_resolvers.pop("=")

def safe_load_all(data):
  return load_all(data, Loader=PatchedSafeLoader)
