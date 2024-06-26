#!/ usr / bin / env python
import argparse
import textwrap
import socket
import sys
from tunnel import Tunnel
def main () :
parser = argparse . ArgumentParser (
formatter_class = argparse . RawDescriptionHelpFormatter ,
description = textwrap . dedent ( '''\A VPN - like server / client that utilizes a user specified one time pad for the XOR ' ing of network traffic over a TAP
interface .
''') ,
epilog = textwrap . dedent ( '''\
Examples :
To start a server listening on default settings ,
naclshuttle -S -K ~/ random . bin
If that server 's IP is 192.168.1.1 , and you have the same
keyfile
in your home directory , you can connect to it using ,
naclshuttle -K ~/ random . bin -A 192.168.1.1 --tap - addr 10.8.0.2
'''))
parser . add_argument (' -S ', '-- server ', action =" store_true ", dest = 'server ',
help =" set server mode ( default : client mode ) ")
parser . add_argument (' -A ', dest =' remote_address ',
help =' set remote server address ')
parser . add_argument (' -P ', type = int , dest =' remote_port ', default
= '12000 ' ,
help =' set remote server port ')
parser . add_argument (' -- tap - addr ', type = str , dest =' taddr ' , default
= '10.8.0.1 ' ,
help =' set tunnel local address ( default :
10.8.0.1 for '
' server , 10.8.0.2 for client ) ')
parser . add_argument (' -- tap - netmask ' , default = '24 ' , dest = ' tmask ',
help =' set tunnel netmask ( default : 24) ')
parser . add_argument (' -- tap - mtu ', type = int , default =32768 , dest ='
tmtu ',
help =' set tunnel MTU ( default : 32768) ')
parser . add_argument (' -- local - addr ', default = '0.0.0.0 ' , dest = ' laddr
',
help =' address to which OTPTunnel will bind (
default : 0.0.0.0) ')
parser . add_argument (' -- local - port ', type = int , default =12000 , dest
=' lport ',
help =' set local port ( default : 12000) ')
args = parser . parse_args ()
if not args . server :
if args . taddr == '10.8.0.1 ':
args . taddr = '10.8.0.2 '
if not args . remote_address :
parser . print_help ()
return 1
try :
client = Tunnel (
args . taddr , args . tmask , args . tmtu ,
args . laddr , args . lport , args . remote_address ,
args . remote_port )
except socket . error as e:
print >> sys . stderr , str (e)
return 1
print ' NaClShuttle : Running in client mode , press Ctrl + C to
cancel . '
client . run ()
return 0
else :
server = Tunnel (
args . taddr , args . tmask , args . tmtu ,
args . laddr , args . lport , args . remote_address ,
args . remote_port )
print ' NaClShuttle : Running in server mode , press Ctrl + C to
cancel . '
server . run ()
return 0
if __name__ == ' __main__ ':
sys . exit ( main () )