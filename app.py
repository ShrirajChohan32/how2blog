#!/usr/bin/env python3
import aws_cdk as cdk
from blog.blog_stack import BlogStack

env_dev = cdk.Environment(account="account name",region="ap-southeast-2")

app = cdk.App()

BlogStack(app, "BlogStack",env=env_dev)

app.synth()


