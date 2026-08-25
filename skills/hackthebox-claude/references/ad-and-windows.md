# Windows and Active Directory Playbook

Use this playbook only for an explicitly authorized Windows or Active Directory lab. It is a decision guide, not a collection of target-specific solutions. Prefer read-only enumeration, preserve identity context, and require approval before writes, relay, coercion, secrets extraction, replication, or persistence.

## Identity and Host Model

Create a graph before attempting lateral movement. Record the host, IP, hostname, domain, forest, site, time source, service, account, credential type, privilege, and evidence source for every edge.

```text
Host: <host>
Address: <ip>
Hostname: <fqdn>
Domain/forest: <domain>
Role: workstation | member server | domain controller | SQL server | CA | file server
Reachable protocols: <ports and services>
Observed identities: <accounts, groups, machine accounts>
Evidence: <file and line or query reference>
```

Do not convert a discovered hostname into a new scan target unless the lab scope permits it. Treat domain controllers, certificate authorities, SQL servers, management hosts, and file servers as separate assets with separate evidence.

## Baseline Checks

From the operator side, establish DNS, time, and service reachability. From an authorized Windows shell, collect identity and token context before changing anything.

```powershell
whoami /all
hostname
systeminfo
ipconfig /all
nltest /dsgetdc:<domain>
klist
```

From the operator side, use the smallest service checks first:

```bash
nmap -Pn -sC -sV -p 53,88,135,139,389,445,464,636,1433,3268,3269,5985,5986,9389 <dc-or-host>
```

Check clock skew before Kerberos. If the lab requires a hosts-file entry, add only the named lab hosts and record the change.

## SMB and File Services

Start with anonymous or supplied-credential share enumeration where permitted. Record share names, access level, signing, server and domain names, and only the relevant directory paths. Download named artifacts one at a time and hash them.

```bash
smbclient -L //<host> -N
smbclient //<host>/<share> -U '<domain>/<user>'
```

Use a small, evidence-driven search for filenames such as configuration files, deployment manifests, backup archives, and credential stores. Do not spider an entire domain or collect every home directory. Treat file-write operations as a separate approval step.

## LDAP and Directory Services

Discover the naming context, domain controllers, users, groups, computers, trusts, SPNs, delegation settings, GPOs, certificate services, and ACLs. Begin with a narrow query and expand only when the returned object relationships justify it.

```bash
ldapsearch -x -H ldap://<dc> -D '<user>@<domain>' -W \
  -b '<base-dn>' '(objectClass=user)' sAMAccountName memberOf
```

For Kerberos-bound LDAP, establish realm configuration and hostname resolution before querying. Prefer JSON or another machine-readable format when the local tool supports it, but preserve the raw output.

## Kerberos

Use hostnames and correct realm context. Record the principal, ticket type, service principal name, cache path, lifetime, encryption type if relevant, and the evidence that authorized the request. Never copy tickets or keys into a public report.

```bash
kinit <user>@<REALM>
klist
kvno <service>/<host>
```

For a user-supplied nimux installation, read `references/nimux-command-surface.txt` and the local `nimux --help` output before using `nimux krb5conf` or `nimux kerberos`. Do not assume flags or behavior across versions.

## Authentication Material

Classify material before use:

| Material | Safe first action | Boundary |
| --- | --- | --- |
| Cleartext password | Validate once against the service where it was found | Do not spray across users or hosts. |
| NT hash | Confirm account and permitted protocol | Treat pass-the-hash as an approved lab action. |
| Kerberos cache or ticket | Inspect principal and service context | Do not export or reuse outside scope. |
| Certificate or PFX | Inspect subject, SAN, EKU, and validity | Protect private keys and require approval for authentication use. |
| GMSA material | Confirm read permission and account relationship | Do not dump unrelated accounts. |
| Browser or application token | Identify audience and scope | Do not send it to outside services. |

## WinRM, RDP, and Remote Execution

Validate the account’s logon rights and use a one-command probe before opening an interactive shell. Record the host and identity returned by the service, not just the operator-side username.

```bash
evil-winrm -i <host> -u <user> -p '<password>' -c 'whoami'
xfreerdp /v:<host> /u:<user> /d:<domain> /cert:ignore
```

If the lab supports hash or Kerberos authentication, follow the local tool’s syntax and capture the authentication context. Avoid creating services, scheduled tasks, or persistent sessions unless the lab explicitly requires a controlled test.

## MSSQL

Establish server identity, database context, login role, linked servers, and application relationships before considering command execution. Start with read-only metadata queries:

```sql
SELECT @@SERVERNAME, @@VERSION;
SELECT SUSER_SNAME(), IS_SRVROLEMEMBER('sysadmin');
SELECT name FROM sys.databases;
```

Do not enable `xp_cmdshell`, CLR, external scripts, OLE automation, or other execution features without explicit approval. If a feature is already enabled, prove the permission boundary with the minimum command and record the before and after state.

## Privilege and Delegation Analysis

For each candidate path, record the principal that can perform the action, the object or service affected, the resulting identity, and the evidence. Relevant relationships include local administrator, remote management rights, service logon, constrained delegation, unconstrained delegation, resource-based constrained delegation, certificate enrollment, group membership, ACL control, GPO application, and trust direction.

Treat relay, coercion, ticket capture, delegation abuse, and password changes as high-risk. Do not enable or trigger them merely because an enumeration result suggests they may work. Require an explicit lab approval record, a narrow target, a cleanup plan, and a rollback or verification step.

## AD CS

Inventory certificate authorities, templates, enrollment permissions, EKUs, subject or SAN rules, manager approval, and mapping behavior. Separate read-only certificate inventory from policy changes or certificate requests. Protect PFX files, private keys, and Kerberos caches.

Before a policy or mapping change, capture the original state, use dry-run support if available, save rollback information, and confirm the exact object and attribute. Verify the resulting identity mapping with a minimal, in-scope authentication check, then remove temporary material.

## GPO, ACL, and Directory Writes

Write operations require explicit approval because they can affect many hosts or users. The minimum safe sequence is:

```text
read current value
→ identify exact object and attribute
→ preview or dry-run
→ obtain approval
→ apply one change
→ verify intended effect
→ restore original state when safe
→ record rollback result
```

Do not link a GPO, change group membership, set delegation, add credentials, reset a password, or alter an ACL as an experiment. Do not use a write-capable account to explore unrelated objects.

## Secrets and Replication

Secrets extraction and domain replication are not baseline enumeration. Use them only when the explicit lab objective requires them and the user approves the narrow target, account, and output path. Redact secrets in summaries and delete temporary exports when safe.

The supplied nimux reference contains `secrets` and `dcsync` command families. Treat those examples as approval-gated, version-sensitive reference material. The local binary help and user authorization override the reference.

## Completion Criteria

A Windows or AD case is complete only when the identity transition and objective are verified. Record domain and host context at each step, preserve the smallest evidence set, redact secrets, document rejected paths, and clean up tunnels, temporary files, tickets, and write changes when safe.
