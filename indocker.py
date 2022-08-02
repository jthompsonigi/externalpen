import os

def main():
    a_file = open('forjok3r.txt','r')
    info = [(line.strip()).split() for line in a_file]
    a_file.close()
    ips_string = info[0]
    ips = ips_string.split()
    domains_string = info[1]
    domains = domains_string.split()
    title = info[2]
    output = info[3]
    conf = info[4]
    for ip in ips:
        os.system(conf + ' ' + ip)
    print("Jok3r is finished running, please enter the following commands to generate an html report:")
    print("python3 jok3r.py db")
    print("report")



#def indocker():
    #print("Starting Jok3r, this may take a while...")
    #os.system("docker start jok3r-container")
    #old_reports = os.system('docker exec jok3r-container ls /root/jok3r/reports/')
    #if old_reports != "" or old_reports != " ":
        #old_reports_list = old_reports.split()
        #for item in old_reports_list:
            #os.system('docker exec jok3r-container rm -r jok3r-container:/root/')
    #os.system('docker exec jok3r-container python3 jok3r.py db')
    #os.system('docker exec jok3r-container mission -a ' + title)
    #for ip in ips:
        #command = configs['jok3r']
        #os.system('docker exec jok3r-container ' + command + ' https://' + ip)
    #print('Jok3r finished for scoped ips')
    #print('Retrieving report from jok3r container')
    #results = os.system('docker exec jok3r-container ls /root/jok3r/reports/')
    #os.system('docker cp jok3r-container:/root/jok3r/reports/' + results + ' .')
    #os.system('docker exec jok3r-container rm -r jok3r-container:/root/jok3r/reports/' + results)
    # list_of_files = glob.glob('/root/jok3r/reports/*')
    # latest_file = max(list_of_files, key=os.path.getctime())
    # os.system('exit')
    # os.system('docker cp jok3r-container:/root/jok3r/reports/'+latest_file + " .")
    # os.system('mv ' + latest_file + " " + output)
    # os.system('firefox &lt;/root/jok3r/reports/')
    # os.system('firefox &lt;/root/jok3r/reports/'+latest_file+'>.html')