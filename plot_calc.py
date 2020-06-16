import dpkt
import datetime
import socket
import matplotlib.pylab as plt

f = open('final.pcap','rb')
pcap = dpkt.pcap.Reader(f)
s = set()
hour_req = {}
hour_uni = {}
ini = 0
req_num = 0
ip_num = 0
minutes = seconds = hours = 0
total_count = 0
for ts, buf in pcap:
    dt = datetime.datetime.utcfromtimestamp(ts)
    if ini is 0:
        ini = dt
    diff = dt - ini
    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    #minutes, seconds = divmod(diff.seconds, 60)
    #hours, minutes = divmod(minutes, 60)
   if hours in hour_req:
        hour_req[hours] += 1
    else:
        hour_req[hours] = 1

    #print ('Timestamp: ', dt)
    #dt = str(datetime.datetime.strptime(str(dt),'%Y-%m-%d %H:%M:%S.%f'))
    #dt = dt.split()
    #t = dt[1]
    #print(t)
    #if ini is 0:
     #   ini = t
    eth = dpkt.ethernet.Ethernet(buf)
    s_addr = socket.inet_ntop(socket.AF_INET6,eth.data.src) 
    d_addr = socket.inet_ntop(socket.AF_INET6,eth.data.dst) 
    if s_addr not in s:
        total_count = total_count + 1
        s.add(s_addr)
        if hours in hour_uni:
            hour_uni[hours] += 1
        else:
            hour_uni[hours] = 1
    if d_addr not in s:
        total_count = total_count + 1
        s.add(d_addr)
        if hours in hour_uni:
            hour_uni[hours] += 1
        else:
            hour_uni[hours] = 1

#list_1 = sorted(hour_req.items())
#list_2 = sorted(hour_uni.items())
#x1,y1 = zip(*list_1)
#x2,y2 = zip(*list_2)
#plt.plot(x1,y1)
#plt.show()

print(hour_req)
print(hour_uni)
print(total_count)
