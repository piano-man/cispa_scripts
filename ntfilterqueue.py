#not being able to reorder packets because of the way in which the library is designed

from random import randint
from time import sleep
from netfilterqueue import NetfilterQueue
packet_list = []
count = 0

def print_and_accept(pkt):
    global count
    global packet_list
    count = count+1
    payload = pkt.get_payload()
    #print(payload)
    #pkt.repeat()
    #sleep(randint(0,10)/10)
    pkt.accept()

def pass_verdict(packet_list):
    print("reached here")
    for pkt in packet_list:
        print("processing here")
        pkt.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(1, print_and_accept)
try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')
     
nfqueue.unbind()
