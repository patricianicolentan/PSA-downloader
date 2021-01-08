# PSA Downloader

# Note: the final file names will sometimes be too many characters to open, renaming them will be a separate project

import webbrowser, requests, bs4, os
from bs4 import BeautifulSoup

os.makedirs('PSA', exist_ok=True)

# this is the Philippine Statistics Authority's website 
PSAurl = 'http://www.psa.gov.ph/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
response = requests.get(PSAurl, headers=headers)
PSAsoup = BeautifulSoup(response.text, "lxml")
main_urls = []

# specify the data you are looking to follow in this follow_list
follow_list = ["Inflation", "Approved Foreign Investments", "Philippine Export and Import Statistics", "Labor Force Survey", "Performance of the Philippine Economy", "GDP"]

# this is how the PSA website formats the new release links on the main page
found = PSAsoup.select('h3 > a')
for x in found:
	for y in follow_list:
		if y in str(x):
			# this prints the data title 
			print(y)
			# if the linked page is a file, it starts with http already
			if (x.get('href')).startswith("http"):
				URL = x.get('href')
			else:
				URL = 'https://psa.gov.ph/' + x.get('href')
			main_urls.append(URL)
			print('Done with main link ' + URL)


if not main_urls:
	print('There was no preferred data point on the PSA website today.')

for link in main_urls:
	response = requests.get(link, headers=headers)	
	soup = BeautifulSoup(response.text, "lxml")
	# sometimes, the link on the main page is the file itself
	if link.endswith(('.pdf', '.xlsx')):
		# use that link as the file
		req = requests.get(link)
		saveFile = open(os.path.join('PSA', os.path.basename(str(link))), 'wb')
		for chunk in req.iter_content(chunk_size=1000000):
			saveFile.write(chunk)
		saveFile.close()
		print('Done with file link ' + str(link))

	# other times, it goes to a press release page with further links	
	else:
		for files in soup.select('span.file > a'):
			req = requests.get(files.get('href'))
			saveFile = open(os.path.join('PSA', os.path.basename(str(files.get('href')))), 'wb')
			for chunk in req.iter_content(chunk_size=1000000):
				saveFile.write(chunk)
			saveFile.close()
			print('Done with file link ' + str(files.get('href')))


