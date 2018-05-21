#!/usr/bin/python
import os
import sys
import shutil
import boto3
import datetime

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class Keys(object):
    def __init__(self, Access, Secret, Token):
        self.Access = Access
        self.Secret = Secret
        self.Token = Token

Options = {}
Options['MainProfile'] = os.environ.get('AWS_MAIN_PROFILE')
Options['MainUser'] = os.getenv('AWS_MAIN_USER_ARN')
Options['MfaToken'] = os.getenv('AWS_MAIN_MFA_TOKEN')
Options['StsProfile'] = os.getenv('AWS_STS_PROFILE')
Options['StsRoleArn'] = os.getenv('AWS_STS_ROLE_ARN')

def validate_options(Options):
    if not Options['MainProfile']:
        print("""-- No AWS profile provide. 
            "default" profile will be used.""")
        Options['MainProfile'] = "default"

    if not Options['MainUser']:
        print("""-- No MFA user found for custom authentication.
            Role based authentication will be used by default""")

    try:
        Session = boto3.Session(profile_name=Options['StsProfile'])
        print('-- Profile "%s" already exists in your AWS credential file.\n-- Please, remove it if you need to update credentials.' % Options['StsProfile'])
        sys.exit(1)
    except Exception:
        pass

    return Options

def aws_connect(Options):
    try:
        Options = validate_options(Options)
        Session = boto3.Session(profile_name=Options['MainProfile'])
        StsClient = Session.client('sts')
        Role = None
        if not Options['MainUser']:
            Role = StsClient.assume_role(RoleArn=Options['StsRoleArn'],
                                    RoleSessionName='TempSession')
        else:
            Role = StsClient.assume_role(RoleArn=Options['StsRoleArn'],
                                    RoleSessionName='TempSession',
                                    SerialNumber=Options['MainUser'],
                                    TokenCode=Options['MfaToken'])
        AccessKey = Role['Credentials']['AccessKeyId']
        SecretKey = Role['Credentials']['SecretAccessKey']
        SessionToken = Role['Credentials']['SessionToken']

        return(Keys(AccessKey, SecretKey, SessionToken))
    except Exception as e:
        print('-- Problem found during AWS session token generation: "%s"' % e)
        sys.exit(1)

print(__file__)
Credentials = aws_connect(Options)
AwsConfigFile = os.getenv('HOME') + '/.aws/credentials'
AwsBackupConfigFile = AwsConfigFile + ".backup-" + str(datetime.datetime.now())

shutil.copyfile(AwsConfigFile, AwsBackupConfigFile)
print('-- Copied "%s" to "%s"' % (AwsConfigFile, AwsBackupConfigFile))

with open(AwsConfigFile, 'a') as f:
    f.write("\n[" + Options['StsProfile'] + "]\n")
    f.write("aws_access_key_id = " + Credentials.Access + "\n")
    f.write("aws_secret_access_key = " + Credentials.Secret + "\n")
    f.write("aws_security_token = " + Credentials.Token + "\n")
print('-- Added profile "%s" to AWS credential file' % (Options['StsProfile']))
sys.exit(0)