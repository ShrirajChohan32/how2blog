from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_ec2 as ec2,
    aws_route53 as route53,
    aws_route53_targets as target,
    aws_s3 as s3,
    aws_cloudfront_origins as origins,
    aws_certificatemanager as acm,
    aws_cloudfront as cloudfront,
    aws_iam as iam,
    cloud_assembly_schema as cloud_assembly_schema,
)

from aws_cdk.aws_cloudfront import *
import aws_cdk as cdk

record_name12 = "www"
dom_name = "www.shrirajchohan.com"

class BlogStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #Create a Bucket
        bucket_website = s3.Bucket(self, "BucketWebsite",
            bucket_name="www.shrirajchohan.com",  # www.example.com
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            website_index_document="index.html",
            )        

       # i had a created a bucket policy to grant public access for testing, but turned it off after deploying Cloudfront.
        # bucket_website.grant_public_access()  


        # Create an Origin Access Identity for the CloudFront distribution
        oai = cloudfront.OriginAccessIdentity(self, "MyOAI")

        # Create a bucket policy that allows access only from the OAI
        bucket_website.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["s3:GetObject"],
                principals=[iam.CanonicalUserPrincipal(oai.cloud_front_origin_access_identity_s3_canonical_user_id)],
                resources=[bucket_website.arn_for_objects("*")],
            ),
        )

        #Create Route53 Hosted Zone
        zone = route53.HostedZone(self, "Zone", zone_name = "shrirajchohan.com",) # example.com

        #Create an ACM Certificate
        cert_dns_val = acm.DnsValidatedCertificate(self,
            'DnsValidation',
            hosted_zone=zone, # Add a record in the Route53 hosted zone (hosted zone that we crearted above),
            domain_name=dom_name,
            validation=acm.CertificateValidation.from_dns_multi_zone({ "www.shrirajchohan.com" : zone}),
            region='us-east-1') #Certificate must be created in North Virginia since it will be attached to the Cloudfront (Regional Service) 

        #Create a Cloudfront 
        Cloudfront_distribution = cloudfront.CloudFrontWebDistribution(
            self, "MyDistribution",
            origin_configs=[
                cloudfront.SourceConfiguration(
                    s3_origin_source=cloudfront.S3OriginConfig(
                        s3_bucket_source=bucket_website,# Associate with S3 Bucket.
                        origin_access_identity=oai,
                    ),
                    behaviors=[cloudfront.Behavior(is_default_behavior=True)]
                )
            ],default_root_object="index.html", #Look for Index.html in S3 bucket as default blog page
            viewer_certificate=cloudfront.ViewerCertificate.from_acm_certificate(
                cert_dns_val, # Associate the above Certificate to the Cloudfront.
                aliases=["www.shrirajchohan.com"], # Give alternate domain
                security_policy=cloudfront.SecurityPolicyProtocol.TLS_V1.TLS_V1_2_2021 #Recommended SSL Security policy protocol
            ),
        )

        #Create a Cloudfront record in Route 53 hosted zone
        route53.ARecord(self, "AliasRecord", 
            zone=zone, record_name=record_name12, 
            target=route53.RecordTarget.from_alias(
                target.CloudFrontTarget(Cloudfront_distribution) # Redirect blog domain(www.shrirajchohan.com) to Cloudfront domain)
            )
        )

# class ACM_Certificate(acm.Certificate):
#     def __init__(self, scope: Construct) -> None: 
#         super().__init__(scope, "ACM_Certificate", domain_name="www.shrirajchohan.com",validation=acm.CertificateValidation.from_dns({ "www.shrirajchohan.com" })),


        

# class ACM_Certificate_stack(Stack):
#     """Implement an ACM"""

