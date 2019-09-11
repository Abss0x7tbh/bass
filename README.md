# bass

**bass** aim's at collecting a huge number of authoritative nameservers that can be used as resolvers from your target's DNS Provider/(s). bass will act more like a combiner that would eventually determine the DNS Providers used by your target, combine the nameservers from each of them & by default add a properly filtered list of public-dns resolvers to give you a `Maximum` resolver count against your target.

# Concept 

Detect DNS Providers > Gather resolvers from detected Providers > Combine them with filtered public-dns resolvers > use against your target (massdns etc)

![Concept Of bass](https://github.com/Abss0x7tbh/bass/blob/master/ss/concept_bass.png)

**Example :**

Assume your target is `PayPal`.

```
paypal.com	nameserver = pdns100.ultradns.com.
paypal.com	nameserver = ns1.p57.dynect.net.
paypal.com	nameserver = pdns100.ultradns.net.
paypal.com	nameserver = ns2.p57.dynect.net.

```

bass will combine all the resolvers from `dynect` & `ultradns` which totals to `4017` resolvers. You should be able to use these `4017` resolvers against your list of paypal hosts. 

# Limitations

More DNS Providers are yet to be added.

# To-Do

script the combiner in python
