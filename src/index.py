from shutil import copyfile
from os.path import dirname, join
from jinja2 import Environment, FileSystemLoader

jinja = Environment(loader=FileSystemLoader(join(dirname(__file__), "templates")))

index_template = jinja.get_template("index.html")

def render_index_page(out_dir, data):
  reformatted_data = {}
  for crd in data:
    group = crd['group']
    if group not in reformatted_data:
      reformatted_data[group] = []
    reformatted_data[group].append(crd)
  index_file = index_template.render(all_crds=reformatted_data)
  f = open(join(out_dir, "index.html"), "w")
  f.write(index_file)
  f.close()
