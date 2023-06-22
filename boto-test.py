import boto3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

#s3 config
s3_target = boto3.resource('s3', 
    endpoint_url='http://192.168.103.115:9000',
#     aws_access_key_id='eMGlzS6htbj0yoDHMByI',
#     aws_secret_access_key='OXkOTQEunJx8o89UztkkDXhYMORewlOjZb2fSAfo',
    aws_access_key_id='OaFn6VxBLd7m4DSvXc7X',
    aws_secret_access_key='9JEq9jRFGJ795dimlfG5LIIUW9tqn3wB23MGVwR2',
    aws_session_token=None,
    config=boto3.session.Config(signature_version='s3v4'),
    verify=False
)
# s3 = boto3.resource('s3')
for bucket in s3_target.buckets.all():
        print(bucket.name)

# Login Page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Perform login authentication (add your own logic here)
        username = request.form['username']
        password = request.form['password']
        
        # Redirect to bucket page after successful login
        return redirect('/bucket')
    
    # Render login page template
    return render_template('login.html')

# Bucket Page
@app.route('/bucket')
def bucket():
    # List bucket names
    response = s3_target.list_buckets()
    buckets = [bucket['Name'] for bucket in response['Buckets']]

    # Render bucket page template
    return render_template('bucket.html', buckets=buckets)

# Add Item to Bucket
@app.route('/add_item', methods=['POST'])
def add_item():
    bucket_name = request.form['bucket']
    # Code to add item to the bucket (add your own logic here)
    # Example: s3_client.put_object(Bucket=bucket_name, Key='example.txt', Body='Example content')
    
    # Redirect back to bucket page
    return redirect('/bucket')

# Delete Item from Bucket
@app.route('/delete_item', methods=['POST'])
def delete_item():
    bucket_name = request.form['bucket']
    key = request.form['key']
    # Code to delete item from the bucket (add your own logic here)
    # Example: s3_client.delete_object(Bucket=bucket_name, Key=key)
    
    # Redirect back to bucket page
    return redirect('/bucket')

if __name__ == '__main__':
    app.run(debug=True)