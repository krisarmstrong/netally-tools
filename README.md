# NetAlly Tools

[![CI](https://github.com/krisarmstrong/netally-tools/workflows/CI/badge.svg)](https://github.com/krisarmstrong/netally-tools/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Comprehensive toolkit for NetAlly hardware devices including LinkRunner, AirCheck, and AirMapper.

## Features

### LinkRunner Tools
- MAC address recovery and update
- Serial number management
- Option bits configuration
- Device recovery utilities

### AirCheck Tools
- Profile decryption
- Configuration management
- Security section processing

### Related Tools
- **airmapper-json-parser** - Separate tool for AirMapper JSON processing (kept as standalone project)

## Installation

```bash
pip install netally-tools
```

## Usage

### LinkRunner Recovery
```bash
netally linkrunner recover --mac <mac> --serial <serial>
```

### AirCheck Profile Decryption
```bash
netally aircheck decrypt --profile <profile.acg2>
```

## Project Structure

```
netally-tools/
├── src/netally_tools/
│   ├── linkrunner/      # LinkRunner recovery tools
│   ├── aircheck/        # AirCheck profile tools
│   └── common/          # Shared utilities
├── tests/
├── docs/
│   ├── LINKRUNNER.md   # LinkRunner documentation
│   └── AIRCHECK.md     # AirCheck documentation
└── README.md
```

## Documentation

- [LinkRunner Tools](docs/LINKRUNNER.md)
- [AirCheck Tools](docs/AIRCHECK.md)

## License

MIT License

---

Consolidated from:
- linkrunner-recovery
- aircheck-profile-decrypter

Related projects:
- airmapper-json-parser (separate, for JSON processing)
