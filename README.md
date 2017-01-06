# sanscan-py
Scan website for sub domains, then check each sub domain for SAN certificates.
<BR><BR>

**Useage example:**<BR>
./sanscan.py https://www.github.com
<BR><BR>

**Why?**<BR>
A good number of organizations use Subject Alternative Name (SAN) certificates on their websites. The benefit of these being you can purchase one SSL certificate to cover multiple sites and hostnames.

SAN certs can be a point where data can leak if you are registering SAN entries for hostnames which you would not normally want external parties to be aware of. For example you might have a certificate for your www.company.com site, but have a SAN entry for dev.company.com. So by reading the SAN details, unpublished systems can become discoverable. Of course best-practice would be to not use SAN certs for these systems.

To enhance this, I have the script first search the website for subdomains, then check each of those for SAN certs in turn.
