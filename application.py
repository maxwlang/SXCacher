from bs4 import BeautifulSoup
from twisted.internet import task
from twisted.internet import reactor
import urllib, os

url = "https://sx.xecuter.com/"
timeout = 1800.0
userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'

soup = ""
osSavePath = "./SXOS"
gearSavePath = "./SXGear"
toolsSavePath = "./SXTools"

def updateScrapeContent():
	global userAgent
	global soup

	request = urllib.request.Request(url)
	request.add_header('User-Agent', userAgent)
	result = urllib.request.urlopen(request)
	page = result.read()
	soup = BeautifulSoup(page, features="lxml")
	soup.prettify()

def downloadFile(url, dir):
	global userAgent
	print(url + " (" + dir + "/" + os.path.basename(url) + ")")
	
	if(not os.path.isfile(dir + "/" + os.path.basename(url))):
		print("Downloading..")
		opener = urllib.request.build_opener()
		opener.addheaders = [('User-agent', userAgent)]
		urllib.request.install_opener(opener)
		urllib.request.urlretrieve(url, dir + "/" + os.path.basename(url))
	else:
		print("File exists. Not Downloading")
	
def tryUpdateFiles():
	print("Grabing html..")
	updateScrapeContent()

	print("Checking..")

	global soup
	global osSavePath
	global gearSavePath
	global toolsSavePath
	global loaderSavePath
	
	for anchor in soup.findAll('a', href=True):
		if(anchor['href'].startswith('/download')):
			if('SXOS' in anchor['href'] and '.zip' in anchor['href']):
				downloadFile(url + "download/" + os.path.basename(anchor['href']), osSavePath)
			if('SX_Gear' in anchor['href'] and '.zip' in anchor['href']):
				downloadFile(url + "download/" + os.path.basename(anchor['href']), gearSavePath)
			if('SXTools' in anchor['href'] and '.apk' in anchor['href']):
				downloadFile(url + "download/" + os.path.basename(anchor['href']), toolsSavePath)
	print("Complete.")
	pass

l = task.LoopingCall(tryUpdateFiles)
l.start(timeout)

reactor.run()