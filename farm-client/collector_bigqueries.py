import re
import os
import requests
import json
from subprocess import Popen, PIPE
from datetime import datetime

api_url = "http://localhost:8081/farm/api/"
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
    response = requests.post(url, data, headers=api_headers)
    return handle_response(response)


def create_packagecheck(packagecheck):
    url = api_url + "packagecheck/"
    data = json.dumps(packagecheck)
    response = requests.post(url, data, headers=api_headers)
    return handle_response(response)


def update_packagecheck(packagecheck):
    url = api_url + "packagecheck/%d" % packagecheck['id']
    data = json.dumps(packagecheck)
    response = requests.put(url, data, headers=api_headers)
    return handle_response(response)


def delete_packagecheck(id):
    url = api_url + "packagecheck/%d" % id
    response = requests.delete(url)
    if response.status_code == 204:
        return True
    return False


def handle_response(response):
    if response.status_code >= 200 or response.status_code <= 299:
        return json.loads(response.text)
    return False


def find_key(dictionary, key):
    for keys in dictionary:
        if key in keys:
            return True
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
                slug = reverse_sub("([a-z0-9-_]+)", localpackage)
                newpackage = {'name': localpackage,
                              'slug': slug,
                              'packagetype': '1'}
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
