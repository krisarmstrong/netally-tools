#!/usr/bin/env python3
"""
Tests for LinkRunnerRecovery.
"""
import pytest
from pathlib import Path
from linkrunner_recovery import __version__, parse_arguments, check_sensitive_data, Config

@pytest.fixture
def tmp_device_path(tmp_path):
    """Create a temporary device path with command.txt and results.txt."""
    device_path = tmp_path / "device"
    device_path.mkdir()
    (device_path / Config.MARKER_FILE).touch()
    return device_path

def test_version() -> None:
    """Test version format."""
    assert __version__ == "2.0.1"

def test_parse_arguments_valid():
    """Test parsing valid command-line arguments."""
    args = parse_arguments(["--mac_address", "00:11:22:33:44:55", "--serial_number", "ABC123"])
    assert args.mac_address == "00:11:22:33:44:55"
    assert args.serial_number == "ABC123"
    assert args.opt_8021x == 0
    assert args.opt_reports == 0
    assert args.opt_reflector == 0

def test_parse_arguments_invalid_mac():
    """Test parsing invalid MAC address."""
    with pytest.raises(SystemExit):
        parse_arguments(["--mac_address", "invalid", "--serial_number", "ABC123"])

def test_check_sensitive_data_clean(tmp_device_path):
    """Test checking for sensitive data in a clean command.txt."""
    command_file = tmp_device_path / Config.COMMAND_FILE
    command_file.write_text("MAC=00:11:22:33:44:55\n", encoding=Config.ENCODING)
    assert check_sensitive_data(tmp_device_path) is True

def test_check_sensitive_data_sensitive(tmp_device_path):
    """Test checking for sensitive data in command.txt."""
    command_file = tmp_device_path / Config.COMMAND_FILE
    command_file.write_text("api_key='secret123'\n", encoding=Config.ENCODING)
    assert check_sensitive_data(tmp_device_path) is False