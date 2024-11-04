# AWS Resilience Hub GenAI

## Pre-requisites

- [CDK v2.160.0 or higher installed](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html)  
- [Bootstraped AWS Account](https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping-env.html)  
- [Shell with AWS Credentials](https://docs.aws.amazon.com/cli/v1/userguide/cli-configure-files.html)  

**One or more applications with assessments in Resilience Hub.**
- [Add an application to Resilience Hub (RH)](https://docs.aws.amazon.com/resilience-hub/latest/userguide/describe-applicationlication.html)  
- [Browse the GitHub repository for more RH samples.](https://github.com/aws-samples/aws-resilience-hub-tools)

## QuickStart

`git clone https://github.com/aws-samples/resilience-hub-genai.git`

The application requires signon via email.
Browse to the backend/constants.py file and edit the EMAIL parameter with your email address.

```
# REPLACE EMAIL with your email address
EMAIL = 'REPLACE with your email address'
```

Then run the deployment script.

`cd aws-resilience-hub-genai`
`./deploy.sh`

Once the deployment is completed you will see the following output in your shell:
```
Here is the site url 👇 :
    "CLOUDFRONTDISTRIBUTION": "d2guh719waj454.cloudfront.net",
```

Browse to the url and you will see the signon page.
Check your email for a message from no-reply@verificationemail.com 

It will contain your username(email) and temporary password.
Login and you will be prompted to change your password.

After that you will see the Welcome page.
You can begin generating your reports.



