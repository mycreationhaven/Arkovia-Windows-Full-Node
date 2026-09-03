# Daily operation and synchronization

[Back to README](../README.md)

## Start, stop, resume

Use `Start-Arkovia.bat` every time. Keep the node folder together and leave its console open. Closing just the wallet browser does not stop the node. Sleep, hibernation, shutdown, loss of internet, or closing the Java process interrupts its operation.

Press Ctrl+C once to stop, then wait for `Arkovia server 1.13.1 stopped.` Database compaction may take time. Do not force-close a healthy node merely because compaction is still running.

The launcher uses `-Xms256m -Xmx2g`: Java starts with a modest heap and can grow to 2 GB. Total process memory can exceed the heap. Advanced users may adjust the launcher after assessing available system memory.

## Check whether it is catching up

These read-only addresses work on the computer running the node:

| Address | What to inspect |
|---|---|
| http://127.0.0.1:4876/nxt?requestType=getBlockchainStatus | Application, network mode, block count, feeder height, downloading/scanning status |
| http://127.0.0.1:4876/nxt?requestType=getPeers&state=CONNECTED | Currently connected peer addresses |
| http://127.0.0.1:4876/nxt?requestType=getBlock&height=0 | Genesis block information |

The response appears as JSON: field names with values. Refresh the status after allowing some time for connections and downloads.

| Field | Meaning |
|---|---|
| `application` | Should be `Arkovia` |
| `isTestnet` | Should be `false` for this package |
| `isLightClient` | Should be `false` |
| `apiProxy` | Should be `false`; local node answers requests |
| `numberOfBlocks` | Includes genesis; local height is this value minus one |
| `lastBlockchainFeederHeight` | Height last reported by a feeding peer; may be absent, zero or stale before connection |
| `isDownloading` | A current download-state indicator, not proof of synchronization by itself |
| `isScanning` | Indicates database scanning activity |
| `blockchainState` | Node's broader view of its current state |

**Confirm all three:** peers are connected, height progresses when behind, and your final height agrees with a trusted live Arkovia node or explorer. `isDownloading=false` with no connected peers may simply mean the node cannot obtain blocks. On a quiet chain, height may not rise until a new block is forged.

Genesis-only state has `numberOfBlocks=1`, height `0`, and genesis ID `10203308059164672611`. Remaining there after startup is a reason to check networking, not to change genesis data.

## Logs and storage

The database is under `nxt_db/`. Logs are normally named `logs/nxt.0.log`, with rotated files alongside it. Both can grow over time. Keep free disk space available. An initial sync duration or permanent disk requirement cannot be promised without measuring the live chain.

The source retains NXT-compatible technical names such as `nxt.Nxt`, `nxt.properties`, and `/nxt?requestType=...`; those names do not by themselves mean you are connected to the Nxt network. Check application, genesis and peer settings together.

## Account use

Wait for verified sync before relying on balances or transaction confirmations. Follow your established Arkovia account procedures when using the wallet. Your database backup is not a substitute for securely preserving your account secret phrase. Never include secrets in support requests.
