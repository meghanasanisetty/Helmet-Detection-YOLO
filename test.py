import yaml
with open("data.yaml") as f:
    print(yaml.safe_load(f))
