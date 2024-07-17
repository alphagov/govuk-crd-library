import logging
import subprocess
from os import listdir
from os.path import exists, isdir
from shutil import rmtree
from crdyaml import safe_load_all

logger = logging.getLogger(__name__)

def find_yaml_files(path):
  logger.debug("Finding yaml files in %s", path)
  files = []
  for file in listdir(path):
    full_path = f"{path}/{file}"
    if isdir(full_path):
      files.extend(find_yaml_files(full_path))
    else:
      if full_path.endswith(".yaml") or full_path.endswith(".yml"):
        with open(full_path, "r") as f:
          contents = f.read()
        files.append(safe_load_all(contents))
  return files


def process(repo, path, revision):
  if exists("/tmp/crd_gen_git"):
    rmtree("/tmp/crd_gen_git")
  logger.debug("Starting git clone for %s", repo)
  git_command = [
    "git", "clone",
    "--depth", "1",
    "-b", revision,
    repo,
    "/tmp/crd_gen_git"
  ]
  logger.debug("Git command: %s", git_command)
  git_run = subprocess.run(git_command, capture_output=True)
  git_stderr = git_run.stderr.decode("utf-8")
  if git_run.returncode != 0:
    logger.error("Git command errored during clone: %s", git_stderr)
    exit(1)
  
  search_path = f"/tmp/crd_gen_git/{path}"
  files = find_yaml_files(search_path)
  logger.debug("Found %s yaml files", len(files))

  crds = []
  for file in files:
    for resource in file:
      if resource and 'kind' in resource and resource['kind'] == 'CustomResourceDefinition':
        crds.append(resource)
  logger.debug("Got %s CRDs", len(crds))

  return crds
