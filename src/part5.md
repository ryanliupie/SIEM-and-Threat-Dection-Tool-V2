## Purpose 🤔❔ 

AWS Lamda is a type of serverless AWS service that allows developers to run code without the management of servers. In this case, everytime a log gets uploaded to S3, Lamda will help us do something with that log. 

<hr>

<img src="/src/images/ec52.JPG" width="800px" alt="lambda-function">

Go to `IAM` and create a role and name it `LambdaS3LogProcessorRole` and attach policies `AmazonS3ReadOnlyAccess` and `AWSLambdaBasicExecutionRole`. 


<img src="/src/images/ec51.JPG" width="800px" alt="lambda-function">

Type in `Lambda` in the search bar and click on `Create a function` below. 

<img src="/src/images/ec53.JPG" width="800px" alt="lambda-function">

Stick with `Author from Scratch`. Choose a name like `SIEMLogProcessor`. The Language we will use will be `Python` and it will be the 3.13 version, you could use the 3.12 as well. Now with the role we just made, click on `Use an existing role` and choose `LambdaS3LogProcessorRole`. 


