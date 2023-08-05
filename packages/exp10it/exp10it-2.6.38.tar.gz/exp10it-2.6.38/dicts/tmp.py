import re
with open("top100pass.txt","r+") as f:
    contnet=f.readlines()
for eachLine in contnet:
    re.search(mm)
a=re.findall(r"(\S+)\s+\S+\n",contnet)
print(a)
