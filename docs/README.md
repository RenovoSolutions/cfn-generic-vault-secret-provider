# Generic::Vault::Secret

A resource to handle creating Vault secrets.

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "Type" : "Generic::Vault::Secret",
    "Properties" : {
        "<a href="#secretpath" title="SecretPath">SecretPath</a>" : <i>String</i>,
        "<a href="#server" title="Server">Server</a>" : <i>String</i>,
        "<a href="#secretenginemountpath" title="SecretEngineMountPath">SecretEngineMountPath</a>" : <i>String</i>,
        "<a href="#token" title="Token">Token</a>" : <i>String</i>,
        "<a href="#secretlength" title="SecretLength">SecretLength</a>" : <i>Integer</i>,
    }
}
</pre>

### YAML

<pre>
Type: Generic::Vault::Secret
Properties:
    <a href="#secretpath" title="SecretPath">SecretPath</a>: <i>String</i>
    <a href="#server" title="Server">Server</a>: <i>String</i>
    <a href="#secretenginemountpath" title="SecretEngineMountPath">SecretEngineMountPath</a>: <i>String</i>
    <a href="#token" title="Token">Token</a>: <i>String</i>
    <a href="#secretlength" title="SecretLength">SecretLength</a>: <i>Integer</i>
</pre>

## Properties

#### SecretPath

Specify the secret path in Vault. This should be everything after the mount location in a path. For example `secret/some/path/to/somesecret` would be `some/path/to/somesecret`

_Required_: Yes

_Type_: String

_Update requires_: [Replacement](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement)

#### Server

The Vault server address. Like `https://vault.example.com/` for KV v2 secrets

_Required_: Yes

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### SecretEngineMountPath

The secret engine's mount path. For example KV v2 might be `secret`

_Required_: Yes

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Token

The Vault token to authorize to Vault with.

_Required_: Yes

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### SecretLength

The length of a randomly generated secret. Otherwise defaults to `32`

_Required_: No

_Type_: Integer

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

## Return Values

### Fn::GetAtt

The `Fn::GetAtt` intrinsic function returns a value for a specified attribute of this type. The following are the available attributes and sample return values.

For more information about using the `Fn::GetAtt` intrinsic function, see [Fn::GetAtt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html).

#### Version

The version of the secret.

#### SecretData

Optional property to define secret data directly. If left blank the secret will be randomly generated and the key will be `value`. Like: `{"data": {"value": "theSecretSecret"}}`

