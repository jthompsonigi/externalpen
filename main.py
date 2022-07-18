# IGI Cybersecurity external pen test automation tool
# Author: John Lyons (jlyons@igius.com)

# todo: impliment jok3r tool
# todo: better parsing of results from nmapautomator
# todo: determine domains for associated ips
# todo: package results into file (csv with nessus format for input into plextrac?)


# imports
import argparse
import yaml
import os

# Main function used to call child functions specific to external pen test tools and provide updates to the user on the scripts progress
def main():
    parser = argparse.ArgumentParser(description='External Pen Testing Automation tool made by IGI Cybersecurity')

    parser.add_argument('-o', '--output', required=True, help='folder for script outputs')
    parser.add_argument('-v', '--verbose', action='store_true', help='push cli outputs for individual tools to the cli')
    parser.add_argument('-d', '--domains', required=False, help='optional list of domains to test')
    parser.add_argument('-l', '--lightscan', action='store_true', help='run less time consuming version of tools when possible, this option may reduce how many results are found')
    parser.add_argument('ips')
    args = parser.parse_args()

    verbose = False
    light = False
    output = ""
    domains = []
    ips = []

    if args.verbose:
        verbose = True
    if args.lightscan:
        light = True
    if args.output:
        output = args.output
    if args.domains:
        domainfile = open(args.domain,"r")
        for line in domainfile:
            stripped_line = line.strip()
            domains.append(stripped_line)
        domainfile.close()
    ipfile = open(args.ips,"r")
    for line in ipfile:
        stripped_line = line.strip()
        ips.append(stripped_line)
    ipfile.close()

    with open(r'config.yaml') as file:
        configs = yaml.full_load(file)

    os.system('mkdir ' + output)

    nmapauto(ips,verbose,output,domains,light,configs)

#function that runs nmapAutomator tool, outputs saved in output directory + /nmapAutomator/
def nmapauto(ips,verbose,output,domains,light,configs):
    print("Starting nmap automator tool.")
    if light == True:
        print("running tool in light scan mode, conducting less intensive scan in favor of shorter time spent")
    else:
        print("running tool in full scan mode, this might take a while.")
    os.system('mkdir ' + output + '/nmapAutomator')
    for ip in ips:
        if light == True:
            command = configs["nmapauto_light"]
        else:
            command = configs["nmapauto_full"]
        command = command + ' -o ' + output + '/nmapAutomator/' + ip + ' -H ' + ip
        os.system(command)
    print("nmap automator tool done!")

#function that runs magicRecon tool, outputs saved in output directory + /magicrecon/
#NOTE: currently only pulls from domains list
def magicrecon(ips,verbose,output,domains,light,configs):
    print("Starting Magic Recon tool.")
    if light == True:
        print('running tool in light scan mode, conducting less intensive scan in favor of shorter time spent')
    else:
        print('running tool in full scan mode, this might take a while.')
    os.system('mkdir ' + output + '/magicrecon')
    for domain in domains:
        output = '> ' + output + '/magicrecon/' + domain + '.txt'
        if light == True:
            command = configs['magicrecon_light']
        else:
            command = configs['magicrecon_light']
        command = command + domain + " > " + output
        os.system(command)
    print('Magic Recon tool done!')

def jok3r(ips,verbose,output,domains,light,configs):
    pass

main()