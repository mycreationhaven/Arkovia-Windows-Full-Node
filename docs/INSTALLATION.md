# Install your first Arkovia node

[Back to README](../README.md)

## 1. Download the ready-to-run package

Visit [Releases](https://github.com/mycreationhaven/Arkovia-Windows-Full-Node/releases). Open the release's **Assets** section and download `Arkovia-Full-Node-1.13.1-Windows-x64.zip`.

Use the named full-node ZIP. GitHub's automatically generated **Source code (zip)** and **Source code (tar.gz)** are developer downloads; they do not include the assembled node and Java runtime. If no release is available, inspect the [Actions page](https://github.com/mycreationhaven/Arkovia-Windows-Full-Node/actions) for build progress.

You may also download the `.zip.sha256` file to verify your download using the [verification guide](VERIFICATION.md).

## 2. Extract everything

Right-click the ZIP in File Explorer and select **Extract All**. Choose a folder you can write to, such as `C:\Arkovia-Node` or a folder under your Windows user account. Avoid placing an ordinary portable installation under `Program Files`.

The ZIP has a top-level `Arkovia-Full-Node-1.13.1-Windows-x64` folder. Open that folder until you can see `Start-Arkovia.bat`, `Open-Wallet.bat`, `arkovia.jar`, and `jre`. Do not run the launcher from inside the compressed ZIP or move only the launcher to another folder.

## 3. Start the node

Double-click **Start-Arkovia.bat**. A console opens and prints startup messages. The first run creates a local database and imports the original genesis accounts. This can take several minutes on slower computers.

Wait for **`Arkovia server 1.13.1 started successfully.`** Keep the console open. Do not repeatedly start additional copies while waiting.

If Windows or your security software blocks execution, inspect the exact warning and verify the package's origin and checksum. Do not turn off security software as a general fix. See [troubleshooting](TROUBLESHOOTING.md).

## 4. Open the wallet

Double-click **Open-Wallet.bat**, or enter **http://127.0.0.1:4876/** into your browser's address bar. This address points to your own computer. It opens only while your node's API server is running and does not work on another device as a link to this node.

The browser wallet is included in the package. No JavaFX desktop application or separate Java download is needed.

## 5. Let it synchronize

Startup success means the program is running; it does not mean the chain is current. Follow [operation and synchronization](OPERATING.md) to check connected peers, increasing height, and agreement with a trusted live Arkovia node.

A full node does not need your wallet secret phrase to download blocks. Keep account recovery information separately and privately. Running this package does not automatically start forging or guarantee rewards.

## 6. Shut down safely

Press **Ctrl+C once** in the console and wait for the database to close and **`Arkovia server 1.13.1 stopped.`** Only then close the window or restart Windows. Starting the same launcher later resumes from the saved database.
