#!/usr/bin/python

#
# This script sends push notification messages to various subscribed endpoints 
# such as: Mobile device Apps, Email, etc.
#

import sys
import boto.sns
import logging

from ConfigParser import ConfigParser

class Sns():
    """Implements AWS boto.sns"""
    
    def __init__(self):
        # parse configs
        self.config = ConfigParser()
        # place below config file on the same folder as this script
        self.config.read("sns.conf")
        self.account = self.config.get("default", "account")
        self.region = self.config.get("default", "region")
        self.log_level = self.config.getint("default", "log_level")
        self.log_file = self.config.get("default", "log_file")
        self.aws_access_key_id = self.config.get("credentials", "aws_access_key_id")
        self.aws_secret_access_key = self.config.get("credentials", "aws_secret_access_key")

        # set log level
        logging.basicConfig(filename=self.log_file, level=self.log_level)

        # initialize connection to Aws Sns
        try:
            self.sns_connection = boto.sns.connect_to_region(self.region, 
                                aws_access_key_id=self.aws_access_key_id, 
                                aws_secret_access_key=self.aws_secret_access_key)
        except:
            print("Connection error: %s" % str(sys.exc_info()))
            raise

    def publish(self, topic, subject, message):
        """Publish a message to all topic subscribers"""
        
        topic_arn = "arn:aws:sns:%s:%s:%s" % (self.region, self.account, topic)
        
        try:
            publishing = self.sns_connection.publish(topic_arn, message, subject=subject)
        except:
            print("Error: %s" % sys.exc_info()[1])
            return False, sys.exc_info()[1]
            
        return True, publishing

    def send_sns_msg(self, endpoint_arn, message):
        """Send a message to single endpoint"""
        
        try:
            sending = self.sns_connection.publish(target_arn=endpoint_arn, message=message)
        except:
            print("Error: %s" % sys.exc_info()[1])
            return False, sys.exc_info()[1]
            
        return True, sending

    def subscribe(self, topic, protocol, endpoint):
        """Subscribe to a topic"""
        
        topic_arn = "arn:aws:sns:%s:%s:%s" % (self.region, self.account, topic)
        
        try:
            subscribing = self.sns_connection.subscribe(topic_arn, protocol, endpoint)
        except:
            print("Error: %s" % str(sys.exc_info()))
            return False, sys.exc_info()[1]
            
        return True, subscribing

    def unsubscribe(self, subscription_arn):
        """Un-subscribe from a topic"""
        
        try:
            un_subscribing = self.sns_connection.unsubscribe(subscription_arn)
        except:
            print("Error: %s" % str(sys.exc_info()))
            return False, sys.exc_info()[1]
            
        return True, un_subscribing

    def create_platform_endpoint(self, application_name, token, user_data):
        """Delete an endpoint"""
        
        application_arn = "arn:aws:sns:%s:%s:app/APNS/%s" % (self.region, self.account, application_name)
        
        try:
            creating_endpoint = self.sns_connection.create_platform_endpoint(platform_application_arn=application_arn, token=token, custom_user_data=user_data)
        except:
            print("Error: %s" % str(sys.exc_info()))
            return False, sys.exc_info()[1]
            
        return True, creating_endpoint

    def delete_endpoint(self, endpoint_arn):
        """Delete an endpoint"""
        
        try:
            deleting_endpoint = self.sns_connection.delete_endpoint(endpoint_arn)
        except:
            print("Error: %s" % sys.exc_info()[1])
            return False, sys.exc_info()[1]
            
        return True, deleting_endpoint

if __name__ == '__main__':
    print("To use this class, do: from awssns import Sns \
    \nPlease refer to runsns.py as an example.")
