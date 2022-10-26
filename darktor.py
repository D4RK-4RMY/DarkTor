#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import getopt
from requests import get
import subprocess
import time
import signal
from stem import Signal
from stem.control import Controller
from packaging import version
from pystyle import *

VERSION = "1.2"

IP_API = "https://api.ipify.org/?format=json"

LATEST_RELEASE_API = "https://api.github.com/repos/D4RK-4RMY/DarkTor/releases/latest"


def clear_console():
    os.system('clear')


clear_console()


class bcolors:

    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[31m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    BGRED = '\033[41m'
    WHITE = '\033[37m'


def t():
    current_time = time.localtime()
    ctime = time.strftime('%H:%M:%S', current_time)
    return '[' + ctime + ']'


def sigint_handler(signum, frame):
    print("User interrupt ! shutting down")
    stop_torghost()


def logo():
    os.system('clear')
    #print(bcolors.RED + bcolors.BOLD)
    print("""
\033[92m                 ,:          
\033[92m          .      ::           
\033[92m          .:    :2.           
\033[92m           .:,  1L            
\033[92m            .v: Z, ..::,      
\033[92m             :k:N.Lv:         
\033[97m              22ukL           
\033[97m              JSYk.           
\033[97m             ,B@B@i           
\033[97m             BO@@B@.          
\033[97m           :B@L@Bv:@7         
\033[97m         .PB@iBB@  .@Mi       
\033[97m       .P@B@iE@@r  . 7B@i     
\033[97m      5@@B@:NB@1\033[0m\033[95m r  ri:\033[0m\033[97m7@M    
\033[97m    .@B@BG.OB@B\033[0m\033[95m  ,.. .i,\033[0m\033[97m MB,  
\033[97m    @B@BO.B@@B\033[0m\033[95m  i7777,\033[0m\033[97m    MB. 
\033[97m   PB@B@.OB@BE\033[0m\033[95m  LririL,.L.\033[0m\033[97m @P \033[0m\033[91m ╔╦╗╔═╗╦═╗╦╔═╔╦╗╔═╗╦═╗         \033[0m
\033[97m   B@B@5iB@B@i\033[0m\033[95m  :77r7L, L7\033[0m\033[97m O@ \033[0m\033[91m  ║║╠═╣╠╦╝╠╩╗ ║ ║ ║╠╦╝         \033[0m
\033[97m   @B1B27@B@B,\033[0m\033[95m . .:ii.  r7\033[0m\033[97m BB \033[0m\033[91m ═╩╝╩ ╩╩╚═╩ ╩ ╩ ╚═╝╩╚═         \033[0m      
\033[97m   O@.@M:B@B@:\033[0m\033[95m v7:    ::.\033[0m\033[97m  BM \033[0m\033[91m                               \033[0m
\033[97m   :Br7@L5B@BO\033[0m\033[95m irL: :v7L.\033[0m\033[97m P@, \033[0m\033[91m  By © 1ucif3r | 2022          \033[0m
\033[97m    7@,Y@UqB@B7\033[0m\033[95m ir ,L;r:\033[0m\033[97m u@7  \033[0m\033[91m A Anonymization Script        \033[0m
\033[97m     r@LiBMBB@Bu\033[0m\033[95m   rr:.\033[0m\033[97m:B@i   \033[0m\033[91m        v1.2                   \033[0m
\033[97m       FNL1NB@@@@:   ;OBX     \033[0m\033[91m
\033[97m         rLu2ZB@B@@XqG7      
\033[92m            . rJuv:: 
""".format(V=VERSION))
    print(bcolors.ENDC)

def usage():
    logo()
    print("""
   \033[91mDarkTor usage:\033[0m

    \033[97m-s    --start       Start DarkTor\033[0m
    \033[97m-r    --switch      Request new tor exit node\033[0m
    \033[97m-x    --stop        Stop DarkTor\033[0m
    \033[97m-h    --help        For Help and Exit\033[0m
    \033[97m-u    --update      check for update\033[0m


    """)
    sys.exit()


def ip():
    while True:
        try:
            jsonRes = get(IP_API).json()
            ipTxt = jsonRes["ip"]
        except:
            continue
        break
    return ipTxt


def check_root():
    if os.geteuid() != 0:
        print("You must be root; Say the magic word 'sudo'")
        sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)

TorrcCfgString = \
    """
VirtualAddrNetwork 10.0.0.0/10
AutomapHostsOnResolve 1
TransPort 9040
DNSPort 5353
ControlPort 9051
RunAsDaemon 1
"""

resolvString = 'nameserver 127.0.0.1'

Torrc = '/etc/tor/darktorrc'
resolv = '/etc/resolv.conf'


