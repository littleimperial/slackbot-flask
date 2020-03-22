from flask import Blueprint, jsonify, request, redirect, url_for
import os, urllib
import slack

blueprint = Blueprint('slack', __name__, url_prefix='/slack')

AUTHORIZE_URL = 'https://slack.com/oauth/v2/authorize'
ACCESS_URL = 'https://slack.com/api/oauth.v2.access'

@blueprint.route('/start_install', methods=['GET'])
def start_install():
    scope = 'channels:join chat:write'
    client_id = os.environ['SLACK_CLIENT_ID']
    redirect_uri = urllib.parse.urljoin(request.url_root, url_for('slack.finish_install'))
    return redirect(AUTHORIZE_URL + '?' + urllib.parse.urlencode({ 'scope': scope, 'client_id': client_id, 'redirect_uri': redirect_uri }))

@blueprint.route('/finish_install', methods=['GET'])
def finish_install():
    code = request.args.get('code')
    client_id = os.environ['SLACK_CLIENT_ID']
    client_secret = os.environ['SLACK_CLIENT_SECRET']
    channel = os.environ['SLACK_CHANNEL']

    client = slack.WebClient(token="")
    response = client.oauth_v2_access(client_id=client_id, client_secret=client_secret, code=code)
    os.environ['SLACK_BOT_ACCESS_TOKEN'] = response['access_token']

    client = slack.WebClient(token=os.environ['SLACK_BOT_ACCESS_TOKEN'])
    response = client.channels_join(name=channel)
    print(response)

    response = client.chat_postMessage(channel=channel, text='hello')
    print(response)

    return jsonify({'status': 'ok'})
