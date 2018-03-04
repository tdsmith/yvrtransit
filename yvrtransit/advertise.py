from glob import glob
import os
from os.path import basename

import click
import jinja2


@click.command()
@click.option("--repository", type=click.Path(exists=True), default=os.curdir,
              help="Path to data repository")
def advertise(repository):
    rollups = sorted(basename(i) for i in glob(os.path.join(repository, "*.zip")))
    dailies = sorted(basename(i) for i in glob(os.path.join(repository, "*.tar.xz")))

    template_path = os.path.join(
        os.path.dirname(__file__),
        "front_page.html")

    with open(template_path, "r") as f:
        template = jinja2.Template(f.read())

    print(template.render(rollups=rollups, dailies=dailies))
