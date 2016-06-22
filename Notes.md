
Testing on FF 47 and Chrome 51


Chrome does STUN keep alive every 10 seconds, FF does not

Chrome and FF do not pace between different PeerConnection objects


Chrome in first 100 ms sends 100 packets each 74 bytes 
(and 200 packets in first 200 ms)

FF in first 100ms sends 100 packets each 70 bytes 
(and in first 200 ms sends 200 packets ) 

---------


grab traffic with:
sudo tcpdump -i en1 -s 0 -w /tmp/dump.pcap 'port 10053'

