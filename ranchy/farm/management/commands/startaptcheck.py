from django.core.management.base import BaseCommand, CommandError
from farm.models import Node, PackageCheck, Package, PackageType
from subprocess import Popen
from lxml import objectify
from datetime import datetime
import logging, subprocess, pytz, os

class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO)
        logging.info("apt-dater is refreshing, please standby...")

        with open(os.devnull, 'w') as dnull:
            rawreport = Popen(['apt-dater','-r'], stdout=subprocess.PIPE, stderr=dnull).communicate()

        report = objectify.fromstring(rawreport[0])
        checkdate = datetime.fromtimestamp(report.timestamp,pytz.timezone("Europe/Brussels"))
        logging.info("last check: %s" % checkdate)
        okhosts = self.checkhosts(report)

        for host in okhosts:
            logging.info("checking packages of %s" % host[0].identifier)

            for pkg in host[1].packages.iterchildren(tag='pkg'):
                pt = PackageType.objects.get(name='Aptitude')
                find_pkg = self.findpkg(pkg.get('name'),pt)
                pkgcheck = PackageCheck.objects.filter(package=find_pkg,node=host[0])

                if(pkgcheck.count()>=1):
                    find_pkgcheck = pkgcheck[0]
                else:
                    find_pkgcheck = PackageCheck()
                    find_pkgcheck.node = host[0]
                    find_pkgcheck.package = find_pkg
                    
                find_pkgcheck.lastcheck = checkdate
                find_pkgcheck.current = pkg.get('version')

                if(pkg.get('hasupdate')): 
                    find_pkgcheck.hasupdate = True
                else:
                    find_pkgcheck.hasupdate = False

                if(find_pkgcheck.hasupdate):
                    find_pkgcheck.latest = pkg.get('data')
                else:
                    find_pkgcheck.latest = pkg.get('version')

                find_pkgcheck.save()

    def checkhosts(self, report):
        logging.info("checking hosts...")
        okhosts = [];
        for group in report.iterchildren(tag='group'):
            domain = group.get('name')
            for host in group.iterchildren(tag='host'):
                ident = "%s.%s" % (host.get('hostname'), domain)
                try:
                    node = Node.objects.get(identifier=ident)
                    okhosts.append([node,host])
                except Node.DoesNotExist:
                    logging.warning('Node "%s" does not exist' % ident)
                    pass
        return okhosts

    def findpkg(self, pkgname, pkgtype):
        find_pkg = Package.objects.filter(name=pkgname)
        if(find_pkg.count()==1):
            db_pkg = find_pkg[0]
        else:
            db_pkg = Package()
            db_pkg.slug = pkgname 
            db_pkg.name = pkgname
            db_pkg.packagetype = pkgtype
            db_pkg.save()
        return db_pkg
