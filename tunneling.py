import errno
import fcntl
import os
import select
import socket
import sys
import struct
import threading
import tweetnacl as nacl
class Tunnel ( threading . Thread ):
    def __init__ ( self , taddr , tmask , tmtu , laddr , lport ,
remote_address , remote_port ):
super ( Tunnel , self ). __init__ ()
self . _tmtu = tmtu
self . _sock = socket . socket ( socket . AF_INET , socket . SOCK_DGRAM )
self . _sock . bind (( laddr , lport ))
self . _remote_address = remote_address
self . _remote_port = remote_port
if not remote_address :
try :
print ' NaClShuttle : Waiting for client ... '
msg , addr = self . _sock . recvfrom (65535)
print(" NaClShuttle : Client (' + 'addr [0] '+ ') connected.")
self . _remote_address = addr [0]
except KeyboardInterrupt :
print u '\ u0008 \ u0008NaClShuttle : Closed .'
sys . exit (0)
else :
print ' NaClShuttle : Sending initialisation message to ' +
str ( self . _remote_address ) + ': ' + str ( self .
_remote_port )
init_sock = socket . socket ( socket . AF_INET , socket .
SOCK_DGRAM )
init_sock . sendto (' init ', ( self . _remote_address , self .
_remote_port ))
os . system (' route add default gw 10.8.0.1 ')
print ' Connecting to TAP '
tap = os . open ( '/ dev / net / tun ', os . O_RDWR | os . O_NONBLOCK )
ifr = struct . pack ( '16 sH ', 'tap0 ', 2 | 4096)
fcntl . ioctl ( tap , 0 x400454ca , ifr )
self . _tap = tap
def run ( self ):
mtu = self . _tmtu
files = [ self . _tap , self . _sock ]
to_tap = None
to_sock = None
while True :
try :
r , w , x = select . select ( files , files , [])
if self . _tap in r:
to_sock = os . read ( self . _tap , mtu )
if self . _sock in r:
to_tap , addr = self . _sock . recvfrom (65535)
key = ' ThisKeyIsNotSoSecretThisKeyIsNot ' # Debug ,
can be replaced with keyfile
nonce = ' NonceNonceNonceNonceNonc '
to_tap_decrypted = nacl . crypto_secretbox_open (
to_tap , nonce , key )
to_tap = to_tap_decrypted
if to_tap and self . _tap in w:
os . write ( self . _tap , to_tap )
to_tap = None
if to_sock and self . _sock in w:
    key = ’ ThisKeyIsNotSoSecretThisKeyIsNot ’ # Debug ,
    can be replaced with keyfile
nonce = ’ NonceNonceNonceNonceNonc ’
to_sock_encrypted = nacl . crypto_secretbox ( to_sock ,
nonce , key )
to_sock = to_sock_encrypted
self . _sock . sendto (
to_sock , ( self . _remote_address , self .
_remote_port ))
to_sock = None
except ( select . error , socket . error ) as e:
if e [0] == errno . EINTR :
continue
sys . stderr . write ( str (e))
break
except KeyboardInterrupt :
print u ’\ u0008 \ u0008NaClShuttle : Closed .’
sys . exit (0)