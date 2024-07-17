import logging
from os import makedirs
from os.path import exists
import openapi2json

logger = logging.getLogger(__name__)

def process(crds):
  if len(crds) < 1:
    logger.error("No CRDs found")
    exit(1)
  
  logger.debug("Processing %s CRDs", len(crds))

  processed = []

  for crd in crds:
    group = crd['spec']['group']
    kind = crd['spec']['names']['kind'].lower()
    logger.debug("Processing CRD %s/%s", group, kind)
    versions = []
    for version in crd['spec']['versions']:
      version_name = version['name']
      logger.debug("Got version %s", version_name)
      schema = version['schema']['openAPIV3Schema']
      schema_json = openapi2json.schema_to_json(schema)
      versions.append({
        "name": version_name,
        "schema": schema_json
      })
    processed.append({
      "group": group,
      "kind": kind,
      "versions": versions
    })
  return processed

def dump(path, crds):
  for crd in crds:
    group = crd['group']
    kind = crd['kind']
    if not exists(f"{path}/{group}"):
      makedirs(f"{path}/{group}")
    for version in crd['versions']:
      version_name = version['name']
      file_name = f"out/{group}/{kind}_{version_name}.json"
      f = open(file_name, "w")
      f.write(version['schema'])
      f.close()
