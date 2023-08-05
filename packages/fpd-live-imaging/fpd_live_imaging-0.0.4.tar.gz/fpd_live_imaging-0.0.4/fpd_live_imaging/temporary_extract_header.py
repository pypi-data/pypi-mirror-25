import re

f = open("packet_list.txt", "rb")
packet_content = b"".join(f.readlines())

p = re.compile(b"MPX")
for m in p.finditer(packet_content):
    print(m.start())
    print(m.group())
