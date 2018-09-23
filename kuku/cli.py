import sys

from docopt import docopt
from kubernetes import config

from kuku.__version__ import __version__
from kuku.dump import dump
from kuku.render import render
from kuku.templates import find
from kuku.values import resolve


def cli():
    """kuku: Kubernetes templating tool.
    
    Usage:
      kuku apply [-v] [-f <FILE>]... [-s <key=value>]... <TEMPLATES_DIR>
      kuku delete [-v] [-f <FILE>]... [-s <key=value>]... <TEMPLATES_DIR>
      kuku generate [-v] [-f <FILE>]... [-s <key=value>]... <TEMPLATES_DIR>
      kuku (-h | --help)
      kuku --version

    Options:
      -h --help                     Show this screen.
      -v --verbose                  Dump debug info to stderr.
      --version                     Show version.
      -s KEY=VALUE --set KEY=VALUE  Set values on the command line (accepts multiple options or separate values with commas: Ex: -s key1=val1,key2=val2).
      -f FILE --file FILE           Specify values in a YAML file (accepts multiple options).

    Notes:
      Resolution of values: --set overrides values in --file by merging. The last value wins.
    """

    # Parse cli arguments from docstring
    arguments = docopt(str(cli.__doc__), version=__version__)

    # Load k8s config -- needed to the correct API versions of k8s
    config.load_kube_config()

    # Find all templates
    try:
        templates = find(arguments["<TEMPLATES_DIR>"])
    except ValueError as e:
        print(e)
        exit(1)
        raise

    try:
        # Resolve values
        context = resolve(arguments["--set"], arguments["--file"])
    except ValueError as e:
        print(e)
        exit(1)
        raise

    # Render templates with resolved context
    rendering = render(context, templates)

    output = dump(rendering)
    if arguments["generate"]:
        # print yaml
        print(output)

    if arguments["apply"]:
        print("Not implemented yet. Use kuku generate ... | kubectl apply -f-")
        exit(1)

    if arguments["delete"]:
        print("Not implemented yet. Use kuku generate ... | kubectl delete -f-")
        exit(1)

    if arguments["--verbose"]:
        print(output, file=sys.stderr)


if __name__ == "__main__":
    cli()
