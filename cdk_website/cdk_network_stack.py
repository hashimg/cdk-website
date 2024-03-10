from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
)
from constructs import Construct

class CdkNetworkStack(Stack):

    @property
    def vpc(self):
        return self.cdk_lab_vpc
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        
    
        self.cdk_lab_vpc = ec2.Vpc(
            self, 
            "cdk_vpc",
            max_azs=2, 
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PublicSubnet",  
                    subnet_type=ec2.SubnetType.PUBLIC
                ),
                ec2.SubnetConfiguration(
                    name="PrivateSubnet",  
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT
                )
            ]
        )