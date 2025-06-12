import os
import pytest
from unittest import mock
from azure.core.exceptions import ResourceNotFoundError

from entrypoint import main

@mock.patch("entrypoint.ResourceManagementClient")
@mock.patch("entrypoint.ClientSecretCredential")
def test_rg_exists(mock_cred, mock_client, monkeypatch, capsys):
    monkeypatch.setenv("INPUT_RESOURCE_GROUP", "existing-rg")
    monkeypatch.setenv("AZURE_CLIENT_ID", "fake")
    monkeypatch.setenv("AZURE_TENANT_ID", "fake")
    monkeypatch.setenv("AZURE_CLIENT_SECRET", "fake")
    monkeypatch.setenv("AZURE_SUBSCRIPTION_ID", "fake")

    mock_instance = mock.Mock()
    mock_client.return_value = mock_instance
    mock_instance.resource_groups.get.return_value = mock.Mock()

    main()

    out = capsys.readouterr().out
    assert "exists" in out

@mock.patch("entrypoint.ResourceManagementClient")
@mock.patch("entrypoint.ClientSecretCredential")
def test_rg_does_not_exist(mock_cred, mock_client, monkeypatch, capsys):
    monkeypatch.setenv("INPUT_RESOURCE_GROUP", "nonexistent-rg")
    monkeypatch.setenv("AZURE_CLIENT_ID", "fake")
    monkeypatch.setenv("AZURE_TENANT_ID", "fake")
    monkeypatch.setenv("AZURE_CLIENT_SECRET", "fake")
    monkeypatch.setenv("AZURE_SUBSCRIPTION_ID", "fake")

    mock_instance = mock.Mock()
    mock_client.return_value = mock_instance
    mock_instance.resource_groups.get.side_effect = ResourceNotFoundError("Not Found")

    main()

    out = capsys.readouterr().out
    assert "does NOT exist" in out