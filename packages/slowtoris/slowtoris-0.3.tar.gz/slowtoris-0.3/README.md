# SlowToris

A Slow Loris attack implementation in Python3 with support for the Tor network and SOCKS5 proxies.

You can view the usage of this script by running:

    $ slowtoris.py --help
### Installing Slowtoris:

##### Using pip:

    $ pip install slowtoris

If you choose this solution you can jump to the Tor installation part.

##### Manually:

You must clone the git:

    $ git clone https://github.com/naganori-san/slowtoris

Move to the directory:

    $ cd slowtoris

Install the script:

    $ sudo python3 setup.py install

You must have the `click` Python3 module which can be installed with pip:

    $ sudo pip3 install click

You must have the socks Python3 module which can be installed through
various packages by using pip, we suggest `PySocks`:

    $ sudo pip3 install PySocks

You must have the `stem` Python3 module which can be installed with pip:

    $ sudo pip3 install stem

If you wish to use the Tor network, tor must be installed and the service
must be started.

### Installing Tor:

    Ubuntu/Debian:  https://www.torproject.org/docs/debian.html.en

    Arch Linux:     # pacman -S tor

    Gentoo Linux:   # emerge --ask --verbose net-vpn/tor

    CentOS/Fedora:  # yum install tor

### Configuring tor:

We use the tor controller to refresh the circuit through port 9051.

You must thus activate it and add your password to be able to authenticate.

Get the password hash:

    # tor --hash-password YOUR_PASSWORD
    
Open the torrc file (probably `/etc/torrc` or `/etc/tor/torrc`) and uncomment
he following line:
    
    ControlPort 9051

A few lines later uncomment the line:

    HashedControlPassword 

And replace the hased password with the one your generated earlier.

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

    -T, --tor PASSWORD     Open the connections through the Tor network by
			   using localhost:9050 as a SOCKS5 proxy. The password
                           is the one chose for the controller in your torrc file.
                           If you wish to use the Tor network through another host or port
			   you must use the -x option.

    -x, --proxy host:port  Use a SOCKS5 proxy to communicate with the target.

    -q, --quiet            Run the script in quiet mode removing all output.

    --help                 Show this message and exit.
