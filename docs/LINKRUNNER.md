# LinkRunnerRecovery

Recovers and updates MAC address, serial number, and option bits on a LinkRunner Pro/Duo device.

## Installation

```bash
git clone https://github.com/krisarmstrong/linkrunner-recovery
cd linkrunner-recovery
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
python linkrunner_recovery.py --mac_address 00:11:22:33:44:55 --serial_number ABC123 --verbose
```

- `--mac_address`: MAC address (XX:XX:XX:XX:XX:XX, e.g., 00:11:22:33:44:55).
- `--serial_number`: Serial number of the device.
- `--opt_8021x`: 802.1x option bit (0=disabled, 1=enabled, default: 0).
- `--opt_reports`: Reports option bit (0=disabled, 1=enabled, default: 0).
- `--opt_reflector`: Reflector option bit (0=disabled, 1=enabled, default: 0).
- `--verbose`: Enable verbose logging.
- `--logfile`: Log file path (default: linkrunner_recovery.log).

## Files

- `linkrunner_recovery.py`: Main script.
- `version_bumper.py`: Version management tool.
- `tests/test_linkrunner_recovery.py`: Pytest suite.
- `requirements.txt`: Dependencies.
- `CHANGELOG.md`: Version history.
- `LICENSE`: MIT License.
- `CONTRIBUTING.md`: Contribution guidelines.
- `CODE_OF_CONDUCT.md`: Contributor Covenant.

## GitHub Setup

```bash
gh repo create linkrunner-recovery --public --source=. --remote=origin
git init
git add .
git commit -m "Initial commit: LinkRunnerRecovery v2.0.1"
git tag v2.0.1
git push origin main --tags
```

## Notes

- **Drive Detection**: Requires a mounted device with volume label “LR” or `linkrunner.id` file.
- **Testing**: Tests cover argument parsing and sensitive data checks; physical device testing requires a LinkRunner Pro/Duo.

## Contributing

See CONTRIBUTING.md for details.

## License

MIT License. See LICENSE for details.