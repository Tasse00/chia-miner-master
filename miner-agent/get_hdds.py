#!.venv/bin/python
from utils.diskutil import get_hdds

json_data = get_hdds()

import json
print( json.dumps(json_data))