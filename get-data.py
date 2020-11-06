import requests
import os
import ftplib
import json

filename = "data.json"
clientpath = "public/data/"
serverpath = "/public_html/japan-by-bike/data/"
data_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTg_NYClqpOEzBmdyP-rZdIYkhBJomwUFQTl_sdI7IoXQdgm_8pe369YyFTPB1b66lgKw3Lj5VKGDfg/pub?gid=0&single=true&output=csv"
trans_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTg_NYClqpOEzBmdyP-rZdIYkhBJomwUFQTl_sdI7IoXQdgm_8pe369YyFTPB1b66lgKw3Lj5VKGDfg/pub?gid=1997455458&single=true&output=csv"

session_requests = requests.session()
result = session_requests.get(
	data_url, 
	headers = dict(referer = data_url)
)

data = []
data_rows = result.content.split("\n")
row_count = 0
for row in data_rows:
	data_cols = row.split(",")
	if row_count > 0 and data_cols[1]:
		data.append({
            "filename": data_cols[0],
            "title": data_cols[2],
            "distance": data_cols[3],
            "completed": data_cols[4]            
        })
	row_count = row_count + 1

result = session_requests.get(
	trans_url, 
	headers = dict(referer = trans_url)
)

data_rows = result.content.split("\n")
translations = []
for row in data_rows:
    data_cols = row.split(",")
    if row_count > 0 and data_cols[1]:
        translations.append({
            "key": data_cols[0],
            "ja": data_cols[1]
        })
	row_count = row_count + 1

content = {
    "rides": data,
    "translations": translations
}


try:
    os.remove(clientpath + filename)
except OSError:
    pass

def upload(ftp, file):
    ext = os.path.splitext(clientpath + file)[1]
    if ext in (".txt", ".json", ".htm", ".html"):
        ftp.storlines("STOR " + serverpath + file, open(clientpath + file))
    else:
        ftp.storbinary("STOR " + serverpath + file, open(clientpath + file, "rb"), 1024)

with open(clientpath + filename, 'w') as f:
    f.write(json.dumps(content))


ftp = ftplib.FTP("sl217.web.hostpoint.ch")
ftp.login("hanjoch", "392_%^sm635!5^zY")

upload(ftp, filename)

print (json.dumps(content))
