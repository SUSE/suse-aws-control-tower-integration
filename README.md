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

For further information on this integration, how to deploy and use, please view the SUSE documentation linked from the AWS Marketplace website.
https://aws.amazon.com/marketplace/solutions/control-tower/operational-intelligence

LICENSE:

Copyright (C) 2021 SUSE LLC

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

SUSE Software Solutions Germany GmbH
Maxfeldstr. 5
D-90409 Nürnberg
Tel: +49 (0)911 740 53 - 0
Email: info@suse.com
Registrierung/Registration Number: HRB 36809 AG Nürnberg
Geschäftsführer/Managing Director: Felix Imendörffer
Steuernummer/Sales Tax ID: DE 192 167 791
Erfüllungsort/Legal Venue: Nürnberg
© 2021 GitHub, Inc.

SUPPORT:

This CT integration comes with no support entitlement, but if you have any queries, please raise an issue for the project via github or contact the SUSE team at:

aws@suse.com
