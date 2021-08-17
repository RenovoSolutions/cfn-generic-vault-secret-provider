import logging
from typing import Any, MutableMapping, Optional

from cloudformation_cli_python_lib import (
    Action,
    HandlerErrorCode,
    OperationStatus,
    ProgressEvent,
    Resource,
    SessionProxy,
    exceptions,
    identifier_utils,
)

from .models import ResourceHandlerRequest, ResourceModel

from secrets import token_urlsafe
from .vault_lib import VaultLib
import json

# Use this logger to forward log messages to CloudWatch Logs.
LOG = logging.getLogger(__name__)
LOG.setLevel('INFO')

TYPE_NAME = "Generic::Vault::Secret"

resource = Resource(TYPE_NAME, ResourceModel)
test_entrypoint = resource.test_entrypoint

@resource.handler(Action.CREATE)
def create_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    type_configuration = request.typeConfiguration
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=model,
    )

    LOG.info('Running creation handler.')

    try:
        # If no secret is given then generate one.
        if model.SecretData == None or model.SecretData == '':
            if model.SecretLength == 0:
                model.SecretLength = 32

            model.SecretData = f"'value={token_urlsafe(model.SecretLength)}'"

        LOG.info(type_configuration)

        vault = VaultLib(
            model,
            type_configuration.VaultConnection.Server,
            type_configuration.VaultConnection.Token,
            LOG
        )

        response = vault.write_secret(model.SecretData)

        model.Version = response.json()["data"]["version"]

        progress.status = OperationStatus.SUCCESS
    except Exception as e:
        # exceptions module lets CloudFormation know the type of failure that occurred
        raise exceptions.InternalFailure(e)
        # this can also be done by returning a failed progress event
        # return ProgressEvent.failed(HandlerErrorCode.InternalFailure, f"was not expecting type {e}")

    return read_handler(session, request, callback_context)

@resource.handler(Action.DELETE)
def delete_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    type_configuration = request.typeConfiguration
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=None,
    )

    LOG.info('Running deletion handler.')

    try:
        vault = VaultLib(
            model,
            type_configuration.VaultConnection.Server,
            type_configuration.VaultConnection.Token,
            LOG
        )

        response = vault.read_secret_version(model.Version)
        if response.status_code == 404 and response.json()['data']['data'] == None:
            return ProgressEvent.failed(HandlerErrorCode.NotFound, f"secret {model.SecretPath} version {model.Version} does not exist so it can't be deleted")

        vault.delete_secret_version(model.Version)

        progress.status = OperationStatus.SUCCESS

        return progress
    except Exception as e:
        # exceptions module lets CloudFormation know the type of failure that occurred
        raise exceptions.InternalFailure(e)
        # this can also be done by returning a failed progress event
        # return ProgressEvent.failed(HandlerErrorCode.InternalFailure, f"was not expecting type {e}")

@resource.handler(Action.READ)
def read_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    type_configuration = request.typeConfiguration

    LOG.info(f'Running read handler.')

    try:
        vault = VaultLib(
            model,
            type_configuration.VaultConnection.Server,
            type_configuration.VaultConnection.Token,
            LOG
        )

        response = vault.read_secret_version(model.Version)

        # 404 is a valid Vault response for a secret that has been deleted or destroy
        # We can identify this with response data that has null data for the data key
        # null returns as None in python
        if response.status_code == 404 and response.json()['data']['data'] == None:
            return ProgressEvent.failed(HandlerErrorCode.NotFound, f"secret {model.SecretPath} version {model.Version} does not exist")
        else:
            model.SecretData = response.json()['data']['data']
            return ProgressEvent(
                status=OperationStatus.SUCCESS,
                resourceModel=model,
            )
    except Exception as e:
        # exceptions module lets CloudFormation know the type of failure that occurred
        raise exceptions.InternalFailure(e)
        # this can also be done by returning a failed progress event
        # return ProgressEvent.failed(HandlerErrorCode.InternalFailure, f"was not expecting type {e}")
