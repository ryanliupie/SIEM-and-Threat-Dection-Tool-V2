<img src="/src/images/ec21.jpg" width="800px" alt="ec2-name">

On the search bar, search up `EC2`. Name the EC2 `Detection` as this EC2 will feed the SSH login attempts to other AWS services, then choose the `Amazon Linux` AMI. 

<img src="/src/images/ec22.JPG" width="800px" alt="ec2-instance-type">

Choose the `t2.micro` instance type and then click on `Create new key pair`

<img src="/src/images/ec23.JPG" width="800px" alt="ec2-key-pair">

Name the key pair `ssh-detection-key`, keep RSA, and then click on `Create key pair`. Once created, your computer will automatically download a `.pem` file containing the key content; make sure to store it in a safe place. This key lets us securely connect to the instance using asymmetric encryption. 

<img src="/src/images/ec24.JPG" width="800px" alt="ssh-allow-anywhere">

The SSH protocol lets us securely connect to a device commonly through the command-line. In this instance, we are "allowing traffic from any IP address" which means anyone on the internet can try to access it. 

A couple reasons why companies allow SSH `0.0.0.0/0` open include: 

- <b>Convenience & Remote Access:</b> There are many employees that need remote access to servers from many locations and restricting specific IPs get extremely difficult especially if users are using dynamic IP addresses. 

- <b>Safe Enough:</b> Some companies would rather prioritize ease of access over a lot of security, assuming other controls such as SSH key pairs and MFA are in place. 

Some security risks of Open SSH `0.0.0.0/0` include: 

- <b>Brute Force Attacks:</b> Exposed SSH ports allow users all over the internet to attack by trying default keys or passwords (if a company uses passwords instead).
- <b>Zero-Day Exploits:</b> If a vulnerability were to exist in SSH, attackers can easily exploit it before patches are applied. 
- <b>Credential Stuffing:</b> If employee credentials are leaked, attackers can gain direct access by injecting those stolen passwords.
- <b>Compliance Violations:</b> Open SSH may lead to violations when following certain security frameworks that require strict access control in a more technical manner based on certain conditions of what the system is doing. 

Some best practices to secure SSH include: 

- <b>Use SSH Key Authentication:</b> As mentioned, we do not want to use passwords, rather use a key pair. 
- <b>Enforce MFA:</b> Making sure the only way a user can log in is if they provide a couple of methods. 
- <b>Using Network ACLs or Security Groups:</b> Try your best to restrict specific access to resources even though it may be hard to in a larger environment. 
- <b>Implement Fail2Ban:</b> This is type of IPS that dynamically blocks IPs after repeated failed login attempts. 
- <b>Restrict SSH to VPN:</b> Instead of allowing 0.0.0.0/0 open, you can restrict the access by only allowing specific connections from an VPN's IP range. A person would authenticate to the corporate VPN, then the server's firewall would whitelist the VPN subnet so users only on the VPN can reach SSH. 
- <b>Regularly Rotate SSH Keys:</b> It's good practice to change SSH keys from time to time in case that key were to be compromised. 

<img src="/src/images/ec24.JPG" width="800px" alt="ssh-allow-anywhere">

Click on `Launch instance` after everything is set and ready to go.





