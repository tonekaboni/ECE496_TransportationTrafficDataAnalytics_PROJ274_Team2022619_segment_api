from flask import Flask, render_template, url_for, send_file, request
import boto3
import os
app = Flask(__name__)
def download_file(file_name, bucket, object_name):
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket, Key=file_name)
    data = response['Body'].read().decode('utf-8')
    return data
    #try:
    #    s3_client.download_file(bucket, object_name, file_name)
    #except Exception as e:
    #    logging.error(e)
    #    return False
    #return True
    

def find_file_names(name):
    
    s3 = boto3.client('s3')

    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket="prod-traffic-data-094380741183", Prefix=name)
    return_pair =['P'] * 2
    iter = 0
    for page in pages:
        for obj in page['Contents']:
            return_pair[iter] = obj['Key']
            iter = iter + 1
            #print(obj['Key'])
    return return_pair
#find_file_names ("prod-traffic-data-094380741183")
#result_download = download_file("2022-12-02 20:50:21.233592.txt", "prod-traffic-data-094380741183", "2022-12-02 20:50:21.233592.txt")

@app.route('/download/<string:filename>', methods=['GET'])
def download(filename):
    index = 0
    minute = int(filename[15])
    print ("minute: " + filename[15] + "\n")
    if (minute>5):
        index = 1
    depracated_filename = filename[:-1]
    print ("depracated_filename: " + depracated_filename + "\n")
    matched_names = find_file_names (depracated_filename)
    final_name = matched_names[index]
    print ("final_name: " + final_name + "\n")
    #p = filename+".txt"
    data = download_file(final_name,"prod-traffic-data-094380741183",final_name)

    #with open(final_name) as file:
    #    data = f.read()
     
    #print("data:\n"+data)

    return data
    
    
    #send_file(p, as_attachment=True)

#download("2022-12-02 20:52")
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)