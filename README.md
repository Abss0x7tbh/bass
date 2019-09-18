# bass

**bass** aim's at maximizing your resolver count wherever it can by combining different valid dns servers from the targets DNS Providers & adding them to your initial set of public resolvers ( here located in `public.txt`), thereby allowing you to use the maximum number of resolvers obtainable for your target. This is more of a `best-case-scenario` per target.

More the resolvers , lesser the traffic to each resolver when using tools like massdns that perform concurrent lookups using internal hash table. So easier to scale your target list.

# Find

[massNS](https://github.com/Abss0x7tbh/massNS) partially showed a simple case of existence of what i call "*backup authoritative dns servers*" that exist with DNS Providers and contain the same zone files as the primary authoritative nameservers of your target. They usually act as secondary/slave nameserver(backup strategy). They also answer authoritatively to the targets DNS queries. This is handled by a domains DNS Provider & most of them are configured the same way.

# Concept

Concept is to gather all abiding DNS servers from the providers network(their ASN) and in cases of multiple providers combine them. Eventually add them to your filtered list of `public.txt` to give you a maximum count.

**Algorithm:**

Detect DNS Providers > Gather resolvers from detected Providers (all `.txt` files inside `./bass/resolvers/` > Combine them with filtered public-dns resolvers (`pubic.txt`) > use against your target (massdns etc)

![Concept Of bass](https://user-images.githubusercontent.com/32202226/65170066-cab27a80-da3f-11e9-84c1-c70973d0a684.png)

**Example:**

Assume your target is `PayPal`.

```
paypal.com	nameserver = pdns100.ultradns.com.
paypal.com	nameserver = ns1.p57.dynect.net.
paypal.com	nameserver = pdns100.ultradns.net.
paypal.com	nameserver = ns2.p57.dynect.net.
```

bass will combine all the resolvers from `/resolvers/dynect.txt` & `/resolvers/ultradns.txt` which totals to `4017` resolvers. These resolvers are then added to a filtered public-dns resolvers `public.txt`, giving you a final list of resolvers that you can use against target list of paypal domains. The count in this case is public.txt + `4017` resolvers. Use them as resolvers with massdns for best results.

# Usage


```
git clone https://github.com/Abss0x7tbh/bass.git
cd bass
pip3 install -r requirements.txt
python3 bass.py -d target.com -o output/file/for/final_resolver_list.txt
```

**Reference:**

| Flag  | What it does |
| ------------- | ------------- |
| -d / --domain  | Specify target root domain  |
| -o/ --output  | Specify where bass has to ouput the final resolver list  |



**Example:**

```
python3 bass.py -d paypal.com -o paypal_resolvers.txt
```

# Limitations

- More DNS Providers are yet to be found & added.

- Some NS record of `target 1` might be `ns1.xyz.com` and `target 2` might be `ns2.xyz.com` . So there are some DNS servers of providers that have only zone file of `ns1.xyz.com` so they wouldn't function for `target 2`. I have just added them all together as further classification is difficult. This only happens in the case of `nsone` as far as i have observed.

# Providers

There are close to 11 DNS Providers added. There could be more.

# public.txt

You can use your own custom filtered list of public-dns resolvers. Just add them to your `public.txt` so that bass defaults to it when there are no additional resolvers to be found or adds to it in case they are found. i have just added what i could validate.

# Contributors

Thanks to [Patrik Hudak](https://twitter.com/0xpatrik) for some good suggestions and help!
