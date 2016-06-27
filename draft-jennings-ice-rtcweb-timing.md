%%%

    #
    # STUN TIming 
    #
    # Generation tool chain:
    #   mmark (https://github.com/miekg/mmark)
    #   xml2rfc (http://xml2rfc.ietf.org/)
    #

    Title = "ICE and STUN Timing Experiments for WebRTC"
    abbrev = "Double SRTP"
    category = "std"
    docName = "draft-jennings-ice-rtcweb-timing-00"
    ipr= "trust200902"
    area = "Internet"
    keyword = ["ICE", "STUN", "WebRTC" ]
    
    [pi]
    symrefs = "yes"
    sortrefs = "yes"

    [[author]]
    initials = "C."
    surname = "Jennings"
    fullname = "Cullen Jennings"
    organization = "Cisco"
      [author.address]
      email = "fluffy@iii.ca"

  
%%%

.# Abstract

This draft summarizes the results in some experiments looking at the
impact of proposed changes to STUN and ICE based on the latest
consumer NATs.

This draft is not meant to every become an RFC. It is purely
information to help guide development of other specifications.


{mainmatter}

# Introduction

The ICE WG at IETF has been considering speeding up the rate of
starting new STUN and TURN connections when doing ICE. The two primary
questions that have been raised about this are 1) can the NATs create
new connections fast enough to not cause problems 2) what will the
impact on bandwidth usage be.


# Background

A web page using WebRTC can form multiple PeerConnections. Each one of
these starts an ICE process that initates STUN transactions towards
varios IP and ports that are specified by the JavaScrpt of the web
page.

Browser do not limit the number of PeerConnections but do limit the
totall amount of STUN traffic that is sent with no congetion
controll. This draft assumes that browsers will limit this traffic to
250kbps thought right now implementation seems to exceed that when
measured over an 100ms window. 

Each PeerConnection starts a new STUN transaction periodically until
all the iCE testing is done. RFC5245 limits this to be 20ms or more
while draft-ietf-ice-rfc5245bis proposes moves the miimium time to 5
ms. Retransmition for previos stun transaction can be happening in
parrallel with this.

The STUN specifiction [RFC5389] specifies 7 retransmition each one
doubleing in timeout starting with a 500ms retransmiton
time unless certian conditions are meant. This largely ignored and
instead system do 7 retransmtions with a retransmition time starting
at 100ms and doubling up to a limit of TODO ms. 

The size of STUN packets can vary based on a vareity of opions
selected but the packets being used by browser today are about 70 TODO
bytes for the the requests. 

As the speed of the pacing is speeded up to 5ms, it increases the
number of new mappings the NAT needs to create as well as increasing
the non congestion coontrolled bandwidht used by by the browser. The
rest of this draft looks at what sort of issue may or may not come out
of this.

## A multi PC use case

A common design for small conferences is to have a full mesh of media
formed between all participants where each participants sends their
audio and video to all other participants who mix and render the
results. If there are 9 people on a confernce call and a 10th one
joins, one design might be for the new peron to in parallel fourm 9
new PeerConnections - one to each existing partipcipant.

This might result in 9 ICE machine each starting a new STUN
transaction every 5 ms. Assuming no retransmitons, that is a new NAT
mapping every 5ms / 9 ice machine = 0.5 ms and about 5 ms / 9 ice
machine * 70 bytes / packet * 8 bits per byte = TODO kbps. WIth
hat retransmtion it can get up to significnatly more.

An alternative design would be to form these connection to the 9
people in the confernce sequentially. Given the bandwith limitations
and other issues, later parts of this draft propose that if we move
the pacing to 5ms, the WebRTC drafts proabbkly need to cuation
developers that parrallel impltentation wtih these many candiates are
likely to have falures.

# Nat Connection Rate Results

The first set of tests are concerned with how many new mappings the
NAT can create. The 20ms limit in [RFC5389] was based on going faster
than than exceeded the rate of which NATs widely deployed at that time
could create new mappings.

The test were run on the very latest models NATs from Asus, Dlink,
Netgear, and Linksys. These four vendors were selected due to the
large market share they represent. This is not at all representative
of what is actually deployed in the field today but represents what we
will be seeing widely deployed in the next 3 to 7 years as this
generation of NATs moves into the marketplace as well as the lower end
NATs in the product lines. It is also clear that in some geographies,
a national broadband provider may use some globally less common NAT
causing that vendors NAT to prevalent in a given country even if it is
not common world wide.

Test were only run using wired interfaces and consisted of connecting
both sides of the NAT to two different interfaces on the same computer
and using a single program to send packet various direction as well as
measure the exact arrival times of packets. Key results were verified
using Wireshark to look wire captures made on a separate computer. The
first test was normal tests made to classify the type of the NAT for
the cases when 1, 2, and 3 internal clients all have the same source
port. The second test created many new mappings to measure the maximum
rate mapping could reliably be made.

The conclusion of the first test was that all of the NATs tested were
behave complaint (for UDP) with [RFC4787]. This is great news as well
as a strong endorsement on the success of the BEHAVE WG. The fact that
we see a non trivial percentage of non behave compliant NATs deployed
in the field does highlight that this sample set of NATs tested is not
a representative sample of what is deployed. It does suggest that we
should see a reduced use of TURN servers over time.

On the second test, all the NATs tested could reliably create new
mapping in under 1ms - often more like several hundred micro
seconds. Looking at the code of one NAT, this largely seems to be due
to vast increase in CPU speed of CPUs in the NATs vs the speed in the
NATs tested in 2005 in [draft-jennings-behave-test-results-00].

This implies that as long as there or less than 5 or 10 PC doing ICE
in parallel in a given brwser, we do not anticipate problems on the
texted nats moving the ICE pacing to 5ms. 


# ICE Bandwidth Usage

## History of RFCb5389

## TODO 


# Conclusions

The speed of NATs mapping creation going forward in the future is
likely adequate to move the pacing to 5ms. However applications that
create parallel peer connections on sitirtuatio where more than a
handfull of PeerConnections are funnin in pararrelel in the same
rowwser (poisbly in differnt tabs or web pages) need to be avoided.



# Acknowledgments

Many thanks to review from ...

{backmatter}
