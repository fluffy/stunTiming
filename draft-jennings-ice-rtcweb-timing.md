%%%

    #
    # STUN Timing 
    #
    # Generation tool chain:
    #   mmark (https://github.com/miekg/mmark)
    #   xml2rfc (http://xml2rfc.ietf.org/)
    #

    Title = "ICE and STUN Timing Experiments for WebRTC"
    abbrev = "ICE Timing Experiments"
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
impact of proposed changes to  ICE based on the latest
consumer NATs.

This draft is not meant to  become an RFC. It is purely
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
these starts an ICE process that imitates STUN transactions towards
various IP and ports that are specified by the Javascript of the web
page.

Browser do not limit the number of PeerConnections but do limit the
total amount of STUN traffic that is sent with no congestion
control. This draft assumes that browsers will limit this traffic to
250kbps thought right now implementation seems to exceed that when
measured over an 100ms window. 

Each PeerConnection starts a new STUN transaction periodically until
all the iCE testing is done. [@!RFC5245] limits this to be 20ms or more
while [@I-D.ietf-ice-rfc5245bis] proposes moves the minimum time to 5
ms. Retransmission for previous stun transaction can be happening in
parallel with this.

The STUN specification [@!RFC5389] specifies 7 retransmission each one
doubling in timeout starting with a 500ms retransmission time unless
certain conditions are meant. This was only put in the RFC to make the
IESG happy and is largely ignored and instead system several
retransmissions (6 for Firefox, 8 for Chrome) with a retransmission
time starting at 100ms and doubling every retransmission up to a limit
of 1600 ms for chrome where it stop increasing the time between
retransmissions. 

The size of STUN packets can vary based on a variety of options
selected but the packets being used by browser today are about 70 
bytes for the the requests. 

As the speed of the pacing is speeded up to 5ms, it increases the
number of new mappings the NAT needs to create as well as increasing
the non congestion controlled bandwidth used by by the browser. The
rest of this draft looks at what sort of issue may or may not come out
of this.

## A multi PC use case

A common design for small conferences is to have a full mesh of media
formed between all participants where each participants sends their
audio and video to all other participants who mix and render the
results. If there are 9 people on a conference call and a 10th one
joins, one design might be for the new person to in parallel form 9
new PeerConnections - one to each existing participant.

This might result in 9 ICE machine each starting a new STUN
transaction every 5 ms. Assuming no retransmissions, that is a new NAT
mapping every 5ms / 9 ice machine = 0.5 ms and about 5 ms / 9 ice
machine * 70 bytes / packet * 8 bits per byte which comes to about 1
mbps. As many of the ICE candidates are expected not to work, they will
result in the full series of retransmitting which will up the bandwidth
usage significantly.

An alternative design would be to form these connection to the 9
people in the conference sequentially. Given the bandwidth limitations
and other issues, later parts of this draft propose that if we move
the pacing to 5ms, the WebRTC drafts probably need to caution
developers that parallel implementation with these many peers are
likely to have failures.

With the current timings, doing this in parallel often works and
there are applications that do it in parallel that ill likely need
to change if the timing change.


# Nat Connection Rate Results

The first set of tests are concerned with how many new mappings the
NAT can create. The 20ms limit in [@RFC5389] was based on going faster
than than exceeded the rate of which NATs widely deployed at that time
could create new mappings.

The test for this draft were run on the very latest models NATs from
Asus, DLink, Netgear, and Linksys. These four vendors were selected
due to the large market share they represent. This is not at all
representative of what is actually deployed in the field today but
represents what we will be seeing widely deployed in the next 3 to 7
years as this generation of NATs moves into the marketplace as well as
the lower end NATs in the product lines. It is also clear that in some
geographies, a national broadband provider may use some globally less
common NAT causing that vendors NAT to prevalent in a given country
even if it is not common world wide.

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
behave complaint (for UDP) with [@RFC4787] with regards to mapping and
filtering allocations. This is great news as well as a strong
endorsement on the success of the BEHAVE WG. The fact that we see a
non trivial percentage of non behave compliant NATs deployed in the
field does highlight that this sample set of NATs tested is not a
representative sample of what is deployed. It does suggest that we
should see a reduced use of TURN servers over time.

On the second test, all the NATs tested could reliably create new
mapping in under 1ms - often more like several hundred micro
seconds. Looking at the code of one NAT, this largely seems to be due
to vast increase in CPU speed of CPUs in the NATs vs the speed in the
NATs tested in 2005 in [@I-D.jennings-behave-test-results].

This implies that as long as there or less than 5 or 10 PC doing ICE
in parallel in a given browser, we do not anticipate problems on the
texted NATs moving the ICE pacing to 5ms.


# ICE Bandwidth Usage

## History of RFC 5389

At the time [@RFC5389] was done, the argument made was it was OK for
STUN to use as much non congestion controlled bandwidth as RTP audio
was likely to do as the STUN was merely setting up a connection for
an RTP phone call. The premise was the networks that IP Phones were used on were
designed to have enough bandwidth to reasonable work with the audio
codecs being used and that the RTP audio was not elastic and not
congestion controlled in most implementations. There was a form of
"User congestion control" in that if your phone call sounded like
crap because it was having 10% packet loss, the user ended the call,
tried again, and if it was till bad gave up and stopped causing
congestion.

