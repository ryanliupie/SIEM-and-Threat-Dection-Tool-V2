<img src="/src/images/ec26.JPG" width="800px" alt="ec2-cloudwatch">

Once the EC2 is running and is initialized, click on the empty box right next to the name of the EC2, then click on `Connect`. 

<img src="/src/images/ec27.JPG" width="800px" alt="ec2-cloudwatch">

In this case, we are not going to use our `.pem` file for ease of access. We do not need to change `ec2-user` because that refers to the default login username of the Amazon Linux AMI, not the actual instance name. Go ahead and click on `Connect`. 

<img src="/src/images/ec28.JPG" width="800px" alt="ec2-cloudwatch">

Once connected, run the command `sudo yum install amazon-cloudwatch-agent` which is referenced from <a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/install-CloudWatch-Agent-on-EC2-Instance.html">AWS Documentation</a> to install the CloudWatch agent. Some commands will be referenced from it with the addition of my personal experience. 

<img src="/src/images/ec29.JPG" width="800px" alt="ec2-cloudwatch">

Next, CloudWatch needs a configuration file because it needs to know what logs to collect, which log group to send them to, and what format timestamps use, etc... We are going to make a directory for this; run the command `sudo mkdir -p /opt/aws/amazon-cloudwatch-agent/etc`

<img src="/src/images/ec30.JPG" width="800px" alt="ec2-cloudwatch">

Next, we are going to make a JSON file to include all the information mentioned. Run the command `sudo nano /opt/aws/amazon-cloudwatch-agent/etc/cw-config.json`. 

<img src="/src/images/ec31.1.JPG" width="800px" alt="ec2-cloudwatch">

To explain this JSON file, `logs` is the top-level key that indicates to CloudWatch that log files will be sent. `logs_collected` indicates the types of logs that will be collected, and in this case "file-based logs" from the local server. 

`files` specifes we are collecting logs from local file paths. `collect_list` contains different types of objects which include: 
- `"file_path": "/var/log/secure"` which is the path on the EC2 instance to the log file we're monitoring. In this case, this tracks authentication logs, attempts and failures for SSH, and more. 

- `"log_group_name":  "SSHLogGroup"` is the CloudWatch Log Group name where logs will be sent in AWS.

- `"log_stream_name": "{instance_id}/secure"` defines how logs are grouped within the Log Group where "instance_id" autofills the actual EC2 instance ID.

- `"timestamp_format": "%b %d %H:%M:%S"` tells CloudWatch how to read the time in logs.
    
    -   `%b` ➳ short month (Apr)
    - `%d` ➳ day of month (26)
    - `%H:%M:%S` ➳ hour, minute, second (11:23:12)

- An example log in CloudWatch could look like this hopefully: 
    ```
    Apr 26 11:23:12 ec2-user sshd[1234]: Failed password for invalid user admin
    ```
After writing up the JSON file, click `Ctrl + O` ➳ `Enter` (to save). Then, click `Ctrl + X` (to exit). 

<img src="/src/images/ec32.JPG" width="800px" alt="ec2-cloudwatch">

Now, we need to apply the configuration JSON file to the CloudWatch agent so it knows what logs to collect and where to send them hence the JSON file we just created. To do this run the command `sudo /usr/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file:/opt/aws/amazon-cloudwatch-agent/etc/cw-config.json -s
`. 

<img src="/src/images/ec33.JPG" width="800px" alt="ec2-cloudwatch">

Even though, we have configured what the CloudWatch agent should do, it isn't running yet since in the photo before, it said `amazon-cloudwatch-agent has already stopped`. To explicitly start it, run the command `sudo systemctl start amazon-cloudwatch-agent`. If it says "active" we are good to go. 

<img src="/src/images/ec34.JPG" width="800px" alt="ec2-cloudwatch">

To enable the CloudWatch agent to have permissions to create and write logs to CloudWatch, first search up `IAM` in the AWS management console, head over to `Access management` → `Roles` → `Create`. 

<img src="/src/images/ec35.JPG" width="800px" alt="ec2-cloudwatch">

Choose the default `AWS service` then select `EC2` as the use case since that is the service we are trying to perform actions on. 

<img src="/src/images/ec36.JPG" width="800px" alt="ec2-cloudwatch">

The policy that we are going to set is `CloudWatchAgentServerPolicy` which is the minimum permissions needed for the CloudWatch agent to function. Do not choose ❌`CloudWatchAgentAdminPolicy`❌ because this would grant full administrative access to the CloudWatch agent running on our EC2. This would let the agent modify/access sensitive monitoring configurations, create and delete other agents etc... 

<img src="/src/images/ec37.JPG" width="800px" alt="ec2-cloudwatch">

Now, name the IAM role for the agent anything in relation such as `EC2CloudWatchAgentRole` and give it any easily readable description. After, scroll down and click `Create role`.  

<img src="/src/images/ec38.JPG" width="800px" alt="ec2-cloudwatch">

Go back to the EC2. Click on `Actions` → `Security` → `Modify IAM role`. 

<img src="/src/images/ec39.JPG" width="800px" alt="ec2-cloudwatch">

Choose the IAM role for the Agent we just created, then click on `Update IAM role`. 

<img src="/src/images/ec40.JPG" width="800px" alt="ec2-cloudwatch">

After updating the IAM Role, restart the CloudWatch Agent by connecting to the EC2 instance to make sure everything updates and is in working order. 

<img src="/src/images/ec41.JPG" width="800px" alt="ec2-cloudwatch">

Let's check if the `SSHLogGroup` was automatically created, so in the search bar, type in `CloudWatch` → `Logs` → `Log groups`. This Log group will specifically capture SSH-related events based on the `"file_path": "/var/log/secure"` we discussed earlier. 


<hr>

# ⚠️

Above when connected to the instance, it says `Amazon Linux 2023`. Remember in step 2, make sure you choose `Amazon Linux 2 AMI`. However, if you chose the 2023 AMI, here is what to look out for when configuring the JSON file: 

- If using the Amazon Linux 2023 AMI use → `"file_path": "/var/log/messages"` 

- If using the Amazon Linux 2 AMI use → `"file_path": "/var/log/secure"` (preferrably use this one ✔)

    - Above I used the 2023 AMI with "secure" which does not exist on it, so I just made another EC2 and repeated all the steps. However, if you did initially choose the Linux 2 AMI, everything should work 😎. 