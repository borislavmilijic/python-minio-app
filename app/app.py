from flask import Flask, render_template, request, redirect
import boto3
from botocore.config import Config

app = Flask(__name__)

# S3 Configuration
s3_client = None
bucket_name = None

my_config = Config(
    region_name = 'us-east-1',
    # signature_version = 'v4',
    # retries = {
    #     'max_attempts': 10,
    #     'mode': 'standard'
    # }
)


# Configure S3 Client
@app.route('/', methods=['GET', 'POST'])
def configure_s3_client():
    global s3_client
    if request.method == 'POST':
        access_key = request.form['access_key']
        secret_key = request.form['secret_key']
        endpoint_type = request.form['endpoint_type']
        endpoint = request.form['endpoint']
        if endpoint_type == 'Server':
            s3_client = boto3.client(
                's3',
                endpoint_url=endpoint,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                aws_session_token=None,
                config=boto3.session.Config(signature_version='s3v4'),
                verify=False
            )
        else:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                config=my_config
            )
        
        return redirect('/bucket')
    
    return render_template('configure.html')

# Bucket Page
@app.route('/bucket', methods=['GET', 'POST'])
def bucket():
    global s3_client, bucket_name

    if s3_client is None:
        return redirect('/')

    if request.method == 'POST':
        file = request.files['file']
        
        if file.filename == '':
            # Handle case when no file is selected for upload
            error_message = "Please select a file to upload."
            return render_template('error.html', error_message=error_message)
        
        s3_client.upload_fileobj(file, bucket_name, str(file.filename))
        
        return redirect('/bucket')
    
    response = s3_client.list_buckets()
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    
    selected_bucket = request.form.get('bucket', '')
    print(selected_bucket)
    if selected_bucket and selected_bucket != bucket_name:
        bucket_name = selected_bucket

    # bucket_name = request.form['bucket']
    # print('s'*30)
    # print(response['Buckets'])
    print(request.form.get('bucket'))
    if bucket_name == None:
        bucket_name = buckets[0]
    # print(type(bucket_name))
    # print('s'*30)
    if bucket_name:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        bucket_contents = [obj['Key'] for obj in response.get('Contents', [])]
    else:
        bucket_contents = []

    if request.method == 'POST':
        file = request.files['file']
        
        if file.filename == '':
            # Handle case when no file is selected for upload
            error_message = "Please select a file to upload."
            return render_template('error.html', error_message=error_message)

        s3_client.upload_fileobj(file, bucket_name, str(file.filename))

        return redirect('/bucket')

    return render_template('bucket.html', buckets=buckets, selected_bucket=bucket_name, bucket_contents=bucket_contents)

# Delete Item from Bucket
@app.route('/delete_item', methods=['POST'])
def delete_item():
    
    selected_bucket = request.form.get('bucket', '')
    print(selected_bucket)
    bucket = request.form['bucket']
    key = request.form['key']
    
    if not bucket:
        # Handle empty bucket name error
        error_message = "Invalid bucket name. Please select a valid bucket."
        return render_template('error.html', error_message=error_message)
    
    try:
        s3_client.delete_object(Bucket=bucket, Key=key)
    except Exception as e:
        # Handle delete object error
        error_message = f"Failed to delete object: {str(e)}"
        return render_template('error.html', error_message=error_message)
    
    return redirect('/bucket')

# List Objects in Bucket
@app.route('/list_objects', methods=['POST'])
def list_objects():
    # List bucket names
    if s3_client is not None:
        response = s3_client.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
    else:
        buckets = []
    
    bucket_name = request.form['bucket']
    
    # Retrieve bucket contents
    if s3_client is not None:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        bucket_contents = [obj['Key'] for obj in response.get('Contents', [])]
    else:
        bucket_contents = []
    
    # Render bucket page template with updated bucket contents
    return render_template('bucket.html', buckets=buckets, bucket_contents=bucket_contents)

if __name__ == '__main__':
    app.run(debug=True)
