#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `awssh` package."""

import pytest
import mock
import os
import boto3
import json
import sys
import botocore

from click.testing import CliRunner

from awssh import awssh


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


@pytest.fixture
def ec2_describe_success():
    def mock_api(self, serv, arg, **kwargs):
        if serv == 'DescribeInstances':
            return {'Reservations': [
                {'Instances': [
                    {
                        'State': {'Code': 16},
                        'Tags': [
                            {'Key': 'Name', 'Value': 'Name1'},
                            {'Key': 'Bunk', 'Value': 'Ugh'}
                        ],
                        'PublicIpAddress': '1.1.1.1',
                        'PrivateIpAddress': '2.2.2.2'
                    },
                    {
                        'State': {'Code': 16},
                        'Tags': [
                            {'Key': 'Name', 'Value': 'Name2'},
                            {'Key': 'Bunk', 'Value': 'Ugh'}
                        ],
                        'PublicIpAddress': '3.3.3.3',
                        'PrivateIpAddress': '4.4.4.4'
                    },
                ]},
                {'Instances': [
                    {
                        'State': {'Code': 3},
                        'Tags': [
                            {'Key': 'Name', 'Value': 'Name3'},
                            {'Key': 'Bunk', 'Value': 'Ugh'}
                        ],
                        'PublicIpAddress': '5.5.5.5',
                        'PrivateIpAddress': '6.6.6.6'
                    },
                    {
                        'State': {'Code': 16},
                        'Tags': [
                            {'Key': 'NameNope', 'Value': 'Name4'},
                            {'Key': 'Bunk', 'Value': 'Ugh'}
                        ],
                        'PublicIpAddress': '7.7.7.7',
                        'PrivateIpAddress': '8.8.8.8'
                    },
                ]},
                {'Instances': [
                    {
                        'State': {'Code': 16},
                        'Tags': [
                            {'Key': 'Name', 'Value': 'Name5'},
                            {'Key': 'Bunk', 'Value': 'Ugh'}
                        ],
                        'PublicIpAddress': '9.9.9.9',
                        'PrivateIpAddress': '10.10.10.10'
                    },
                    {
                        'State': {'Code': 16},
                        'Tags': [
                            {'Key': 'Name', 'Value': 'NoIp'},
                            {'Key': 'Bunk', 'Value': 'Ugh'}
                        ],
                        'PublicIpAddress': '',
                        'PrivateIpAddress': ''
                    },
                ]},
            ]}
    return mock_api


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    # runner = CliRunner()
    # result = runner.invoke(awssh.cli.main)
    # assert result.exit_code == 0
    # # assert 'awssh.cli.main' in result.output
    # help_result = runner.invoke(awssh.cli.main, ['--help'])
    # assert help_result.exit_code == 0
    # assert '--help' in help_result.output


@mock.patch('awssh.awssh.boto3')
def test_awssh_client(my_mock):
    return
    awh = awssh.Awssh()

    awh.client("swf")
    my_mock.client.assert_called_with("swf", region_name='us-west-2')

    os.environ['AWS_DEFAULT_REGION'] = 'iraq-west-1'

    awh = awssh.Awssh()
    awh.client('rds')
    my_mock.client.assert_called_with("rds", region_name='iraq-west-1')

    awssh.Awssh._clients = {}
    awssh.Awssh._region = None
    del os.environ['AWS_DEFAULT_REGION']

    awssh.Awssh._clients = {}
    awssh.Awssh._region = None
    awh = awssh.Awssh(region='us-east-2')

    awh.client('sns')
    my_mock.client.assert_called_with('sns', region_name='us-east-2')

    my_mock.client.return_value = False
    with pytest.raises(Exception) as exe:
        awh.client('sqs')
    assert "Could not create" in str(exe.value)


    my_mock.client.side_effect = Exception("Test")
    with pytest.raises(Exception) as exe:
        awh.client("sts")
    assert "Unable to connect" in str(exe.value)


    awssh.Awssh._clients = {}
    awssh.Awssh._region = None


