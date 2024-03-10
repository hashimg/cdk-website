#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_website.cdk_network_stack import CdkNetworkStack
from cdk_website.cdk_server_stack import CdkServerStack


app = cdk.App()
NetworkStack = CdkNetworkStack(app, "CdkNetworkStack")
CdkServerStack(app, "CdkServerStack", cdk_lab_vpc=NetworkStack.vpc)

app.synth()
