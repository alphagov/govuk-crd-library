import logging
import subprocess
from crdyaml import safe_load_all

logger = logging.getLogger(__name__)



def process(repo, chart, version, values):
  logger.debug("Starting helm template for %s@%s", chart, version)

  if values:
    logger.debug("Writing values file")
    values_file = open("/tmp/crds_gen_values.yaml", "w")
    values_file.write(values)
    values_file.close()
  else:
    logger.debug("No values specified")
  
  crds = []

  helm_command = [
    "helm", "template",
    "--include-crds",
    "--repo", repo,
    "crd-gen",
    chart
  ]

  if version != "latest":
    helm_command.extend([
      "--version", version
    ])

  if values:
    helm_command.extend([
      "--values", "/tmp/crds_gen_values.yaml"
    ])

  logger.debug("Helm command: %s", helm_command)
  
  helm_run = subprocess.run(helm_command, capture_output=True)
  helm_stdout = helm_run.stdout.decode("utf-8")
  helm_stderr = helm_run.stderr.decode("utf-8")

  if helm_run.returncode != 0:
    logger.error("Helm errored during template: %s", helm_stderr)
    exit(1)
  
  resources = safe_load_all(helm_stdout)

  for resource in resources:
    if resource and resource['kind'] == 'CustomResourceDefinition':
      crds.append(resource)
  
  logger.debug("Got %s CRDs", len(crds))

  return crds
