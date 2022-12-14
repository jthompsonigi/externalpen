# IGI Cybersecurity external pen test automation tool
# Author: John Lyons (jlyons@igius.com)

# todo: finish implimenting jok3r tool
# todo: package results into file (csv with nessus format for input into plextrac?)
# todo: check if jok3r container is installed


# imports
import argparse
import yaml
import os
import pandas
import glob

# Main function used to call child functions specific to external pen test tools and provide updates to the user on the scripts progress
def main():
    parser = argparse.ArgumentParser(description='External Pen Testing Automation tool made by IGI Cybersecurity. \n NOTE: This script must currently be run in su mode, as some tools require root access. \n NOTE 2: currently any domains intended to be scanned by magicRecon must be input manualy')

    parser.add_argument('-o', '--output', required=True, help='Folder for script outputs')
    parser.add_argument('-v', '--verbose', action='store_true', help='Push cli outputs for individual tools to the cli')
    parser.add_argument('-d', '--domains', required=False, help='H3 hosts file that contains discovered domains for all ips')
    parser.add_argument('-l', '--lightscan', action='store_true', help='Run less time consuming version of tools when possible, this option may reduce how many results are found')
    parser.add_argument('-t', '--title', required=True, help='Title for jok3r mission (recommended to just use client name)')
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
        ipdomainlist, domains = obtainDomains(args.domains)
    ipfile = open(args.ips,"r")
    for line in ipfile:
        stripped_line = line.strip()
        ips.append(stripped_line)
    ipfile.close()

    with open(r'config.yaml') as file:
        configs = yaml.full_load(file)

    os.system('mkdir ' + output)

    nmapauto(ips,verbose,output,domains,light,configs)
    magicrecon(ips,verbose,output,domains,light,configs)
    jok3r(ips, domains, args.title, output, configs)

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


#todo testing on jok3r, stability?
#function that runs jok3r tool, outputs saved at current file location
def jok3r(ips,domains,title,output,configs):
    file_output = []
    ips_string = ""
    for ip in ips:
        ips_string = ips_string + ip + " "
    file_output.append(ips_string)
    domains_string = ""
    for domain in domains:
        domains_string = domains_string + domain + " "
    file_output.append(domains_string)
    file_output.append(title)
    file_output.append(output)
    file_output.append(configs['jok3r'])
    with open(r'forjok3r.txt', 'w') as fp:
        for item in file_output:
            fp.write("%s\n" % item)
    os.system('docker start')
    os.system('docker cp indocker.py jok3r-container:indocker.py')
    os.system('docker cp forjok3r.txt jok3r-container:forjok3r.txt')
    print('script finished ')

#Function that intakes H3 csv file of hosts and associates each ip with coresponding hosts.
def obtainDomains(domains):
    colnames = ['FirstSeen','Subnet','SubnetSource','IP','Hostname','DNSHostname','LDAPHostname','InScope','OS','Hardware','Device','NumWeaknesses','NumConfirmedWeaknesses','NumDataResources','NumCredentials','NumConfirmedCredentials','NumServices','NumWebShares','RiskScore','RiskScoreDescription','OpID']
    data = pandas.read_csv(domains,names=colnames)
    ips = data.IP.tolist()
    hosts = data.Hostname.tolist()
    ips = ips[1:]
    hosts = hosts[1:]

    ipwithhost = {}
    for i in range(len(ips)):
        ipwithhost[ips[i]] = hosts[i]

    return ipwithhost, hosts

main()
