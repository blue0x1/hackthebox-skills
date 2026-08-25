# Study Roadmap

Use this roadmap to choose an appropriate learning loop without relying on a static machine catalog or copying writeups. The live platform label, the user’s skill level, and the authorized objective determine the next exercise.

## Progression by Mode

| Stage | Machines | Challenges | Sherlocks | ProLabs |
| --- | --- | --- | --- | --- |
| Foundation | Easy targets with clear service inventory and one or two transitions | Very Easy or Easy file and web tasks | Easy log analysis and basic artifact triage | Beginner-friendly enclosed network with a known entry point |
| Development | Medium targets with source review, credential context, or local privilege boundaries | Easy or Medium category-specific tasks | Medium memory, cloud, AD, or malware investigations | Intermediate network mapping and first pivot |
| Advanced | Hard targets with multiple identities, hosts, or protocols | Hard tasks requiring custom reasoning or binary analysis | Hard multi-source correlation and threat hunting | AD, lateral movement, trust, and segmentation workflows |
| Expert | Insane targets with deep dependency chains and specialized state | Insane pwn, reversing, crypto, or mixed tasks | Insane incident reconstruction and attribution analysis | Hardened, multi-host environments with several verified pivots |

## How to Use Hints and Writeups

Use the platform’s own hints, task text, and permitted retired-content resources before seeking external explanations. Ask for the smallest hint that answers the current blocker. When a human studies a writeup, record only a short concept note in their own words and return to the lab to reproduce the method independently.

Do not paste protected writeups, active solutions, challenge files, Sherlock evidence, flags, credentials, or proprietary course material into an AI context. Do not scrape or compile writeup indexes into a dataset or knowledge base. Verify publication permission under the current HTB rules before sharing any lab-specific explanation.

## Learning Loop

1. Define one skill objective, such as DNS mapping, API authorization, memory analysis, or SSH forwarding.
2. Choose a target whose live difficulty and scope match that objective.
3. Attempt the task independently with a hypothesis log.
4. Take one permitted hint or consult one permitted human-readable reference only when blocked.
5. Reproduce the concept on the authorized target without copy-pasting secrets or protected content.
6. Write a sanitized note explaining the generic technique, the evidence, the failure mode, and the remediation.
7. Revisit the same concept in another category or operating system.

## Coverage Matrix

Track concepts rather than target names:

| Concept family | Minimum evidence to demonstrate mastery |
| --- | --- |
| Reconnaissance | Service, version, hostname, and scope-linked attack-surface record. |
| Web | Baseline request, input boundary, authorization context, observed effect, and remediation. |
| Linux | Identity, privilege boundary, minimal validation, and cleanup. |
| Windows and AD | Host, domain, principal, protocol, relationship, transition, and evidence. |
| Pivoting | Approved pivot, route verification, one internal service test, and cleanup. |
| Forensics | Artifact hash, timeline, correlated evidence, question answer, and uncertainty. |
| Malware | Static triage, isolated dynamic behavior if required, indicators, and snapshot cleanup. |
| Pwn or reversing | Architecture, mitigations, controlled baseline, primitive or logic, and local proof. |
| Crypto | Primitive and implementation model, tested hypothesis, verification, and query budget. |
| OSINT | Source provenance, corroboration, scope, and privacy minimization. |

## Mastery Check

A learner should be able to explain why the next action is needed, what result would falsify the hypothesis, how the action is bounded, what evidence proves the result, and how the environment is restored. Speed is secondary to correctness, reproducibility, and safe scope control.
