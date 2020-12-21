import argparse
from lib.payloads_engine import generate_payloads
from lib.payloads_engine import run_payloads
from lib.args_validation import validate_argparser
from lib.tcp import get_ip_address


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--rhosts',
                        type=str,
                        help='rhosts used by metasploit exploit')

    args = parser.parse_args()

    if validate_argparser(args):
        exit(0)

    generate_payloads({'LHOST': get_ip_address(),
                       'RHOSTS': args.rhosts})

    artifacts = run_payloads()


if __name__ == "__main__":
    main()
