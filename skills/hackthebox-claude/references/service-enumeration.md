# Service Enumeration Reference

Use this reference only after the target and scope have been confirmed. Select the smallest check that answers the current hypothesis. Replace placeholders before execution and save raw output under the target workspace.

## General Rules

Record the target, port, protocol, command, timestamp, and output path for every check. Treat banners and version strings as leads, not proof. Prefer read-only inspection, narrow port lists, small wordlists, low concurrency, and explicit timeouts. Stop if a check begins to affect availability or leaves unexplained changes.

| Service or surface | First questions | Bounded checks | Evidence to retain |
| --- | --- | --- | --- |
| HTTP/HTTPS | What hostnames, paths, technologies, and authentication boundaries exist? | Inspect headers and responses; review `robots.txt`, known application routes, forms, and a small content-discovery wordlist. Test one parameter or upload behavior at a time. | URLs, status codes, headers, request/response pairs, technology observations, and relevant source paths. |
| DNS | Is the service authoritative, recursive, or hosting useful records? | Query the target domain and explicitly identified names; test zone transfer only when the target is an authorized lab DNS server. | Queries, answers, TTLs, nameservers, and the exact record source. |
| SMB/NetBIOS | Are shares, signing settings, or domain relationships exposed? | Enumerate host and share metadata with null or supplied lab credentials; inspect only authorized shares. | Share names, access level, server/domain names, and representative directory paths. |
| LDAP | What directory naming context, users, groups, or policies are exposed? | Discover the base naming context, then make narrow anonymous or supplied-credential queries. | Naming context, query filter, returned attributes, and access result. |
| FTP | Is anonymous access enabled, and are files or write permissions exposed? | Check banner and anonymous login; list authorized directories and download only relevant lab artifacts. Avoid uploads unless the objective requires a controlled test. | Banner, login result, directory listing, filenames, permissions, and hashes where useful. |
| SSH | Is remote access available, and what authentication methods are allowed? | Inspect banner and host keys; use only credentials supplied by the user or discovered and validated inside the lab. Do not spray or brute-force. | Port, banner, authentication method, and the source of any validated credential. |
| Databases | Is the service reachable, and what authentication or application relationship exists? | Identify protocol/version; use provided credentials or a single lab account; inspect metadata before reading data. | Server/version, database names, account scope, and minimal query results. |
| Containers and orchestration | Are local sockets, container metadata, or deployment files exposed? | Inspect local configuration and process mounts; query only the scoped host/container endpoint. | Mounts, socket permissions, image names, deployment files, and the least data needed to prove impact. |

## HTTP/HTTPS Notes

Use the canonical scheme and host discovered from the scan. Preserve redirects and compare responses rather than relying on a single status code. Test virtual hosts only when names are supported by certificates, DNS, page content, source code, or another concrete clue. When content discovery is justified, begin with a small wordlist and a low request rate; filter by known baseline size or status behavior rather than blindly accepting every result.

For source-backed applications, map routes to handlers and identify where user-controlled input crosses an interpreter, filesystem, template, database, or authorization boundary. Validate the smallest behavior that demonstrates the hypothesis. Do not upload or execute a payload merely because an endpoint appears to accept files.

## Linux Local Checks

After a lab shell is obtained, start with identity, groups, host information, environment, running processes, network listeners, `sudo` policy, SUID/SGID files, Linux capabilities, scheduled jobs, service definitions, writable paths, and application configuration. Correlate each candidate with the current user, file ownership, and execution context. Avoid recursive reads of unrelated home directories or system data.

## Evidence Pattern

For each candidate, use this record:

```text
Observation: <what was directly observed>
Source: <command, file, URL, or captured response>
Hypothesis: <what it may mean>
Test: <one bounded validation>
Result: <observed outcome>
Confidence: observed | strongly supported | unconfirmed | rejected
Next action: <single next step>
```
