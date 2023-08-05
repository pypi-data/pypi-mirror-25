from delfick_logging import lc

from contextlib import contextmanager
import subprocess
import itertools
import requests
import tempfile
import zipfile
import logging
import shutil
import boto3
import json
import os

log = logging.getLogger("simple_aws_lambda_maker.maker")

@contextmanager
def a_temp_dir():
    try:
        d = tempfile.mkdtemp()
        yield d
    finally:
        if os.path.exists(d):
            shutil.rmtree(d)

def extract_zip_contents(contents, directory):
    with tempfile.NamedTemporaryFile() as fle:
        fle.write(contents)
        fle.flush()

        with zipfile.ZipFile(fle.name) as z:
            z.extractall(path=directory)

class LambdaMaker(object):
    def __init__(self, functions, dry_run=False):
        self.functions = functions
        self.dry_run = dry_run

    def fulfill(self):
        for region, functions in self.functions_by_region:
            client = boto3.client('lambda', region_name=region)
            log.info(lc("Finding existing lambda functions", region=region))
            existing = dict(self.find_functions(client))
            for function in functions:
                if function.name in existing:
                    self.modify(client, function, existing[function.name])
                else:
                    self.create(client, function)

    def find_functions(self, client):
        marker = None
        while True:
            kwargs = {}
            if marker:
                kwargs["Marker"] = marker
            found = client.list_functions(**kwargs)
            for function in found["Functions"]:
                yield function["FunctionName"], function

            marker = found.get("NextMarker")
            if not marker:
                break

    @property
    def functions_by_region(self):
        getter = lambda f: f.region
        functions = sorted(self.functions, key=getter)
        return itertools.groupby(functions, getter)

    def modify(self, client, into, existing):
        new_conf = {k: v for k, v in into.configuration.items() if k not in ("Publish", "Tags")}
        old_conf = {k: v for k, v in existing.items() if k in new_conf}

        new_tags = into.configuration["Tags"]
        old_tags = client.list_tags(Resource=existing['FunctionArn'])["Tags"]

        code_difference = ""
        with into.code_options() as code:
            location = client.get_function(FunctionName=into.name)["Code"]["Location"]
            res = requests.get(location)
            with a_temp_dir() as parent:
                extract_zip_contents(res.content, directory=os.path.join(parent, "existing"))
                extract_zip_contents(code["ZipFile"], directory=os.path.join(parent, "new"))

                # Ideally I'd use python to do this, but it's not straight forward :(
                p = subprocess.run("diff -u -r ./existing ./new", cwd=parent, shell=True, stdout=subprocess.PIPE)
                code_difference = p.stdout.decode()

            if new_tags != old_tags or new_conf != old_conf or code_difference:
                self.print_header("CHANGING FUNCTION: {0}".format(into.name))
                self.print_difference(new_conf, old_conf)
                self.print_difference({"Tags": new_tags}, {"Tags": old_tags})

                if code_difference:
                    print()
                    print(code_difference)

            if not self.dry_run:
                if code_difference:
                    client.update_function_code(FunctionName=into.name, **code)
                if new_conf != old_conf:
                    client.update_function_configuration(**new_conf)
                if new_tags != old_tags:
                    client.tag_resource(Resource=existing["FunctionArn"], Tags=new_tags)
                    missing = set(old_tags) - set(new_tags)
                    if missing:
                        client.untag_resource(Resource=existing["FunctionArn"], TagKeys=list(missing))

    def create(self, client, into):
        self.print_header("NEW FUNCTION: {0}".format(into.name))
        configuration = dict(into.configuration)
        self.print_difference(configuration, {})
        with into.code_options() as code:
            configuration["Code"] = code
            if not self.dry_run:
                client.create_function(**configuration)

    def print_difference(self, into, frm):
        def printed(val):
            dumped = json.dumps(val, sort_keys=True, indent=4).split('\n')
            if len(dumped) == 1:
                return dumped[0]
            else:
                return "\n\t{0}".format("\n\t".join(dumped))

        for key, val in into.items():
            if key not in frm:
                print("+ {0} = {1}".format(key, printed(val)))
            elif frm[key] != val:
                print("M {0}\n\tWAS = {1}\n\tINTO = {2}".format(key, printed(frm[key]), printed(val)))

        for key, val in frm.items():
            if key not in into:
                print("- {0}".format(key))

    def print_header(self, text):
        print()
        print(text)
        print("=" * len(text))
