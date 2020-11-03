import firebase_admin

from firebase_admin import messaging

from firebase_admin import credentials

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