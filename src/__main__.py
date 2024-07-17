import logging
from argparse import ArgumentParser
import helm
import sources
import crds
import git
import index

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
  parser = ArgumentParser(
    prog='govuk-crd-fetch',
    description='Automatically fetches and formats CRDs for use with kubeconform and similar tools'
  )
  parser.add_argument(
    '-o', '--out-dir',
    default='out',
    help='Directory to output processed CRDs'
  )
  parser.add_argument(
    '-s', '--sources',
    default='sources.yaml',
    help='Path to sources.yaml'
  )

  args = parser.parse_args()

  config = sources.load(args.sources)
  logger.info("Loaded sources from file")
  all_crds = []
  for source in config:
    logger.debug("Processing source: %s", source)
    if source['kind'] == 'helm':
      source_crds = helm.process(
        source['repository'],
        source['chart'],
        source.get('version', 'latest'),
        source.get('values', None)
      )
    elif source['kind'] == 'git':
      source_crds = git.process(
        source['repository'],
        source['path'],
        source.get('revision', 'main')
      )
    else:
      logger.error("Unsupported source kind '%s'", source['kind'])
      exit(1)
    processed = crds.process(source_crds)
    crds.dump(args.out_dir, processed)
    all_crds.extend(processed)
  index.render_index_page(args.out_dir, all_crds)
