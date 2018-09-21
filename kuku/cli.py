from docopt import docopt

from kuku.templates import load
from kuku.values import resolve
from kuku.generate import generate
from kuku.dump import dump


def cli():
    cli_docs = """kuku: Kubernetes templating tool.
    
    Usage:
      kuku apply [-f <FILE>]... [-s <key=value>]... <TEMPLATES_DIR> 
      kuku delete [-f <FILE>]... [-s <key=value>]... <TEMPLATES_DIR> 
      kuku generate [-f <FILE>]... [-s <key=value>]... <TEMPLATES_DIR> 
      kuku (-h | --help)
      
    Options:
      -h --help                     Show this screen.
      --version                     Show version 
      -s KEY=VALUE --set KEY=VALUE  Set values on the command line (accepts multiple options or separate values with commas: Ex: -s key1=val1,key2=val2)
      -f FILE --file FILE           Specify values in a YAML file (accepts multiple options)
      
    Notes:
      Resolution of values: --set overrides all values in --file. If multiple --file are specified then last one wins. 
    """

    # Parse cli.
    arguments = docopt(cli_docs)
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
