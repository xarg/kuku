from docopt import docopt

from kuku.__version__ import __version__
from kuku.templates import load
from kuku.values import resolve
from kuku.generate import generate
from kuku.dump import dump
from kubernetes import config


def cli():
    cli_docs = """kuku: Kubernetes templating tool.
    
    Usage:
      kuku apply [-f <FILE>]... [-s <key=value>]... <TEMPLATES_DIR> 
      kuku delete [-f <FILE>]... [-s <key=value>]... <TEMPLATES_DIR> 
      kuku generate [-f <FILE>]... [-s <key=value>]... <TEMPLATES_DIR> 
      kuku (-h | --help)
      kuku --version
      
    Options:
      -h --help                     Show this screen.
      --version                     Show version.
      -s KEY=VALUE --set KEY=VALUE  Set values on the command line (accepts multiple options or separate values with commas: Ex: -s key1=val1,key2=val2).
      -f FILE --file FILE           Specify values in a YAML file (accepts multiple options).
      
    Notes:
      Resolution of values: --set overrides values in --file by merging. The last value wins.
    """

    # Parse cli.
    arguments = docopt(cli_docs, version=__version__)

    # Load k8s config
    config.load_kube_config()

    # Read templates
    templates = load(arguments["<TEMPLATES_DIR>"])
    # Resolve values
    context = resolve(arguments["--set"], arguments["--file"])
    # Render templates
    rendering = generate(context, templates)

    if arguments["generate"]:
        # print yaml
        print(dump(rendering))


if __name__ == "__main__":
    cli()
