#!/usr/bin/env python3
import argparse
import os
import sys
from operator import itemgetter

import requests

desc = """Download task from UCCA-App and convert to a passage in standard format"""

DEFAULT_SERVER = "http://ucca.staging.cs.huji.ac.il"
API_PREFIX = "/api/v1/"
AUTH_TOKEN_ENV_VAR = "UCCA_APP_AUTH_TOKEN"


def main(args):
    auth_token = args.auth_token or os.environ[AUTH_TOKEN_ENV_VAR]
    headers = {"Authorization": "Token " + auth_token}
    task = requests.get(args.server_address + API_PREFIX + "user_tasks/" + str(args.passage_id), headers=headers).json()
    print(task)
    passage = task["passage"]
    passage_id = passage["id"]
    text = passage["text"]
    tokens = sorted(task["tokens"], key=itemgetter("start_index"))
    annotation_units = task["annotation_units"]


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description=desc)
    argparser.add_argument("passage_id", help="ID of passage to download and convert")
    argparser.add_argument("server_address", nargs="?", help="UCCA-App server", default=DEFAULT_SERVER)
    argparser.add_argument("--auth_token", help="specify authorization token, otherwise from" + AUTH_TOKEN_ENV_VAR)
    main(argparser.parse_args())
    sys.exit(0)
