"""Build the Windows package from pinned source; standard-library Python only."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import struct
import subprocess
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE_URL = "https://github.com/mycreationhaven/Arkovia-Blockchain.git"
SOURCE_COMMIT = "dabcf44d51dcf5047118ca47347465a97b26369a"
RUNTIME_URL = "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.20.1%2B1/OpenJDK17U-jre_x64_windows_hotspot_17.0.20.1_1.zip"
RUNTIME_SHA256 = "bc21a93923103cdaac93ee337b0ae4365e739fde36df823dd456bc67c8a9d352"
NAME = "Arkovia-Full-Node-1.13.1-Windows-x64"


def sha256(path):
    with open(path, "rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def run(args, cwd, log=None, timeout=600):
    print("Running:", args[0], flush=True)
    result = subprocess.run([str(a) for a in args], cwd=cwd, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            encoding="utf-8", errors="replace", timeout=timeout)
    if log:
        Path(log).write_text(result.stdout, encoding="utf-8")
    if result.returncode:
        print(result.stdout)
        raise RuntimeError(f"{args[0]} failed with exit code {result.returncode}")
    return result.stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime-archive", type=Path, help="Use a previously downloaded, hash-checked JRE ZIP")
    options = parser.parse_args()
    work = ROOT / ".build"
    work.mkdir(exist_ok=True)
    source = work / "source"
    if not source.exists():
        run(["git", "clone", "--no-checkout", SOURCE_URL, source], ROOT)
    run(["git", "checkout", "--detach", SOURCE_COMMIT], source)
    assert run(["git", "rev-parse", "HEAD"], source).strip() == SOURCE_COMMIT
    # Only committed files may enter the build, even when reusing a work directory.
    assert not run(["git", "status", "--porcelain", "--untracked-files=no"], source).strip(), "Source has local edits"
    package = ROOT / "dist" / NAME
    if package.exists():
        shutil.rmtree(package)
    package.mkdir(parents=True)
    evidence = package / "verification"
    evidence.mkdir()
    javac, jar, java = (shutil.which(x) for x in ("javac", "jar", "java"))
    if not all((javac, jar, java)):
        raise RuntimeError("Install JDK 17 and put java, javac and jar on PATH")
    build_java = run([java, "-version"], ROOT)
    if 'version "17.' not in build_java:
        raise RuntimeError("Build requires JDK 17")
    classes = work / "classes"
    if classes.exists():
        shutil.rmtree(classes)
    classes.mkdir()
    sources = work / "sources.txt"
    sources.write_text("\n".join('"' + p.as_posix() + '"' for p in sorted((source / "src/java/nxt").rglob("*.java"))), encoding="utf-8")
    cp = os.pathsep.join([str(source / "lib/*"), str(classes)])
    run([javac, "-encoding", "UTF-8", "--release", "17", "-sourcepath", source / "src/java",
         "-cp", cp, "-d", classes, "@" + str(sources)], ROOT, evidence / "compile.log")
    run([jar, "--create", "--file", package / "arkovia.jar", "--main-class", "nxt.Nxt", "-C", classes, "."], ROOT)
    for directory in ("lib", "html", "conf"):
        shutil.copytree(source / directory, package / directory)
    (package / "conf/nxt.properties.txt").unlink(missing_ok=True)
    shutil.copytree(ROOT / "package", package, dirs_exist_ok=True)
    for path in package.glob("*.bat"):
        path.write_bytes(path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\n", "\r\n").encode("utf-8"))
    for name in ("LICENSE.txt", "AUTHORS.txt", "3RD-PARTY-LICENSES.txt", "JPL-NRS.pdf"):
        shutil.copy2(source / name, package / name)
    shutil.copytree(ROOT / "docs", package / "docs")
    shutil.copy2(ROOT / "README.md", package / "README.md")
    shutil.copy2(ROOT / "package/START-HERE.txt", package / "START-HERE.txt")
    (package / "logs").mkdir(exist_ok=True)
    # Preserve the exact corresponding blockchain source, including its notices.
    run(["git", "archive", "--format=zip", "--output=" + str(package / "Arkovia-Source-dabcf44.zip"), SOURCE_COMMIT], source)
    test_classes = work / "test-classes"
    test_classes.mkdir(exist_ok=True)
    test_cp = os.pathsep.join([cp, str(source / "testlib/*"), str(test_classes)])
    tests = work / "tests.txt"
    tests.write_text("\n".join('"' + p.as_posix() + '"' for p in sorted((source / "test/java/nxt/crypto").rglob("*.java"))), encoding="utf-8")
    run([javac, "-encoding", "UTF-8", "--release", "17", "-cp", test_cp,
         "-sourcepath", os.pathsep.join([str(source / "src/java"), str(source / "test/java")]),
         "-d", test_classes, "@" + str(tests)], ROOT, evidence / "test-compile.log")
    test_output = run([java, "-cp", test_cp, "org.junit.runner.JUnitCore", "nxt.crypto.CryptoSuite"], source, evidence / "crypto-tests.log")
    assert "OK (7 tests)" in test_output
    archive = options.runtime_archive.resolve() if options.runtime_archive else work / "windows-jre.zip"
    if not archive.exists():
        print("Downloading pinned Windows x64 Java runtime", flush=True)
        with urllib.request.urlopen(RUNTIME_URL, timeout=120) as response, open(archive, "wb") as output:
            shutil.copyfileobj(response, output)
    assert sha256(archive) == RUNTIME_SHA256, "Runtime SHA-256 mismatch"
    with zipfile.ZipFile(archive) as z:
        for member in z.infolist():
            parts = Path(member.filename).parts[1:]
            if not parts:
                continue
            target = package / "jre" / Path(*parts)
            assert target.resolve().is_relative_to((package / "jre").resolve())
            if member.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(z.read(member))
    executable = (package / "jre/bin/java.exe").read_bytes()
    pe = struct.unpack_from("<I", executable, 0x3C)[0]
    assert executable[pe:pe + 4] == b"PE\0\0" and struct.unpack_from("<H", executable, pe + 4)[0] == 0x8664
    for path in (source / "conf/data").iterdir():
        if path.is_file():
            assert sha256(path) == sha256(package / "conf/data" / path.name)
    # A separate directory keeps the generated database out of the deliverable.
    smoke = work / "smoke"
    if smoke.exists():
        shutil.rmtree(smoke)
    smoke.mkdir()
    for directory in ("conf", "html"):
        shutil.copytree(package / directory, smoke / directory)
    (smoke / "logs").mkdir()
    smoke_cp = os.pathsep.join([str(package / "arkovia.jar"), str(package / "lib/*"), str(smoke / "conf"), str(smoke)])
    run([javac, "--release", "17", "-cp", smoke_cp, "-d", smoke, ROOT / "scripts/NodeSmokeTest.java"], ROOT)
    windows = platform.system() == "Windows"
    smoke_java = package / "jre/bin/java.exe" if windows else java
    smoke_output = run([smoke_java, "-Xms256m", "-Xmx2g", "-Dfile.encoding=UTF-8", "-cp", smoke_cp,
                        "NodeSmokeTest", "windows" if windows else "linux"], smoke, evidence / "startup.log", timeout=600)
    assert "SMOKE_PASS" in smoke_output and "Database shutdown completed" in smoke_output
    assert "Can't load log handler" not in smoke_output
    assert (smoke / "logs/nxt.0.log").is_file(), "File logging did not initialize"
    provenance = {
        "source_repository": SOURCE_URL, "source_commit": SOURCE_COMMIT,
        "packaging_commit": run(["git", "rev-parse", "HEAD"], ROOT).strip(),
        "build_java": build_java.strip(), "build_platform": platform.platform(),
        "runtime_url": RUNTIME_URL, "runtime_sha256": RUNTIME_SHA256,
        "checks": {"crypto_tests": 7, "original_genesis_unchanged": True,
                   "genesis_block": "10203308059164672611", "wallet_http": 200,
                   "full_node_api": True, "graceful_shutdown": True,
                   "bundled_windows_runtime_executed": windows,
                   "windows_batch_launcher_manually_tested": False,
                   "live_network_sync_verified": False},
        "notes": "Startup test uses an isolated database and offline mode. Release configuration remains online."
    }
    (package / "BUILD-INFO.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    sums = [sha256(p) + "  " + p.relative_to(package).as_posix() for p in sorted(package.rglob("*")) if p.is_file()]
    (package / "SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="utf-8")
    output = package.parent / (NAME + ".zip")
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for path in sorted(package.rglob("*")):
            # Include directories: logs is empty before first startup but required
            # by Java's FileHandler. File-only archives silently lost it.
            z.write(path, path.relative_to(package.parent))
    with zipfile.ZipFile(output) as z:
        assert z.testzip() is None
        log_entry = NAME + "/logs/"
        assert z.getinfo(log_entry).is_dir(), "Release ZIP is missing logs/"
        extracted_check = work / "archive-check"
        if extracted_check.exists():
            shutil.rmtree(extracted_check)
        z.extract(log_entry, extracted_check)
        assert (extracted_check / NAME / "logs").is_dir()
    checksum = sha256(output)
    (package.parent / (NAME + ".zip.sha256")).write_text(checksum + "  " + output.name + "\n", encoding="utf-8")
    (package.parent / "release-notes.md").write_text(
        "Windows x64 portable Arkovia full node with bundled Java, local browser wallet, launchers, and complete guides.\n\n"
        "Packaging fix: preserves the empty logs directory and creates it at launcher startup if missing. "
        "If an older installation reports a locked database, stop the other node cleanly; do not delete its database.\n\n"
        "Download **" + output.name + "**, extract the entire ZIP, then run **Start-Arkovia.bat**. "
        "After startup, open **Open-Wallet.bat**. The database downloads locally on first use.\n\n"
        "Source: `" + SOURCE_COMMIT + "`. Cryptography: 7 tests passed. Genesis import, wallet/API, "
        "full-node settings and clean database shutdown checked. Bundled Windows runtime executed: **" + str(windows) + "**.\n\n"
        "Live-network synchronization and interactive batch-launcher behavior remain unverified. "
        "No pre-synchronized database, private keys, installer, or Windows service is included.\n\n"
        "SHA-256: `" + checksum + "`\n", encoding="utf-8")
    print("Built", output, "SHA256", checksum, flush=True)


if __name__ == "__main__":
    main()
