from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import defaultdict

import ssl
import re
import json
import datetime

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

try:
	html = urlopen("http://idengue.arsm.gov.my/hotspot.php", context=ctx).read()
except:
	print("Host unreachable!")
	quit()

soup = BeautifulSoup(html, "html.parser")

meta = soup.find_all('tr')[0] # metadata for last updated date and week
data = soup.find_all('tr')[2] # list of hotspot

row_marker = 1
column_marker = 0
column = 0
df = defaultdict(dict)
key = ["no", "negeri", "pbt_kkm", "lokaliti_wabak", "kumulatif_kes", "tarikh_mula", "tempoh_wabak"]

# start processing meta data
updated_at = re.findall("[0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9]", str(meta))[0].split('-')
updated_at = datetime.date(int(updated_at[2]), int(updated_at[1]), int(updated_at[0]))

# start processing list of hotspot
# to process all <td> tags only, <tr> was no properly closed
for td in data.find_all('td'):

	df[row_marker][key[column_marker]] = td.get_text().strip()
	column += 1
	column_marker += 1

	# split to new row for every 7 columns
	if column % 7 == 0:
		row_marker += 1
		column_marker = 0

with open('output/idengue_output_' + updated_at.strftime("%Y%m%d_%U") + '.json', 'w') as outfile:
	json.dump(df, outfile)

print("Last update : ", updated_at)
