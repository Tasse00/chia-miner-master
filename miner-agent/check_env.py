#!.venv/bin/python

import os
import json
import pathlib
dirpath = os.path.dirname(__file__)
version = pathlib.Path(os.path.join(dirpath, "version")).read_text()


print(json.dumps({
    "version": version
}))