#     def __init__(self, scope: Construct, construct_id: str,default_action="allow", **kwargs) -> None:
#         super().__init__(scope, construct_id, **kwargs)


        # s3_certificate = acm.Certificate(self, "Certificate",
        #     domain_name=dom_name,
        #     validation=acm.CertificateValidation.from_dns_multi_zone({ "www.shrirajchohan.com" : zone})),

        # acm_cert = acm.Certificate.from_certificate_arn()

        # acm_cert= acm.Certificate.from_certificate_arn(self, "Cert", certificate_arn="arn:aws:acm:us-east-1:Certificate*")

        # print(acm_cert)



        # cdk.CfnOutput(self,"web_cert",value=acm_cert.certificate_arn,export_name="RealCertificate")


 
        # export_name="s3_certificate")
        
        # value=s3_certificate.acm
        # ,export_name="s3_certificate")










        # 👇 assign the arn to a variable
        # certArn = cer



        #create an output object which defined value and exportName


        # certificate = acm.Certificate.certificate_arn()


        # cdk.CfnOutput(self,"web_cert",value=s3_certificate,export_name="s3_certificate")

            # exportName= "web_cert")

        
        



    # new cdk.CfnOutput(this, "ec2RoleArn", {
    #   value: ec2Role.roleArn,
    #   exportName: "web_cert",
    # });









        

        # Cloudfront12 = cloudfront.Distribution(self, "myDist",
        #     default_behavior=cloudfront.BehaviorOptions(
        #         origin=origins.S3Origin(bucket_website)),
        #         domain_names=["www.shrirajchohan.com"],
        #         certificate=cert_dns_val,
        #         default_root_object="index.html"),

