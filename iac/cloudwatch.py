"""
Troposphere template: Cloudwatch demonstration for localstack
"""

from troposphere import Template, Ref
from troposphere.logs import LogGroup, LogStream

t = Template()
t.set_description("LocalStack CloudWatch Logs setup")

# Log group
log_group = t.add_resource(LogGroup(
    "DemoLogGroup",
    LogGroupName="cloudgrindset2026-logs",
    RetentionInDays=14  # Keep logs for 2 weeks
))

# Log stream
log_stream = t.add_resource(LogStream(
    "DemoLogStream",
    LogGroupName=Ref(log_group),
    LogStreamName="demo-stream"
))

print(t.to_yaml())
