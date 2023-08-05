"""Core classes for compsinig AWS Cloud Formation Stacks."""

class BaseAWSObject(object):
    """Base class to represent an object in AWS Cloud Formation."""
    pass


class Resource(BaseAWSObject):
    """Base class to represent an AWS CFN resource, plus other low level primitives."""
    pass