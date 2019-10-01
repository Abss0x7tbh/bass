# 🅑🅐🅢🅢

**bass** aim's at maximizing your resolver count wherever it can by combining different valid dns servers from the targets DNS Providers & adding them to your initial set of public resolvers (here located in [/resolvers/public.txt](https://github.com/Abss0x7tbh/bass/blob/master/resolvers/public.txt)), thereby allowing you to use the maximum number of resolvers obtainable for your target. This is more of a `best-case-scenario` per target.

More the resolvers, lesser the traffic to each resolver when using tools like massdns that perform concurrent lookups using internal hash table. So easier it is to scale your target list 

# Table Of Contents


- [Concept Of Tool](#concept-of-tool)
    + [DIY to know how exactly are these resolvers extracted](#diy-to-know-how-exactly-are-these-resolvers-extracted)
- [About public.txt](#publictxt)
- [Usage](#usage)
- [Output](#output)
- [Limitations](#limitations)
- [Providers](#providers)
     + [Provider Contributors](#provider-contributors)
- [Contributors](#contributors)


# Concept Of Tool

Concept is to gather all abiding DNS servers from the providers network(their ASN) and in cases of multiple providers combine their nameservers. Eventually add them with your filtered list of `public.txt` to give you a maximum count of resolvers for the specified target.

**Algorithm of bass :**

Detect DNS Providers > Gather resolvers from detected Providers (all `.txt` files inside `./bass/resolvers/` > Combine them with filtered public-dns resolvers (`pubic.txt`) > use against your target (via massdns etc)

![Concept Of bass](https://user-images.githubusercontent.com/32202226/65170066-cab27a80-da3f-11e9-84c1-c70973d0a684.png)

**Example using live test case :**

1. Assume your target is `PayPal`.

```
paypal.com	nameserver = pdns100.ultradns.com.
paypal.com	nameserver = ns1.p57.dynect.net.
paypal.com	nameserver = pdns100.ultradns.net.
paypal.com	nameserver = ns2.p57.dynect.net.
```

bass will combine all the resolvers from `/resolvers/dynect.txt` & `/resolvers/ultradns.txt` which totals to `4017` resolvers. These resolvers are then added to a filtered public-dns resolvers `public.txt`, giving you a final list of resolvers that you can use against target list of paypal domains. The count in this case is public.txt + `4017` resolvers. Use them as resolvers with massdns for best results.

### DIY to know how exactly are these resolvers extracted

DNS Providers and their network have a lot of nameservers. Some primary, some secondary and some both. bass looks for those nameservers that share the same zone files as the primary authoritative nameservers employed to all their clients. So these nameservers would also answer authoritatively. They can also in bulk be used as resolvers for your target.


- Let's take a target , [airbnb.com](https://airbnb.com). First let's find it's nameservers :
```
$ host -t ns airbnb.com
airbnb.com name server ns2.p74.dynect.net.
airbnb.com name server dns1.p08.nsone.net.
airbnb.com name server dns2.p08.nsone.net.
airbnb.com name server ns3.p74.dynect.net.
airbnb.com name server dns4.p08.nsone.net.
airbnb.com name server dns3.p08.nsone.net.
airbnb.com name server ns1.p74.dynect.net.
airbnb.com name server ns4.p74.dynect.net.
```
- We could see that airbnb uses dynect & nsone nameservers. Our goal is to ask these providers if they have more nameservers in their network that could also resolve airbnb.
- Let's take one of the providers for this DIY, dynect. Let's explore the nameservers subnet for more nameservers that share zone file. Get ip address of `ns2.p74.dynect.net` using `host ns2.p74.dynect.net` i.e `162.88.18.12`.
- Search this ip on [bgp.he.net](https://bgp.he.net/ip/162.88.18.12) & get ASN & CIDR. In this case CIDR is `162.88.18.0/24`.
- Now masscan this cidr for port 53 to get all DNS servers first.
```
sudo masscan 162.88.18.0/24 -p 53 --rate=1000 | awk '{print $NF}' > diy.txt
```
- We get close to 31 DNS servers in diy.txt. They are :

```
162.88.18.18
162.88.18.28
162.88.18.20
162.88.18.15
162.88.18.23
162.88.18.19
162.88.18.11
162.88.18.12
162.88.18.4
162.88.18.27
162.88.18.10
162.88.18.26
162.88.18.24
162.88.18.9
162.88.18.16
162.88.18.25
162.88.18.1
162.88.18.13
162.88.18.17
162.88.18.6
162.88.18.22
162.88.18.3
162.88.18.31
162.88.18.21
162.88.18.29
162.88.18.8
162.88.18.7
162.88.18.30
162.88.18.2
162.88.18.14
162.88.18.5
```
- **In this case** all of these 31 DNS servers share the same zone files as the primary nameserver of airbnb and hence answer authoritatively. So pick any one in random and run lookup on it as :

```
 dig @162.88.18.25 airbnb.com

; <<>> DiG 9.11.3-1ubuntu1.8-Ubuntu <<>> @162.88.18.25 airbnb.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 42042
;; flags: qr aa rd; QUERY: 1, ANSWER: 3, AUTHORITY: 8, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;airbnb.com.                    IN      A

;; ANSWER SECTION:
airbnb.com.             60      IN      A       52.87.45.227
airbnb.com.             60      IN      A       52.205.157.89
airbnb.com.             60      IN      A       34.200.100.113

;; AUTHORITY SECTION:
airbnb.com.             86400   IN      NS      dns3.p08.nsone.net.
airbnb.com.             86400   IN      NS      dns2.p08.nsone.net.
airbnb.com.             86400   IN      NS      ns3.p74.dynect.net.
airbnb.com.             86400   IN      NS      dns4.p08.nsone.net.
airbnb.com.             86400   IN      NS      ns1.p74.dynect.net.
airbnb.com.             86400   IN      NS      dns1.p08.nsone.net.
airbnb.com.             86400   IN      NS      ns4.p74.dynect.net.
airbnb.com.             86400   IN      NS      ns2.p74.dynect.net.

;; Query time: 4 msec
;; SERVER: 162.88.18.25#53(162.88.18.25)
;; WHEN: Wed Sep 18 16:50:03 UTC 2019
;; MSG SIZE  rcvd: 343


```
You will be able to resolve your target authoritatively using +31 more nameservers now.

The process does not end here. Not all cases are such. Out of the nameservers collected some would/could be used for a completely different purpose and would REFUSE . Also all the networks of the Providers have been sourced & validated, so multiple ASN lookups on the provider have been done. I have validated them and placed them under `~/resolvers/*.txt` 



# public.txt

[/resolvers/public.txt](https://github.com/Abss0x7tbh/bass/blob/master/resolvers/public.txt) is a default constant operand to the addition of nameservers. It contains validated public nameservers from [public-dns](https://public-dns.info/nameservers.txt). You can either add more or delete public resolvers from here as you might have your own validated list of them already. This is what bass will use as a default i.e it will either add more resolvers to it or just give you the same.

All nameservers in `public.txt` have been validated using **[dnsvalidator](https://github.com/vortexau/dnsvalidator)**

In short you either walk away with what you already have in your `public.txt` or something more!


# Usage


```
git clone https://github.com/Abss0x7tbh/bass.git
cd bass
pip3 install -r requirements.txt
python3 bass.py -d target.com -o output/file/for/final_resolver_list.txt
```

**Reference :**

| Flag  | What it does |
| ------------- | ------------- |
| -d / --domain  | Specify target root domain  |
| -o/ --output  | Specify where bass has to ouput the final resolver list  |



**Example :**

```
cd bass && python3 bass.py -d paypal.com -o ~/output/paypal_resolvers.txt
```


# Output

This output shows the **total** count of validated public resolvers present in `/resolvers/public.txt` which are ~3.5k in number and the remaining `4017` that bass could collect from the targets (here paypal) providers. They are subject to change if you have a different `public.txt`.

![output](https://user-images.githubusercontent.com/33752861/65172764-3c53ee00-da6b-11e9-8d6d-610987916770.png)


# Limitations

- More DNS Providers are yet to be found & added.

- Some NS record of `target 1` might be `ns1.xyz.com` and `target 2` might be `ns2.xyz.com` . So there are some DNS servers of providers that have only zone file of `ns1.xyz.com` so they wouldn't function for `target 2`. I have just added them all together as further classification is difficult. This only happens in the case of `nsone` as far as i have observed.


# Providers

There are close to 20 DNS Providers added. There could be more.

## Provider Contributors

- Kudos to [streaak](https://twitter.com/streaak) for sourcing more than 9+ providers with resolvers ranging anywhere between 100 - 6000!


# Contributors

- Thanks a lot [Patrik Hudak](https://twitter.com/0xpatrik) for some good suggestions and help!
- Thanks a lot [Shuaib Oladigbolu](https://twitter.com/_sawzeeyy) for your contributions with the code & other refactorings!

bass automatically tells you of any new providers it does not have resolvers for. If you want to contribute then open an issue with the providers name so that we could increase the reach. Thanks
