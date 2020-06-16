import subprocess
import sys
f = open("/etc/network/interfaces.d/50-cloud-init.cfg","a")
i = 503
while i <= 2500:
    #print(hex(i).split("0x")[1])
    f.write("        up ip -6 addr add 2a01:4f8:c0c:86eb::"+hex(i).split("0x")[1]+"/64 dev $IFACE"+"\n")
    f.write("        down ip -6 addr del 2a01:4f8:c0c:86eb::"+hex(i).split("0x")[1]+"/64 dev $IFACE"+"\n")
    i = i+1
f.close()
