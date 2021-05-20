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
import time

def retmatch(st, lst):
    retval = "None"
    for le in lst:
        #if re.sub(" +", "", st) == re.sub(" +", "", le):
        if st.split(" ")[0] == le.split(" ")[0]:
            retval = le
    return retval

#url = "https://secure.ssa.gov/apps10/poms.nsf/lnx/0423022375"
# the following links had issues
urls1 = ["https://secure.ssa.gov/poms.nsf/lnx/0423022927",
        "https://secure.ssa.gov/poms.nsf/lnx/0423022365",
        "https://secure.ssa.gov/poms.nsf/lnx/0423022130",
        "https://secure.ssa.gov/poms.nsf/lnx/0423022150",
        "https://secure.ssa.gov/poms.nsf/lnx/0423022155",
        "https://secure.ssa.gov/poms.nsf/lnx/0423022185",
        "https://secure.ssa.gov/poms.nsf/lnx/0423022440",
        "https://secure.ssa.gov/poms.nsf/lnx/0423022973",
        "https://secure.ssa.gov/poms.nsf/lnx/0423022270",
        "https://secure.ssa.gov/poms.nsf/lnx/0423022645",
        "https://secure.ssa.gov/poms.nsf/lnx/0423022290",
        "https://secure.ssa.gov/poms.nsf/lnx/0423022347"]

urls = [
    "https://secure.ssa.gov/poms.nsf/lnx/0423022085", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022090", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022921", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022923", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022665", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022095", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022925", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022670", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022675", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022680", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022350", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022927", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022355", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022100", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022105", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022600", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022540", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022106", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022929", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022110", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022360", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022111", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022365", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022931", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022933", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022370", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022115", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022125", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022127", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022130", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022685", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022580", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022935", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022133", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022135", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022690", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022695", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022700", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022937", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022705", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022136", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022140", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022141", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022939", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022143", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022710", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022605", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022145", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022375", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022380", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022941", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022146", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022943", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022385", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022390", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022545", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022945", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022550", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022150", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022947", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022155", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022156", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022715", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022160", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022949", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022395", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022163", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022720", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022165", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022170", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022951", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022725", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022400", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022953", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022730", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022175", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022180", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022181", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022185", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022735", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022470", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022186", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022190", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022555", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022560", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022405", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022745", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022955", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022957", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022750", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022191", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022755", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022760", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022765", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022770", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022565", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022775", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022420", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022780", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022195", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022425", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022200", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022201", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022959", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022202", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022430", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022785", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022205", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022207", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022210", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022790", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022215", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022435", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022440", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022961", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022216", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022220", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022610", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022221", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022795", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022225", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022615", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022800", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022805", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022226", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022963", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022965", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022620", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022227", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022230", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022445", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022231", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022815", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022967", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022820", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022233", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022234", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022969", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022825", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022450", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022235", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022575", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022455", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022415", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022410", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022495", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022460", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022625", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022630", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022830", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022465", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022470", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022835", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022971", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022236", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022240", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022475", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022973", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022245", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022840", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022845", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022246", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022250", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022850", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022255", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022120", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022260", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022261", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022265", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022635", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022480", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022855", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022860", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022865", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022870", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022270", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022975", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022875", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022977", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022877", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022275", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022280", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022640", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022645", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022483", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022485", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022281", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022490", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022650", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022282", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022585", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022655", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022979", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022285", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022286", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022880", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022885", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022887", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022981", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022287", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022290", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022295", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022890", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022296", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022298", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022983", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022590", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022985", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022297", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022810", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022300", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022305", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022310", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022311", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022315", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022320", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022325", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022895", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022326", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022330", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022900", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022500", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022905", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022335", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022505", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022337", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022910", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022510", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022343", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022515", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022660", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022340", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022987", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022595", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022520", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022345", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022989", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022570", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022525", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022915", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022530", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022920", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022346", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022347", 
    "https://secure.ssa.gov/poms.nsf/lnx/0423022535"
    ]


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
#print out columns followed by the row of data
print("\t".join(cols))

for url in urls:
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
        #print(re.sub(u"\u200b", " ", str(i) + "\t" + "\t".join(rowdata)))
        if re.search("DIAGNOSTIC", rowdata[0]):
            print(re.sub(" +", " ", rowdata[0]))
    time.sleep(1)
