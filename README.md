# suse-controltower-solution

Using AWS Marketplace, you can discover, purchase, migrate and deploy SUSE Linux Enterprise Service
(SLES) for SAP Applications Linux platform for SAP HANA, SAP NetWeaver, SAPP s/4HANA and SAP Business
Applications. The AWS Marketplace subscriptions are local to each AWS account by default and they are not
shared with remaining accounts in your Organization. With the combination of Managed entitlements for
AWS Marketplace and AWS License Manager, you can subscribe to the product from AWS Management
account and share it with remaining accounts in the organization. Users in the managed accounts can
directly access the approved marketplace products without a need to go to AWS Marketplace and initiate a
new subscription.

Using this solution, you can automate the creation of grants for accounts with in selected Organizational
Units (OUs). In addition, this solution leverages AWS Control Tower lifecycle events to automatically create
the grants when a new AWS Account is created in those OUs using Account Factory.
This solution is delivered as an AWS CloudFormation template for easy deployment into the environment.

Using this solution, you can:
✓ Specify a set of Organizational Units that you like create grant for.
✓ Automatically create the grants for both existing accounts and new accounts.
✓ Quickly deploy SLES for SAP instances within these Amazon Machine IDs (AMIs) in the managed
accounts

Pre-requisites
• AWS Control Tower should be deployed and working correctly.
• An active subscription to SUSE Linux Enterprise Server for SAP Applications 15 SP1 in the
management account.
• The SUSE Integration solution should be downloaded from the SUSE GitHub Repository.

To get started with AWS Control Tower, check out the Control Tower User Guide

For further information on this integration, how to deploy and use, please view the documentation on the marketplace website.
https://aws.amazon.com/marketplace/solutions/control-tower/operational-intelligence

Please check the LICENSE information.

Or contact SUSE.
email:  aws@suse.com