def start_darktor():
    print(t() + ' Always check for updates using -u option')
    os.system('sudo cp /etc/resolv.conf /etc/resolv.conf.bak')
    if os.path.exists(Torrc) and TorrcCfgString in open(Torrc).read():
        print(t() + ' Torrc file already configured')
    else:

        with open(Torrc, 'w') as myfile:
            print(t() + ' Writing torcc file ')
            myfile.write(TorrcCfgString)
            print(bcolors.GREEN + '[done]' + bcolors.ENDC)
    if resolvString in open(resolv).read():
        print(t() + ' DNS resolv.conf file already configured')
    else:
        with open(resolv, 'w') as myfile:
            print(t() + ' Configuring DNS resolv.conf file.. '),
            myfile.write(resolvString)
            print(bcolors.GREEN + '[done]' + bcolors.ENDC)

    print(t() + ' Stopping tor service '),
    os.system('sudo systemctl stop tor')
    os.system('sudo fuser -k 9051/tcp > /dev/null 2>&1')
    print(bcolors.GREEN + '[done]' + bcolors.ENDC)
    print(t() + ' Starting new tor daemon '),
    os.system('sudo -u debian-tor tor -f /etc/tor/darktorrc > /dev/null'
              )
    print(bcolors.GREEN + '[done]' + bcolors.ENDC)
    print(t() + ' setting up iptables rules'),

    iptables_rules = \
        """
	NON_TOR="192.168.1.0/24 192.168.0.0/24"
	TOR_UID=%s
	TRANS_PORT="9040"

	iptables -F
	iptables -t nat -F

	iptables -t nat -A OUTPUT -m owner --uid-owner $TOR_UID -j RETURN
	iptables -t nat -A OUTPUT -p udp --dport 53 -j REDIRECT --to-ports 5353
	for NET in $NON_TOR 127.0.0.0/9 127.128.0.0/10; do
	 iptables -t nat -A OUTPUT -d $NET -j RETURN
	done
	iptables -t nat -A OUTPUT -p tcp --syn -j REDIRECT --to-ports $TRANS_PORT

	iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
	for NET in $NON_TOR 127.0.0.0/8; do
	 iptables -A OUTPUT -d $NET -j ACCEPT
	done
	iptables -A OUTPUT -m owner --uid-owner $TOR_UID -j ACCEPT
	iptables -A OUTPUT -j REJECT
	""" \
        % subprocess.getoutput('id -ur debian-tor')

    os.system(iptables_rules)
    print(bcolors.GREEN + '[done]' + bcolors.ENDC)
    print(t() + ' Fetching current IP...')
    print(t() + ' CURRENT IP : ' + bcolors.GREEN + ip() + bcolors.ENDC)


def stop_darktor():
    print(bcolors.RED + t() + 'STOPPING DarkTor.....' + bcolors.ENDC)
    print(t() + ' Flushing iptables, resetting to default'),
    os.system('mv /etc/resolv.conf.bak /etc/resolv.conf')
    IpFlush = \
        """
	iptables -P INPUT ACCEPT
	iptables -P FORWARD ACCEPT
	iptables -P OUTPUT ACCEPT
	iptables -t nat -F
	iptables -t mangle -F
	iptables -F
	iptables -X
	"""
    os.system(IpFlush)
    os.system('sudo fuser -k 9051/tcp > /dev/null 2>&1')
    print(bcolors.GREEN + '[done]' + bcolors.ENDC)
    print(t() + ' Restarting Network manager'),
    os.system('service network-manager restart')
    print(bcolors.GREEN + '[done]' + bcolors.ENDC)
    print(t() + ' Fetching current IP...')
    time.sleep(3)
    print(t() + ' CURRENT IP : ' + bcolors.GREEN + ip() + bcolors.ENDC)


def switch_tor():
    print(t() + ' Please wait...')
    time.sleep(7)
    print(t() + ' Requesting new circuit...'),
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
    print(bcolors.GREEN + '[done]' + bcolors.ENDC)
    print(t() + ' Fetching current IP...')
    print(t() + ' CURRENT IP : ' + bcolors.GREEN + ip() + bcolors.ENDC)


def check_update():
    print(t() + ' Checking for update...')
    jsonRes = get(LATEST_RELEASE_API).json()
    newversion = jsonRes["tag_name"][1:]
    print(newversion)
    if version.parse(newversion) > version.parse(VERSION):
        print(t() + bcolors.GREEN + ' New update available!' + bcolors.ENDC)
        print(t() + ' Your current DarkTor version : ' + bcolors.GREEN + VERSION + bcolors.ENDC)
        print(t() + ' Latest DarkTor version available : ' + bcolors.GREEN + newversion + bcolors.ENDC)
        yes = {'yes', 'y', 'ye', ''}
        no = {'no', 'n'}

        choice = input(
            bcolors.BOLD + "Would you like to download latest version and install from Git repo? [Y/n]" + bcolors.ENDC).lower()
        if choice in yes:
            os.system(
                'cd /tmp && git clone  https://github.com/D4RK-4RMY/DarkTor')
            os.system('cd /tmp/darktor && sudo ./install.sh')
        elif choice in no:
            print(t() + " Update aborted by user")
        else:
            print("Please respond with 'yes' or 'no'")
    else:
        print(t() + " DarkTor is up to date!")



def main():
    check_root()
    if len(sys.argv) <= 1:
        check_update()
        usage()
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'srxhu', [
            'start', 'stop', 'switch', 'help', 'update','credit'])
    except (getopt.GetoptError):
        usage()
        sys.exit(2)
    for (o, a) in opts:
        if o in ('-h', '--help'):
            usage()
        elif o in ('-s', '--start'):
            start_darktor()
        elif o in ('-x', '--stop'):
            stop_darktor()
        elif o in ('-r', '--switch'):
            switch_tor()
        elif o in ('-u', '--update'):
            check_update()
        else:
            usage()


if __name__ == '__main__':
    main()
