import subprocess
import os
import pytest
from unittest import mock
from azure.core.exceptions import ResourceNotFoundError

@mock.patch("entrypoint.ResourceManagementClient")
@mock.patch("entrypoint.ClientSecretCredential")
def test_rg_exists(mock_cred, mock_client, monkeypatch):
    monkeypatch.setenv("INPUT_RESOURCE_GROUP", "existing-rg")
    monkeypatch.setenv("AZURE_CLIENT_ID", "fake")
    monkeypatch.setenv("AZURE_TENANT_ID", "fake")
    monkeypatch.setenv("AZURE_CLIENT_SECRET", "fake")
    monkeypatch.setenv("AZURE_SUBSCRIPTION_ID", "fake")

    # Mock the client and its method
    mock_instance = mock.Mock()
    mock_client.return_value = mock_instance
    mock_instance.resource_groups.get.return_value = mock.Mock()

    result = subprocess.run(["python", "entrypoint.py"], capture_output=True, text=True)
    assert "exists" in result.stdout

@mock.patch("entrypoint.ResourceManagementClient")
@mock.patch("entrypoint.ClientSecretCredential")
def test_rg_does_not_exist(mock_cred, mock_client, monkeypatch):
    monkeypatch.setenv("INPUT_RESOURCE_GROUP", "nonexistent-rg")
    monkeypatch.setenv("AZURE_CLIENT_ID", "fake")
    monkeypatch.setenv("AZURE_TENANT_ID", "fake")
    monkeypatch.setenv("AZURE_CLIENT_SECRET", "fake")
    monkeypatch.setenv("AZURE_SUBSCRIPTION_ID", "fake")

    mock_instance = mock.Mock()
    mock_client.return_value = mock_instance
    mock_instance.resource_groups.get.side_effect = ResourceNotFoundError("Not Found")

    result = subprocess.run(["python", "entrypoint.py"], capture_output=True, text=True)
    assert "does NOT exist" in result.stdout
    assert result.returncode != 0