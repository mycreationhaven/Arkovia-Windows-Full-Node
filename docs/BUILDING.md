# Build and publish the Windows package

[Back to README](../README.md)

This guide is for maintainers. Ordinary users should download a release ZIP.

## Inputs

| Input | Pinned value |
|---|---|
| Blockchain repository | https://github.com/mycreationhaven/Arkovia-Blockchain |
| Blockchain commit | `dabcf44d51dcf5047118ca47347465a97b26369a` |
| Application version | `1.13.1` |
| Runtime | Eclipse Temurin `17.0.20.1+1`, Windows x64 JRE |
| Runtime ZIP SHA-256 | `bc21a93923103cdaac93ee337b0ae4365e739fde36df823dd456bc67c8a9d352` |

The runtime comes from the [official Temurin release](https://github.com/adoptium/temurin17-binaries/releases/tag/jdk-17.0.20.1%2B1). `scripts/build.py` rejects a different hash and verifies the Windows AMD64 executable header.

## Local build

Install Git, Python 3.11 or newer, and JDK 17, with `git`, `python`, `java`, `javac`, and `jar` on PATH. Clone this packaging repository and run from its root:

```powershell
python scripts/build.py
```

An optional `--runtime-archive C:\Downloads\windows-jre.zip` reuses a downloaded runtime; the hash is still checked.

The script checks out the pinned source under `.build/source` (including the Arkovia Signer PWA web assets), compiles the Java core with `--release 17`, runs seven cryptography tests, builds `arkovia.jar`, copies the wallet/dependencies/genesis, and adds the launchers and guides. It includes an exact source archive for the blockchain and preserves notices.

The smoke test uses a disposable directory under `.build/smoke`. It starts the node offline, imports genesis, checks the local wallet/API and full-node configuration, and calls a clean shutdown. On Windows it executes **the bundled JRE**. On Linux it uses the installed Java and records that Windows execution was not performed. It does not change the online release configuration.

Outputs appear under `dist/`:

- `Arkovia-Full-Node-1.13.1-Windows-x64.zip`
- `Arkovia-Full-Node-1.13.1-Windows-x64.zip.sha256`
- `release-notes.md`
- The extracted package directory.

Do not commit `.build`, `dist`, live databases, credentials, or installed runtimes. Build commands reuse only a clean pinned source checkout; local source edits cause the build to stop. JAR/ZIP timestamps and build metadata can differ between builds, so matching source inputs do not imply byte-identical ZIP files.

## GitHub Actions

The [Windows workflow](https://github.com/mycreationhaven/Arkovia-Windows-Full-Node/blob/main/.github/workflows/windows-release.yml) builds on a Windows runner. It runs on pushes to `main` and can be started manually from **Actions → Build and publish Windows full node → Run workflow**.

A successful main-branch build creates a release named for application version and the short packaging commit, and attaches the ZIP and its checksum. Re-running the same commit detects its existing release and leaves its published files intact. Failed builds do not publish a download.

The workflow uses GitHub's standard `GITHUB_TOKEN` with repository `contents: write` for publishing. It needs no wallet secrets or personal access token. Organization or repository policy can prevent Actions or publication; a failed permission check must be resolved by the repository owner under their policy. Source compilation does not receive the release token in its environment.

## Manual release fallback

If automated publishing is unavailable, a maintainer can run the local build and attach its ZIP and `.sha256` file through the repository's **Releases → Draft a new release** page. Use a unique tag, describe the tested platform accurately, and paste the generated release notes. Do not upload the large distribution ZIP as a normal Git source file.

See [GitHub release instructions](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository) and the [GitHub CLI release command](https://cli.github.com/manual/gh_release_create).

## Updating the source or runtime

Review the new blockchain source before changing the pinned commit. Check mainnet parameters, compatible genesis ID, ports and database compatibility. If these legitimately change, update the smoke-test expectations and user guides deliberately. Do not remove a failing genesis check just to produce a ZIP.

For a Java update, verify the official download and SHA-256, update the pin, rerun compilation and Windows startup tests, and publish a new packaging release. Keep the original blockchain licenses and the new runtime's notices.
