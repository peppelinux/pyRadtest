pyEapol_test is a Pure Python implementation of a eapol_test client.

It doesn't need any dependencies to work.
A very special thanks to Sergej Srepfler <sergej.srepfler@gmail.com> for his libRadius lib, the client is based on it.

To use pyEapol_test you should simply download this repository and then run in its directory:

````
Usage: python EapolClient.py -u UserLogin-p UserPassword-s ServerSecret

optional arguments:
  -h, --help            show this help message and exit
  -u U                  radius radcheck username
  -p P                  radius radcheck password
  -s S                  radius client secret
  -host HOST            radius server ip
  -port PORT            radius server port
  -f [F]                file path where dictRadius is
  -calling_id CALLING_ID
                        Calling-Station-Id
  -called_id CALLED_ID  Called-Station-Id
  -m M                  Message size. Default 4KB
  -t T                  Timeout. Default 15 secs
  -nas_port NAS_PORT    NAS port. Default 6000
  -nas_port_type NAS_PORT_TYPE
                        NAS port type. Default 5
````
