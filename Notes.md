

The deprecated
{ offerToReceiveAudio: 1,  offerToReceiveVideo: 2 }
works in FF but not in Chrome. But this version of chrome and FF does not yet have the addTranceiver stuff yet so no way to do this in chrome (there is an open bug on this)

Chrome includes the HTML origin URL in the STUN packet, FF does not seem to.

Chrome does STUN keep alive every 10 seconds, FF does not

Chrome and FF do not pace between different PeerConnection objects

Both FF and Chrome see to send at a max rate of about 1 ms between STUN packets


-------------

Testing on FF 47 and Chrome 51

The dump1,2 pcap files done on mac with wired connection sending to an IP
address that does not exist. 

Chrome in first 100 ms sends 100 packets each 74 bytes =  592kbps 
(and 200 packets in first 200 ms)

FF in first 100ms sends 100 packets each 70 bytes = 560kbps 
(and in first 200 ms sends 200 packets ) 

---------


grab traffic with:
sudo tcpdump -i en1 -s 0 -w /tmp/dump.pcap 'port 10053'

