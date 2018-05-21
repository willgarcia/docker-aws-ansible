# Docker aws-ansible

Run Ansible and Cloudformation templates locally with Docker.

The `Dockerfile` in this repository provides:
* AWS credential management to deploy locally against existing AWS accounts (with MFA enabled and an STS role)
* CentOS 7 as a base image
* Python 2.7.5
* Ansible
* AWS CLI
* credstash
* jq
* [cfn_nag](https://github.com/stelligent/cfn_nag) which is used by AWS itself as part of they AWS developer tools (for more context, see [AWS CloudFormation Validation Pipeline
](https://docs.aws.amazon.com/solutions/latest/aws-cloudformation-validation-pipeline/considerations.html#test-functions) and [Implementation Considerations
](https://docs.aws.amazon.com/solutions/latest/aws-cloudformation-validation-pipeline/considerations.html#test-functions))

Note: These tools are install in the Docker image, so you don't need to install them locally.

## Requirements 

* Docker
* AWS Access Key and Secret to create a local profile that will be used to enable permissions to other AWS accounts - See section "Initial setup" to set up your first key.

## Initial setup

* Go to the AWS Console of the main AWS account
* Go to "Services" > "IAM" > "Users" and search for your username. e.g: "John.Doe"
* Open the user details view, and go to "Security credentials" tab > "Create access key" button. Make sure you keep a copy of the secret access key, as this value is only supplied at the creation time of the key. If you forget to take note of it, please delete your key and re-create a new one.
* Store the access key id and secret key id in a new local profile on your machine:

You don't necessarily need to install the AWS cli locally. If the file `$HOME/.aws/credentials` does not exist, you can create it.

If the AWS CLI is already installed, the AWS credential file is also located in `$HOME/.aws/credentials`, unless it has been changed by configuration.

Content to add to `$HOME/.aws/credentials`:

```
[generated]
aws_access_key_id = [...]
aws_secret_access_key = [...]
```

`generated`: new local profile name of your choice
`aws_access_key_id`: Access Key ID visible in the AWS Console
`aws_secret_access_key`: Secret Access Key provided during the key creation

* Build the docker image and generate your AWS STS temporary credentials. You will be prompted with your MFA token:

```
$ make build
$ make mfa-token
```

If your token is expired in the middle of a deployment or when you run an AWS CLI command, you will get the following error message which means that you need to re-generate a new one with `make run`:

```
An error occurred (ExpiredToken) when calling the DescribeStacks operation: The security token included in the request is expired
````

/!\ Note on security: 
* do not git push or share AWS credentials with anyone (present in `dockerenv` or `$HOME/.aws/credentials`). If you have shared this information by mistake, please contact your administrator and revoke your AWS keys.
* `dockerenv` needs to stay in the `.gitignore` file to avoid the issue mentioned previously

## Usage

```
$ make run
```
This will create a Docker container and give you access it to run Ansible.

## Generate STS Profile

The use of STS results in a similar approach to switching roles in the AWS Web console and enables programmatic access to your AWS sub-accounts.

Getting temporary permissions on a remote AWS account is possible via AWS Security Token Service (STS). AWS STS is a web service that enables you to request temporary, limited-privilege credentials for AWS Identity and Access Management (IAM) users or for users that you authenticate (federated users).


Provide your current IAM user ARN, your current AWS main profile, the target user role and your STS MFA token:

```
$ make mfa-token
AWS local profile (see ~/.aws/credentials):
AWS user name [eg: John.Doe]:
AWS MFA token (Google Auth, etc). 6-digits value:
```

The result of this command is new AWS profile generated directly in your `~/.aws/credentials` file (available inside and outside the Docker container)
