# sanscan-py
Scan website for sub domains, then check each sub domain for SAN certificates.
<BR><BR>

**Useage example:**<BR>
./sanscan.py https://www.github.com
<BR><BR>


A good number of organizations use Subject Alternative Name (SAN) certificates on their websites. The benefit of these being you can purchase one SSL certificate to cover multiple sites and hostnames.

SAN certs can be a point where data can leak if you are registering SAN entries for hostnames which you would not normally want external parties to be aware of. For example you might have a certificate for your www.company.com site, but have a SAN entry for secretserver.company.com. So by reading the SAN details, unpublished systems can become discoverable. Of course best-practice would be to not use SAN certs for these systems.

To make this into a quick proof of concept, I built a Bash script which will scan a site for subdomains found in hyperlinks, then it will attempt to download the SSL certificate for each sub domain and extract the SAN details from each of them! This quickly gives a list of all discoverable subdomains. 
