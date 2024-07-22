# govuk-crd-library

A tool to automatically fetch and process CRDs
for use with kubeconform.

## How it works

The fetcher tool takes a list of repositories to scan and outputs a
directory with the CRDs found converted to JSON OpenAPI schemas
for use with tools such as kubeconform.
It also generates an HTML index page which lists the available schemas.

This repo also contains a GitHub Actions workflow which runs the
fetcher tool and uploads the result to GitHub Pages.

## Usage

### Running the fetcher locally

#### With Nix

1. Start a shell
   ```
   nix-shell
   ```
2. Run the fetcher
   ```
   python src -s sources.yaml -o out
   ```
#### Without Nix

1. Ensure Python 3, Git and Helm are installed
2. Set up the virtualenv
   ```
   python -m venv env
   pip install -r requirements.txt
   ```
3. Run the fetcher
   ```
   python src -s sources.yaml -o out
   ```

### Adding new CRD sources

The repositories and charts scanned for CRDs is specified in `sources.yaml`.
There is an example entry for both Git and Helm repositories in `sources.example.yaml`.

#### Helm

Helm charts are rendered using `helm template` before being scanned for CRDs.
Some charts require values to be specified for it to render CRDs.
This can be done by providing the values in the form of a YAML string in the `values` key.

#### Git

Git repositories are cloned, then immediately scanned for CRDs.
If the CRDs are templated or require additional processing before being consumed,
this tool will not be able to parse them. 
In this case, if a Helm chart is also provided, that should be used instead.
