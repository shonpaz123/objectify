from rgwadmin import RGWAdmin, RGWUser
from flask import Flask, request 
from flask import jsonify
import argparse

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

args = parser.parse_args()

rgw = RGWAdmin(access_key=args.access_key, secret_key=args.secret_key, server=args.endpoint_url,secure=False, verify=False)

@app.route("/createuser", methods=['GET', 'POST'])

def createuser():
    if request.method == 'POST':
      result = request.form
      username = request.args.get('uid')
      displayname = request.args.get('displayname')
      u = rgw.create_user(uid=username, display_name=displayname)
      realm_dict[username] = 'realm1'
      return u

@app.route("/getusermapping", methods=['GET'])

def getusermapping():
    if request.method == 'GET':
      return jsonify(realm_dict)

if __name__ == "__main__":
    app.run(debug=True)
