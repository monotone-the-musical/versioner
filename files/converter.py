
import ConfigParser
import json
from os.path import expanduser

vtable={}

# afce6dfe0cbb57f6bf73963a3bf6de7094f9a20614a054abff43706e6638a761,
# /Users/tsdacc/Documents/Downloads/PaymentReceipt_P5553598_20160726.pdf
# adams-macbook-pro.local
# tsdacc
# staff
# 33188
# 2016-07-31 18:03:46
# comment

config = ConfigParser.ConfigParser()
config.read('/etc/versioner/versioner.cfg')
tmpvault = config.get('Main', 'vault')
home = expanduser("~")
vault = tmpvault.replace("~", home)

with open(vault+"/versions.table", "r") as fh:
  filedata = fh.readlines()
  for arecord in filedata:
    check=arecord.split(",")
    thehash=check[0]
    thefilename=check[1]
    thehostname=check[2]
    theuid=check[3]
    thegid=check[4]
    theperms=check[5]
    thelabel=check[6]
    thecomment=check[7]

    if not vtable.get(thehash):
      vtable[thehash]=[{thefilename:thecomment},thehostname,theuid,thegid,theperms,thelabel]
    else:
      thefiledict=vtable[thehash][0]
      thefiledict[thefilename]=thecomment
      vtable[thehash][0]=thefiledict

# now write out dictionary
with open("./versions.table.NEW","w") as outputfile:
  json.dump(vtable, outputfile)
