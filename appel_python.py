import firebase_admin

from firebase_admin import messaging

from firebase_admin import credentials

import requests

def requestToken():
    """
    OAuth v.2 token request to RTE identification server
    :return: a token valid for 2 hours
    """
    RTE_ID64 = open('credit_RTE', 'r')
    RTE_ID64 = RTE_ID64.read()
    header = {'Authorization' : 'Basic ' + RTE_ID64}
    r = requests.post('https://digital.iservices.rte-france.com/token/oauth/', headers=header)
    # print(r.status_code)
    # print(r.headers)
    # print(r.text)
    if r.status_code == requests.codes.ok :
        token = r.json()['access_token']
        return token
    else :
        return ''

def headerWithToken():
    token = requestToken()
    return {'Authorization' : 'Bearer ' + token}

def getActualGenerationPerProductionType():
    """
    Cette ressource a pour objectif de permettre de récupérer la production infrajournalière réalisée agrégée par filière
    Doc : https: // data.rte - france.com / catalog / - / api / user_guide / 226953
    :return: json structure
    """
    url = 'https://digital.iservices.rte-france.com/open_api/actual_generation/v1/actual_generations_per_production_type'
    sandbox_url = 'https://digital.iservices.rte-france.com/open_api/actual_generation/v1/sandbox/actual_generations_per_production_type'
    datefmt = '%Y-%m-%dT%H:%M:%S%z'
    today = datetime.today()
    start_date = (today-period).strftime(datefmt)
    end_date = today.strftime(datefmt)
    payload = '?start_date={}%2B02:00&end_date={}%2B02:00'.format(start_date, end_date)
    print(payload)

    try :
        r = requests.get(url+payload, headers=headerWithToken())
        r.raise_for_status()
    except requests.exceptions.HTTPError as e :
        print(e)
        print('request headers : {}'.format(r.headers))
        return
    return r.json()

def envoi_notif():
    if not firebase_admin._apps:
        cred = credentials.Certificate("succopuce-firebase.json") 
        default_app = firebase_admin.initialize_app(cred)


    # Define a condition which will send to devices which are subscribed
    # to either the Google stock or the tech industry topics.
    condition = "'tac' in topics"

    # See documentation on defining a message payload.
    message = messaging.Message(
        notification=messaging.Notification(
            title='$GOOG up 1.43% on the day',
            body='$GOOG gained 11.80 points to close at 835.67, up 1.43% on the day.',
        ),
        condition=condition,
    )

    # Send a message to devices subscribed to the combination of topics
    # specified by the provided condition.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)
