# Sherlock Playbooks

Use this guide for authorized defensive investigation scenarios. Sherlocks may be linear or free-flow, and they may include evidence packages that contain malicious code. The supplied readme and live platform instructions always take precedence over this document.

## Safety-First Intake

Before opening an investigation package, record its filename, hash, source, password source, scenario name, question mode, and storage path. Use a disposable VM with a snapshot, no personal files, and restricted or disabled network access. Read the package readme before extraction. Do not execute binaries, macros, scripts, installers, or active content unless the scenario explicitly requires it and the isolated environment is prepared.

```bash
mkdir -p sherlock/<name>/{original,work,inventory,evidence,notes,report}
sha256sum <package> | tee sherlock/<name>/notes/package.sha256
7z l <package> | tee sherlock/<name>/notes/package-list.txt
```

Extract a working copy, preserve the original archive, and hash important artifacts. Record the tool version, analysis VM identity, time zone, and clock assumptions.

## Question Management

Create a question ledger before answering anything:

| ID | Question | Required format | Candidate artifacts | Evidence | Answer status |
| --- | --- | --- | --- | --- | --- |
| Q-001 |  | timestamp / account / host / text |  |  | open |

For linear scenarios, answer and verify each unlocked question before moving forward. For free-flow scenarios, prioritize questions that establish the incident time window, principal, initial access, or key artifact relationships. Never let a plausible answer overwrite a conflicting artifact without explaining the conflict.

## Artifact Inventory

| Artifact class | Preserve | Inspect first |
| --- | --- | --- |
| Windows event logs | Original file and hash | Provider, event IDs, timestamps, user, host, command, and logon type. |
| Linux logs | Original file and hash | Authentication, process, sudo, web, service, and kernel messages. |
| PCAP | Original capture | Endpoint summary, protocol, DNS, authentication, transfer, and time range. |
| Memory image | Original image | OS profile, processes, network, handles, modules, and credential-related artifacts. |
| Disk or filesystem image | Original image | Partitions, file system, user profiles, deleted content, and execution traces. |
| Registry hives | Original hive files | User activity, persistence, network settings, and execution artifacts. |
| Browser and email data | Original databases or exports | URLs, downloads, timestamps, account context, and message headers. |
| Cloud logs | Original JSON or CSV | Principal, source, API call, resource, region, response, and time. |
| Malware sample | Original sample | Hash, type, signature, metadata, strings, imports, and static behavior. |

## Timeline Construction

Normalize timestamps to UTC while retaining the original time zone and offset. Use a timeline table with a source reference for every event. Cluster events into preparation, initial access, execution, persistence, discovery, lateral movement, collection, exfiltration, and cleanup only when the evidence supports the phase.

```text
Time (UTC) | Source | Actor or process | Host | Action | Object | Confidence | Question links
```

Do not infer a user from a process name alone. Correlate account, logon session, process lineage, source address, host, and artifact timestamp where possible.

## DFIR Workflow

1. Establish scope, evidence integrity, and the time zone.
2. Inventory artifacts and identify the highest-yield sources.
3. Build a baseline of normal users, hosts, processes, and services.
4. Create an event timeline and group related activity.
5. Trace the incident from initial access to impact and cleanup.
6. Answer each question using the smallest sufficient evidence set.
7. Mark conflicts, uncertainty, and unavailable artifacts.
8. Produce a sanitized findings summary and evidence map.

## SOC and Network Forensics

For alert triage, identify the alert rule, source and destination, user or device, time window, and expected baseline. For PCAP work, start with capture metadata, conversations, DNS, TLS certificate or SNI clues, HTTP objects, authentication exchanges, and unusual periodicity. Use display filters or small scripts that can be reproduced. Do not transmit reconstructed payloads to outside services.

A network finding should include the packet or flow range, five-tuple, protocol interpretation, associated host or account, and reason it matters. Separate a detection signal from proof of compromise.

## Malware Analysis

Use static analysis first. Record hashes, file type, architecture, signing information, sections, imports, strings, embedded resources, configuration, and indicators. Only use dynamic analysis in a disposable snapshot with controlled networking when explicitly required. Capture process tree, file writes, registry changes, network attempts, and persistence behavior. Revert the snapshot after analysis.

Do not upload samples to public scanning services unless the user explicitly confirms that the sample is non-sensitive and the action is allowed. Do not execute samples on a host containing personal or production data.

## Threat Hunting

Convert each hypothesis into a query with a time range, data source, expected signal, and false-positive check. Hunt for process ancestry, unusual parent-child relationships, authentication anomalies, new services, scheduled execution, credential access indicators, uncommon network destinations, and data staging. Record the query text and result count, not just a screenshot.

## Threat Intelligence

Separate factual indicators from attribution hypotheses. Preserve the source URL or report identifier, publication time, indicator type, confidence, and independent corroboration. Avoid doxxing, collecting personal information, or treating a username, handle, or infrastructure overlap as attribution proof.

## Cloud Investigation

Map principal, session, source address, region, API call, resource, permission change, and resulting action. Check identity and access logs, audit events, object access, security-group or firewall changes, metadata access, and persistence in the relevant platform. Keep the investigation to supplied logs or the explicitly scoped tenant; do not query unrelated cloud accounts.

## Answer Quality

For every answer, capture the artifact path, parser or query, relevant line or event identifier, normalized value, and confidence. If the platform expects a precise timestamp, preserve seconds and time zone. If it expects an account or hostname, preserve case and domain context. Recheck the answer against the question wording before submission.

## Final Sherlock Report

Use this order: scenario summary, scope and safety assumptions, artifact integrity, question ledger, timeline, initial-access hypothesis, affected accounts and hosts, attack or incident chain, evidence map, answers, uncertainty, and recommended defensive controls. Do not include unneeded malware, credentials, flags, or sensitive personal data in a public copy.
