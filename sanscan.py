#!/usr/bin/python3
#Take a given domain, extract all subdomains found in HTML source, check each one for SSL certs

import sys
import ssl, socket
import urllib.request
import lxml.html


if len(sys.argv) < 2:
    quit("Useage example: \n ./sanscan.py https://www.github.com \n")
else:
    website = str(sys.argv[1])
    domain = website.replace("https://","")
    domain = domain.replace("www.","")
#need something to clean up the input, i.e. add/remove http/https if present

#Testing vars
print("SAN Scan running for Website:", website, "(Raw domain:", domain, ")\n")


#Function to connect via SSL and grab the cert details
def getCert(hostname):
    ctx = ssl.create_default_context()
    s = ctx.wrap_socket(socket.socket(), server_hostname=hostname)
    s.connect((hostname, 443))
    cert = s.getpeercert()
    altName = cert['subjectAltName'] #get the SAN piece from the cert
    altName = [x[1] for x in altName] #get the values from the DNS field
    altName = ' '.join((altName)) #make Tuple nice to read
    print("Listing Subject Alternative Names found for", hostname)
    print(altName, "\n")


#Function to connect via HTTP and find unique subdomains within the HTML source
def getLinks(website):
    global subdomains
    subdomains = []
    connection = urllib.request.urlopen(website)
    dom = lxml.html.fromstring(connection.read())
    for link in dom.xpath('//a/@href'): # select the url in href for all a tags(links)
        if domain in str(link):
            link = link.split('/', 3)
            #print(link[2])
            subdomains.append(link[2]) #add subdomain to list

        #else:
            #print("Link found not part of original domain")

#getCert(domain)

#Call function and add subdomains to list for scanning
getLinks(website)

#Clean up discovered subdomain list
subdomains = list(set(subdomains)) #Use a set to take unique items from list


#Scan list of subdomains for SAN certs
for s in subdomains:
    getCert(s)
