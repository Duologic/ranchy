import re, os, subprocess, requests, json
from datetime import datetime

api_url = "http://localhost:8080/farm/api/"
api_headers = {'content-type': 'application/json'}
nodename = "ranchy"

def reverse_sub(regex,string):
    ret = ""
    for letter in string:
        if re.match(regex,letter):
            ret += letter
        else:
            ret += "_"
    return ret

def collect_data():

    with open(os.devnull, 'w') as dnull:
        rawoutput = subprocess.Popen(['apt-dater-host','status'], stdout=subprocess.PIPE, stderr=dnull).communicate()

    rawoutput_lines = rawoutput[0].split("\n")
    packagelist = {}

    for line in rawoutput_lines:
        if re.match('^STATUS:', line):
            localpackage = line[8:len(line)].split('|')

            packagelist[localpackage[0].strip()] = {}
            packagelist[localpackage[0].strip()]['current'] = localpackage[1].strip()
            packagelist[localpackage[0].strip()]['latest'] = localpackage[1].strip()
            packagelist[localpackage[0].strip()]['hasupdate'] = False

            if re.match('^u=', localpackage[2].strip()):
                packagelist[localpackage[0].strip()]['latest'] = localpackage[2].split("=")[1].strip()
                packagelist[localpackage[0].strip()]['hasupdate'] = True
    return packagelist

def find_node(name):
    slug = reverse_sub("([a-z0-9-_]+)",name)
    url = api_url + "node/" + slug
    response = requests.get(url, headers=api_headers)
    if response.status_code == 200: # OK
        queryset = json.loads(response.text)
        return queryset 
    else:
        return False

def find_create_package(name, packagetype_id):
    id = None
    url = api_url + "package/"
    slug = reverse_sub("([a-z0-9-_]+)",name)
    check_url = url + slug 
    response = requests.get(check_url, headers=api_headers)
    if response.status_code == 200: # OK
        queryset = json.loads(response.text)
        return queryset['id']
    elif response.status_code == 404: # Not Found
        data = json.dumps({'name':name, 'slug': slug, 'packagetype':packagetype_id})
        response = requests.post(url, data, headers=api_headers)
        if response.status_code == 201: # Created
            queryset = json.loads(response.text)
            return queryset['id']
        else:
            raise Exception
            return False # not Created
    else:
        return False # uh oh, no 200 or 404, shit is broken now

def find_create_update_packagecheck(packageid, node, packagecheckinfo):
    id = None
    url = api_url + "packagecheck/"
    find_url = '%s%s/%d' % (url, node['slug'], packageid)
    response = requests.get(find_url)
    if response.status_code == 200: # OK
        queryset = json.loads(response.text)
        respone = None
        if len(queryset) == 1:
            id = queryset[0]['id']
            packagecheckinfo['id']=id
            packagecheckinfo['node']=node['id']
            url = "%s%s" % (url, id)
            data = json.dumps(packagecheckinfo)
            response = requests.put(url,data,headers=api_headers)
        else:
            data = json.dumps(packagecheckinfo)
            response = requests.post(url,data,headers=api_headers)
        if response.status_code == 201 or response.status_code == 200: # Created or updated
            queryset = json.loads(response.text)
            return queryset['id']
        else:
            return False # not Created

    else:
        return "end" 

def main():
    localpackages = collect_data()
    node = find_node(nodename)
    currentdatetime = datetime.now().replace(microsecond=0).isoformat()
    for localpackage in localpackages:
        packageid = find_create_package(localpackage,"1")
        localpackages[localpackage]['node'] = node['id']
        localpackages[localpackage]['package'] = packageid
        localpackages[localpackage]['lastcheck'] = currentdatetime
        find_create_update_packagecheck(packageid,node,localpackages[localpackage])
        

main()
