# Challenge Playbooks

Use this guide for authorized, bounded challenge work. A challenge may be file-based, instance-based, or mixed. The platform’s live description is authoritative for scope, instance lifecycle, and flag format. Do not publish active challenge solutions or upload challenge files to a public repository.

## Intake and Triage

Record the category, difficulty, instance address and port if present, downloaded filenames, archive hash, supplied readme, allowed tools, objective, and evidence directory. Preserve the original archive and work on a copy. Do not execute unknown binaries or scripts until the readme and file inventory have been reviewed.

```bash
mkdir -p challenge/<name>/{original,work,evidence,notes,scripts,report}
sha256sum <archive> | tee challenge/<name>/notes/archive.sha256
7z l <archive> | tee challenge/<name>/notes/archive-list.txt
file challenge/<name>/work/* | tee challenge/<name>/notes/file-types.txt
```

If the challenge has a remote instance, treat its host and port as the only network scope. Start with a harmless banner or protocol check and use explicit timeouts. Never turn a challenge instance into a scanner for unrelated hosts.

## Universal Challenge Loop

1. Read the prompt and supplied readme completely.
2. Inventory files, formats, metadata, dependencies, and expected input or output.
3. Establish a local baseline with a benign input.
4. Form one hypothesis about the transformation, parser, trust boundary, or bug.
5. Build the smallest local test that can discriminate the hypothesis.
6. Capture outputs, exceptions, hashes, and environment details.
7. Escalate only after local evidence supports the next test.
8. Prove the flag or condition with the minimum required data.
9. Write a solution explanation that teaches the method without exposing protected active content.

## Web Challenges

Start by mapping routes, methods, headers, cookies, roles, forms, APIs, static files, and server-side dependencies. Establish a normal request and response before changing one input. Track authentication and authorization separately: a valid session does not prove access to another user’s object.

Prioritize the smallest controlled test for the relevant class:

| Observation | Bounded test |
| --- | --- |
| Reflected or stored input | Use a harmless marker first, then verify context and encoding. |
| Object identifier or API resource | Compare access to owned and unowned identifiers using two lab accounts if provided. |
| File path or download parameter | Test a non-sensitive known file within the challenge fixture. |
| Template or expression behavior | Use a non-destructive arithmetic marker before any command-oriented test. |
| Upload or parser boundary | Use a benign file with controlled metadata and compare server-side processing. |
| Signed or serialized client state | Decode locally, identify integrity protection, and do not guess keys without challenge support. |

Preserve request and response pairs with secrets redacted. Avoid automated recursion until a small manual map shows that it is necessary.

## Crypto Challenges

Identify the primitive, mode, key size, nonce or IV behavior, encoding layers, and message structure. Separate encoding from encryption. Check for repeated nonces, reused keystreams, weak randomness, known plaintext, predictable counters, oracle behavior, padding errors, key derivation mistakes, and implementation defects.

Use a local notebook or script that records input, output, and assumptions. Verify a recovered key or plaintext against more than one sample. Do not claim a cryptographic break because a decoder returns printable text. For remote oracles, send the minimum number of queries and respect the instance rate limit.

## Reversing Challenges

Perform static triage first:

```bash
file ./sample
sha256sum ./sample
strings -n 6 ./sample | tee evidence/strings.txt
readelf -hSWs ./sample 2>/dev/null | tee evidence/readelf.txt
objdump -d ./sample 2>/dev/null | head -n 200 | tee evidence/disassembly.txt
```

For managed or mobile binaries, identify the runtime and use an appropriate decompiler. For native binaries, map input, validation, transformations, and output. Use a debugger only in a disposable environment and begin with a benign input. Isolate anti-analysis behavior from actual flag logic. Do not run an untrusted sample on the host or connect it to the internet.

## Pwn and Binary Exploitation

Work in an isolated VM or local challenge container. Establish architecture, mitigations, input length, crash reproducibility, and the exact controllable state before developing an exploit. Prefer a local copy or provided instance and never test a payload against a non-challenge host.

A disciplined sequence is:

