#!/usr/bin/env python
from libRadius import *
import datetime
import time
import socket 

#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

class EapolClient(object):
    def __init__(self, username, password, secret, host='127.0.0.1', 
                 port=1812, radiusDict='dictRadius.xml', 
                 calling_station_id="00381123456", called_station_id='mms',
                 msg_size=4096, timeout=15, nas_port_type=5, 
                 nas_port=6000, nas_identifier="FBG01"):
        self.username = username
        self.password = password
        self.secret   = secret
        self.host     = host
        self.port     = port
        self.calling_station_id = calling_station_id
        self.called_station_id  = called_station_id
        
        # LoadDictionary creates a bunch of global variables!
        # It should must be reworked, all those globals should disappear
        self.radiusDict      = LoadDictionary(radiusDict)
        
        self.radiusDict_path = radiusDict
        self.nas_port_type   = nas_port_type
        self.nas_port        = nas_port
        self.msg_size        = msg_size
        self.timeout         = timeout
        self.nas_identifier  = nas_identifier

    def create_request(self):
        # Create message header (empty)
        REQ=HDRItem()
        # Set command code
        REQ.Code=dictCOMMANDname2code("Access-Request")
        REQ.Identifier=1
        REQ.Authenticator=createAuthenticator()
        # Let's build Request 
        REQ_avps=[]
        REQ_avps.append(encodeAVP("Calling-Station-Id", self.calling_station_id))
        REQ_avps.append(encodeAVP("Called-Station-Id", self.called_station_id))
        REQ_avps.append(encodeAVP("User-Name", self.username))
        REQ_avps.append(encodeAVP("User-Password", 
                                  PwCrypt(self.password, REQ.Authenticator, self.secret)))
        REQ_avps.append(encodeAVP("NAS-Identifier", self.nas_identifier))
        REQ_avps.append(encodeAVP("NAS-IP-Address", self.host))
        REQ_avps.append(encodeAVP("NAS-Port-Type", self.nas_port_type))
        REQ_avps.append(encodeAVP("NAS-Port", self.nas_port))
        REQ_avps.append(encodeAVP("Acct-Session-Id", "sessionID"))
        REQ_avps.append(encodeAVP("Acct-Multi-Session-Id", "multisessionID"))
        REQ_avps.append(encodeAVP("Service-Type", 2))
        REQ_avps.append(encodeAVP("Framed-Protocol", 1))
        # Add AVPs to header and calculate remaining fields
        # msg now contains Access-Request as hex string
        self.msg = createReq(REQ,REQ_avps)
        return self.msg

    def create_socket(self):
        self.conn=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # socket is in blocking mode, so let's add a timeout
        self.conn.settimeout(self.timeout)

    def eapol_test(self):
        self.create_request()
        self.create_socket()

        # msg now contains Access-Request as hex string
        #~ print("Access-Request ", self.msg)
        # send data
        self.conn.sendto(self.msg.decode("hex"),(self.host,self.port))
        
        # Receive response
        received = self.conn.recv(self.msg_size)
        
        # Process response
        RES=HDRItem()
        stripHdr(RES,received.encode("hex"))
        radius_avps=splitMsgAVPs(RES.msg)
        for avps in radius_avps:
            print decodeAVP(avps)
            
        # print radius_avps as []
        # And close the connection
        self.conn.close()


if __name__ == '__main__':
    import argparse
    
    # defaults
    #~ username
    #~ password
    #~ secret
    _host='127.0.0.1'
    _port=1812
    _radiusDict='dictRadius.xml'
    _calling_station_id="pyEapol_test"
    _called_station_id="guest.eduroam.eu"
    _msg_size=4096
    _timeout=15
    _nas_port_type=5
    _nas_port=6000
    _nas_identifier="ThatNAS"
    
    parser = argparse.ArgumentParser(description='Usage:\n'
                                     'python EapolClient.py '
                                     '-u UserLogin'
                                     '-p UserPassword'
                                     '-s ServerSecret')
    parser.add_argument('-u', required=True, help="radius radcheck username")
    parser.add_argument('-p', required=True, help="radius radcheck password")
    parser.add_argument('-s', required=True, help="radius client secret")
    parser.add_argument('-host', required=False, 
                              default=_host, help="radius server ip")
    parser.add_argument('-port', type=int, required=False, 
                              default=_port, help="radius server port")
    parser.add_argument('-f', nargs='?', required=False, 
                              type=argparse.FileType('r'), default=_radiusDict,
                              help="file path where dictRadius is")

    parser.add_argument('-calling_id', required=False, 
                                       default=_calling_station_id, 
                                       help="Calling-Station-Id")
    parser.add_argument('-called_id', required=False, 
                                       default=_called_station_id, 
                                       help="Called-Station-Id")

    parser.add_argument('-m', type=int, required=False, 
                              default=_msg_size,
                              help="Message size. Default 4KB")
    parser.add_argument('-t', type=int, required=False, 
                              default=_timeout,
                              help="Timeout. Default 15 secs")
    parser.add_argument('-nas_port', type=int, default=_nas_port,
                                     required=False, help="NAS port. Default 6000")
    parser.add_argument('-nas_port_type', type=int, default=_nas_port_type,
                                          required=False, 
                                          help="NAS port type. Default 5")
    
    args = parser.parse_args()
    
    eapol_test = EapolClient(
                             args.u, args.p, args.s,
                             host=args.host, 
                             port=args.port,
                             radiusDict=args.f,
                             calling_station_id=args.calling_id,
                             called_station_id=args.called_id,
                             msg_size=args.m,
                             timeout=args.t,
                             nas_port=args.nas_port,
                             nas_port_type=args.nas_port_type,
                             nas_identifier=_nas_identifier,
                            )
    eapol_test.eapol_test()
