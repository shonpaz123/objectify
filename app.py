from rgwadmin import RGWAdmin, RGWUser
from flask import Flask, request 
from flask import jsonify
import argparse
import requests


class Notifier:
    def __init__(self, url):
        self.url = url

    def notify(self, data):
        headers = {'AccessKey': data["key"], 'Realm': data["realm"], 'Profile': data["profile"]}
        a = requests.post("http://" + self.url, headers=headers)
        return a.status_code

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

realm_dict = {}

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--endpoint-url', help="endpoint url for s3 object storage",
                            required=True)
parser.add_argument('-a', '--access-key', help='access key for s3 object storage',
                            required=True)
parser.add_argument('-s', '--secret-key', help='secret key for s3 object storage',
                            required=True)
parser.add_argument('-p', '--proxy', help='HA proxy to notify about storage account creation',
                            required=True)

args = parser.parse_args()

rgw = RGWAdmin(access_key=args.access_key, secret_key=args.secret_key, server=args.endpoint_url,
               secure=False, verify=False)
my_notifier = Notifier(args.proxy)

@app.route("/createuser", methods=['GET', 'POST'])

def createuser():
    if request.method == 'POST':
      result = request.form
      username = request.args.get('uid')
      displayname = request.args.get('displayname')
      u = rgw.create_user(uid=username, display_name=displayname)
      realm_dict[username] = 'realm1'
      notification = {'key': u["keys"][0]["access_key"], 'realm': "realm1", 'profile': "Gold"}
      my_notifier.notify(notification)
      return u

@app.route("/getusermapping", methods=['GET'])

def getusermapping():
    if request.method == 'GET':
      return jsonify(realm_dict)

if __name__ == "__main__":
    app.run(debug=True, port=8080)
