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

def get_remote_packages():
    url = api_url + "package/"
    response = requests.get(url)
    return handle_response(response)

def get_remote_packagechecks(nodename):
    url = api_url + "packagecheck/" + nodename
    response = requests.get(url)
    return handle_response(response)

def create_package(package):
    url = api_url + "package/"
    data = json.dumps(package)
    response = requests.post(url,data,headers=api_headers)
    return handle_response(response)

def create_packagecheck(packagecheck):
    url = api_url + "packagecheck/"
    data = json.dumps(packagecheck)
    response = requests.post(url,data,headers=api_headers)
    return handle_response(response)

def update_packagecheck(packagecheck):
    url = api_url + "packagecheck/%d" % packagecheck['id']
    data = json.dumps(packagecheck)
    response = requests.put(url,data,headers=api_headers)
    return handle_response(response)

def delete_packagecheck(id):
    url = api_url + "packagecheck/%d" % id
    response = requests.delete(url)
    if response.status_code == 204:
        return True
    return False

def handle_response(response):
    if response.status_code >= 200 or response.status_code <= 299: #OK
        return json.loads(response.text)
    return False

def find_key(dictionary, key):
    for keys in dictionary:
        if key in keys:
            return true
    return False

def bigmain():
    localpackages = collect_data()
    node = find_node(nodename)
    currentdatetime = datetime.now().replace(microsecond=0).isoformat() + "Z"

    if node:
        remotepackages = get_remote_packages()
        remotepackagechecks = get_remote_packagechecks(nodename)

        for localpackage in localpackages:
            found = False
            localpackageinfo = localpackages[localpackage]

            for remotepackage in remotepackages:
                if remotepackage['name'] == localpackage:
                    found = remotepackage
                    break

            if not found:
                newpackage = {'name': localpackage, 'slug': reverse_sub("([a-z0-9-_]+)", localpackage), 'packagetype': '1'}
                found = create_package(newpackage)

            if not found:
                    raise Exception

            localpackageinfo['package'] = found['id']
            localpackageinfo['node'] = node['id']
            localpackageinfo['lastcheck'] = currentdatetime

            updated = False
            for remotepackagecheck in remotepackagechecks:
                if remotepackagecheck['package'] == localpackageinfo['package']:
                    localpackageinfo['id'] = remotepackagecheck['id']
                    updated = update_packagecheck(localpackageinfo)
                    if not updated:
                        raise Exception
                    break

            if not updated:
                created = create_packagecheck(localpackageinfo)

            localpackages[localpackage] = localpackageinfo

            if not updated and not created:
                raise Exception

        for remotepackagecheck in remotepackagechecks:
            installed = False

            for localpackage in localpackages:
                if remotepackagecheck['id'] == localpackages[localpackage]['id']:
                    installed = True
                    break

            if not installed:
                deleted = delete_packagecheck(remotepackagecheck['id'])

                if not deleted:
                    raise Exception

        return True
    else:
        raise Exception

bigmain()
