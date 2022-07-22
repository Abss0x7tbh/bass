testdns
=======

Abss0x7tbh's 'bass' is a good idea. 'testdns' is a tool to help identify valid resolvers for a given hostname. 'bass' 
aims to provide lists of resolvers for a given DNS provider, testdns (along with a handful of other free tools) aims to 
help us create these lists.

lets imagine we're interested in finding resolvers for 'tripadvisor.com'. we follow the process described in detail in 
the main advisory.

running a whois on tripadvisor.com yields the following:

    Name Server: dns1.p08.nsone.net
    Name Server: dns4.p08.nsone.net
    Name Server: dns3.p08.nsone.net
    Name Server: pdns3.ultradns.org
    Name Server: dns2.p08.nsone.net
    Name Server: pdns6.ultradns.co.uk
    Name Server: pdns1.ultradns.net
    Name Server: pdns2.ultradns.net
    Name Server: pdns4.ultradns.org
    Name Server: pdns5.ultradns.info

lets focus on nsone for the time being. the first thing we're going to want to do is identify all IP ranges associated 
with 'nsone.net'. to do this we could spend 25 minutes combing through open RIPE data (and the like) or we could use 
'asnip' (https://github.com/harleo/asnip) which seems to do pretty good job of things for us.

    nslookup dns1.p08.nsone.net
    Server:		192.168.1.1
    Address:	192.168.1.1#53
    
    Non-authoritative answer:
    Name:	dns1.p08.nsone.net
    Address: 198.51.44.8

    ./asnip --help
    Usage of ./asnip:
    -p	Print results to console
    -t string
    Domain or IP address (Required)

    ./asnip -t 198.51.44.8
    [?] ASN: "62597" ORG: "NSONE, US"
    [:] Writing 32 CIDRs to file...
    [:] Converting to IPs...
    [:] Writing 8128 IPs to file...
    [!] Done.

with asnip's help we should now have a list of prefixes belonging to nsone, cidr.txt
     
    wc -l cidrs.txt
    32 cidrs.txt

next we're going to scan these ranges for DNS servers. while nowadays it's common to find DNS servers running over TCP, 
traditionally DNS is a UDP thing for now at least we can assume providers will ensure that first and foremost UDP is 
available.

as we all know UDP is entirely stateless and is in so many ways a pleasure to work with when it comes to mass scanning.
SYN scanning for TCP is always going to produce a heft of results that require further validation, while scanning for 
UDP services involves us sending a specific payload and simply listening for valid responses.

the zmap repo comes complete with a handful of useful UDP payloads, so we're going to use zmap for this. the same effect
can almost certainly be achieved using masscan, alas off the top of my head i couldn't tell you how.
    
    git clone https://github.com/zmap/zmap
    Cloning into 'zmap'...
    remote: Enumerating objects: 6876, done.
    remote: Counting objects: 100% (301/301), done.
    remote: Compressing objects: 100% (164/164), done.
    remote: Total 6876 (delta 167), reused 221 (delta 123), pack-reused 6575
    Receiving objects: 100% (6876/6876), 6.03 MiB | 1.24 MiB/s, done.
    Resolving deltas: 100% (4805/4805), done.
    cd zmap
    ls
    10gigE.md	CHANGELOG.md	CONTRIBUTING.md	INSTALL.md	README.md	conf		examples	lib		src
    AUTHORS		CMakeLists.txt	Dockerfile	LICENSE		checkFormat.sh	containers	format.sh	scripts		test
    # BUILD ZMAP AS PER THE DOCS.
    zmap -M udp -p 53 --probe-arg=file:examples/udp-probes/dns_53.pkt -w ../asnip/cidr.txt > asone_udp53_dns

if all is well we now have a file called 'asone_udp53_dns' containing ips of valid DNS servers inside the ranges kindly 
discovered by 'asnip' earlier. all that's left is to use the attached tool to identify ones who give valid responses for
'tripadvisor.com' (either because they're authoritative or recursive).

    ulimit -SHn 99999 # we like fast.
    cat asone_udp53_dns | go run main.go -hostname tripadvisor.com -workers 50 | tee asone_resolvers.txt

in an ideal world we now have 'asone_resolvers.txt', which should look a lot like nsone.txt from the parent project :)