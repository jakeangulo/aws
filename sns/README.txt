AWS SNS API Scripts Document

awssns.py - This is the script that contains the re-usable Class: Sns
        Sns contains functions that can send sns messages to a single endpoint 
        or to a group of endpoints subscribed to a Topic

runsns.py - This script is provided as an example on how to call functions from the Sns 
        class.  It is also a convenience tool to publish messages on the command-line.
        
Examples:

1) How to send a message to a single endpoint

a) by implementing Sns class, send_sns_msg function:

from awssns import Sns
sns = Sns()
sns.send_sns_msg(endpoint_arn, message)

b) using the command line:

./runsns.py --send_sns_msg -e "arn:aws:sns:us-east-1:XXXXXXXXXXXX:endpoint/APNS/MyApplicationName/563ff065-4564-3bf9-a4c1-d99b27196cc9" -m "Test message to single endpoint"

NOTE: You can command: "./runsns.py -h" to invoke the help menu!

If successful, the following response is sent by AWS:

{   u'PublishResponse': {   u'PublishResult': {   u'MessageId': u'ba64a864-d569-5b7a-b9a1-e5f5e2ca4f96'},
                            u'ResponseMetadata': {   u'RequestId': u'72aa5eb2-7c2e-521a-a950-13234b8de6f6'}}}
     


2) How to send a message to a multiple endpoints (Group)

a.1) Subscribe the endpoint to a Topic / Group (Sns subscribe function):

sns.subscribe(topic, protocol, endpoint)

Where valid protocols are: email|email-json|http|https|sqs|sms|application

a.2) Subscribe the endpoint to a Topic / Group (command line):

./runsns.py --subscribe -t TestTopic1 -e "arn:aws:sns:us-east-1:XXXXXXXXXXXX:endpoint/APNS/MyApplicationName/07c7a1dc-0434-383b-b57e-8db0faa504df" -p application

If successful, the following response is sent by AWS:

{   u'SubscribeResponse': {   u'ResponseMetadata': {   u'RequestId': u'42979ec6-0594-5115-b61b-d3573163d318'},
                              u'SubscribeResult': {   u'SubscriptionArn': u'arn:aws:sns:us-east-1:XXXXXXXXXXXX:TestTopic1:571c7779-23f5-439a-a16f-93c66c3b33eb'}}}

b.1) Then do a publish call to send to the Grop / Topic

sns.publish(topic, subject, message)

b.2) This is the equivalent to run publish on command-line:

./runsns.py --publish -t TestTopic1 -m "This is a message to a group"

If successful, the following response is sent by AWS:

{   u'PublishResponse': {   u'PublishResult': {   u'MessageId': u'f7ce8061-f9b1-560d-89e7-cdf0cf362093'},
                            u'ResponseMetadata': {   u'RequestId': u'75f90a3b-cdf6-5b9f-849a-47aafb713d01'}}}

c) This is a wrapper script to send to multiple endpoint arns in a text file

./runsns.py --send_sns_msg_multi -f endpoint-arns.txt -m "This is the message string"



3) How to create a new platform endpoint

a) Use the function create_platform_endpoint

sns.create_platform_endpoint(application_name, token, user_data)

b) Or using the command line:

./runsns.py --create_endpoint -l MyApplicationName -k a2388e710d7c83a636c4fd4b8c58e04e31950efd9fe811c3bd61ba0c6889bcd6 -u "Juan iPad Monkey Prod"

NOTE: You need to store the EndpointArn - this is needed to send sns message



4) How to create multiple platform endpoints from csv file 
Note: this is just a wrapper script that loops the create_platform_endpoint function

Using the command-line:

./runsns.py --create_endpoint_csv -f sns-clients.csv -l MyApplicationName
-o ep-arns-output.txt

If successful, the following response is sent by AWS:
{   u'CreatePlatformEndpointResponse': {   u'CreatePlatformEndpointResult': {
  u'EndpointArn':
  u'arn:aws:sns:us-east-1:XXXXXXXXXXXX:endpoint/APNS/MyApplicationName/10c9a7e3-e8c1-361f-b503-79faa5287f6d'},
                                             u'ResponseMetadata': {
                                               u'RequestId':
                                               u'c71d209c-4273-5825-af1f-6d3200e6bbff'}}}

And all Endpoint ARNs will be written to output file:
cat ep-arns-output.txt
arn:aws:sns:us-east-1:XXXXXXXXXXXX:endpoint/APNS/MyApplicationName/10c9a7e3-e8c1-361f-b503-79faa5287f6d
arn:aws:sns:us-east-1:XXXXXXXXXXXX:endpoint/APNS/MyApplicationName/563ff065-4564-3bf9-a4c1-d99b27196cc9

.
