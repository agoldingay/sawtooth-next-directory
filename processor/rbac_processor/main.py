# Copyright 2017 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------

import argparse
import sys

from sawtooth_sdk.processor.core import TransactionProcessor
from sawtooth_sdk.processor.log import init_console_logging


from rbac_processor.handler import RBACTransactionHandler


def parse_args(args):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
        '-v',
        '--verbosity',
        action='count',
        help="The logging level.")

    parser.add_argument(
        "validator_endpoint",
        nargs='?',
        default='tcp://localhost:4004',
        help="The validator's component address.")

    return parser.parse_args(args)


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    opts = parse_args(args)
    processor = None
    try:
        processor = TransactionProcessor(url=opts.validator_endpoint)

        init_console_logging(verbose_level=opts.verbosity)

        handler = RBACTransactionHandler()

        processor.add_handler(handler)

        processor.start()
    except KeyboardInterrupt:
        pass
    except Exception as exe:  # pylint: disable=broad-except
        print("Error: {}".format(exe), file=sys.stderr)
    finally:
        if processor is not None:
            processor.stop()
