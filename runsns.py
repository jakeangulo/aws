#!/usr/local/bin/python

#
# This is an example implementation of the awssns.Sns class
# You can reuse awssns.Sns from anywhere if you import it
#
# This is also a working command-line executable if you chose to run 
# Sns operations via shell
#

import csv
import pprint
import argparse
from awssns import Sns

# parse command-line arguments
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-C", "--create_endpoint", action="store_true", 
    help="Create new platform endpoint [requires: application name, token, user data]")
group.add_argument("-P", "--publish", action="store_true", 
    help="Publish a message to a topic [requires: topic, subject, message]")
group.add_argument("-E", "--send_sns_msg", action="store_true", 
    help="Send a message to a single endpoint [requires: endpoint_arn, message]")
group.add_argument("-M", "--send_sns_msg_multi", action="store_true", 
    help="Send a message to multiple endpoints [requires: txt file, message]")
group.add_argument("-S", "--subscribe", action="store_true", 
    help="Subscribe to a topic [requires: topic, protocol, endpoint]")
group.add_argument("-U", "--unsubscribe", action="store_true", 
    help="Unsubscribe from a topic [requires: subscription_arn]")
group.add_argument("-V", "--create_endpoint_csv", action="store_true", 
    help="Create new platform endpoints from Csv file [requires: application name, csv file]")
parser.add_argument("-a", type=str, help="SubscriptionArn")
parser.add_argument("-e", type=str, help="Endpoint or Application EndpointArn")
parser.add_argument("-f", type=str, help="CSV File (tokens and user data) or TXT file (endpoint arns)")
parser.add_argument("-k", type=str, help="Token")
parser.add_argument("-l", type=str, help="Application Name")
parser.add_argument("-m", type=str, help="Message body")
parser.add_argument("-o", type=str, help="Output TXT file for endpoint arns")
parser.add_argument("-p", type=str, help="Protocol, any of: \
    email | email-json | http | https | sqs | sms | application")
parser.add_argument("-s", type=str, help="Subject, max 100 characters")
parser.add_argument("-t", type=str, help="Name of the topic")
parser.add_argument("-u", type=str, help="User data")
args = parser.parse_args()
pp = pprint.PrettyPrinter(indent=4)

# initialize awssns.Sns
sns = Sns()

# How to publish a message to all topic subscribers (group)
def publish():
    topic = args.t
    subject = args.s
    message = args.m
    published, response = sns.publish(topic, subject, message)
    if published:
        print("\nSuccessfully sent notification! \nAWS response:")
    else:
        print("Push notification failed!")
    pp.pprint(response)

# How to send message directly to endpoint
def send_sns_msg():
    endpoint_arn = args.e
    message = args.m
    sent_msg, response = sns.send_sns_msg(endpoint_arn, message)
    if sent_msg:
        print("\nSuccessfully sent notification! \nAWS response:")
    else:
        print("Push notification failed!")
    pp.pprint(response)

def send_sns_msg_multi():
    message = args.m
    txtfile = args.f
    with open(txtfile, 'r') as f:
        for line in f:
            endpoint_arn = line.rstrip()
            sent_msg, response = sns.send_sns_msg(endpoint_arn, message)
            if sent_msg:
                print("\nSuccessfully sent notification! \nAWS response:")
            else:
                print("Push notification failed!")
            pp.pprint(response)

# How to subscribe to a topic
# valid protocols are: email|email-json|http|https|sqs|sms|application
def subscribe():
    topic = args.t
    protocol = args.p
    endpoint = args.e
    subscribed, response = sns.subscribe(topic, protocol, endpoint)
    if subscribed:
        print("\nSuccessfully subscribed! \nAWS response:")
    else:
        print("Subscribe failed!")
    pp.pprint(response)

# How to unsubscribe from a topic
def unsubscribe():
    subscription_arn = args.a
    unsubscribed, response = sns.unsubscribe(subscription_arn)
    if unsubscribed:
        print("\nSuccessfully unsubscribed! \nAWS response:")
    else:
        print("Unsubscribe failed!")
    pp.pprint(response)

def create_platform_endpoint():
    application_name = args.l
    token = args.k
    user_data = args.u
    created_endpoint, response = sns.create_platform_endpoint(application_name, token, user_data)
    if created_endpoint:
        print("\nSuccessfully created endpoint! \nAWS response:")
    else:
        print("Create endpoint failed!")
    pp.pprint(response)

def create_platform_endpoint_csv():
    csvfile = args.f
    ep_arn_file = args.o
    application_name = args.l
    with open(csvfile, 'rb') as f:
        csvreader = csv.reader(f)
        with open(ep_arn_file, 'a') as o:
            for row in csvreader:
                user_data = row[0]
                token = row[1]
                created_endpoint, response = sns.create_platform_endpoint(application_name, token, user_data)
                if created_endpoint:
                    print("\nSuccessfully created endpoint! \nAWS response:")
                    o.write(response['CreatePlatformEndpointResponse']['CreatePlatformEndpointResult']['EndpointArn'] + "\n")
                else:
                    print("Create endpoint failed!")
                pp.pprint(response)

if __name__ == '__main__':
    if args.publish:
        publish()
    elif args.send_sns_msg:
        send_sns_msg()
    elif args.send_sns_msg_multi:
        send_sns_msg_multi()
    elif args.subscribe:
        subscribe()
    elif args.unsubscribe:
        unsubscribe()
    elif args.create_endpoint:
        create_platform_endpoint()
    elif args.create_endpoint_csv:
        create_platform_endpoint_csv()
    else:
        print("To display help: ./runsns.py -h")
