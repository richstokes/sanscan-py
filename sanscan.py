#!/usr/bin/python3
#Take a given domain, extract all subdomains found in HTML source, check each one for SSL certs
import sys
import ssl, socket
import urllib.request
import lxml.html


if len(sys.argv) < 2:
    quit("Useage example: \n ./sanscan.py https://www.github.com \n")
elif "https" not in str(sys.argv[1]):
    quit("Error: Please specify https website as first argument. \n\nUseage example: \n ./sanscan.py https://www.github.com \n")
else:
    website = str(sys.argv[1])
    domain = website.replace("https://","")
    domain = domain.replace("www.","")

#Intro message
print("SAN Scan running for Website:", website, "(Raw domain:", domain, ")\n")


#Function to connect via SSL and grab the cert details
def getCert(hostname):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    s = ctx.wrap_socket(socket.socket(), server_hostname=hostname)
    try:
        s.connect((hostname, 443))
        cert = s.getpeercert()
    except:
        print("SSL Connection error")
    try:
        altName = cert['subjectAltName'] #get the SAN piece from the cert
        altName = [x[1] for x in altName] #get the values from the DNS field
        altName = ' '.join((altName)) #make Tuple nice to read
        print("Listing Subject Alternative Names found for", hostname)
        print(altName, "\n")
    except:
        print("Trying next")

#Function to connect via HTTP and find unique subdomains within the HTML source
def getLinks(website):
    global subdomains
    subdomains = []
#configure urllib context
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.check_hostname=False
    context.verify_mode=ssl.CERT_NONE
#configure request details
    req = urllib.request.Request(
    website,
    data=None,
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }
    )
    connection = urllib.request.urlopen(req, context=context)
    dom = lxml.html.fromstring(connection.read())
    for link in dom.xpath('//a/@href'): # select the url in href for all a tags(links)
        if domain in str(link):
            link = link.split('/', 3)
            #print(link[2])
            subdomains.append(link[2]) #add subdomain to list

        #else: #debug text
            #print("Link found not part of original domain")



#Call function to add subdomains to list for scanning
getLinks(website)

#Clean up discovered subdomain list
subdomains = list(set(subdomains)) #Use a set to take unique items from list

#Scan list of subdomains for SAN certs
for s in subdomains:
    getCert(s)
