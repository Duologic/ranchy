import os
import re
import requests
import json
from subprocess import Popen, PIPE
from datetime import datetime

api_url = "http://localhost:8080/farm/api/"
api_headers = {'content-type': 'application/json'}
nodename = "ranchy"


def reverse_sub(regex, string):
    ret = ""
    for letter in string:
        if re.match(regex, letter):
            ret += letter
        else:
            ret += "_"
    return ret


def collect_data():

    with open(os.devnull, 'w') as dnull:
        rawoutput = Popen(['apt-dater-host', 'status'],
                          stdout=PIPE,
                          stderr=dnull).communicate()

    rawoutput_lines = rawoutput[0].split("\n")
    packagelist = {}

    for line in rawoutput_lines:
        if re.match('^STATUS:', line):
            localpackage = line[8:len(line)].split('|')

            temp = {}
            temp['current'] = localpackage[1].strip()
            temp['latest'] = localpackage[1].strip()
            temp['hasupdate'] = False

            if re.match('^u=', localpackage[2].strip()):
                temp['latest'] = localpackage[2].split("=")[1].strip()
                temp['hasupdate'] = True

            packagelist[localpackage[0].strip()] = temp
    return packagelist


def find_node(name):
    slug = reverse_sub("([a-z0-9-_]+)", name)
    url = api_url + "node/" + slug
    response = requests.get(url, headers=api_headers)
    if response.status_code == 200:
        queryset = json.loads(response.text)
        return queryset
    else:
        return False


def find_create_package(name, packagetype_id):
    url = api_url + "package/"
    slug = reverse_sub("([a-z0-9-_]+)", name)
    check_url = url + slug
    response = requests.get(check_url, headers=api_headers)
    if response.status_code == 200:
        queryset = json.loads(response.text)
        return queryset['id']
    elif response.status_code == 404:
        data = json.dumps({'name': name,
                           'slug': slug,
                           'packagetype': packagetype_id})
        response = requests.post(url, data, headers=api_headers)
        if response.status_code == 201:
            queryset = json.loads(response.text)
            return queryset['id']
        else:
            raise Exception
            return False
    else:
        return False


def find_create_update_packagecheck(packageid, node, packagecheckinfo):
    id = None
    url = api_url + "packagecheck/"
    find_url = '%s%s/%d' % (url, node['slug'], packageid)
    response = requests.get(find_url)
    if response.status_code == 200:
        queryset = json.loads(response.text)
        if len(queryset) == 1:
            id = queryset[0]['id']
            packagecheckinfo['id'] = id
            packagecheckinfo['node'] = node['id']
            url = "%s%s" % (url, id)
            data = json.dumps(packagecheckinfo)
            response = requests.put(url, data, headers=api_headers)
        else:
            data = json.dumps(packagecheckinfo)
            response = requests.post(url, data, headers=api_headers)
        if response.status_code == 201 or response.status_code == 200:
            queryset = json.loads(response.text)
            return queryset['id']
        else:
            return False

    else:
        return "end"


def main():
    localpackages = collect_data()
    node = find_node(nodename)
    currentdatetime = datetime.now().replace(microsecond=0).isoformat()
    for localpackage in localpackages:
        packageid = find_create_package(localpackage, "1")
        localpackages[localpackage]['node'] = node['id']
        localpackages[localpackage]['package'] = packageid
        localpackages[localpackage]['lastcheck'] = currentdatetime
        find_create_update_packagecheck(packageid,
                                        node,
                                        localpackages[localpackage])


main()
