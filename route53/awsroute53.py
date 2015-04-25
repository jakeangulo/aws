#!/bin/env python

from ConfigParser import ConfigParser
import route53
import argparse
import socket
import time
import sys

# parse configs
config = ConfigParser()
config.read("route53.conf")
aws_access_key_id = config.get("credentials", "aws_access_key_id")
aws_secret_access_key = config.get("credentials", "aws_secret_access_key")
default_zone = config.get("default", "zone_id")
default_hostname = config.get("default", "hostname")

# detect system eth0 private ip, and set as default
# override this with "-i" argument to specify the public ip
default_ip = socket.gethostbyname(socket.gethostname())

# parse command-line arguments
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
parser.add_argument("-n", type=str, help="fqdn, eg: host.domain.com.", default=default_hostname)
parser.add_argument("-i", type=str, help="ip address", default=default_ip)
parser.add_argument("-t", type=int, help="ttl value", default=300)
parser.add_argument("-z", type=str, help="zone id", default=default_zone)
group.add_argument("-l", "--list", action="store_true", help="list current records")
group.add_argument("-c", "--create", action="store_true", help="create new record")
group.add_argument("-g", "--change", action="store_true", help="change record ip")
group.add_argument("-d", "--delete", action="store_true", help="CAUTION: delete record; specify '-n fqdn' to delete")
args = parser.parse_args()

# initialize connection to aws
conn = route53.connect(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

def list_records():
    # list hosted zones & record sets
    print("listing current records")
    for zone in conn.list_hosted_zones():
        print(zone.name)
        for record_set in zone.record_sets:
            print(record_set)

def create_record(zone_id, name, ip, ttl):
    # create new record set
    zone = conn.get_hosted_zone_by_id(zone_id)
    print("creating new record in zone: ", zone.name, name)
    try:
        new_record, change_info = zone.create_a_record(name=name,values=[ip],ttl=ttl)
        print("new record: %s \nchange info: %s" %(new_record, change_info))
    except:
        print("Check if duplicate record exists, or if ip is valid!")
        #print("Unexpected error:", sys.exc_info())

def get_record_set(zone_id, name):
    # Note that nameshould be a fully-qualified domain name, like: 'host.domain.com.'
    zone = conn.get_hosted_zone_by_id(zone_id)
    for record_set in zone.record_sets:
        if record_set.name == name:
            return record_set # Return / exit once record is found

def change_record_ip(record_set, ip):
    # change the ip address of a record
    print("changing record ip: ", record_set.name, ip)
    record_set.values = [ip]
    record_set.save()

def delete_record(record_set):
    # delete a record set
    print("deleting record set: ", record_set.name)
    record_set.delete()

if __name__=="__main__":
    #print(args.n, args.i, args.t, args.z)
    if args.list:
        list_records()
    elif args.create:
        create_record(args.z, args.n, args.i, args.t)
    elif args.change:
        # workaround: the apis 'record_set.values' is not working, 
        # instead, delete & re-create record set
        record_set = get_record_set(args.z, args.n)
        # delete record
        if record_set is not None:
            delete_record(record_set)
        else:
            print("record not found!")
        time.sleep(2) # waiting for aws to delete record
        # then re-create record
        create_record(args.z, args.n, args.i, args.t)
    elif args.delete:
        record_set = get_record_set(args.z, args.n)
        if record_set is not None:
            delete_record(record_set)
        else:
            print("record not found!")
    else:
        print("Invalid argument!")
