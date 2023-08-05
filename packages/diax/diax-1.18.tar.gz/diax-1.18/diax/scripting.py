import argparse
import logging
import sys

import diax.log

def excepthook(_type, value, tb):
    import pdb
    import traceback
    traceback.print_exception(_type, value, tb)
    pdb.pm()

class ArgumentParserDiax(argparse.ArgumentParser):
    def parse_args(self):
        results = super().parse_args()
        if results.pdb:
            sys.excepthook = excepthook
        diax.log.setup(level=logging.DEBUG if results.verbose else logging.INFO)
        return results


def parser(*args, **kwargs):
    _parser = ArgumentParserDiax(*args, **kwargs)
    _parser.add_argument('--impersonate',
        dest='impersonate',
        help=("Impersonate another user in 3DIAX. This will only work if your user credentials "
            "are allowed to impersonate, otherwise login will fail entirely"),
    )
    _parser.add_argument('-e', '--env', '--environment',
        dest='environment',
        default='authentise.com',
        help=("The base URL of the environment to interact with. This should be something like "
            "'dev-auth.com' or 'authentise.com'. Service URLs will be built from this base"),
    )
    _parser.add_argument('-u', '--username',
        dest='username',
        help=("The username to use when logging in to 3DIAX"),
    )
    _parser.add_argument('-p', '--password',
        dest='password',
        help=("The password to use when logging in to 3DIAX"),
    )
    _parser.add_argument('--internal-token',
        dest='internal_token',
        help=("The internal token for the installation which grants superuser access"),
    )
    _parser.add_argument('--pdb',
        action='store_true',
        dest='pdb',
        help=("When provided, drop into a debugger on unhandled exception"),
    )
    _parser.add_argument('-v',
        action='store_true',
        dest='verbose',
        help=("When provided show more verbose logging"),
    )
    _parser.add_argument('--ssl-no-verify',
        action='store_true',
        dest='ssl_no_verify',
        help=("When provided do not verify SSL certificates. Useful for local dev work"),
    )
    _parser.add_argument('--certificate-bundle',
        default=None,
        dest='certificate_bundle',
        help=("When provided, use this certificate bundle to verify sSL"),
    )
    return _parser
