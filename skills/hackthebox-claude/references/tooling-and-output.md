# Tooling and Output Handling

Use this guide to keep investigations reproducible across Claude, Codex, and terminal environments. The tool installed in the lab, its local help output, and the user’s scope govern behavior. Do not invent flags or assume that a tool’s output is complete.

## Command Record

For each significant action, record:

```text
Timestamp UTC: <time>
Purpose: <question being tested>
Working directory: <path>
Command or script: <sanitized exact invocation>
Target: <host, port, URL, file, or artifact>
Tool version: <version>
Expected observation: <what would support the hypothesis>
Output path: <raw output file>
Exit status: <code>
Observed result: <summary>
Next action: <single next step>
```

Capture stdout and stderr separately when a failure or warning matters. Do not put secrets in command arguments, shell history, logs, or issue reports.

## Discovery Discipline

Start with the smallest command that establishes reachability, service identity, or file type. Prefer focused ports after an initial inventory. Use explicit timeouts and a conservative concurrency. A high-volume scanner is not a substitute for a hypothesis.

```bash
nmap -Pn -sC -sV -p <OPEN_PORTS> -oA scans/focused <TARGET>
curl --silent --show-error --max-time 10 -D evidence/response.headers -o evidence/response.body http://<TARGET>:<PORT>/
```

For web content discovery or DNS enumeration, begin with a small wordlist, record the baseline response, and stop if error rates or service stability change. Never scan an unconfirmed hostname or subnet.

## Machine-Readable Output

Use JSON, CSV, or tool-native structured output when it can be parsed reliably. Preserve the original output and the parser version. A parser failure is evidence about the parser, not evidence that the target has no result.

```bash
<tool> <args> --json > evidence/result.json 2> evidence/result.stderr
printf 'exit=%s\n' "$?" >> evidence/result.meta
```

If the tool does not support structured output, keep raw text and summarize with line or section references.

## Hashing and Naming

Use stable names based on purpose, not assumptions about success. Do not overwrite raw evidence. Version reruns with a sequence or timestamp.

```text
scans/tcp-all-01.nmap
scans/tcp-focused-01.nmap
requests/login-baseline-01.txt
artifacts/app-config-01.sha256
notes/hypotheses.md
```

Hash downloaded files, source snapshots, challenge packages, and suspicious artifacts before analysis. Keep the original and working copy distinct.

## Failure Interpretation

| Failure | Preserve | Next step |
| --- | --- | --- |
| Timeout | Target, command, timeout, timestamp, retry count | Verify route and service with one smaller probe. |
| Connection refusal | Address, port, and instance state | Check the lab instance and scope; do not switch hosts silently. |
| Authentication failure | Account context and protocol | Confirm username, domain, time, and intended service; do not spray. |
| Parser error | Raw response and tool version | Inspect format manually or use a local parser. |
| Permission denied | Identity, path, mode or ACL | Recheck context and scope; do not force permissions. |
| Unexpected output | Full raw output and environment | Update the hypothesis before any new action. |

## Tool Selection

Prefer a well-supported standard utility or a small local script over an opaque downloaded binary. Read `--help`, inspect the version, and check network and file behavior before use. If a script is obtained from a target or public source, follow `references/exploit-review.md`.

## Final Evidence Bundle

A sanitized evidence bundle should contain raw outputs, hashes, command records, scope, hypotheses, relevant request or artifact references, and the final report. Exclude credentials, flags, VPN configuration, private keys, suspicious binaries, challenge archives, and unrelated personal data from public copies.
