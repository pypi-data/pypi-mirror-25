import argparse

from salty import __version__
from salty.api import store, get_secret, new, add_secret, current, select


def keyfunc(args):
    if args.action == 'ls':
        for p, k in enumerate(store.keys):
            print("Key (%d) : %s" % (p, k))
        return

    if args.action == 'current':
        print(store.current)
        return

    if args.action == 'new':
        k = new()
        store.add_key(k)
        print(k.decode())
        return

    if args.action == 'set':
        print(args)
        if args.value is None and args.pos is None:
            raise ValueError("Either value or position should be provided")

        if args.value is not None:
            current(args.value)
            return

        if args.pos is not None:
            select(args.pos)
            return

    raise ValueError("Missing command %s" % args.action)


def messagefunc(args):
    for name, message in store.secrets.items():
        print("Message named (%s) : %s" % (name, message))


def encryption(args):
    add_secret(args.name, args.message)


def decryption(args):
    print(get_secret(args.name).decode())


def make_parser():
    parser = argparse.ArgumentParser(description='Salty password management tool (v%s).' % __version__)

    subparsers = parser.add_subparsers(help='Sub command list')

    key_parser = subparsers.add_parser('keys', help='Key sub command')

    key_parser.add_argument('action', nargs='?', default="ls", help='Action to perform available are (ls/current/new/set)')
    key_parser.add_argument('--value', required=False, help="Value for the command (optional depending on the command).")
    key_parser.add_argument('--pos', type=int, default=0, help="Position of the element on to operate.")
    key_parser.set_defaults(func=keyfunc)

    msg_parser = subparsers.add_parser('messages', help='List available messages')
    msg_parser.set_defaults(func=messagefunc)

    enc = subparsers.add_parser('encrypt', help='Encryption sub command')

    enc.add_argument('name', help="Name of the secret")
    enc.add_argument('message', help="Message for the secret")
    enc.set_defaults(func=encryption)

    dec = subparsers.add_parser('decrypt', help='Decryption sub command')

    dec.add_argument('name', help="Name of the secret")
    dec.set_defaults(func=decryption)

    return parser


def main():
    parser = make_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as e:
        parser.print_help()


if __name__ == "__main__":
    main()