def test_return_ec2_servers(ec2_describe_success):
    return
    with mock.patch('botocore.client.BaseClient._make_api_call', new=ec2_describe_success):
        a = awssh.Awssh()

        res = a.return_ec2_servers()

        test_str = json.dumps(res)

        assert '5.5.5.5' not in test_str
        assert 'NoIp' not in test_str
        assert 'Name5' in test_str
        assert '9.9.9.9' in test_str


def __test_return_ec2_servers(monkeypatch):
    return
    mock_describe_instances(monkeypatch)
    awsh = awssh.Awssh()

    servers = awsh.return_ec2_servers()

    servers_json = json.dumps(servers)

    assert '3.3.3.3' in servers_json
    assert '9.9.9.9' in servers_json
    assert '5.5.5.5' not in servers_json

    monkeypatch.undo()
    awssh.Awssh._clients = {}

    # mock_describe_instances_exception(monkeypatch)

    # awsh.return_ec2_servers()
    # print(sys.stdout)


def mock_describe_instances(monkeypatch):

    class ec2_mock():

        def __init__(self, name):
            self.name = name

        def describe_instances(self):
            return {
                'Reservations': [
                    {'Instances': [
                        {
                            'State': {'Code': 16},
                            'Tags': [
                                {'Key': 'Name', 'Value': 'server1'},
                                {'Key': 'NotName', 'Value': 'Bunk'},
                            ],
                            'PublicIpAddress': '0.0.0.0',
                            'PrivateIpAddress': '1.1.1.1',
                        },
                        {
                            'State': {'Code': 16},
                            'Tags': [
                                {'Key': 'Name', 'Value': 'server2'},
                                {'Key': 'NotName', 'Value': 'Bunk'},
                            ],
                            'PublicIpAddress': '3.3.3.3',
                            'PrivateIpAddress': '4.4.4.4',
                        }
                    ]
                    },
                    {'Instances': [
                        {
                            'State': {'Code': 3},
                            'Tags': [
                                {'Key': 'Name', 'Value': 'server3'},
                                {'Key': 'NotName', 'Value': 'Bunk'},
                            ],
                            'PublicIpAddress': '5.5.5.5',
                            'PrivateIpAddress': '6.6.6.6',
                        },
                        {
                            'State': {'Code': 16},
                            'Tags': [
                                {'Key': 'Name', 'Value': 'server4'},
                                {'Key': 'NotName', 'Value': 'Bunk'},
                            ],
                            'PublicIpAddress': '7.7.7.7',
                            'PrivateIpAddress': '8.8.8.8',
                        }
                    ]
                    },
                    {'Instances': [
                        {
                            'State': {'Code': 16},
                            'Tags': [
                                {'Key': 'NotName', 'Value': 'Bunk'},
                            ],
                            'PublicIpAddress': '9.9.9.9',
                            'PrivateIpAddress': '10.10.10.10',
                        },
                        {
                            'State': {'Code': 16},
                            'Tags': [
                                {'Key': 'Name', 'Value': 'server4'},
                                {'Key': 'NotName', 'Value': 'Bunk'},
                            ],
                            'PublicIpAddress': '11.11.11.11',
                            'PrivateIpAddress': '12.12.12.12',
                        }
                    ]
                    }
                ]
            }

    def boto_client_mock(service, **kwargs):
        return ec2_mock(service)

    monkeypatch.setattr(boto3, 'client', boto_client_mock)


def mock_describe_instances_exception(monkeypatch):

    class ec2_mock():

        def __init__(self, name):
            self.name = name

        def describe_instances(self):
            raise Exception("Connection Error")

    def boto_client_mock(service, **kwargs):
        return ec2_mock(service)

    monkeypatch.setattr(boto3, 'client', boto_client_mock)
