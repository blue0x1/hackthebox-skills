# Machine Report

## Scope and Authorization

Record the HTB machine or authorized lab target, target address, hostnames, access route, starting knowledge, time window, objective, and out-of-scope systems.

## Executive Summary

Summarize the verified path in terms of root cause and security impact. Use sanitized placeholders for credentials, flags, tokens, and private files.

## Attack Surface

| Port or URL | Service | Version or technology | Authentication | Evidence |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Initial Access Finding

**Title:** <short root-cause title>

**Status:** Observed / Inferred / Unverified

**Affected service:** <host, port, route, or share>

**Root cause:** <code, configuration, credential, or boundary failure>

**Evidence:** <raw output, request/response, file, or screenshot reference>

**Minimal reproduction:**

```text
<sanitized and reproducible steps for the authorized lab>
```

**Impact:** <what access or capability was obtained>

**Remediation:** <specific corrective action and verification>

## Identity and Host Transitions

| Step | Host | Identity before | Action | Identity after | Evidence |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## Privilege Escalation

Describe the candidate boundary, the evidence that made it plausible, the least invasive validation, the resulting identity, and the cleanup state. Reference `references/privilege-escalation.md` for the evidence pattern.

## Pivot or Lateral Movement

If applicable, record the approval, pivot host, internal destination, protocol, tunnel type, listener binding, route verification, identity context, and cleanup result. Do not include private keys or live credentials.

## Objective Proof

Record the minimum proof of the user, root, or lab objective. Redact the exact flag in public copies unless it is required for a private submission.

## Rejected Hypotheses

| Hypothesis | Test | Result | Why rejected |
| --- | --- | --- | --- |
|  |  |  |  |

## Reproducibility

| Step | Command or code reference | Working directory | Assumptions | Evidence path |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Cleanup and Limitations

State which temporary files, listeners, tunnels, tickets, uploaded files, accounts, services, or configuration changes were removed. List anything that could not be reverted and explain the residual risk.
