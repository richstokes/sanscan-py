# sanscan-py
Scan website for sub domains, then check each sub domain for SAN certificates.  


### Usage example  
`python3 sanscan.py https://www.github.com`  


### Why?  

A good number of website use Subject Alternative Name (SAN) certificates. The benefit of these being you can purchase one SSL certificate to cover multiple sites and hostnames.  

SAN certs can be a leak information if you are registering SAN entries for hostnames which you would not normally want external parties to be aware of. For example you might have a certificate for your www.company.com site, but have a SAN entry for staging.company.com. So by reading the SAN details, unpublished systems can become discoverable.  

This script searches the site for subdomains (via links), and then prints all SAN's for all subdomains.  

It can be useful for discovering endpoints that are not part of the top level certificate.  
