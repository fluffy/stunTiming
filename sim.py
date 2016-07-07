#!/usr/bin/env python
import argparse
import sys

PAIRS = []
PACKETS = []
SLICES = []
MAX_TIME = 0
TIME_SLICE = 100

def debug(msg):
    sys.stderr.write(str(msg))
    sys.stderr.write("\n")

def send_packet(pair_id, time):
    global MAX_TIME
    debug("%d, %d"%(pair_id, time))
    PACKETS.append({
        'pair':pair_id,
        'time':time
    })
    if time > MAX_TIME:
        MAX_TIME = time
    
class Pair(object):
    def __init__(self, pair_id, start_time, args):
        self.pair_id_ = pair_id
        self.next_time_ = start_time
        self.timeout_ = args.start_timeout
        self.num_retransmits_ = args.num_retransmits
        self.max_timeout_ = args.max_timeout
        self.transmissions_ = 0

    def run_once(self):
        send_packet(self.pair_id_, self.next_time_)
        if self.transmissions_ >= self.num_retransmits_:
            return False
        self.transmissions_ += 1
        self.timeout_ *= 2
        if self.timeout_ > self.max_timeout_:
            self.timeout_ = self.max_timeout_
        self.next_time_ += self.timeout_
        return True
        
    def run(self):
        rv = True
        while rv:
            rv = self.run_once()
        
        




parser = argparse.ArgumentParser()
parser.add_argument('--start_interval', dest = 'start_interval', type=int, default = 20)
parser.add_argument('--start_timeout', dest = 'start_timeout', type=int, default = 100)
parser.add_argument('--num_retransmits', dest = 'num_retransmits', type=int, default=6)
parser.add_argument('--max_timeout', dest='max_timeout', type=int, default=1600)
parser.add_argument('--num_pairs', dest='num_pairs', type=int, default=1)
parser.add_argument('--packet_size', dest='packet_size', type=int, default=70)

args = parser.parse_args()
st = 0
for i in range(0, args.num_pairs):
    PAIRS.append(Pair(i, st, args))
    st += args.start_interval

for a in PAIRS:
    a.run()

debug(PACKETS)

for s in range(0, (MAX_TIME / TIME_SLICE) + 1):
    SLICES.append(0)
    
for p in PACKETS:
    s = p['time']
    SLICES[s/TIME_SLICE] += 1

T = 0

debug(SLICES)
debug(args)
OUT = open("pairs_%d_interval_%d.txt"%(args.num_pairs, args.start_interval), "w")

OUT.write("TIME\tRATE\n")

for s in SLICES:
    t = T * TIME_SLICE
    T += 1
    r = (s * args.packet_size * 8) * (1000/TIME_SLICE)
    OUT.write("%d\t%d\n"%(t, r))

        

    

