# DarkTor

## What is DarkTor ?
DarkTor is an anonymization script which redirects all internet traffic through SOCKS5 tor proxy. DNS requests are also redirected via tor, thus preventing DNSLeak. The scripts also disables unsafe packets exiting the system. Some packets like ping request can compromise your identity.

# Build and install from source
`git clone https://github.com/D4RK-4RMY/DarkTor.git`

`cd DarkTor`

`chmod +x build.sh`

`./build.sh`


## Usage
Darktor v1.0.1 usage:

`  -s      --start        Start DarkTor`

`  -r      --switch       Request new tor exit node`

`  -x      --stop         Stop DarkTor`

`  -h      --help         Print this help and exit`

`  -u      --update       Checks for updates`

`By D4rk4rmy`
