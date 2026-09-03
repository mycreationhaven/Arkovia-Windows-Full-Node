# Verify a download and understand the tests

[Back to README](../README.md)

## Verify the downloaded ZIP

Download the ZIP and its matching `.zip.sha256` attachment from the same release. Open PowerShell in the download directory and run:

```powershell
Get-FileHash -Algorithm SHA256 .\Arkovia-Full-Node-1.13.1-Windows-x64.zip
```

Compare the entire displayed hash with the value in the `.sha256` file or release notes. Letter case does not matter. If they differ, do not use that download; verify the release source and download it again. A checksum detects changed bytes but is not a code-signing certificate or an independent security audit.

The package also includes `SHA256SUMS.txt` covering individual files as built. Editing a configuration file intentionally changes its checksum. The checksum list does not list itself.

## What is checked

| Check | Meaning |
|---|---|
| Pinned source commit | Build uses the stated Arkovia source revision |
| Compilation | Java core compiles for Java 17 |
| Cryptography suite | Seven existing source tests complete successfully |
| Runtime archive hash | Bundled Java matches the pinned publisher archive |
| AMD64 executable header | Bundled `java.exe` is a Windows x64 binary |
| Original genesis comparison | Distributed genesis files match source bytes |
| Genesis import | A fresh disposable node imports the original accounts |
| Genesis ID | Expected block ID is `10203308059164672611` |
| Local API | Reports Arkovia 1.13.1, mainnet, full-node mode, and API proxy disabled |
| Wallet | Local wallet responds with HTTP 200 and HTML |
| Shutdown | Test closes the database cleanly |
| ZIP CRC check | Created archive passes `testzip()` |
| Empty log directory | The final ZIP contains `logs/` and extraction creates it |
| File logger | Startup creates `logs/nxt.0.log` without a FileHandler initialization warning |

`BUILD-INFO.json` records whether the bundled Windows runtime was executed for the specific build. Inspect the release's Actions log for workflow success. The startup test overrides offline mode only in its isolated test process. Distributed settings still enable normal peer connections.

## What remains outside those checks

- Connection to current live bootstrap peers and complete mainnet synchronization.
- Manual double-click behavior, every Windows edition, and every security-software configuration.
- Full consensus/security auditing, wallet usability testing, and every blockchain feature.
- Exhaustive dependency review or guaranteed availability of historical prunable data.
- Windows installer signing or Windows service installation; neither is provided.

The initial local package was tested on Linux. Automated Windows release builds improve runtime coverage; they do not retroactively change the tests performed on that original ZIP. Release builds include the expanded documentation and build evidence and therefore have their own checksums.

## Genesis provenance

The original mainnet genesis file contains 83,270 account balances totaling **99,999,999,999,954,968 atomic units**, or **999,999,999.99954968 ARKOS** at eight decimal places. The packaging process does not round or change that total. Consensus and genesis remain controlled by the source blockchain project.
