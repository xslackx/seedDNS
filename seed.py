from seedDNS import seedDNS as sd
from asyncio import run
import argparse

def main():
    opt = argparse.ArgumentParser(description='seedDNS', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    opt.add_argument('-s', "--host", help='DNS server address', required=True)
    opt.add_argument('-m', "--mode", help='0 to asyncio mode or 1 to sync mode', required=True)
    opt.add_argument('-t', "--type", help='Type of DNS message', required=True) 
    user_options = vars(opt.parse_args())
    seed = sd()
    print('Downloading csv data...\n')
    seed.top1m()
    print('Formating the data...\n')
    seed.fmtfile()
    print('Starting the consult in DNS')
    seed.consult(user_options["host"], user_options["mode"], user_options["type"] )
    
main()