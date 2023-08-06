'''
AWS connection handlers
'''
import boto3.ec2
from configAWSEnv.prints import print_and_exit

def connect_to_ec2():
    try:
        ec2client = boto3.client('ec2')
    except Exception as e:
        print_and_exit("failed to connect to ec2, check your boto configuration\nException: {}".format(e), 2)
    return ec2client


def connect_to_ec2_resources():
    try:
        ec2resourcers = boto3.resource('ec2')
    except Exception as e:
        print_and_exit("failed to connect to ec2, check your boto configuration\nException: {}".format(e), 2)
    return ec2resourcers