# distribution = CloudFrontWebDistribution(
#     self,
#     "SiteDistribition",
#     origin_configs=[
#         {
#             "s3OriginSource": {
#                 "s3BucketSource": sourceBucket,
#                 "originAccessIdentityId": oai.ref,
#             },
#             "behaviors": [{"isDefaultBehavior": True}],
#         }
#     ],
#     alias_configuration={"acmCertRef": cert_arn, "names": [host_name]},
#     viewer_protocol_policy=ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
# )

        # Cloudfront12 = cloudfront.CloudFrontWebDistribution(self, "MyDistribution",
        #     origin_configs=[cloudfront.SourceConfiguration(
        #     s3_origin_source=cloudfront.S3OriginConfig(
        #         s3_bucket_source=bucket_website
        #     ),
        #     behaviors=[cloudfront.Behavior(is_default_behavior=True)]
        #         )
        #     ],default_root_object="index.html",viewer_protocol_policy=ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
        # )  

        

        # Cloudfront12 = cloudfront.CloudFrontWebDistribution(
        #     self,
        #     "MyDistribution",
        #     origin_configs=[
        #         cloudfront.SourceConfiguration(
        #             s3_origin_source=cloudfront.S3OriginConfig(
        #                 s3_bucket_source=bucket_website
        #             ),
        #             behaviors=[cloudfront.Behavior(is_default_behavior=True)]
        #         )
        #     ],alias_configuration=cloudfront.CustomOriginConfig(
        #         domain_name=dom_name,
        #         acm_cert_ref=cert_dns_val.certificate_arn,
        #         names=["www.shrirajchohan.com"],
        #         security_policy=cloudfront.SecurityPolicyProtocol.TLS_V1,
        #         ssl_method=cloudfront.SSLMethod.SNI
        #     ),
        #         )       


        #Alias Configuration

        # front_target = route53.RecordTarget.from_alias(target.CloudFrontTarget(Cloudfront12))

        # frond_r53_record = route53.AaaaRecord(self,'frontendAlias',
        #     zone=zone, target=front_target,record_name=record_name12)



            
            # CloudFrontTarget(Cloudfront)),
            # removal_policy=cdk.RemovalPolicy.DESTROY


        # s3_certificate = acm.Certificate(self, "Certificate",
        #     domain_name=dom_name,
        #     validation=acm.CertificateValidation.from_dns_multi_zone({ "www.shrirajchohan.com" : zone})),



     

        
        # cert_dns_val = acm.DnsValidatedCertificate(self,
        #     'DnsValidation',
        #     hosted_zone=zone,
        #     domain_name='www.shrirajchohan.com', region='us-east-1')
        

        # create the S3 bucket
        # bucket = s3.Bucket(
        #     self,
        #     "MyBucket",
        #     bucket_name="shrirajchohan.com"
        #     # website_configuration={
        #     #  "index_document": "index.html"
        #     # }
        # )

        # create a Route 53 hosted zone
        # hosted_zone = route53.HostedZone(
        #     self,
        #     "MyHostedZone",
        #     zone_name="shrirajchohan.com"
        # )


        # vpc = ec2.Vpc.from_lookup(self,"vpc",vpc_id=vpcID)

        # create the Route 53 alias record

 




            # Creates a distribution from an S3 bucket.

        # bucket_origin = origins.S3Origin(bucket_website),

        # imported_cert= cdk.Fn.import_value('RealCertificate')
        # print(imported_cert)

                
                # certificate=imported_cert,


                
                
                # allowed_methods=cloudfront.AllowedMethods.ALLOW_ALL,
                # viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                

        
        
        # cloudfront_distribution= cloudfront.Distribution(self, "myDist",
        #     default_behavior=cloudfront.BehaviorOptions(origin=origins.S3Origin(bucket_website)),
        #     domain_names=["www.shrirajchohan.com"],
        #     minimum_protocol_version=cloudfront.SecurityPolicyProtocol.TLS_V1,
        #     ssl_support_method=cloudfront.SSLMethod.SNI
        # )

        # alias_configuration=cloudfront.AliasConfiguration(
        #         acm_cert_ref=s3_certificate.certificate_arn,
        #         names=["shrirajchoha.com"]
        #     )

        # # Create an instance of the CloudFront distribution
        # distribution = cloudfront.CloudFrontWebDistribution(
        #     self,
        #     "MyDistribution",
        #     origin_configs=[
        #         cloudfront.SourceConfiguration(
        #             s3_origin_source=cloudfront.S3OriginConfig(
        #                 s3_bucket_source=bucket_website
        #             ),
        #             behaviors=[cloudfront.Behavior(is_default_behavior=True)]
        #         )
        #     ],
        #     alias_configuration=cloudfront.
        #     (
        #         acm_cert_ref=certificate.certificate_arn,
        #         names=["www.shrirajchohan.com"],
        #         security_policy=cloudfront.SecurityPolicyProtocol.TLS_V1,
        #         ssl_method=cloudfront.SSLMethod.SNI
        #     ),
        # )   

 

 




        # route53.ARecord(
        #     self,
        #     "MyAliasRecord",
        #     record_name="www",
        #     target=route53.RecordTarget.from_alias(
        #         route53.Bu(
        #             hosted_zone_id=hosted_zone.hosted_zone_id,
        #             dns_name=bucket.bucket_website_domain_name
        #         )
        #     ),
        #     zone=hosted_zone
        # )



        # # Create an S3 bucket
        # bucket = s3.Bucket(
        #     self,
        #     "MyBucket",
        #     bucket_name="shriraj2022",
        #     versioned=True,
        #     encryption=s3.BucketEncryption.S3_MANAGED
        # ),

        # # Create the Route 53 Hosted Zone
        # hosted_zone = route53.HostedZone(self, "MyHostedZone",
        #     zone_name="shriraj.com",
        # )

        # # Create the Route 53 Record Set that points to the S3 bucket
        # record_set = route53.ARecord(self, "MyRecordSet", zone=hosted_zone,
        #     record_name="www",
        #     target=route53.RecordTarget.from_alias(target.BucketWebsiteTarget)
        #     # target=route53.RecordTarget.from_alias(alias_target=bucket
        #         # route53.AliasRecordTarget(
        #         ,alias_target=bucket
        #     )
        #     # zone=hosted_zone
        # # )