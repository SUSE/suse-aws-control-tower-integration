'''
Create grants to accounts that are part of allowed OUs
'''
from uuid import uuid1
import logging
from os import environ
import sys

import boto3
from botocore.exceptions import ClientError

import cfnresponse

LM = boto3.client("license-manager", region_name='us-east-1')
ORG = boto3.client("organizations")
SSM = boto3.client("ssm")
STS = boto3.client('sts')

LOG = logging.getLogger()
LOG.setLevel(logging.INFO)
HANDLER = logging.StreamHandler(sys.stdout)
HANDLER.setLevel(logging.DEBUG)

LM = boto3.client("license-manager")
ORG = boto3.client("organizations")
SSM = boto3.client("ssm")
STS = boto3.client("sts")

LOGGER = logging.getLogger()


def assume_role(account, role='AWSControlTowerExecution'):
    '''
    Return a session in the target account using Control Tower Role
    '''

    try:
        curr_account = STS.get_caller_identity()['Account']
        if curr_account != account:
            part = STS.get_caller_identity()['Arn'].split(":")[1]

            role_arn = 'arn:' + part + ':iam::' + account + ':role/' + role
            ses_name = str(account + '-' + role)
            response = STS.assume_role(RoleArn=role_arn, RoleSessionName=ses_name)
            sts_session = boto3.Session(
                aws_access_key_id=response['Credentials']['AccessKeyId'],
                aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                aws_session_token=response['Credentials']['SessionToken']
                )
            LOG.info('Assumed session for %s, %s', account, role)
            return sts_session
    except ClientError as exe:
        LOG.error('Unable to assume role')
        raise exe


def get_grants(g_type='distributed', state='ACTIVE',
               product_sku=None, g_principal=None):
    '''
    List all distributed/recieved grants that match the filter
    Recieved grants includes AWS Marketplace Subscriptions.
    Notes: Only one filter value is allowed for state and licesnce_arn
    '''

    result = list()
    m_filter = [{"Name": "GrantStatus", "Values": [state]}]

    if product_sku:
        m_filter.append({"Name": "ProductSKU", "Values": [product_sku]})

    if g_principal:
        m_filter.append({"Name": "GranteePrincipalARN", "Values": [g_principal]})

    try:
        if g_type == 'distributed':
            LOG.info('Distributed licenses with filter: %s', m_filter)
            result = LM.list_distributed_grants(Filters=m_filter)['Grants']
        else:
            LOG.info('Recieved licenses with filter: %s', m_filter)
            result = LM.list_received_grants(Filters=m_filter)['Grants']
    except ClientError as exe:
        LOGGER.error('Unable to list grants: %s', str(exe))

    return result


def delete_grant(account, sku):
    '''
    Delete a grant if a grant exist for the account
    '''

    out = {}

    if grant_exists(account, sku):
        principal = 'arn:aws:iam::' + account + ':root'
        d_grnt = get_grants(g_type='distributed', product_sku=sku, g_principal=principal)
        LOG.info('D_GRNT: %s', d_grnt)
        if len(d_grnt) > 0:
            g_arn = d_grnt[0]['GrantArn']
            ver = d_grnt[0]['Version']
            try:
                out = LM.delete_grant(GrantArn=g_arn, Version=ver)
                LOG.info('GRANT DELETED: %s', out)
            except ClientError as exe:
                LOG.error('%s', str(exe))
        else:
            LOG.info('No Grant Exist to delete for %s', account)
    else:
        LOG.warning('Account: %s, SKU: %s', account, sku)

    return out


def create_grant(account, sku, reg='us-east-1'):
    '''
    Create a grant if grant do not exist already
    '''

    out = {}
    if not grant_exists(account, sku):
        l_arn = get_grants(g_type='recieved', product_sku=sku)[0]['LicenseArn']
        token = str(uuid1())
        grant_name = 'Grant for ' + account
        ops = ['CheckoutLicense', 'CheckInLicense']
        ops += ['ExtendConsumptionLicense', 'ListPurchasedLicenses']
        try:
            out = LM.create_grant(ClientToken=token, GrantName=grant_name, LicenseArn=l_arn,
                                  Principals=['arn:aws:iam::' + account + ':root'],
                                  HomeRegion=reg, AllowedOperations=ops)
            LOG.info('GRANT CREATED:%s', out)
            sts_session = assume_role(account)
            rlm = sts_session.client('license-manager')
            act_out = rlm.create_grant_version(GrantArn=out['GrantArn'],
                                               ClientToken=token,
                                               SourceVersion=out['Version'],
                                               Status='ACTIVE')
            LOG.info('Accepted Grant:%s', act_out)
        except ClientError as exe:
            LOG.error('%s', str(exe))
    else:
        LOG.info('SKIPPING: Grant exist')

    return out