```text
identify binary and protections
→ find a benign input baseline
→ reproduce a controlled crash or state change
→ determine the primitive and offset
→ validate a non-destructive proof
→ assemble the minimum challenge-specific payload
→ prove the flag and preserve the environment
```

Record compiler or libc assumptions when supplied. Keep payloads parameterized and avoid persistence, destructive file operations, or network spread.

## Forensics and DFIR Challenges

Use a disposable analysis VM. Hash the original artifact and analyze a copy. Build an artifact inventory before opening files. Establish time zones and clock assumptions, then create a timeline from the narrowest relevant data sources.

| Artifact | Questions |
| --- | --- |
| Event logs | What account, process, host, logon type, and time window are involved? |
| Shell or command history | What command ran, from which context, and what object did it touch? |
| Registry hives | What persistence, execution, user, or network configuration is recorded? |
| Browser data | Which account, URL, download, cookie, or history event is relevant? |
| Memory image | What processes, connections, handles, tokens, and injected regions are present? |
| PCAP | What endpoints, protocols, authentication exchanges, and transfer sequence are supported? |
| Disk image or filesystem | What file system timestamps, deleted content, and user activity correlate with the incident? |
| Cloud logs | Which principal, API call, source address, resource, and permission change form the sequence? |

Use tool output as evidence, not as a verdict. Correlate at least two independent artifacts for material claims whenever the challenge provides them. Keep a question-to-artifact matrix and record why each answer is supported.

## OSINT Challenges

Define the question and the permitted public sources before searching. Use the smallest search surface, preserve URLs and access time, and distinguish primary evidence from reposts or speculation. Do not investigate real private individuals, infer sensitive personal traits, bypass access controls, or collect more personal data than the challenge requires. For images, record reverse-image search candidates, metadata, visible landmarks, and corroborating sources separately.

## Steganography

Preserve the original bytes, inspect metadata and file signatures, compare file length and structure, and test one extraction layer at a time. Use `strings`, `exiftool`, format-specific viewers, archive listing, and bit-plane or channel analysis as appropriate. Do not execute embedded files. Validate extracted text against the challenge’s expected flag grammar and record every transformation.

## Mobile Challenges

Analyze APK, IPA, or mobile traffic locally. Inventory manifests, exported components, permissions, embedded URLs, hard-coded secrets, certificate configuration, local databases, deep links, and client-side checks. Use a disposable emulator or device profile. Treat network endpoints as challenge scope only and preserve traffic captures with credentials removed from the final report.

## Hardware, ICS, and OT-Themed Challenges

Use the supplied simulator, firmware, packet capture, or local fixture. Identify the protocol, message framing, state machine, safety interlocks, and intended test boundary. Prefer read-only state queries and offline firmware analysis. Do not send control commands to real devices or public infrastructure. For protocol puzzles, build a local parser and replay only the minimum message sequence needed to prove the challenge condition.

## Blockchain and Smart-Contract Challenges

Work against the supplied local chain, emulator, or explicitly scoped instance. Identify accounts, balances, contract addresses, ABI, compiler assumptions, access-control roles, and transaction state. Reproduce the baseline transaction locally before testing one invariant or authorization hypothesis. Never broadcast transactions to a public chain or use real funds.

## AI/ML-Themed Challenges

Keep model and dataset analysis local unless the challenge explicitly provides a scoped endpoint. Inventory prompt or input format, preprocessing, model version, output constraints, and state. Test one controlled input at a time and avoid sending challenge data or secrets to third-party model APIs. Distinguish model behavior from application authorization and verify outputs independently.

## Coding, Miscellaneous, and Game-Focused Challenges

Read the protocol or prompt as a specification. Implement a small parser with strict framing, timeouts, and error handling. For games or interactive services, model state transitions and use harmless inputs before optimizing. Keep automated solvers deterministic and log inputs, outputs, and the reason each move was chosen.

## Challenge Completion

A completed challenge record contains the archive hash or instance identifier, the local environment, the hypothesis chain, the minimal solver or proof, the flag format check, and the evidence path. Do not include active challenge files, private flags, challenge secrets, or copied proprietary writeups in a public repository.
