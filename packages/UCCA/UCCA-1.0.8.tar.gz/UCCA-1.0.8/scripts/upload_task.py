#!/usr/bin/env python3
import argparse
import sys

desc = """Convert a passage file to JSON format and upload to UCCA-App as a completed task"""

# https://github.com/omriabnd/UCCA-App/blob/master/UCCAApp_REST_API_Reference.pdf
# ucca-demo.cs.huji.ac.il or ucca.staging.cs.huji.ac.il
# upload the parse as a (completed) task:
# 0. decide which project and user you want to assign it to
# 1. POST passage (easy format)
# 2. POST task x (of type tokenization)
# 3. PUT task x (submit)
# 4. POST task y (of type annotation with parent x; this is the more complicated format)
# 5. PUT task y (submit)


def main(args):
    pass


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description=desc)
    argparser.add_argument("filename", help="passage file name to convert and upload")
    argparser.add_argument("server_address", help="URL of UCCA-App server", default="http://ucca.staging.cs.huji.ac.il")
    main(argparser.parse_args())
    sys.exit(0)
