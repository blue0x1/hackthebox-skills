# Machine Playbooks

Use this guide for authorized vulnerable-machine labs. It provides decision patterns, not writeups for individual targets. Replace every placeholder and keep all actions inside the confirmed lab scope.

## Machine Intake

Record the live platform label, operating system if known, target address, hostnames, VPN or access route, starting credentials, objective, and whether the content is active or retired. Create a target directory and keep raw output separate from interpretation.

```bash
mkdir -p htb/<target>/{scans,loot,notes,scripts,reports}
printf '%s\n' '<TARGET>' > htb/<target>/notes/scope.txt
nmap -Pn -p- --min-rate 2000 -oA htb/<target>/scans/tcp-all <TARGET>
nmap -Pn -sC -sV -p <OPEN_PORTS> -oA htb/<target>/scans/tcp-focused <TARGET>
```

Choose scan rate for the lab environment. If packet loss or service instability appears, reduce concurrency and preserve the failure output. Use UDP only when a concrete service hypothesis justifies it.

## Difficulty-Aware Planning

| Difficulty | Expected reasoning pattern | Recommended control |
| --- | --- | --- |
| Easy | A small number of exposed services and a direct or lightly chained weakness | Use a narrow inventory and validate the first strong lead. |
| Medium | Several evidence sources, a chained foothold, source review, credentials, or a local boundary | Split the chain into transitions and record the source of every credential. |
| Hard | Multiple identities, protocols, hosts, domains, or custom behavior | Maintain a graph and verify identity, host, and protocol context after every move. |
| Insane | Deep chains, specialized services, unusual state, segmentation, and alternative paths | Work in milestones with immutable evidence, explicit assumptions, and rollback or cleanup notes. |

Difficulty never justifies broad scanning, destructive testing, or unapproved access to another host.

## Linux Machine Workflow

### Surface and Application Mapping

Start with the port and version inventory, then map the web or service surface. Record redirects, hostnames, certificates, technologies, authentication boundaries, upload paths, API routes, and unusual response behavior. Use a small content-discovery list before expanding it. Search downloaded source and configuration locally before making external requests to a URL found inside them.

### Initial Access Decision Tree

| Observation | Next bounded test |
| --- | --- |
| Web application with a clear input or upload path | Compare baseline responses, inspect validation, and test one controlled input. |
| Public source or configuration | Search for routes, credentials, secrets, unsafe interpreter boundaries, and trust decisions locally. |
| Exposed file share or backup | Enumerate metadata first and download only relevant artifacts. |
| Validated credential | Test it once against the service where it was discovered and record the account scope. |
| Service banner suggests a known weakness | Verify version, configuration, and reachability before adapting a public proof of concept. |

### Post-Foothold Checks

Run identity and context checks first, then inspect processes, listeners, mounts, environment, scheduled jobs, service files, application directories, credentials with clear ownership, `sudo` policy, SUID or SGID files, Linux capabilities, writable paths, containers, and backups. Correlate each candidate with the current user and execution context. Avoid recursive reads of unrelated data.

```bash
id
hostname
uname -a
sudo -l
ss -lntup
find / -perm -4000 -type f 2>/dev/null
getcap -r / 2>/dev/null
```

Do not treat kernel exploit suggestions as a first option. Prefer a misconfiguration or application trust-boundary issue that can be validated with less risk.

## Windows Machine Workflow

### Surface and Identity Mapping

Record hostnames, DNS names, domain or workgroup, certificate subjects, SMB signing, LDAP naming contexts, Kerberos reachability, WinRM, MSSQL, RDP, and web services. Build a table linking each service to the identity and authentication mechanism it accepts.

For a supplied Windows shell, begin with:

```powershell
whoami /all
hostname
systeminfo
ipconfig /all
netstat -ano
cmdkey /list
schtasks /query /fo LIST /v
sc query state= all
```

### Initial Access Decision Tree

| Observation | Next bounded test |
| --- | --- |
| Web application on a Windows host | Map routes and server-side execution boundaries before testing input handling. |
| SMB shares or domain metadata | Enumerate with supplied or explicitly permitted credentials; inspect only in-scope shares. |
| MSSQL | Identify database context, permissions, linked-server relationships, and whether command execution is permitted; do not enable features without approval. |
| Kerberos or LDAP | Establish time, DNS, realm, naming context, and identity before requesting tickets or querying directory data. |
| WinRM or RDP | Validate the account’s logon rights and use the narrowest command or shell needed. |

### Local Privilege Boundary Checks

Inspect service paths and permissions, scheduled tasks, unquoted paths, writable directories, weak registry ACLs, stored credentials, token privileges, named pipes, installed software, and container or virtualization boundaries. Test one candidate at a time and capture the exact identity before and after the transition.

## Active Directory Workflow

Use hostnames consistently once DNS and realm information are known. Enumerate domain controllers, trusts, users, groups, computers, service principal names, delegation settings, certificate services, group policy, and accessible shares. Prefer graph collection that can be reviewed locally. Track edges such as `member-of`, `admin-to`, `can-read`, `can-write`, `delegates-to`, `runs-as`, and `trusts`.

Before Kerberos workflows, check clock skew and generate or inspect the realm configuration. Before AD CS, ACL, RBCD, GPO, password, or group changes, use a dry run when available, record the intended object and attribute, save rollback information, and obtain approval.

A useful progression is:

```text
DNS and time → domain and host inventory → anonymous or supplied-credential enum
→ identity and privilege graph → one validated edge → controlled transition
→ re-enumerate from the new identity → objective proof → cleanup
```

Use `references/nimux-command-surface.txt` only as a user-supplied command reference. The local `nimux --help` output and local documentation are authoritative for syntax and version behavior.

## Lateral Movement and Pivoting

Treat every pivot as a new scope checkpoint. Confirm the pivot host, internal destination, permitted protocols, listener address, route, and cleanup plan. Record the tunnel process, local endpoint, remote helper path, and evidence for the route. Read `references/pivoting-and-ssh.md` for complete SSH examples and `references/nimux-command-surface.txt` for the supplied nimux SOCKS patterns.

After a pivot, verify reachability with a harmless probe before sending credentials or collecting data. Keep internal scans narrow and avoid scanning entire routed networks unless the scope explicitly permits it.

## Machine Completion Criteria

Do not report a machine as solved merely because a shell or plausible credential was obtained. Confirm the intended user or root objective, preserve minimal proof, record rejected paths, redact secrets, and note cleanup. If the platform status or flag submission is relevant, let the user submit it through their authenticated account unless they explicitly request an authorized browser action.
