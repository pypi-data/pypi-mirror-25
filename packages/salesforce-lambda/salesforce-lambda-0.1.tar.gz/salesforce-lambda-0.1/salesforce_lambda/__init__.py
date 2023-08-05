import os
from salesforce_analytics import SalesForceAnalytics


def get_resource(event):
    if event['context'].has_key('resource-path'):
        return event['context']['resource-path']

def lambda_handler(event, context):
    http_method = event['context']['http-method']
    payload = event['payload']
    resource = get_resource(event)
    if not resource:
        raise Exception('[BadRequest] Invalid Resource')

    if 'analytics' in resource:
        if http_method == "POST":
            analytics = SalesForceAnalytics(tickets=payload)
            return analytics.run()
        else:
            return {'error': 'Invalid Request'}
