## Purpose 🤔❔ 

Even though we could keep the logs in CloudWatch, there are a couple of benefits of having the logs in an S3 bucket: 

- <b>Easier Event-Driven Workflows:</b> S3 can directly integrate with other AWS services such as Lambda that we will be using. 

- <b>Cost & Retention:</b> In S3, you can control the rention policies and lifecycle rules which is cheaper for long-term storage. CloudWatch logs calcuate pricing based on ingestion + retention + query costs which add up. 

- <b>Flexible Format for Processing:</b> the logs can be stored in formats such as JSON, raw, compressed, etc... which is helpful for situations when you need log parsing, threat hunting, and building detection pipelines. 

- <b>Central Repository:</b> S3 can act as your log aggregration bucket form multiple sources such as on-premise systems, other cloud providers (Azure, GPC), APIs, or custom apps. CloudWatch is only AWS-native, which means it can only log all the events that occur only in AWS. 

<hr>


<img src="/src/images/ec42.JPG" width="800px" alt="s3-bucket"> 

To make an S3 bucket search up `S3`, then choose the first option, → `Create bucket`. 

<img src="/src/images/ec43.JPG" width="800px" alt="s3-bucket"> 

Name the bucket anything in relation to the project. Now scroll down until you see `Bucket Versioning` and click on `enable`. This is optional but it is usually best practice to do so, Some benefits include data protection (recover objects if accidently deleted or overwritten), compliance (can help meet regulatory requirements for data protection), audit trail (versioning helps keep a clear record of data). 

Some use cases where you would not use it would be for data that is temporary and insignificant, and if you would want to reduce costs since each version of an object that is stored costs more. 

Everything else you can leave default, scroll down and hit → `Create bucket`. 

<img src="/src/images/ec44.JPG" width="800px" alt="s3-bucket"> 

Now the IAM role we added earlier needs permissions to write to this bucket, so to do this, search up `IAM`, then hit → `Roles` → then actually click on `EC2CloudWatchAgentRole` don't click the empty box for a check-mark. 

<img src="/src/images/ec45.JPG" width="800px" alt="s3-bucket">

Scroll down until you see `Permission Policies` then click → `Add permissions` → `Create inline policy`. 

<img src="/src/images/ec46.JPG" width="800px" alt="s3-bucket">

Switch over to the `JSON` tab, then copy the the exact same JSON configuration. To understand the JSON file a bit more, here are some things to know: 

- `"Statement":` is the main core the policy so everything inside contains a list of permissions 

- `"Effect": "Allow"` just means you are allowing the specified actions. 

- `"Action":` this is now the list of the specific actions that the EC2 role can perform on the S3 bucket: 

    - `s3:PutObject` → allows you to upload new log files to S3. ("you" refers to the EC2 for clarity)  
    - `s3:GetObject` → allows you to read or download files (optional). 
    - `s3:ListBucket` → allows you to view the list of files/objects inside the bucket. 
    - `s3:DeleteObject` allows you to delete the objects. 

- `"Resource":` specifies which S3 bucket and objects the permissions apply to:

    - `"arn:aws:s3:::ryan-siem-logs"` → refers to the bucket to bucket we created. 
    - `"arn:aws:s3:::ryan-siem-logs/*"` → refers to all the files/objects inside the bucket. 

This policy will let the EC2 instance upload logs, read logs, and list files in the `ryan-siem-logs` bucket. Once the JSON is filled out, click on `Next`. 

<img src="/src/images/ec47.JPG" width="800px" alt="s3-bucket">

name the policy anything in relation and then click on `Create policy`. 

<img src="/src/images/ec48.JPG" width="800px" alt="s3-bucket">

We can't just leave it like that, we need to test if the EC2 is able to upload logs to S3. To do this, connect to the EC2, and run the command `echo "test log from 05/11/2025" > test.log && aws s3 cp test.log s3://ryan-siem-logs/test.log`, but replace the date with the current date of your testing and the name for your S3 bucket, not mine.

<img src="/src/images/ec49.JPG" width="800px" alt="s3-bucket">

To see if it worked, search up `S3` then click on the bucket name. 

<img src="/src/images/ec50.JPG" width="800px" alt="s3-bucket">

Now you should see the `test.log` file uploaded into the S3 bucket! If you want to delete it, run the command `aws s3 rm s3://ryan-siem-logs/test.log` but replace the name with your S3 bucket like mentioned before. 