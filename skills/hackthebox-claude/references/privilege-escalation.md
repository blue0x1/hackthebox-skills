# Privilege-Escalation Playbook

Use this guide only after an authorized lab shell or equivalent access has been obtained. The goal is to identify and validate the smallest privilege boundary that proves the lab objective. Do not dump unrelated secrets, alter system state unnecessarily, or run kernel exploits as a first resort.

## Context First

Capture the current identity, host, groups, session type, current directory, environment, network interfaces, and process context before changing anything.

### Linux

```bash
id
hostname
pwd
umask
cat /etc/os-release
uname -a
ip addr
ip route
ps auxww
ss -lntup
```

### Windows

```powershell
whoami /all
hostname
cd
systeminfo
ipconfig /all
tasklist /v
netstat -ano
```

## Candidate Matrix

| Boundary | Linux checks | Windows checks | Validation principle |
| --- | --- | --- | --- |
| Sudo or elevated command | `sudo -l`, sudoers files | Run-as rights, service accounts | Confirm exact command, arguments, environment, and resulting identity. |
| SUID, SGID, or capabilities | `find`, `getcap`, file owner and version | Token privileges, service permissions | Prefer a narrowly scoped, reversible behavior test. |
| Scheduled execution | cron, timers, writable scripts | Scheduled tasks, startup folders | Prove the scheduler identity and writable path without persistence beyond the lab. |
| Services | unit files, init scripts, writable binaries | service path, ACLs, recovery actions | Verify who runs it and whether a change is necessary. |
| Credentials | application configs, history, keyrings | Credential Manager, files, registry | Use only the account or service needed for the next step. |
| Filesystem permissions | writable directories, symlinks, mounts | weak ACLs, writable shares, junctions | Track owner, group, mode, and execution context. |
| Containers or virtualization | socket, mounts, capabilities | Hyper-V, container service, named pipes | Validate boundary and scope before interacting with control sockets. |
| Kernel or OS defect | version and mitigations | build and patch state | Last resort; use only an approved lab proof and preserve stability. |

## Linux Workflow

Check `sudo -l`, SUID or SGID binaries, capabilities, cron and systemd timers, services, writable paths in executed scripts, environment inheritance, shell histories, application secrets, mounted filesystems, container sockets, and backup utilities. Correlate each candidate with the current user and the exact command or service context.

```bash
sudo -l
find / -xdev -perm -4000 -type f -print 2>/dev/null
getcap -r / 2>/dev/null
find /etc/cron* /var/spool/cron -type f -maxdepth 3 -ls 2>/dev/null
find / -xdev -type f -writable -not -path '/proc/*' -not -path '/sys/*' 2>/dev/null | head -n 200
```

Do not blindly execute every result returned by an enumeration script. Inspect the file, owner, invocation path, and environment first.

## Windows Workflow

Inspect token privileges, services, scheduled tasks, startup execution, registry run keys, writable program paths, weak service ACLs, stored credentials, user profiles, application configuration, named pipes, and local groups.

```powershell
whoami /priv
Get-CimInstance Win32_Service | Select-Object Name,StartName,State,PathName
schtasks /query /fo LIST /v
Get-LocalGroupMember Administrators
cmdkey /list
```

Avoid changing service binaries, registry values, scheduled tasks, or startup entries unless the lab objective explicitly requires it and the user approves. Capture original values and restore them when safe.

## Containers

Determine whether the current process is inside a container, which namespaces and mounts are visible, what capabilities exist, and whether a control socket is accessible. A container socket or privileged mount is a sensitive boundary. Confirm the host and scope before any interaction and avoid mounting or reading the host filesystem beyond the minimum proof.

## Credential Reuse

Treat each recovered credential as a hypothesis with a source, account, domain or host context, and one intended validation target. Do not spray it across accounts or services. If a credential works, record the principal and privileges, then re-enumerate from that identity rather than assuming lateral access.

## Verification and Cleanup

Prove the identity transition with a direct identity command and retain the output. Remove temporary binaries, scripts, scheduled tasks, service changes, registry entries, keys, tickets, and test files when safe. If a change cannot be reverted, record the exact residual state and notify the user.
