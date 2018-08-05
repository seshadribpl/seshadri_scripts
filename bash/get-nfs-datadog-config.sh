#!/usr/bin/env bash

set -e
set -u

host=$1

SSH="ssh -o GlobalKnownHostsFile=/dev/null"

derive () {
    configfile=$1
    # python -c "print '.'.join('$host'.split('.ia55.net')[0].split('.')[::-1]) + '-'.join('$configfile'.split('/'))"
    python -c "
}

for configfile in \
        /etc/exports \
        /etc/samba/smb.conf \
        /etc/sysconfig/nfs \
        /var/www/softnas/config/schedules.ini \
        /var/www/softnas/config/snapshots.ini; do
    filename=$(derive $configfile)
    echo "  $configfile > $filename"
    $SSH ec2-user@$host "sudo cat $configfile" > $filename
    if [[ ${filename} =~ snapshots\.ini$ ]]; then
        ./sort-ini ${filename}
    fi
done

if [[ $host == "nfs2a.i.ia55.net" ]]; then
    configfile=/etc/cron.d/arcmaintenance
    $SSH ec2-user@$host "sudo cat $configfile" > etc-cron.d-arcmaintenance
fi
kothand@narada02:~/git/systems/softnas$ ll ~/scripts/python/get-nfs-datadog-files.py 
-rw-rw-r-- 1 kothand kothand 0 Feb 20 17:50 /u/kothand/scripts/python/get-nfs-datadog-files.py
kothand@narada02:~/git/systems/softnas$ rm !$
rm ~/scripts/python/get-nfs-datadog-files.py
