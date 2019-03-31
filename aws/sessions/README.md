
### AWS Session Provider

This is a set of libraries designed to be able to provide a boto3 session to a python code in an scenario where we want to be able to run it either locally (design/development phase) or directly from amazon using IAM Role on an instance.
The class CredentialValidator has 2 abstract methods to ensure that all inherited objects has the same arguments, no matter if is provided by an aws profile or an iam role. At this point the library accepts "credential" as a string and analizes it fo find  "arn:" in order to choose if it is going to try the validation using the provided arn for the iam role or an aws profile.

