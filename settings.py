import sys
import yaml

with open(sys.argv[1]) as f:
    config = yaml.load(f)