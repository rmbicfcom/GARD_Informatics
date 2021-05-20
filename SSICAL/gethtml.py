#!/usr/bin/env python
# R. Ballew 12-May-2021
# Hit the SSI Compassionate Allowances Conditions web site for a disease.
# The HTML contains useful hidden tags at the end.
#
# pip install requests bs4 
from bs4 import BeautifulSoup
import requests
import re
import sys

def retmatch(st, lst):
    retval = "None"
    for le in lst:
        if st.split(" ")[0] == le.split(" ")[0]:
            retval = le
    return retval

#url = "https://secure.ssa.gov/apps10/poms.nsf/lnx/0423022375"
# the following link had issues
url = "https://secure.ssa.gov/poms.nsf/lnx/0423022927"
"""
https://secure.ssa.gov/poms.nsf/lnx/0423022365
https://secure.ssa.gov/poms.nsf/lnx/0423022130
https://secure.ssa.gov/poms.nsf/lnx/0423022150
https://secure.ssa.gov/poms.nsf/lnx/0423022155
https://secure.ssa.gov/poms.nsf/lnx/0423022185
https://secure.ssa.gov/poms.nsf/lnx/0423022440
https://secure.ssa.gov/poms.nsf/lnx/0423022973
https://secure.ssa.gov/poms.nsf/lnx/0423022270
https://secure.ssa.gov/poms.nsf/lnx/0423022645
https://secure.ssa.gov/poms.nsf/lnx/0423022290
https://secure.ssa.gov/poms.nsf/lnx/0423022347
"""
# define columns of interest. some of these will match the first data element in a table row
cols = ['SECTION_NUMBER',
        'ICD-9',
        'ICD-10',
        'DISEASE_NAME',
        'ALTERNATE NAMES',
        'DESCRIPTION',
        'DIAGNOSTIC TESTING, PHYSICAL FINDINGS, AND ICD-9-CM/ICD-10-CM CODING',
        'PROGRESSION',
        'TREATMENT',
        'LAST_UPDATE']

html_content = requests.get(url)
#print(html_content.text)

# some helpful fields are hidden tags
# <input name="SectionTitle" type="hidden" value="Cri du Chat Syndrome">
# <input name="ComputedID" type="hidden" value="DI 23022.375">
# <input name="LastUpdate" type="hidden" value="10/05/2020">

soup = BeautifulSoup(html_content.text, "html.parser") # "lxml")
#print(soup.prettify()) # print the parsed data of html

# find the table
caltable = soup.find("table", attrs={"class": "poms-table poms-table-brdr-all", "id": "tbl_1"})
#print(re.sub(u"\u200b", " ", caltable.prettify()))
#sys.exit()
# find all rows
calrows = caltable.tbody.find_all("tr")
i = 0
d = {}
#print("***** ROW DATA *****")
for row in calrows:
    rowdata = []
    for td in row.find_all("td"):
        try:
            # replace all newlines with space and strip whitespace
            #print(td.text.replace("\n", " ").strip())
            rowdata.append(td.text.replace("\n", " ").strip())
        except:
            print("tried and failed")
            pass
    # print row data
    print(re.sub(u"\u200b", " ", str(i) + "\t" + "\t".join(rowdata)))
    # purge extra spaces from row headings
    rowdata[0] = re.sub(" +", " ", rowdata[0])
    rowdata[0] = re.sub("DESCRIPTION DIAGNOSTIC", "DIAGNOSTIC", rowdata[0])
    rowdata[0] = re.sub("DIAGNOSTICTESTING", "DIAGNOSTIC TESTING", rowdata[0])
    #print("ROWDATA[0]\t", rowdata[0])
    # if(rowdata[0] in cols):
    #     #print(rowdata[0])
    # return the matched value as a valid key in cols
    key = retmatch(rowdata[0], cols)
    if key != "None":
        d[key] = rowdata[1]
    i += 1

# grab the hidden tag data
# disease name
DISEASE_NAME = soup.find("input", attrs={"name": "SectionTitle", "type": "hidden"})
print("SectionTitle", DISEASE_NAME["value"])
d["DISEASE_NAME"] = DISEASE_NAME["value"]
# section number
SECTION_NUMBER = soup.find("input", attrs={"name": "ComputedID", "type": "hidden"})
print("ComputedID", SECTION_NUMBER["value"])
d["SECTION_NUMBER"] = SECTION_NUMBER["value"]
# grab the last update date
LAST_UPDATE = soup.find("input", attrs={"name": "LastUpdate", "type": "hidden"})
print("LastUpdate", LAST_UPDATE["value"])
d["LAST_UPDATE"] = LAST_UPDATE["value"]
#print out columns followed by the row of data
print("\t".join(cols))

# extract ICD9/10 codes from d['DIAGNOSTIC TESTING, PHYSICAL FINDINGS, AND ICD-9-CM/ICD-10-CM CODING']
d['ICD-9'] = "something"
d['ICD-10'] = "something"

dval = []
for col in cols:
    if col in d:
        # replace multiple spaces with a single space
        dval.append(re.sub(" +", " ", d[col]))
    else:
        dval.append("")
print("\t".join(dval))

