#!/usr/bin/env python3

import aws_cdk as cdk

from blog.blog_stack import BlogStack


app = cdk.App()
BlogStack(app, "blog")

app.synth()
