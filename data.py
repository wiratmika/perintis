from ruamel import yaml

with open("data/indices.yaml", "r") as infile:
    indices = yaml.safe_load(infile)


def write(file, data):
    custom_dumper = yaml.YAML()
    custom_dumper.explicit_start = True
    custom_dumper.representer.ignore_aliases = lambda *data: True

    with open(f"data/{file}.yaml", "w") as outfile:
        custom_dumper.dump(data, outfile)
