
import argparse, os
from openCashPeerClient.utils.pow import POWGenerator

def runProg():
    args = parser.parse_args()
    args.func(args)

def init(args):
    if args.no_gen is True:
        print('init() called with --no-gen flag')
    else:
        print('init() called without --no-gen flag')

def genkey(args):
    print('genkey() called for key length {} and email {}'.format(args.keylen, args.email))

def listkeys(args):
    print('listkeys() called')

def genPow(args):
    powGenerator = POWGenerator(args.key, args.difficulty, args.cores)
    result = powGenerator.getSolution()
    print('The solution is {}'.format(result))

## COMMAND LINE PURSER
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()
# init subcommand
init_cmd = subparsers.add_parser('init', help='Create new, fresh file structure')
init_cmd.set_defaults(func=init)
init_cmd.add_argument('--no-gen', action='store_true', help='If set does not generate new \
    key pair')
# genkey subcommand
genkey_cmd = subparsers.add_parser('genkey', help='Generate new key pair')
genkey_cmd.set_defaults(func=genkey)
genkey_cmd.add_argument('keylen', type=int, choices=[1024, 2048])
genkey_cmd.add_argument('email', default=None)
# listkeys subcommand
listkeys_cmd = subparsers.add_parser('listkeys', help='List the existing keys')
listkeys_cmd.set_defaults(func=listkeys)
# gen-pow subcommand
pow_cmd = subparsers.add_parser('gen-pow', help='Create proof of work')
pow_cmd.add_argument('--cores', type=int, choices = range(1, 65), help='How many cores to use',
    default=1, metavar='<1-64>')
pow_cmd.add_argument('difficulty', type=int, choices=range(1, 21), help='How many leading zeros \
    at pow', metavar='<1-20>')
pow_cmd.add_argument('key', help='The gpg key fingerprint')
pow_cmd.set_defaults(func=genPow)


if __name__=='__main__':
    runProg()


