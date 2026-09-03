# Configuration and network access

[Back to README](../README.md)

## Where settings live

Stop the node before editing **`conf/nxt.properties`** in a plain-text editor. In Notepad, confirm the saved filename remains `nxt.properties`, not `nxt.properties.txt`. Restart to apply settings.

The source's `nxt-default.properties` has inherited defaults that differ from this package's intended ports. Keep the supplied `nxt.properties` overrides. Do not edit `conf/data` or replace genesis files to solve connection problems.

| Property | Packaged value | Purpose |
|---|---|---|
| `nxt.isTestnet` | `false` | Arkovia mainnet |
| `nxt.isLightClient` | `false` | Validate and store the blockchain locally |
| `nxt.enableAPIProxy` | `false` | Answer API requests from this node |
| `nxt.launchDesktopApplication` | `false` | Use a normal browser instead of JavaFX |
| `nxt.peerServerPort` | `4874` | Incoming peer TCP port |
| `nxt.shareMyAddress` | `true` | Permit peer-address sharing |
| `nxt.wellKnownPeers` | Two repository-provided peers | Initial peer discovery |
| `nxt.apiServerHost` | `127.0.0.1` | Wallet/API listens locally |
| `nxt.apiServerPort` | `4876` | HTTP wallet/API port |
| `nxt.apiServerSSLPort` | `4877` | Reserved configured HTTPS port; TLS is not enabled by this package |
| `nxt.dbDir` | `./nxt_db/nxt` | Database path relative to the node folder |

`nxt.includeExpiredPrunable=true` is retained from the source's sample configuration. It does not establish that every historical prunable payload is available or retained forever. Do not describe this package as a verified archival-history service.

## Bootstrap peers

The packaged setting is:

```properties
nxt.wellKnownPeers=147.93.138.255:4874;217.216.64.226:4874
```

These addresses were present in source commit `52172c5`; they have not been confirmed as currently reachable from every network. If they are no longer available, obtain confirmed Arkovia mainnet peers from the network operator. Separate entries with semicolons. Never substitute peers for another blockchain.

## Outbound sync and optional inbound connections

Ordinary synchronization needs working outbound peer connectivity. You generally do not need to forward a router port just to sync.

If you want other nodes to connect inbound, allow **TCP 4874** through the Windows firewall for the relevant network profile. If behind a router, forward the same external TCP port to your node's local address. A stable local address helps keep that mapping valid. CGNAT, provider restrictions, or another router upstream may prevent inbound access even when your own router rule is correct.

Keep **4876** private to the local computer. The standard launcher does not need a public API, remote administrator access, stored account secrets, or an admin password. A remote public API needs a separate reviewed deployment design.

## Changing the wallet port

If another program already uses 4876, first identify it. If it is another Arkovia node, stop the extra instance. If a different local port is intentional, change `nxt.apiServerPort`, update the address in `Open-Wallet.bat` and the launcher message, and use that new port in status URLs. Do not run two processes against one database.
