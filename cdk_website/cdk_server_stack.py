import os
from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_rds as rds,
    aws_autoscaling as autoscaling
)
from constructs import Construct

dirname = os.path.dirname(__file__)

class CdkServerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, cdk_lab_vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Security Group for the web servers allowing inbound traffic on port 80
        web_sg = ec2.SecurityGroup(
            self, 
            "WebServerSG",
            vpc=cdk_lab_vpc,
            allow_all_outbound=True,
            description="Security group for the web server"
            )
        
        web_sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "Allow HTTP traffic")

        # Security Group for the RDS instance allowing inbound traffic on port 3306 from the web servers
        db_sg = ec2.SecurityGroup(
            self, 
            "DatabaseSG",
            vpc=cdk_lab_vpc,
            allow_all_outbound=True,
            description="Security group for the RDS instance"
            )
        
        db_sg.add_ingress_rule(web_sg, ec2.Port.tcp(3306))

        # Launch webserver in Public subnets
        selection = cdk_lab_vpc.select_subnets(subnet_type=ec2.SubnetType.PUBLIC)
        
        # Create an Auto Scaling group for web servers
        autoscaling.AutoScalingGroup(
            self, 
            "WebServerASG",
            vpc=cdk_lab_vpc,
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
            min_capacity=2,  
            max_capacity=2,  
            vpc_subnets=selection,  # Deploy instances in public subnets
            security_group=web_sg
        )
        
        # MySQL RDS instance in private subnets
        rds.DatabaseInstance(
            self, 
            "RDSInstance",
            engine=rds.DatabaseInstanceEngine.mysql(version=rds.MysqlEngineVersion.VER_8_0_19),
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
            vpc=cdk_lab_vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT),
            security_groups=[db_sg]
            )

        
    