from flask import Flask, request, render_template
import boto3
from botocore.client import Config


REGION = 'ap-southeast-1'
PRESIGNED_EXPIRE_IN = 3600
S3_CLIENT = boto3.client('s3', config=Config(signature_version='s3v4'))

app = Flask(__name__, template_folder='template', static_folder='static')

def get_s3_region_endpoint(url):
  if REGION == "us-east-1":
    return url
  else:
    return url.replace(".s3.", f".s3.{REGION}.")

@app.route('/', methods=['GET'])
def home_page():
  return render_template('index.html')

@app.route('/health', methods=['GET'])
def healthcheck():
  return render_template('healthcheck.html')

@app.route('/sign', methods=['GET'])
def signv2_request():
  bucket_name = request.args.get('bucket')
  object_name = request.args.get('object')
  response = S3_CLIENT.generate_presigned_post(
    Bucket=bucket_name,
    Key=object_name,
    Conditions=[
      {
        "acl": "private"
      },
      ["starts-with", "$Content-Type", ""]
    ],
    ExpiresIn=PRESIGNED_EXPIRE_IN
  )
  response['url'] = get_s3_region_endpoint(response['url'])
  return {
    'signed_url': response,
    'bucket_name': bucket_name
  }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
