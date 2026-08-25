# Core Methodology

This document defines the common operating model for authorized lab work. It is original guidance and intentionally avoids reproducing solution paths or protected platform content.

## Engagement Modes

Select one mode before acting. A user may combine modes, such as a machine plus an internal challenge or a ProLab plus a Sherlock-style incident review.

| Mode | Primary objective | First artifact | Success proof |
| --- | --- | --- | --- |
| Machine | Enumerate a scoped host and validate an access or privilege path | Target address, scope, and starting knowledge | User and root or objective flag proof, with evidence chain |
| Challenge | Solve a bounded application, file, or service task | Downloaded archive, prompt, or instance details | Flag or challenge condition plus a minimal explanation |
| Sherlock | Reconstruct a defensive incident from supplied evidence | Package readme and artifact inventory | Answer ledger with artifact provenance and correlated timeline |
| ProLab | Navigate an enclosed multi-host corporate environment | Entry point, VPN route, subnet map, and objective list | Host, credential, trust, and objective graph with cleanup notes |
| Mixed case | Coordinate two or more modes | Case map and explicit dependencies | Separate evidence streams joined by verified transitions |

## Authorization Gate

Before network activity or execution of supplied artifacts, collect the target, exact scope, objective, access method, allowed protocols, time window, credentials or hashes available, write permissions, callback addresses if needed, and evidence directory. If a value is unknown, use read-only local inspection or ask the user. Never infer that an adjacent host or discovered route is in scope.

Treat the following as high-risk and require explicit approval in the case notes: pivot helper deployment, active relay or coercion, credential spraying, password changes, domain replication, secrets extraction, GPO or ACL changes, persistence, remote service creation, binary execution on a second host, and destructive file operations.

## Difficulty Profiles

Difficulty is a planning signal, not permission to be more aggressive. The live platform label is authoritative when available; the profile below describes how to allocate reasoning effort.

| Profile | Planning behavior | Evidence standard |
| --- | --- | --- |
| Very Easy or Easy | Start with a small surface map and one hypothesis. Prefer direct service misconfiguration or a clearly documented application behavior. | One reproducible transition per finding. |
| Medium | Expect chained evidence, source review, credential reuse, or a local privilege boundary. Split the chain into independently tested transitions. | Every credential, session, and privilege change must have a source and validation. |
| Hard | Expect multiple identities, protocols, hosts, trust relationships, or custom logic. Maintain a graph and test the highest-value edge first. | Preserve protocol context, host context, identity, and rejected paths. |
| Insane | Expect deep dependency chains, specialized technologies, cross-host routing, or several alternative paths. Work in small milestones and checkpoint assumptions. | Keep immutable raw evidence, precise timestamps, environment details, and rollback or cleanup state. |

## Evidence Model

Maintain separate raw evidence and interpretation. A conclusion is not complete until it has a source, a test, and a result.

```text
Observation: directly seen output, artifact, request, or file property
Source: command, file hash, URL, packet range, event ID, or screenshot reference
Hypothesis: security or investigation meaning being considered
Test: one bounded action that can confirm or reject the hypothesis
Result: observed outcome, including failure
Confidence: observed | strongly supported | inferred | unverified | rejected
Next action: one discriminating step
```

For a multi-host case, add these graph edge types: `reaches`, `authenticates-as`, `can-read`, `can-write`, `trusts`, `routes-to`, `executes-as`, `contains`, and `proves`. Keep edges directional and attach evidence identifiers.

## Universal Investigation Loop

1. Define the question and expected observation.
2. Inspect local artifacts, existing output, and the target’s documented interface.
3. Choose the smallest bounded command or test.
4. Capture stdout, stderr, status, timestamp, and output path.
5. Compare the result with the hypothesis.
6. Update the evidence table and graph.
7. Decide whether to continue, revise the hypothesis, or stop.

Do not issue a long list of speculative commands. Prefer a sequence of small tests that reduce uncertainty.

## Stop Conditions

Stop and ask when the next action would affect a new host, require an unreviewed payload, change access control, create persistence, extract broad secrets, risk lockout, increase request volume materially, or conflict with the lab’s readme or stated scope. Stop on signs of instability and preserve the last known-good state.

## Artifact Handling

Use a dedicated disposable VM for suspicious Sherlock or challenge artifacts. Read the supplied readme before extraction. Hash the original archive, work on a copy, and record extraction paths. Do not execute binaries or scripts merely because they are present. Prefer static inspection and isolated snapshots. Do not upload artifacts, secrets, or extracted data to third-party services.

## Source and Writeup Policy

Use official platform documentation for platform mechanics and independently licensed public documentation for generic security techniques. Do not scrape, reproduce, summarize, or compile active or protected HTB writeups into an AI skill. Do not publish active solutions, challenge files, flags, credentials, or proprietary course material. Use placeholders and link to official guidance without copying its protected content.

## Reporting Quality

A complete report explains what was observed, why it mattered, how it was tested, what was not tested, and how to reproduce the result inside the authorized lab. Use sanitized evidence references and explicitly mark uncertainty. Do not equate a tool banner, version string, or guessed credential with a verified finding.