def accounts_in_ou(ou_id):
    '''
    Return list of accounts, and email-Ids
    '''

    result = []
    accounts = []

    try:
        page = ORG.get_paginator('list_accounts_for_parent')
        iterator = page.paginate(ParentId=ou_id)
    except ClientError as exe:
        LOGGER.error('Unable to get Accounts list: %s', str(exe))

    for page in iterator:
        result += page['Accounts']

    for item in result:
        accounts.append(item['Id'])

    return accounts


def grant_exists(account, sku):
    '''
    Return True if grant exist for an account
    '''

    info = get_grants(product_sku=sku)
    result = []
    for item in info:
        result.append(item['GranteePrincipalArn'].split(':')[4])

    return bool(account in result)


def process_lifecycle_event(event, account_list, sku):
    '''
    Process a lifecycle event
    '''

    event_name = event['detail']['eventName']
    srv_details = event['detail']['serviceEventDetails']
    if event_name == 'CreateManagedAccount':
        LOG.info('Processing a CreateManagedAccount Event')
        account = srv_details['createManagedAccountStatus']['account']['accountId']
        if account in account_list:
            create_grant(account, sku)
        else:
            LOG.info('SKIPPING: Account %s not in %s', account, account_list)
    elif event_name == 'UpdateManagedAccount':
        LOG.info('Processing a UpdateManagedAccount Event')
        account = srv_details['updateManagedAccountStatus']['account']['accountId']
        if account in account_list:
            create_grant(account, sku)
        else:
            delete_grant(account, sku)
    else:
        LOG.warning('Event not supported: %s', event_name)


def process_cft_event(event, context, account_list, sku):
    '''
    Process Create/Update/Delete event from Cloudformation
    '''

    request_type = event['RequestType']
    LOG.info('Recieved %s request from CFT for %s', request_type, account_list)
    output_list = list()
    result = True
    if request_type in ['Create', 'Update']:
        for account in account_list:
            output = create_grant(account, sku)
    elif request_type == 'Delete':
        for account in account_list:
            output = delete_grant(account, sku)
            output_list.append(output)

    for item in output_list:
        if 'ResponseMetadata' in item:
            if item['ResponseMetadata']['HTTPStatusCode'] != 200:
                result = False
        else:
            result = False

    if result:
        LOG.info('SUCCESS: %s', result)
        send_signal(event, context, status='SUCCESS', data=output)
    else:
        LOG.info('FAILED: %s', result)
        send_signal(event, context, data=output)


def send_signal(event, context, status="FAILED", data=None,
                 rsrc_id='CustomResourcePhysicalID'):
    '''
    Send suscess/failure signal to cfnresponse
    '''

    if not data:
        data = list()
    cfnresponse.send(event, context, status, data, rsrc_id)


def lambda_handler(event, context):
    '''
    Lambda handler
    '''

    event_origin = None
    LOG.info('Event: %s, Context: %s', event, context)

    if 'detail' in event:
        event_origin = 'lc_event'
    elif 'RequestType' in event:
        event_origin = 'cft'

    try:
        ou_list = SSM.get_parameter(Name=environ['OU_PRM'])['Parameter']['Value'].split(',')
        sku = SSM.get_parameter(Name=environ['SKU_PRM'])['Parameter']['Value']
    except Exception as exe:
        if event_origin == 'cft':
            send_signal(event, context, data=[str(exe)])
        else:
            LOG.error('%s', str(exe))

    account_list = []
    LOG.info('OUS:%s, SKU:%s', ou_list, sku)

    for ou_id in ou_list:
        account_list += accounts_in_ou(ou_id)

    if event_origin == 'cft':
        if not len(get_grants(g_type='recieved', product_sku=sku)) > 0:
            send_signal(event, context, data=['NO_SUBSCRIPTION'])
        else:
            process_cft_event(event, context, account_list, sku)
    elif event_origin == 'lc_event':
        process_lifecycle_event(event, account_list, sku)
    else:
        LOG.error('Unsupported Event: %s', event)
