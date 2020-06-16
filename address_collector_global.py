import subprocess
s = set()
f = open("addr_global.txt","w+")
count = 0
while count < 1460:
    process = subprocess.Popen(["dig","@a.ntpns.org","AAAA", "2.pool.ntp.org","+noall","+answer"], stdout=subprocess.PIPE)
    for line in process.stdout:
        if line[0] is 50:
            addr = str(line).split('\\t')[5].split('\\n')[0]
            if addr not in s:
                count  = count + 1
                s.add(addr)
                f.write(addr+"\n")

    process = subprocess.Popen(["dig","@b.ntpns.org","AAAA", "2.pool.ntp.org","+noall","+answer"], stdout=subprocess.PIPE)
    for line in process.stdout:
        if line[0] is 50:
            addr = str(line).split('\\t')[5].split('\\n')[0]
            if addr not in s:
                count  = count + 1
                s.add(addr)
                f.write(addr+"\n")

    process = subprocess.Popen(["dig","@c.ntpns.org","AAAA", "2.pool.ntp.org","+noall","+answer"], stdout=subprocess.PIPE)
    for line in process.stdout:
        if line[0] is 50:
            addr = str(line).split('\\t')[5].split('\\n')[0]
            if addr not in s:
                count  = count + 1
                s.add(addr)
                f.write(addr+"\n")

    process = subprocess.Popen(["dig","@d.ntpns.org","AAAA", "2.pool.ntp.org","+noall","+answer"], stdout=subprocess.PIPE)
    for line in process.stdout:
        if line[0] is 50:
            addr = str(line).split('\\t')[5].split('\\n')[0]
            if addr not in s:
                count  = count + 1
                s.add(addr)
                f.write(addr+"\n")

    process = subprocess.Popen(["dig","@e.ntpns.org","AAAA", "2.pool.ntp.org","+noall","+answer"], stdout=subprocess.PIPE)
    for line in process.stdout:
        if line[0] is 50:
            addr = str(line).split('\\t')[5].split('\\n')[0]
            if addr not in s:
                count  = count + 1
                s.add(addr)
                f.write(addr+"\n")

    process = subprocess.Popen(["dig","@f.ntpns.org","AAAA", "2.pool.ntp.org","+noall","+answer"], stdout=subprocess.PIPE)
    for line in process.stdout:
        if line[0] is 50:
            addr = str(line).split('\\t')[5].split('\\n')[0]
            if addr not in s:
                count  = count + 1
                s.add(addr)
                f.write(addr+"\n")

    process = subprocess.Popen(["dig","@g.ntpns.org","AAAA", "2.pool.ntp.org","+noall","+answer"], stdout=subprocess.PIPE)
    for line in process.stdout:
        if line[0] is 50:
            addr = str(line).split('\\t')[5].split('\\n')[0]
            if addr not in s:
                count  = count + 1
                s.add(addr)
                f.write(addr+"\n")

    process = subprocess.Popen(["dig","@h.ntpns.org","AAAA", "2.pool.ntp.org","+noall","+answer"], stdout=subprocess.PIPE)
    for line in process.stdout:
        if line[0] is 50:
            addr = str(line).split('\\t')[5].split('\\n')[0]
            if addr not in s:
                count  = count + 1
                s.add(addr)
                f.write(addr+"\n")

    process = subprocess.Popen(["dig","@i.ntpns.org","AAAA", "2.pool.ntp.org","+noall","+answer"], stdout=subprocess.PIPE)
    for line in process.stdout:
        if line[0] is 50:
            addr = str(line).split('\\t')[5].split('\\n')[0]
            if addr not in s:
                count  = count + 1
                s.add(addr)
                f.write(addr+"\n")

f.close()
