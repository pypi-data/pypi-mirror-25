from simple_aws_lambda_maker.errors import NoFunctionsSpecified
from simple_aws_lambda_maker.maker import LambdaMaker

from textwrap import dedent

available_actions = {}

def an_action(func):
    available_actions[func.__name__] = func
    return func

@an_action
def help(collector, **kwargs):
    """List the available_tasks"""
    print("Available tasks to choose from are:")
    print("Use the --task option to choose one")
    print("")
    for name, action in sorted(available_actions.items()):
        print("--- {0}".format(name))
        print("----{0}".format("-" * len(name)))
        print("\n".join("\t{0}".format(line) for line in dedent(action.__doc__).split("\n")))
        print("")

@an_action
def deploy(collector, **kwargs):
    """Deploy our lambda functions"""
    dry_run = collector.configuration["salm"].dry_run
    functions = collector.configuration["functions"]
    if not functions:
        raise NoFunctionsSpecified()
    LambdaMaker(collector.configuration["functions"], dry_run=dry_run).fulfill()
