# SlowToris

A Slow Loris atack implementation in Python3 with support for the Tor network and SOCKS5 proxies.

You can view the usage of this script by running:

    $ slowtoris.py --help

### Python modules:

You must have the click Python3 module which can be installed with pip:

    $ sudo pip3 install click

You must have the socks Python3 module which can be installed through
various packages by using pip, we suggest PySocks:

    $ sudo pip3 install PySocks

If you wish to use the Tor network, tor must be installed and the service
must be started.

### Installing Tor:

    Ubuntu/Debian:  https://www.torproject.org/docs/debian.html.en

    Arch Linux:     # pacman -S tor

    Gentoo Linux:   # emerge --ask --verbose net-vpn/tor

    CentOS/Fedora:  # yum install tor

### Starting the tor service:

    If you do not know if you are using Systemd or OpenRC you are very
    probably using Systemd.

    Systemd: # systemctl start tor

    OpenRC:  # rc-service tor start

### Usage:

    slowtoris.py [OPTIONS] TARGET

### Options:

    -p, --port INTEGER     Port to attack on the remote target. Default is 80.

    -s, --sockets INTEGER  Number of sockets to open with the remote target.

    -r, --randomize        Randomize user agents for every new socket.

    -T, --tor              Open the connections the connections through the Tor
                           network by using localhost:9050 as a SOCKS5 proxy. If
                           you wish to use the Tor network through another host
                           or port you must use the -x option.

    -x, --proxy host:port  Use a SOCKS5 proxy
                           to communicate with the target.

    -q, --quiet            Run the script in quiet mode removing all output.

    --help                 Show this message and exit.
