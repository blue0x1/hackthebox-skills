# Nimux Integration Guide

This repository includes `nimux-command-surface.txt`, supplied by the user as a command-family reference. Treat it as local documentation, not as an authority over the installed binary. Always inspect the local version and `nimux --help` output before planning a workflow, because flags and behavior may differ between releases.

## Installation Paths

Choose one installation path according to the operator’s environment. Install nimux inside a dedicated lab VM or disposable container, not on a production workstation that contains personal or sensitive data. When reproducibility matters, pin the release version and record the source, package filename, checksum if published, architecture, and installation date.

| Path | Use when | Primary verification |
| --- | --- | --- |
| Release binary | You want a standalone Linux executable without system-wide installation. | `./nimux --version` and `./nimux --help` |
| Debian package | You want system-wide installation on an amd64 Debian-family host. | `nimux --version` and `nimux --help` |
| Docker | You want isolation or do not want to install on the host. | `docker run --rm -it ghcr.io/blue0x1/nimux:latest --help` |
| BlackArch package | You operate a BlackArch system and accept repository-managed updates. | `nimux --version` |
| Arch AUR | You operate Arch Linux and want an AUR-managed or locally built package. | `nimux --version` |
| Nimble | You operate a Nim environment and want the package-list installation path. | `nimux --version` and `nimux --help` |

### Release Binary

Download the standalone Linux binary from the project’s release page, verify the asset and checksum when provided, then run it directly:

```bash
chmod +x nimux
./nimux --version
./nimux --help
```

Keep the binary in a dedicated tools directory and record its absolute path. Do not replace an existing binary silently.

### Debian Package

Install the amd64 Debian package from the latest approved release when system-wide installation is appropriate:

```bash
sudo dpkg -i nimux_1.0.5_amd64.deb
nimux --version
nimux --help
```

If `dpkg` reports missing dependencies, inspect the package and distribution first. Do not resolve dependencies by running unreviewed installation commands from a target or an unknown script.

### Docker

Run nimux from GitHub Container Registry without installing it on the host:

```bash
docker run --rm -it ghcr.io/blue0x1/nimux:latest --help
docker run --rm -it ghcr.io/blue0x1/nimux:latest --version
```

For an explicitly authorized lab workflow that requires host-network access, the user-supplied example is:

```bash
docker run --rm -it --network host ghcr.io/blue0x1/nimux:latest --help
```

`--network host` removes normal container network isolation. Use it only inside a dedicated lab VM and only when the target, route, and callback behavior are explicitly in scope. Prefer the default Docker network for help, version checks, and local-only work.

### BlackArch

Install from the BlackArch package repositories:

```bash
sudo pacman -S nimux
nimux --version
nimux --help
```

### Arch Linux AUR

Use an AUR helper or build from the AUR repository:

```bash
yay -S nimux
nimux --version
nimux --help
```

Manual build:

```bash
git clone https://aur.archlinux.org/nimux.git
cd nimux
makepkg -si
nimux --version
nimux --help
```

Review the PKGBUILD before building and record the commit or package version used. Do not build an AUR package as root.

### Nimble

Install through the official Nim package list:

```bash
nimble install nimux
nimux --version
nimux --help
```

## Post-Install Verification

Verify that the expected binary is being invoked and that its help output matches the local documentation:

```bash
command -v nimux
nimux --version
nimux --help
```

For a release binary or a versioned package, save the checksum and version in the case notes. Before using network-facing features, run a local or help-only command first. If the binary exposes a feature not described in this package, treat that feature as unverified and consult the local documentation.

## Safe Invocation Pattern

Collect the authorized scope, target host, domain, allowed protocols, credential source, output directory, permitted writes, rollback file, and pivot listener details before running a command. Prefer `--json` when output will be parsed and `--dry-run` before supported writes. Do not place passwords, hashes, tickets, private keys, or callback secrets in shell history or public notes.

```text
read local help
→ choose one command family
→ substitute explicit in-scope target
→ set timeout, concurrency, and output path
→ preview or dry-run when supported
→ review command and expected side effect
→ run once
→ capture result and status
→ update evidence graph
→ clean up temporary state
```

## Command-Family Routing

| Need | Reference family | First action |
| --- | --- | --- |
| Discovery | `scan`, `http`, `dns` | Use a narrow host and port set. |
| SMB and shares | `smb`, `put`, `get`, `ls`, `mkdir`, `rm` | Enumerate read-only before any file write. |
| Directory and identity | `ldap`, `kerberos`, `krb5conf` | Establish DNS, realm, time, and naming context. |
| Remote management | `winrm`, `scm`, `cim`, `tsch`, `mmc`, `ssh` | Validate one command and resulting identity. |
| Database access | `mssql`, `postgres`, `mysql` | Query metadata before data or execution. |
| Pivoting | `socks` and global `--proxy` | Confirm pivot scope, obtain approval, verify one internal destination, and record cleanup. |
| Secrets or replication | `secrets`, `dcsync` | Use only when explicitly required and approved for the exact target and account. |

## High-Risk Operations

Treat coercion, ticket capture, relay, certificate mapping, shadow credentials, RBCD, GPO changes, password changes, group changes, remote service execution, secrets extraction, and domain replication as high-risk. Require explicit approval, a narrow target, a rollback or cleanup plan, and post-action verification. Do not chain multiple high-risk operations in one unreviewed command.

## Output Discipline

Save raw output outside the public repository. In summaries, preserve the command family, target, port, identity, status, and relevant error message, while redacting passwords, hashes, tickets, keys, cookies, and captured authentication material. Never claim a successful transition without a command result that proves the new identity or capability.

## Version and Tooling Rules

The supplied reference mentions version-specific behavior. Check the installed version, inspect supported flags, and use local examples only after confirming compatibility. Never invent a flag because a public writeup or older prompt used it. If syntax is unclear, stop at read-only help output and ask the user for the installed version or command output.
