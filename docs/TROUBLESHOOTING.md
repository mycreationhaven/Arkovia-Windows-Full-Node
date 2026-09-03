# Troubleshooting

[Back to README](../README.md)

| What you see | What to do |
|---|---|
| “Bundled Java is missing” | Extract the complete full-node ZIP. Confirm `jre/bin/java.exe` is beside the expected node files. The GitHub source-only ZIP is not the ready-to-run download. |
| Window closes or startup fails | Run `Start-Arkovia.bat` from Command Prompt to read the error, and inspect `logs/nxt.0.log`. Keep the exact message. |
| Java architecture/unsupported application error | Confirm this is an Intel/AMD 64-bit Windows PC and that the download was fully extracted. This package targets x64, not 32-bit Windows. |
| Browser says connection refused | Wait for the successful startup message. Confirm the console is still running and use `http://127.0.0.1:4876/` on the same PC. |
| Address already in use | A program is already listening on the wallet or peer port. Identify it; stop a duplicate node or configure an intentional non-conflicting port. |
| Database already in use or locked | Make sure only one process uses this node folder. Allow the previous node to finish shutting down. Do not delete lock/database files while a process may still use them. |
| No connected peers | Check internet, firewall and outbound TCP connectivity; confirm bootstrap peers are still valid Arkovia mainnet nodes. See configuration. |
| Height stays at zero | Confirm connected peers first. Review logs for network or genesis mismatch errors. Do not edit genesis balances or parameters. |
| Height stalls later | Compare with a trusted current node. Check disk space, peer connectivity, log errors and whether the live network is producing blocks. |
| Slow first startup | Genesis import and database creation require work before syncing. Watch logs; do not launch extra copies. |
| Slow shutdown | Database compaction can take time. Wait for the completed shutdown message. |
| Disk full | Stop cleanly if possible and make space. Preserve the database; review logs and unrelated files before considering a fresh sync. |
| Balance seems outdated | Confirm mainnet, account address and synchronization before relying on the wallet's figures. |
| Windows/security software blocks the package | Verify origin and checksum, inspect the exact warning, and follow your organization's policy. Do not disable protection broadly. |

## Collect useful status

With the node running, open these URLs locally:

- http://127.0.0.1:4876/nxt?requestType=getBlockchainStatus
- http://127.0.0.1:4876/nxt?requestType=getPeers&state=CONNECTED

For a basic connectivity check in PowerShell, use:

```powershell
Test-NetConnection 147.93.138.255 -Port 4874
Test-NetConnection 217.216.64.226 -Port 4874
```

`TcpTestSucceeded=True` proves only that a TCP connection opened. It does not prove that the peer has the right genesis or that your node is synchronized. A failed result may come from local or remote network conditions.

## Get help

[Open an issue](https://github.com/mycreationhaven/Arkovia-Windows-Full-Node/issues) with:

- The release name and `BUILD-INFO.json` source/packaging commits.
- Your Windows version and whether the PC is x64.
- The exact error and what you were doing when it appeared.
- Whether this is a fresh installation or an update.
- Block height, connected-peer count, and a short relevant log excerpt.

Review any attached material first. Do not post secret phrases, private keys, admin passwords, personal account details, or full database backups. A public issue is visible to other people.
