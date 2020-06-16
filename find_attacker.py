import dpkt
import datetime
import socket

f = open('pool_probe_final_4.pcap','rb')
pcap = dpkt.pcap.Reader(f)
s = set()
req_count = {}
for ts, buf in pcap:
    eth = dpkt.ethernet.Ethernet(buf)
    s_addr = socket.inet_ntop(socket.AF_INET6,eth.data.src) 
    d_addr = socket.inet_ntop(socket.AF_INET6,eth.data.dst) 
    if d_addr not in s:
        s.add(d_addr)
        req_count[d_addr] = 1
    else:
        req_count[d_addr] += 1

for key in req_count:
    if req_count[key] > 1:
        print(key," -> ",req_count[key])
