# This suppresses about 80% of the deprecation warnings from python 3.7.
import warnings
import testinfra.utils.ansible_runner
import os
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

@pytest.fixture()
def AnsibleDefaults():
    with open("defaults/main.yml", 'r') as stream:
        return yaml.load(stream)

def test_socket(host):
    s = host.socket("tcp://0.0.0.0:389")
    assert s.is_listening

def test_service_chronyd(host):
    s = host.service("chronyd")
    assert s.is_enabled
    assert s.is_running

def test_service_firewalld(host):
    s = host.service("firewalld")
    assert s.is_enabled
    assert s.is_running

def test_service_ipa(host):
    s = host.service("ipa")
    assert s.is_enabled
    assert s.is_running

def test_ipa_created_user(host):
    cmd = "ipa user-find | grep hdfs"
    run = host.run(cmd)
    assert run.rc == 0
    assert "User login: hdfs" in run.stdout

def test_ipa_created_dnsrecord(host):
    cmd = "ipa dnsrecord-find example.com | grep host01"
    run = host.run(cmd)
    assert run.rc == 0
    assert "Record name: host01.example.com" in run.stdout