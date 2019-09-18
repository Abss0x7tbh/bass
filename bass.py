import dns.resolver
import argparse
import tldextract
import sys
from colorama import Fore
import pyfiglet

# banner
ascii_banner = pyfiglet.figlet_format("bass")
print(ascii_banner)

# Author & contributor
print("------------------------------------------")
print("------------------------------------------")
print("Author: "+Fore.BLUE+"@abss_tbh")
print(Fore.WHITE+"------------------------------------------")
print("------------------------------------------")
print("\n\n")

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

# global scope
domain = args["domain"]
output = args["output"]
providers = []


# get providers involved, create a list of files to join
def setProv():

    try:
        answers = dns.resolver.query(domain, 'NS')
    except dns.exception.DNSException:
        print("Domain failed to resolve")
        sys.exit(1)
    print(Fore.GREEN+"DNS Providers :")
    print("-----------------------------")
    for server in answers:

        # resolver here outputs with the . at the end, so need to rstrip
        ext = tldextract.extract(str(server.target).rstrip('.'))
        # extensions matter on Win
        providers.append('./resolvers/'+ext.domain+'.txt')

    # set to remove duplicate
    final_providers = list(set(providers))

    # default list of filtered public resolvers
    final_providers.append('./resolvers/public.txt')

    print(Fore.RED+str(final_providers))
    print(Fore.GREEN+"-----------------------------")
    print("\n")
    return final_providers


# join multiple resolvers from different provider txt files
def createFinal(fp):
    outfile = open(output, "w")
    for fname in fp:
        try:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)
        except IOError:
            print("Provider "+fname+" not available. Add an issue with the\
                 name of the provider so that we can look into it")
    outfile.close()


# display output
def displayList():
    f = open(output, 'r')
    file_contents = f.read()
    print(Fore.GREEN + file_contents)
    f.close()


# number of total resolvers that can be used
def displayStats():
    num_lines = sum(1 for line in open(output))
    return num_lines


def main():

    fp = setProv()
    createFinal(fp)
    print(Fore.GREEN+"Final List of Resolver located at "+output+" :")
    print("-----------------------------")
    displayList()
    print("-----------------------------")
    print("\n")
    print(Fore.RED+"Stats")
    print("-----------------------------")
    num = displayStats()
    print(Fore.GREEN+'Total usable resolvers : '+Fore.RED+str(num))
    print(Fore.RED+"-----------------------------")


if __name__ == "__main__":
    main()
