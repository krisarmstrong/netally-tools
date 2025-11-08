#!/usr/bin/env python3
"""
Project Title: LinkRunnerRecovery

Recovers and updates MAC address, serial number, and option bits on a LinkRunner Pro/Duo device.

Writes commands to command.txt and reads results.txt on the device's drive, with cross-platform drive detection for Windows, Linux, and macOS.

Author: Kris Armstrong
"""
__version__ = "2.0.1"

import argparse
import logging
from logging.handlers import RotatingFileHandler
import re
import sys
from pathlib import Path
import os
import string
import time
from typing import List, Tuple, Optional

class Config:
    """Global configuration constants for LinkRunnerRecovery."""
    LOG_FILE: str = "linkrunner_recovery.log"
    ENCODING: str = "utf-8"
    COMMAND_FILE: str = "command.txt"
    RESULTS_FILE: str = "results.txt"
    VOLUME_LABEL: str = "LR"
    MARKER_FILE: str = "linkrunner.id"
    COMMAND_DELAY: float = 1.0

def setup_logging(verbose: bool, logfile: Optional[str] = None) -> None:
    """Configure logging with console and rotating file handler.

    Args:
        verbose: Enable DEBUG level logging to console if True.
        logfile: Path to log file, defaults to Config.LOG_FILE if unspecified.

    Raises:
        PermissionError: If log file cannot be written.
    """
    logger = logging.getLogger()
    level = logging.DEBUG if verbose else logging.INFO
    logger.setLevel(level)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
    logger.addHandler(console_handler)
    logfile = logfile or Config.LOG_FILE
    file_handler = RotatingFileHandler(logfile, maxBytes=10_000_000, backupCount=5)
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
    logger.addHandler(file_handler)

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed command-line arguments.

    Raises:
        SystemExit: If arguments are invalid.
    """
    parser = argparse.ArgumentParser(
        description="Recover and update LinkRunner Pro/Duo device settings.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--mac_address",
        required=True,
        help="MAC address (XX:XX:XX:XX:XX:XX, e.g., 00:11:22:33:44:55)"
    )
    parser.add_argument(
        "--serial_number",
        required=True,
        help="Serial number of the device"
    )
    parser.add_argument(
        "--opt_8021x",
        type=int,
        choices=[0, 1],
        default=0,
        help="802.1x option bit (0=disabled, 1=enabled)"
    )
    parser.add_argument(
        "--opt_reports",
        type=int,
        choices=[0, 1],
        default=0,
        help="Reports option bit (0=disabled, 1=enabled)"
    )
    parser.add_argument(
        "--opt_reflector",
        type=int,
        choices=[0, 1],
        default=0,
        help="Reflector option bit (0=disabled, 1=enabled)"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose console output"
    )
    parser.add_argument(
        "--logfile",
        help="Path to log file"
    )

    args = parser.parse_args()
    mac_pattern = re.compile(r"^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$")
    if not mac_pattern.match(args.mac_address):
        parser.error(f"Invalid MAC address format: {args.mac_address}")

    return args

def check_sensitive_data(device_path: Path) -> bool:
    """Check for sensitive data in command.txt before committing.

    Args:
        device_path: Path to the device drive.

    Returns:
        True if no sensitive data found, False otherwise.
    """
    sensitive_patterns = [r'api_key\s*=\s*["\'].+["\']', r'password\s*=\s*["\'].+["\']']
    command_file = device_path / Config.COMMAND_FILE
    if command_file.exists():
        try:
            content = command_file.read_text(encoding=Config.ENCODING)
            for pattern in sensitive_patterns:
                if re.search(pattern, content):
                    logging.warning(f"Potential sensitive data found in {command_file}")
                    return False
        except IOError as err:
            logging.error(f"Failed to read {command_file}: {err}")
            return False
    return True

def get_windows_drive() -> Path:
    """Get the drive letter for the LinkRunner volume on Windows.

    Returns:
        Path to the drive root (e.g., Path('G:/')).

    Raises:
        FileNotFoundError: If no LinkRunner drive is found.
    """
    logging.debug("Searching for LinkRunner drive on Windows")
    for drive_letter in string.ascii_uppercase:
        drive_path = Path(f"{drive_letter}:/")
        try:
            if drive_path.is_dir():
                if (drive_path / Config.MARKER_FILE).exists() or Config.VOLUME_LABEL in os.path.basename(str(drive_path)):
                    logging.info("Found LinkRunner drive at %s", drive_path)
                    return drive_path
        except OSError:
            continue
    logging.error("No LinkRunner drive found on Windows")
    raise FileNotFoundError("No LinkRunner drive found")

def get_linux_drive() -> Path:
    """Get the mount point for the LinkRunner volume on Linux.

    Returns:
        Path to the mount point (e.g., Path('/mnt/lr')).

    Raises:
        FileNotFoundError: If no LinkRunner drive is found.
    """
    logging.debug("Searching for LinkRunner drive on Linux")
    possible_mounts = ["/mnt", "/media"]
    for base in possible_mounts:
        base_path = Path(base)
        if not base_path.exists():
            continue
        for mount in base_path.iterdir():
            try:
                if mount.is_mount() and (
                    Config.VOLUME_LABEL in mount.name or (mount / Config.MARKER_FILE).exists()
                ):
                    logging.info("Found LinkRunner mount point at %s", mount)
                    return mount
            except OSError:
                continue
    logging.error("No LinkRunner drive found on Linux")
    raise FileNotFoundError("No LinkRunner drive found")

def get_macos_drive() -> Path:
    """Get the mount point for the LinkRunner volume on macOS.

    Returns:
        Path to the mount point (e.g., Path('/Volumes/LR')).

    Raises:
        FileNotFoundError: If no LinkRunner drive is found.
    """
    logging.debug("Searching for LinkRunner drive on macOS")
    volumes_path = Path("/Volumes")
    if not volumes_path.exists():
        logging.error("Volumes directory not found on macOS")
        raise FileNotFoundError("Volumes directory not found")
    for mount in volumes_path.iterdir():
        try:
            if mount.is_mount() and (
                Config.VOLUME_LABEL in mount.name or (mount / Config.MARKER_FILE).exists()
            ):
                logging.info("Found LinkRunner mount point at %s", mount)
                return mount
        except OSError:
            continue
    logging.error("No LinkRunner drive found on macOS")
    raise FileNotFoundError("No LinkRunner drive found")

def write_commands(
    device_path: Path,
    mac_address: str,
    serial_number: str,
    opt_8021x: int,
    opt_reports: int,
    opt_reflector: int
) -> List[Tuple[str, str]]:
    """Write commands one at a time to command.txt and read results.txt.

    Args:
        device_path: Path to the device drive or mount point.
        mac_address: MAC address to write.
        serial_number: Serial number to write.
        opt_8021x: 802.1x option bit (0 or 1).
        opt_reports: Reports option bit (0 or 1).
        opt_reflector: Reflector option bit (0 or 1).

    Returns:
        List of (command, result) tuples for each command.

    Raises:
        IOError: If file operations fail.
        RuntimeError: If a command fails based on results.txt.
    """
    command_path = device_path / Config.COMMAND_FILE
    results_path = device_path / Config.RESULTS_FILE

    commands = [
        f"MAC={mac_address}",
        f"SERIAL={serial_number}",
        f"OPT0_8021X={opt_8021x}",
        f"OPT1_REPORTS={opt_reports}",
        f"OPT2_REFLECTOR={opt_reflector}",
    ]

    results = []
    for command in commands:
        try:
            logging.debug("Writing command to %s: %s", command_path, command)
            with command_path.open("w", encoding=Config.ENCODING) as file:
                file.write(command + "\n")
            logging.info("Successfully wrote command to %s", command_path)
        except IOError as err:
            logging.error("Failed to write to %s: %s", command_path, err)
            raise

        time.sleep(Config.COMMAND_DELAY)

        try:
            logging.debug("Reading from %s", results_path)
            with results_path.open("r", encoding=Config.ENCODING) as file:
                result = file.read().strip()
            logging.info("Result for command '%s': %s", command, result)
            results.append((command, result))
            if result.startswith("ERROR"):
                logging.error("Command failed: %s, Result: %s", command, result)
                raise RuntimeError(f"Command failed: {command}, Result: {result}")
        except FileNotFoundError:
            logging.error("Results file not found after command '%s': %s", command, results_path)
            raise
        except IOError as err:
            logging.error("Failed to read %s: %s", results_path, err)
            raise

    return results

def main() -> int:
    """Recover and update LinkRunner Pro/Duo settings.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    try:
        args = parse_arguments()
        setup_logging(args.verbose, args.logfile)
        logging.info("Starting LinkRunner recovery for MAC: %s, Serial: %s", args.mac_address, args.serial_number)
        print(f"Processing MAC Address: {args.mac_address}, Serial Number: {args.serial_number}")

        system_os = sys.platform
        logging.debug("Detected OS: %s", system_os)
        if system_os.startswith("win32"):
            print("Operating System: Windows")
            device_path = get_windows_drive()
        elif system_os.startswith("linux"):
            print("Operating System: Linux")
            device_path = get_linux_drive()
        elif system_os.startswith("darwin"):
            print("Operating System: macOS")
            device_path = get_macos_drive()
        else:
            logging.error("Unsupported OS: %s", system_os)
            print(f"Error: Unsupported OS: {system_os}")
            return 1

        if not check_sensitive_data(device_path):
            logging.error("Aborted due to potential sensitive data")
            print("Error: Potential sensitive data detected in command.txt")
            return 1

        results = write_commands(
            device_path,
            args.mac_address,
            args.serial_number,
            args.opt_8021x,
            args.opt_reports,
            args.opt_reflector,
        )
        print("\nOperation Results:")
        for command, result in results:
            print(f"Command: {command}, Result: {result}")
        logging.info("Recovery completed successfully")
        return 0

    except FileNotFoundError as err:
        print(f"Error: {err}")
        logging.error("Recovery failed: %s", err)
        return 1
    except (IOError, RuntimeError) as err:
        print(f"Error: {err}")
        logging.error("Recovery failed: %s", err)
        return 1
    except KeyboardInterrupt:
        logging.info("Cancelled by user")
        return 0
    except Exception as err:
        print(f"Unexpected error: {err}")
        logging.error("Unexpected error: %s", err)
        return 1

if __name__ == "__main__":
    sys.exit(main())