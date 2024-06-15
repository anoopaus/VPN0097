#!/ bin / bash
declare error
if [[ $EUID - ne 0 ]]; then
echo ' NaClShuttle : [ ERROR ] This script must be run as root .'
exit 1
fi
function echo_error
{
    echo -n ' NaClShuttle : [ ERROR ] '
echo $1
error = true
}
function ip_forward
{
echo 1 > / proc / sys / net / ipv4 / ip_forward
}
if [[ $1 ]]; then
if [ $1 = '-S ' ]; then
echo ' NaClShuttle : Server mode . '
echo ' NaClShuttle : Setting up network settings ... '
{ echo 1 > / proc / sys / net / ipv4 / ip_forward ; } 2 >/ dev / null ||
echo_error ' Failed to enable IP forwarding .'
iptables -t nat -A POSTROUTING -j MASQUERADE >/ dev / null 2 >&1
|| echo_error ' Failed to setup iptables .'
echo ' NaClShuttle : Creating TAP device ... '
ip tuntap add tap0 mode tap > / dev / null 2 >&1 || echo_error '
Failed to create TAP device . Does it already exist ?'
ifconfig tap0 10.8.0.1/24 > / dev / null 2 >&1 || echo_error '
Failed to configure TAP device . Does the TAP device exist
?'
echo -n ' NaClShuttle : NaClShuttle setup completed '
if [ " $error " = true ]; then
echo ' with errors , check output above .'
else
echo '.'
fi
elif [ $1 = '-C ' ]; then
echo ' NaClShuttle : Client mode . '
echo ' NaClShuttle : Creating TAP device ... '
ip tuntap add tap0 mode tap > / dev / null 2 >&1 || echo_error '
Failed to create TAP device . Does it already exist ?'
ifconfig tap0 10.8.0.2/24 > / dev / null 2 >&1 || echo_error '
Failed to configure TAP device . Does the TAP device exist
?'
echo ' NaClShuttle : Adjusting IP routing table ... '
echo -n ' NaClShuttle : NaClShuttle setup completed '
if [ " $error " = true ]; then
echo ' with errors , check output above .'
else
echo '.'
fi
fi
else
echo ' NaClShuttle : [ ERROR ] No parameter given . Use -S for server
mode , -C for client mode .'