Since that time the number of candidates used in ICE has
siginpificantly increased, the range of networks ICE is used over has
expanded, and uses have increased. We have also seem much more
widespread use of FEC that that allows high packet loss rate with no
impact on the end user perception of media quality. In WebRC there
applications such as file sharing and background P2P backup that form
data channel connecting using ICE with no human interaction to stop if
the packet loss rate is high. ICE in
practical usage has expanded beyond a tool for IP phones to become  the
preferred tool on the internet for setting up end to end connection.



## Bandwidth Usage

To prevent things like DDOS attacks on DNS servers, WebRTC browser
limit the non congestion controlled bandwidth of STUN transaction to
an unspecified number but seems that browsers currently plan to set
this to 250 kbps. An advertisement running on a popular webpage can
create as many PeerConnections as it wants and specify the IP and port
to send all the STUN transaction to. Each Peer Connection objects
sends UDP traffic to an IP and port of specified in the JavaScript which the
browser limits by dropping packets that exceed the global limit for
the browser.

## What should global rate limit be

It is clear that sending 250 kbps on 80 kbps edge cellular connection
severely impacts other application on that connection and is not even
remotely close to TCP friendly. In the age of cellular wifi hot spots
and highly variable backhaul, the browser has no pre installed idea of
what the available bandwidth is.

This draft is not in anyway suggesting what the bandwidth limit should
be but it is looking at what are the implication to ICE timing based
on that number. The limit has security implication in that browser
loading Javascript in paid advertisements on popular web sides could
use this to send traffic to DDOS an UDP server. The limit has
transport implication in how it interacts with other traffic on the
networks that are close to or less than this limit.

More information on this topic can be found in
[@I-D.ietf-tsvwg-rfc5405bis] and [@I-D.ietf-avtcore-rtp-circuit-breakers].


## Rate Limits

This limit to drop packets if the global bandwidth is exceeded means
that applications need to stay under this rate limit or the loss of
STUN packets will cause ICE to start thinking connections which are
valid do not work. At 250 kbps, split across say two web pages, with
no retransmission, each web page can from a new STUN transaction
roughly ever ( 70 * 8 ) / (250000 / 2 )= 4.48 ms. This implies that
really only one Peer Connection can be doing ICE at at time if the
pacing is moved to 5 ms.

If the rate limit was set more around compressed narrowband voice
bitrates, (12 to 40 kbps depending on who you ask), it is clear that
5ms timing fro ICE is far too low and will cause many ICE packet to be
arbitrarily discarded by the browser rate limit before even being sent
on the wire.

## ICE Synchronization

NATs and firewalls create very short windows of time where a response
to an outbound request is allowed to in and allowed to create a new
flow. Though this draft did not test these timing on major firewalls,
some information indicates these windows are being reduced as time
goes on to possible provide better a short attack window for certain
types of attacks.  ICE takes advantage of both one side sending a
suicide packet that will be lost but will create a short window of
time where if the other side sends a packet it will get in a the window
created by the suicide packet and allow a full connection to
form. To make this work, the timing of the packets from either side
needs to be closely coordinated. Most the complexity of the ICE
algorithm comes from trying to coordinate both sides such that they send
the related packets at similar times.

A key implication of this is that if several ICE machine are running
in single browser, what is happening in other ICE machine can't change
the timing of what a given ICE machine is sending. So any solution that
slowed down the transmission in one Peer Connection if there were lots
of other simultaneous Peer Connection is not likely to work well with
ICE unless the far side also knows to slow down.


# Recommendations

The ICE and RTCWeb Transport documents should specify a clear upper
bound on the amount of non congestion controlled traffic an browser or
applications should be limited to. The transported perhaps security
area should provide advice on what that number should be. WebRTC
basically application work better the larger that number is at the
expense of other applications running on the same congested links.

Given the way that setting the ICE pacing to be too fast can cause ICE
to fail, The Javascript application in WebRTC should have a way to tell
the browser what ICE pacing to use with a minimum enforced by the
browser.

There is no way for a JavaScript application to know how many other
web pages or tabs in the browser are also doing stun yet all of these
impact the global rate limit in the browser. If the browser discards
STUN packets due to the global rate limit being exceeded, it results
in applicant failures that look like network problems which are
in fact just an artifact of other applications running the browser at
the same time. This is critical information to understanding why
applications are failing. The recommendation here is that the WebRTC
API be extended to provide a way for the browsers to inform the
application using a given PeerConnection object if STUN packets it is
sending are being discarded by the browser.



# Conclusions

The speed of NATs mapping creation going forward in the future is
likely adequate to move the pacing to 5ms. However applications that
create parallel peer connections or situations where more than a
handful of PeerConnections are forming in parallel in the same
browser (possibly in different tabs or web pages) need to be avoided.

From a bandwidth limit point of view, if the bandwidth is limited at
250 kbps, a 5ms timing will work for a single PeerConnection but not
much more than that. The specification should make developers aware of
this limitation. If the non congestion controlled bandwidth limit is
less than 250 kbps, a 5ms timing is likely too small to work
reliably.


# Acknowledgments

Many thanks to review from ...


{backmatter}

# Appendix A - Bandwidth testing

The following example web page was used to measure how much bandwidth a
browser will send to an arbitrary IP and port when getting 100% packet
loss to that destination.

TODO - add program

