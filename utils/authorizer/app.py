import os, re, json, time, urllib.request
from jose import jwk, jwt
from jose.utils import base64url_decode

### GLOBALS
region = os.getenv('REGION_COGNITO')
USERPOOL_ID = os.environ['POOLS_USER_ID']
APP_CLIENT_ID = os.environ['POOLS_WEB_CLINT_ID']
KEYS_URL = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(region, USERPOOL_ID)
with urllib.request.urlopen(KEYS_URL) as f: response = f.read()
keys = json.loads(response.decode('utf-8'))['keys']

### -------------
### AUTH HANDLER
### -------------
def lambda_handler(event, context):



    TOKEN = event['authorizationToken']
    METHOD_ARN = event['methodArn']
    tmp = event['methodArn'].split(':')
    AWS_ACCOUNT_ID = tmp[4]
    region = tmp[3]
    apiGatewayArnTmp = tmp[5].split('/')
    REST_API_ID = apiGatewayArnTmp[0]

    print('\nnAuthFunction - TOKEN', TOKEN)
    print('\nnAuthFunction - METHOD_ARN', METHOD_ARN)
    print('\nnAuthFunction - AWS_ACCOUNT_ID', AWS_ACCOUNT_ID)
    print('\nnAuthFunction - REST_API_ID', REST_API_ID)
    print('\nnAuthFunction - region', region)


    # get the kid from the headers prior to verification
    ### [CASE_1]
    if not jwt.get_unverified_headers(TOKEN).get('kid'):
        return generateAuthResponse('user','Deny',METHOD_ARN,region,AWS_ACCOUNT_ID,REST_API_ID)
    

    # search for the kid in the downloaded public keys
    ### [CASE_2]
    kid = jwt.get_unverified_headers(TOKEN).get('kid')
    key_index = -1
    for i in range(len(keys)):
        if kid == keys[i]['kid']:
            key_index = i
            break
    if key_index == -1:
        print('\nAuthFunction - CASE_2 - Public key not found in jwks.json')
        return generateAuthResponse('user','Deny',METHOD_ARN,region,AWS_ACCOUNT_ID,REST_API_ID)


    ### Decode...
    public_key = jwk.construct(keys[key_index]) # construct the public key
    message, encoded_signature = str(TOKEN).rsplit('.', 1) # get the last two sections of the token, message and signature (encoded in base64)
    decoded_signature = base64url_decode(encoded_signature.encode('utf-8')) # decode the signature


    # verify the signature
    ### [CASE_3]
    if not public_key.verify(message.encode("utf8"), decoded_signature):
        print('\nAuthFunction - CASE_3 - Signature verification failed')
        return generateAuthResponse('user','Deny',METHOD_ARN,region,AWS_ACCOUNT_ID,REST_API_ID)
    
    ###-----------------------------------------------------------------------------------
    ### [PHASE_2]
    ###-----------------------------------------------------------------------------------


    # since we passed the verification, we can now safely
    # use the unverified claims
    print('\nAuthFunction - Signature successfully verified')
    claims = jwt.get_unverified_claims(TOKEN)


    # additionally we can verify the token expiration
    ### [CASE_4]
    if time.time() > claims['exp']:
        print('\nAuthFunction - CASE_4 - Token is expired')
        return generateAuthResponse('user','Deny',METHOD_ARN,region,AWS_ACCOUNT_ID,REST_API_ID)


    # and the Audience  (use claims['client_id'] if verifying an access token)
    ### [CASE_5]
    if claims['client_id'] != APP_CLIENT_ID:
        print('\nAuthFunction - CASE_5 - Token was not issued for this audience')
        return generateAuthResponse('user','Deny',METHOD_ARN,region,AWS_ACCOUNT_ID,REST_API_ID)


    # now we can use the claims
    ### [CASE_6] => [SUCCESS]
    print('\nAuthFunction - CASE_6 - ', claims)
    return generateAuthResponse('user','Allow',METHOD_ARN,region,AWS_ACCOUNT_ID,REST_API_ID)

### -------
### HELPER
### -------
def generateAuthResponse(principalId, effect, methodArn,region,awsAccountId,restApiId):
    print('\nAuthFunction - generateAuthResponse')
    policyDocument = generatePolicyDocument(effect, methodArn,region,awsAccountId,restApiId)
    authResponse = {
        "principalId": principalId,
        "policyDocument": policyDocument
    }
    print('\nAuthFunction - generateAuthResponse - ', authResponse)
    return authResponse



### -------
### HELPER
### -------
def generatePolicyDocument(effect, methodArn,region,awsAccountId,restApiId):
    print('\nAuthFunction - generatePolicyDocument')
    if len(effect) == 0 or len(methodArn) == 0: return None
    policyDocument = {
        "Version": '2012-10-17',
        "Statement": [{
            "Action": 'execute-api:Invoke',
            "Effect": effect,
            "Resource": "arn:aws:execute-api:{}:{}:{}/dev/*".format(region,awsAccountId,restApiId)
            #"Resource": "arn:aws:execute-api:{}:{}:{}/{}/*".format(region,awsAccountId,restApiId,os.environ['STAGE_NAME'])
            
        }]
    }
    print('\nAuthFunction - generatePolicyDocument - ', policyDocument)
    return policyDocument

