# Generic::Vault::Secret

This repo implements a private custom CloudFormation resource using the CloudFormation Registry. The JSON schema, `generic-vault-secret.json`, includes the details about this resource and the resource handler code is included in `generic_vault_secret/handlers.py`. Some other code in this repo is auto generated. For example don't modify `models.py` by hand as any changes will be overwritten by the `cfn generate` or `cfn package` commands.

## Basics
- Install the [cfn cli tool and the python extension](https://github.com/aws-cloudformation/cloudformation-cli).
- Install the [SAM Cli](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- Make changes to the json schema file as needed
- Run `cfn generate` any time the json file changes
- Modify the `overrides.json` file to point to your actual Vault server and generate yourself a vault token to use from there. You'll need a properly scoped token for the secret you provide in the override.
- Run `sam local start-lambda` to start up the local lambda function and then run `cfn test` to run contract tests
- Kill the local lambda session
- Run `cfn submit` if contract tests succeed

## handlers.py

Implement CloudFormation resource here. Each function must always return a ProgressEvent.

```python
ProgressEvent(
    # Required
    # Must be one of OperationStatus.IN_PROGRESS, OperationStatus.FAILED, OperationStatus.SUCCESS
    status=OperationStatus.IN_PROGRESS,
    # Required on SUCCESS (except for LIST where resourceModels is required)
    # The current resource model after the operation; instance of ResourceModel class
    resourceModel=model,
    resourceModels=None,
    # Required on FAILED
    # Customer-facing message, displayed in e.g. CloudFormation stack events
    message="",
    # Required on FAILED: a HandlerErrorCode
    errorCode=HandlerErrorCode.InternalFailure,
    # Optional
    # Use to store any state between re-invocation via IN_PROGRESS
    callbackContext={},
    # Required on IN_PROGRESS
    # The number of seconds to delay before re-invocation
    callbackDelaySeconds=0,
)
```

Failures can be passed back to CloudFormation by either raising an exception from `cloudformation_cli_python_lib.exceptions`, or setting the ProgressEvent's `status` to `OperationStatus.FAILED` and `errorCode` to one of `cloudformation_cli_python_lib.HandlerErrorCode`. There is a static helper function, `ProgressEvent.failed`, for this common case.

## Resources

- [General Youtube Tutorial](https://www.youtube.com/watch?v=H91wF-_a4eI)
- [re:Invent 2020 talk](https://www.youtube.com/watch?v=qjtsuTVgrjs)
- [blog walkthrough](https://www.cloudar.be/awsblog/writing-an-aws-cloudformation-resource-provider-in-python-step-by-step/)
- [AWS Docs walkthrough](https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/resource-type-walkthrough.html)
- [AWS Blog walkthrough](https://aws.amazon.com/blogs/infrastructure-and-automation/using-python-to-create-aws-cloudformation-resource-providers/)
