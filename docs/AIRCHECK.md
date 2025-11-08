# AirCheck Profile Decrypter (Cleaned)

A cleaned and organized version of legacy utilities for decrypting the **security** section of NetAlly/Fluke **AirCheck** profile files (`.ACP`).

> ⚠️ **Legal & Ethical Notice**  
> Use only on profiles you own/have rights to test. Some sample files are provided for interoperability research.

## Repository Layout
```
src/tools/                 # Buildable legacy tools (C++)
archive/                   # Older or alternative implementations
examples/                  # Sample .ACP and text outputs
certs/                     # Any sample certificates (do NOT use in production)
tests/                     # Future unit/integration tests
.github/workflows/         # CI (CTest) placeholder
```

## Build (CMake)
```bash
mkdir -p build && cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
cmake --build . --parallel
ctest --output-on-failure
```

Two executables are produced (names match legacy sources):
- `ProDecrypt_v103`
- `kll_decrypt_ack_security`

> Note: These are original research tools from ~2011. They build as-is with C++17 flags; code is intentionally left close to original. Modernization recommendations are below.

### Building with Tests
GoogleTest-based unit tests are enabled when configuring with `-DBUILD_TESTING=ON` (default). The first configure step downloads GoogleTest via CMake's `FetchContent`, so ensure outbound network access is allowed. If you need an offline build, configure with `-DBUILD_TESTING=OFF`.

## Usage (Examples)
These tools historically accept an input `.ACP` and print decrypted security parameters. See the original comments in each source for expected args. Example patterns:

```bash
# Example (if tool supports -i/-o flags, see source header):
./ProDecrypt_v103 -i ../examples/default_encrypted.ACP -o out.txt

# Some versions embed test vectors and run with no args:
./kll_decrypt_ack_security
```

If a program prints usage or fails to parse, check the top-of-file comments for exact syntax; the legacy code predates standardized flags.

## Security Considerations
- Do **not** commit real customer profiles, secrets, or private keys.
- The included `certs/` content is for testing only.
- Prefer vetted crypto libraries (OpenSSL, libsodium) for any new work.

## Modernization Roadmap
1. **Refactor into a library + CLI**  
   - Extract AES/decrypt logic into `libaircheck` with clear APIs.  
   - New CLI (`acp-decrypt`) using `cxxopts`/`CLI11` with proper flags, stdin/stdout defaults.

2. **Memory safety & input validation**  
   - Replace raw buffers with `std::vector<uint8_t>`/`std::array`.  
   - Validate lengths, bounds, and hex parsing; return `std::expected` or exceptions with precise error codes.

3. **Testing**  
   - Add GoogleTest tests comparing decrypted outputs against golden files in `examples/`.  
   - `ctest` target should run quick vector tests and a few ACP fixtures.

4. **Portability & Tooling**  
   - Add CI (GitHub Actions) for Linux/macOS/Windows builds and tests.  
   - Add `clang-tidy` and `cppcheck` configs; enable `-fsanitize=address,undefined` in a `SANITIZE=ON` build.

5. **Documentation**  
   - Expand this README with exact CLI syntax for each legacy tool.  
   - Add a `docs/` folder with format specs discovered from ACP parsing.

## Contributing
PRs that move toward a safe, testable, library-first design are welcome. Keep legacy tools in `archive/` once superseded.

## License
See `LICENSE` (inherited from original project).
