''' Currently only gets addresses from MBOX style boxes. I wrote this to deal with a PST file, use readpst to convert from PST to MBOX. 
    Licensed under the WTFPL - http://www.wtfpl.net/txt/copying/
    -- N Crouch, 2013
'''

import mailbox
import re
import os

addresses = {}
regex = re.compile("(?P<name>[\s\S]*)<(?P<email>[\s\S]*)>")
for mob in os.listdir(os.getcwd()):
        mb = mailbox.mbox(mob)
        for each in mb:
                to = each.get_all("To")
                frm = each.get_all("From")
                cc = each.get_all("CC")
                all_adds = []
                if to is not None:
                        all_adds = to
                if frm is not None:
                        all_adds += frm
                if cc is not None:
                        all_adds += cc
                for each_list in all_adds:
                        for each_address in each_list.split(','):
                                r = regex.search(each_address.replace('\n','').replace('\t','').strip())
                                if r is None:
                                        continue
                                dic = r.groupdict()
                                if dic["email"] in addresses:
                                        if addresses[dic["email"]] is None or (addresses[dic["email"]].strip()) == "":
                                                addresses[dic["email"]] = dic["name"]
                                else:
                                        addresses[dic["email"]] = dic["name"]

        file = open("addresses.csv",'wb')
for k,v in addresses.iteritems():
       file.write(k+", "+v+"\r\n")
file.close()
