# check-resource-group/entrypoint.py
import os
import sys
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.core.exceptions import HttpResponseError
from azure.core.exceptions import ResourceNotFoundError


def set_output(name, value):
    output_file = os.environ.get("GITHUB_OUTPUT")
    if output_file:
        with open(output_file, "a") as f:
            f.write(f"{name}={value}\n")
    else:
        print(f"::set-output name={name}::{value}")  # fallback (deprecated)


def main(client=None):
    resource_group = os.environ.get("INPUT_RESOURCE_GROUP")
    subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")

    if not client:
        credentials = ClientSecretCredential(
            tenant_id=os.environ["AZURE_TENANT_ID"],
            client_id=os.environ["AZURE_CLIENT_ID"],
            client_secret=os.environ["AZURE_CLIENT_SECRET"]
        )
        client = ResourceManagementClient(credentials, subscription_id)

    try:
        client.resource_groups.get(resource_group)
        print(f"Resource group '{resource_group}' exists.")
        set_output("rg-exists", "true")
    except ResourceNotFoundError:
        print(f"Resource group '{resource_group}' does NOT exist.")
        set_output("rg-exists", "false")
    except HttpResponseError as e:
        # Still handle other Azure-related HTTP errors
        print(f"Unexpected Azure error: {e.message}")
        raise


if __name__ == "__main__":
    main()