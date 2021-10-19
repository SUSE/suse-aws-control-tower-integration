# suse-controltower-solution

Summary: The solution provided is used to share private AMIs from the Payer account where AWS Control Tower is deployed to the account(s) that will be created via AWS Control Tower Factory. The Cloudformation template is used to create an AWS Lambda function with relevant resources which will be deployed in the account and the region where AWS Control Tower is deployed. The Lambda function monitors the CloudWatch Event Rule which is configured for 'CreateManagedAccount' and 'UpdateManagedAccount' API. As soon a user creates an AWS Account via AWS Control Tower Account Factory or updates the Service Catalog Provisioned Product for an existing account that was deployed via AWS Control Tower Account Factory, the Lambda Function is invoked and shares the Private AMIs that were provided as parameter in the Cloudformation template.

Pre-requisites:

1. Deploy AWS Control Tower

Solution deployment:

1. Log into the AWS Account where you have AWS Control Tower deployed.
2. Navigate to the AWS Cloudformation
3. Make sure you are in the same region where AWS Control Tower is deployed
4. Launch the provided Cloudformation template
5. Add Private AMI IDs in the Parameters section of Cloudformation deployment. Use comma to seperate multiple AMI IDs.
6. Deploy the template

Testing the solution:

Method 1:

This method is used to test the solution when you dont want to deploy a new AWS Account via AWS Control Tower.

Pre-Requisite:

1. You already have an AWS Account created via AWS Control Tower Account Factory.

Steps:

1. Log in to the AWS Account where you have deployed this solution which will be the Payer account where AWS Control Tower is deployed
2. Navigate to AWS Service Catalog console
3. Click on 'Provisioned Products' from the left hand pane
4. Select the Provisioned Product that corresponds to the account that was created via AWS Control Tower Account Factory that you want to test this solution with
5. Click on the 'Actions' dropdown and select 'Update'
6. Fill in the parameters that you had entered when creating the account from AWS Control Tower Account Factory. (Make sure you fill the same parameters and not change anything)
7. Click 'Update'

This will invoke the 'UpdateManagedAccount' API call which will trigger the Lambda function that was created as a part of this solution deployment. Once the Provisioned Product is successfully updated the AMIs that you have entered in the Cloudformation parameter will be shared with this account.

1. Go to the EC2 console of the AWS account you updated the provisioned product for
2. Click on 'AMIs' from the left hand pane
3. Filter for 'Private Images' in the search bar
4. You will see the shared AMIs

Method 2:

This method is used to test the solution when you are deploying a new AWS Account via AWS Control Tower.

1. Log into the AWS Account where you have AWS Control Tower deployed
2. Navigate to the AWS Control Tower console
3. Select Account Factory from the left hand pane
4. Click on 'Enroll Account'
5. Enter the details
6. Click 'Enroll Account'

This will invoke the 'CreateManagedAccount' API call which will trigger the Lambda function that was created as a part of this solution deployment. Once the account is successfully created the AMIs that you have entered in the Cloudformation parameters will be shared with this account.

Caveats:

1. To share the AMIs with the existing AWS account(s) which were created before the deployment of this solution, you need to follow Method 1 in 'Testing the Solution' part.
2. Deleting the Cloudformation template for this solution from AWS Cloudformation console does not have any effect on the shared AMIs meaning the AMIs continue to be shared with the AWS accounts.
3. If you UPDATE the Cloudformation template to add/remove the AMIs from parameters, this does not affect the sharing for existing AWS accounts and it only applies to the accounts you are going to create after the UPDATE. If you want to apply this change to the existing accounts you need to follow Method 1 in 'Testing the Solution' part.
 
For any enquiries regarding this integration, please contact aws@suse.com