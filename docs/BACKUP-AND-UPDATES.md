# Backups and updates

[Back to README](../README.md)

## Back up a stopped node

1. Stop with Ctrl+C and wait for the completed shutdown message.
2. Copy the complete extracted node folder to a separate backup location.
3. Label the backup with the date and package version.
4. Keep private configuration and account recovery information secure.

For a smaller backup, preserve `conf/` and the complete `nxt_db/` folder while stopped, plus any locally customized launchers. Never take an ordinary file-copy backup of the H2 database while the node is writing to it. Copy the database folder as a unit rather than choosing individual database files.

Blockchain data can ordinarily be downloaded again from compatible peers. Account secret phrases cannot be recovered from a blockchain database backup. Keep your account recovery information using your own secure offline process.

## Install a new release

1. Read the new release notes for source, genesis, database or runtime compatibility changes.
2. Download and verify the new ZIP. Extract it into a **new folder**.
3. Stop the old node cleanly and make a backup before migration.
4. If the release confirms database compatibility, copy the stopped old `nxt_db/` folder into the new installation.
5. Compare configuration files. Reapply intentional settings to the new `conf/nxt.properties`; do not blindly overwrite new defaults with an old entire configuration.
6. Preserve the release's expected genesis files. Do not combine different networks' data or replace genesis to force a database to load.
7. Start only the new node. Check its logs, connected peers, and block height.
8. Keep the old backup until the updated node is confirmed healthy.

This repository's packaging builds may keep the same blockchain version while changing documentation or launchers. `BUILD-INFO.json` identifies the source and packaging commits for each build.

## If an update fails

Stop and capture the actual error. Do not repeatedly delete or modify the database. If the new software has changed the database format, copying its database back to an older installation may not be compatible. Use your untouched pre-update backup with its matching old version, or follow a migration process supplied by the blockchain maintainer.

For a fresh sync, use a new separate folder and keep the previous data safe until the fresh node is working. A reset is not the first fix for unreachable bootstrap peers.
