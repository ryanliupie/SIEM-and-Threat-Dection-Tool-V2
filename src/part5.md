## Purpose 🤔❔ 

AWS Lambda is a type of serverless AWS service that allows developers to run code without the management of servers. In this case, everytime a log gets uploaded to S3, Lamda will help us do something with that log. 

<hr>

<img src="/src/images/ec52.JPG" width="800px" alt="lambda-function">

Go to `IAM` and create a role and name it `LambdaS3LogProcessorRole` and attach policies `AmazonS3ReadOnlyAccess` and `AWSLambdaBasicExecutionRole`. 


<img src="/src/images/ec51.JPG" width="800px" alt="lambda-function">

Type in `Lambda` in the search bar and click on `Create a function` below. 

<img src="/src/images/ec53.JPG" width="800px" alt="lambda-function">

Stick with `Author from Scratch`. Choose a name like `SIEMLogProcessor`. The Language we will use will be `Python` and it will be the 3.13 version, you could use the 3.12 as well. Now with the role we just made, click on `Use an existing role` and choose `LambdaS3LogProcessorRole`. 

<img src="/src/images/ec54.JPG" width="800px" alt="lambda-function">

In `IAM`, go to back to `Roles`, then `Permissions`, and then click on `Add permissions`, and lasty click on `Create inline policy`. Since the lambda function will write objects into the S3 bucket, we need to make an inline policy. 

<img src="/src/images/ec55.JPG" width="800px" alt="lambda-function">

Under `Service`, select `Lambda` since we need to give it permission to take the logs from Cloudwatch and write them into S3. Copy the JSON structure, and then click `Next` on the bottom right. Name the policy `LambdaS3WriteAccess`, and then click on `Create policy`. 

<img src="/src/images/ec56.JPG" width="800px" alt="lambda-function">

Go back to Lambda, and click on `Add trigger`. 

<img src="/src/images/ec57.JPG" width="800px" alt="lambda-function">

Pick the `SSHLogGroup`, then name it whatever you want, in this case it could be `SSHDetectionTrigger`. After that, click on `Add`. Theorectically, after this is setup, every new SSH attempt log entry will: 
- Trigger Lambda → Process the log → upload to S3 bucket automatically. 