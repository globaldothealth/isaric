import sys
import json

with open(sys.argv[1]) as fp:
  data = json.load(fp)

its = {k: {"description": data["properties"][k]["description"], "$ref": "#/definitions/mapping"} for k in data["properties"]}

print(json.dumps(its, indent=2))
