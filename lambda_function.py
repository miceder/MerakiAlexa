import requests
import json
import os

_MerakiToken = str(os.getenv("ACCESSTOKEN")) 
_fwUri = 'https://n229.meraki.com/api/v0/networks/L_584905001604748446/ssids/1/l3FirewallRules'
_MerakiHeader = {'X-Cisco-Meraki-API-Key': _MerakiToken, 'Content-Type': 'application/json'}


def lambda_handler(event, context):
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event, context)
		
    elif event['request']['type'] == "IntentRequest":
        return intent_router(event, context)
		
		
def on_launch(event, context):
    return build_response("Hey there")
	
	
def build_response(message):
    response = {}
    response['version'] = '1.0'
    response['response'] = {}
    response['response']['outputSpeech'] = {}
    response['response']['outputSpeech']['type'] = 'PlainText'
    response['response']['outputSpeech']['text'] = message
    response['shouldEndSession'] = 'true'
    return response
	
	
def intent_router(event, context):
    intent = event['request']['intent']['name']
	
    # Custom Intents
    if intent == "BlockAllTrafficIntent":
        print('recognized blockAllTraffic Intent')
        return updateFWRules('block all traffic')
    if intent == "BlockInternetAccessIntent":
        return updateFWRules('Internet Web Access')

    # Required Intents
    if intent == "AMAZON.CancelIntent":
        return cancel_intent()
    if intent == "AMAZON.HelpIntent":
        return help_intent()
    if intent == "AMAZON.StopIntent":
        return stop_intent()
		
		
def updateFWRules(rule_name):
    answerMessage = ''
    update = []
    response = requests.get(_fwUri, headers=_MerakiHeader)
    fwrules = response.json()
    
    for f in fwrules:
        if(f['comment'] == rule_name):
            if (f['policy'] == 'allow'):
                f['policy'] = 'deny'
            update.append(f)
        else:
            if(f['comment'] != 'Default rule' and f['comment'] != 'Wireless clients accessing LAN'):
                update.append(f)
    
    responsePut = requests.put(_fwUri, data=json.dumps({'rules': update}), headers=_MerakiHeader)
    print(responsePut)
    answerMessage = 'I have updated the firewall rules for you'
    return build_response(answerMessage)
