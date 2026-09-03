# Arkovia Windows Full Node

Run an **Arkovia mainnet full node on Windows x64** with a bundled Java runtime, a browser wallet, and double-click startup tools.

A full node downloads and independently validates the blockchain. This package uses the original Arkovia genesis data and does not change the blockchain's consensus rules. **ARKOS** is the native currency; some internal filenames and API fields retain NXT-compatible names.

**[Download the Windows package →](https://github.com/mycreationhaven/Arkovia-Windows-Full-Node/releases)** · **[Installation guide](docs/INSTALLATION.md)** · **[Troubleshooting](docs/TROUBLESHOOTING.md)**

## Start here

1. Open **[Releases](https://github.com/mycreationhaven/Arkovia-Windows-Full-Node/releases)** and expand **Assets** on the release you want.
2. Download **`Arkovia-Full-Node-1.13.1-Windows-x64.zip`**. The automatically generated **Source code** downloads are for developers and do not contain the assembled node.
3. Right-click the downloaded ZIP, choose **Extract All**, and extract it to a writable folder such as `C:\Arkovia-Node`.
4. Open the extracted folder containing `Start-Arkovia.bat`. Double-click it and leave the console open.
5. Wait for **`Arkovia server 1.13.1 started successfully.`** First startup imports the genesis accounts before normal use.
6. Double-click **`Open-Wallet.bat`**, or open **http://127.0.0.1:4876/** in a browser on the same computer.
7. Allow the blockchain to synchronize. Confirm connected peers and compare the height with a trusted live Arkovia node before relying on the displayed balance or transaction status.

If no release is listed yet, check the **[Windows build](https://github.com/mycreationhaven/Arkovia-Windows-Full-Node/actions/workflows/windows-release.yml)**. A download is published only after the build and checks succeed.

## What you need

| Item | Guidance |
|---|---|
| Operating system | Windows 10/11 on an Intel or AMD 64-bit PC; other Windows editions have not been established as supported here |
| Memory | At least 4 GB system RAM recommended; the launcher permits a maximum 2 GB Java heap |
| Storage | Room for the extracted package plus the growing blockchain database; an SSD is recommended |
| Connection | Internet access to Arkovia peers; download time depends on chain size and connectivity |
| Java | Included in the release ZIP; no separate Java installation needed |
| Administrator rights | Not needed for routine startup in a writable folder; firewall changes may require them |

The recommended Windows versions are operating guidance, not a claim of manual testing on every edition. Windows on ARM and 32-bit Windows are not targets for this x64 package.

## Included in the download

| File or folder | Purpose |
|---|---|
| `Start-Arkovia.bat` | Starts the full node with the bundled Java runtime |
| `Open-Wallet.bat` | Opens the local wallet in your default browser |
| `START-HERE.txt` | Short instructions that work without opening GitHub |
| `arkovia.jar` | Compiled Arkovia node |
| `jre/` | Windows x64 Eclipse Temurin Java runtime and its notices |
| `lib/`, `html/` | Node dependencies and browser wallet |
| `conf/nxt.properties` | Editable settings for this installation |
| `conf/data/` | Original genesis files; preserve these unchanged |
| `docs/` | Installation, operation, configuration, backup, troubleshooting and build guides |
| `BUILD-INFO.json`, `verification/` | Source/runtime provenance and results from this build |
| `SHA256SUMS.txt` | Individual packaged-file SHA-256 checksums |
| `Arkovia-Source-52172c5.zip` | Exact corresponding blockchain source and original notices |
| `nxt_db/`, `logs/` | Created/used locally for the blockchain database and logs |

## Everyday use

**Start:** run `Start-Arkovia.bat` from the same extracted folder each time. Keep the console open. A computer that is asleep or shut down cannot keep the node running.

**Stop:** press **Ctrl+C once** in the node console. Let the database finish shutting down and wait for **`Arkovia server 1.13.1 stopped.`** If Windows then asks whether to terminate the batch job, it is safe to answer after that message.

**Restart:** run the same launcher again. The saved database resumes synchronization; a new download is not required just because you closed the wallet browser.

**Update or back up:** stop the node first. Follow the [backup and update guide](docs/BACKUP-AND-UPDATES.md); never overwrite a running installation.

## Network settings

| Setting | Default |
|---|---|
| Network | Arkovia mainnet |
| Node mode | Full node; light-client and API-proxy modes disabled |
| Peer connections | TCP **4874** |
| Wallet/API | **http://127.0.0.1:4876/**, local computer only |
| Bootstrap peers | `147.93.138.255:4874`, `217.216.64.226:4874` |

Bootstrap addresses come from the pinned blockchain source's `conf/nxt.properties.txt`; their current availability is not guaranteed. Outbound sync generally does not need router port forwarding. To accept inbound peers, see [configuration](docs/CONFIGURATION.md). Keep the wallet/API bound to localhost.

## Verification and limitations

The original package passed Java compilation, seven cryptography tests, genesis import, local wallet/API startup and clean shutdown on Linux. The release workflow additionally runs the compiled node using the **bundled Windows x64 runtime** on a Windows runner before publishing. Check each release's `BUILD-INFO.json`, logs, and Actions result for that particular build.

The automated startup check runs offline with a separate disposable database. **Live-network synchronization is not verified by that check.** It also does not automate a person's double-click interaction with the batch launcher. The package contains no pre-synchronized database, does not start forging automatically, and is not a signed installer or a Windows service. No account secret is required to start or synchronize a node.

## Guides

| I want to… | Read |
|---|---|
| Install and start my first node | [Installation](docs/INSTALLATION.md) |
| Understand syncing and daily use | [Operation and synchronization](docs/OPERATING.md) |
| Change settings or allow inbound peers | [Configuration](docs/CONFIGURATION.md) |
| Protect my data or install an update | [Backups and updates](docs/BACKUP-AND-UPDATES.md) |
| Fix startup or connection problems | [Troubleshooting](docs/TROUBLESHOOTING.md) |
| Rebuild or publish a release | [Build and release](docs/BUILDING.md) |
| Understand package verification | [Verification](docs/VERIFICATION.md) |

## Source and licensing

Blockchain source: **[mycreationhaven/Arkovia-Blockchain](https://github.com/mycreationhaven/Arkovia-Blockchain)**, pinned to commit **[`52172c5079dc85e643a566b2cbeccfa5320a7a3a`](https://github.com/mycreationhaven/Arkovia-Blockchain/tree/52172c5079dc85e643a566b2cbeccfa5320a7a3a)**, application version **1.13.1**.

This repository maintains Windows packaging, launchers, documentation and build automation. The blockchain retains its original [LICENSE.txt](LICENSE.txt), [AUTHORS.txt](AUTHORS.txt), and [third-party notices](3RD-PARTY-LICENSES.txt). Java and bundled dependencies retain their own notices. Packaging does not replace those terms with another license.

For help, [open an issue](https://github.com/mycreationhaven/Arkovia-Windows-Full-Node/issues) with the version, Windows edition and relevant error text. Remove secrets and personal information from anything you post. Do not post wallet secret phrases, private keys, passwords, or full database files.
