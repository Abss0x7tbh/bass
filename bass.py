#!/usr/bin/env python3
import dns.resolver
import argparse
import tldextract
import os
from colorama import Fore, Style
from sys import stderr


def banner():
    # banner
    print(''' _
| |__   __ _ ___ ___
| '_ \ / _` / __/ __|
| |_) | (_| \__ \__ \\
|_.__/ \__,_|___/___/''')

    # Author & contributor
    print("------------------------------------------")
    print(f"Author: {Fore.BLUE}@abss0x7tbh{Style.RESET_ALL}")
    print(f"Github: {Fore.BLUE}https://github.com/Abss0x7tbh/bass")
    print(f"{Style.RESET_ALL}------------------------------------------")


# get providers involved, create a list of files to join
def get_providers(domain):
    # list of filtered public resolvers is a provider by default
    providers = {'public'}
    try:
        answers = dns.resolver.query(domain, 'NS')
    except dns.exception.DNSException:
        print(f"Domain {domain} failed to resolve", file=stderr)
        return {}

    for server in answers:
        # resolver here outputs with the . at the end, so need to rstrip
        nsdomain = str(server.target)
        ext = tldextract.extract(nsdomain.rstrip('.'))

        # deal with awsdns
        if "awsdns" in nsdomain:
            awsdns_answers = dns.resolver.query(nsdomain, 'A')
            awsdns_ip = awsdns_answers[0].address
            with open(output_filename, "a+") as outfile:
                outfile.write(awsdns_ip + "\n")
        else:        
            # extensions matter on Win
            providers.add(ext.domain)
    return providers


def get_nameservers(provider_name):
    nameservers = set()
    script_dir = os.path.dirname(__file__)
    if script_dir == '':
        script_dir = '.'
    try:
        with open(f"{script_dir}/resolvers/{provider_name}.txt") as infile:
            for line in infile:
                nameservers.add(line.rstrip())
    except IOError:
        print(f"Provider {Fore.RED}resolvers/{provider_name}.txt {Fore.GREEN}not available. Add an issue with the name of the provider so that we can look into it", file=stderr)
    return nameservers


# puts the resolvers from the provider txts into the output file and returns the number of them
def output_nameservers_to_file(providers):
    nameservers = set()
    for dns_provider in providers:
        nameservers = nameservers|get_nameservers(dns_provider)
    with open(output_filename, "a+") as outfile:
        for nameserver in nameservers:
            outfile.write(f"{nameserver}\n")
    return len(nameservers)


if __name__ == "__main__":
    banner()
    # Input Management
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-d", "--domain", required=True,
        help="target domain"
    )
    ap.add_argument(
        "-o", "--output", required=True,
        help="output file of your final resolver list"
    )
    args = vars(ap.parse_args())

    domain_arg = args["domain"]
    output_arg = args["output"]
    output_filename = output_arg
    providers = get_providers(domain_arg)
    print(f"{Fore.GREEN}DNS Providers : {Fore.RED}{str(providers)}{Fore.GREEN}")
    num_of_resolvers = output_nameservers_to_file(providers)
    print(f"{Fore.GREEN}Final List of Resolver located at {Fore.RED}{output_arg}")
    print(f"{Fore.GREEN}Total usable resolvers : {Fore.RED}{str(num_of_resolvers)}{Style.RESET_ALL}")
