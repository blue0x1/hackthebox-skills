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

## Category Router

HTB-style challenge categories commonly include Web, Reversing, Pwn, Crypto, Forensics, OSINT, Stego, Mobile, Hardware, Blockchain, AI/ML, Coding, Misc, ICS, and game-focused entries. Some platform filters may show a smaller or changing subset. Use the live challenge page as the authority for scope and files.

| Category | First inventory | Safe local focus |
| --- | --- | --- |
| Web | Routes, requests, source, roles, API docs | Request contract and one input boundary. |
| Reversing | File type, architecture, strings, imports, runtime | Static control-flow and validation logic. |
| Pwn | Binary, protections, libc, protocol, crash input | Controlled local crash and primitive proof. |
| Crypto | Encoding, primitive, parameters, samples, oracle | Mathematical assumption and local verification. |
| Forensics | Artifact hash, type, timeline sources | Evidence inventory and question ledger. |
| OSINT | Question, allowed public sources, primary evidence | Corroborated source chain with timestamps. |
| Stego | Container format, metadata, signatures, layers | One extraction layer at a time. |
| Mobile | APK/IPA, manifest, strings, endpoints, storage | Client logic and local data review. |
| Hardware | Firmware, capture, datasheet, protocol, signals | Offline parsing and emulator/simulator work. |
| Blockchain | Chain type, contracts, ABI, accounts, state | Local chain state and invariant checks. |
| AI/ML | Model, prompt, dataset, preprocessing, endpoint | Controlled input and output constraints. |
| Coding | Protocol, input format, limits, scoring | Deterministic parser and solver. |
| Misc | File types, protocol clues, puzzle rules | Decompose into known sub-problems. |
| ICS/game | Protocol, state machine, simulator, safety limits | Local state model and read-only transitions. |

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

Coverage checklist:

- Classical ciphers, substitution, transposition, and custom encodings.
- XOR, stream-cipher misuse, repeated key material, nonce reuse, and known plaintext.
- Block-cipher mode misuse, padding behavior, IV control, and oracle-style responses.
- RSA, Diffie-Hellman, elliptic-curve, lattice, and number-theory assumptions when challenge evidence supports them.
- Hashing, MACs, signatures, length extension, weak randomness, seed recovery, and key derivation mistakes.
- Serialization, compression, base encodings, byte order, and message framing.

Keep attacks local unless the challenge supplies an oracle. For remote services, record query count and stop when the hypothesis is proven or rejected.

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

Expanded reversing workflow:

1. Classify format: ELF, PE, Mach-O, .NET, JVM, Python bytecode, Go, Rust, packed binary, firmware blob, APK, IPA, WASM, or script.
2. Identify architecture, endianness, compiler, symbols, imports, strings, resources, sections, and packer indicators.
3. Build a function map around input parsing, validation, crypto, decompression, anti-debugging, file I/O, network I/O, and output.
4. Reconstruct algorithms in a small local script rather than patching the binary first.
5. Use dynamic analysis only after static triage, in a disposable VM with blocked or simulated networking.
6. If patching is useful, patch only for observation and preserve the original hash.

For malware-like samples, switch to `forensics-and-malware.md` and treat execution as isolated dynamic analysis.

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

Coverage checklist:

- Stack, heap, format string, integer, type confusion, race, logic, sandbox, and seccomp-style boundaries.
- Mitigations: NX, PIE, RELRO, canaries, ASLR, stack alignment, Fortify, safe-linking, and allocator version.
- Inputs: argv, stdin, sockets, files, menu protocols, environment variables, and serialized messages.
- Proof: controlled crash, controlled read/write, instruction pointer influence, leak, or state transition.
- Reliability: local/remote libc mismatch, timeout handling, retries, and clean process exit.

Do not include public exploit code in the repository. Keep challenge-specific solvers private unless publication is allowed.

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

Additional challenge types include email headers and mailboxes, cloud audit logs, container images, Kubernetes artifacts, browser profiles, mobile backups, chat exports, EDR alerts, SIEM exports, document macros, ransomware notes, backup sets, and mixed disk/memory/network evidence. Normalize timestamps early and keep raw parser output separate from analyst notes.

## OSINT Challenges

Define the question and the permitted public sources before searching. Use the smallest search surface, preserve URLs and access time, and distinguish primary evidence from reposts or speculation. Do not investigate real private individuals, infer sensitive personal traits, bypass access controls, or collect more personal data than the challenge requires. For images, record reverse-image search candidates, metadata, visible landmarks, and corroborating sources separately.

Coverage checklist:

- Images, maps, landmarks, weather, shadows, metadata, usernames, domains, certificates, source code references, public posts, breach-free public records, and archived pages.
- Separate primary evidence from mirrors, AI summaries, reposts, and stale caches.
- Save citation URLs, access times, and why each source answers the challenge question.
- Avoid contacting real people, logging into personal accounts, or collecting unrelated personal data.

## Steganography

Preserve the original bytes, inspect metadata and file signatures, compare file length and structure, and test one extraction layer at a time. Use `strings`, `exiftool`, format-specific viewers, archive listing, and bit-plane or channel analysis as appropriate. Do not execute embedded files. Validate extracted text against the challenge’s expected flag grammar and record every transformation.

Check images, audio, video, archives, PDFs, fonts, QR codes, barcodes, whitespace, Unicode, network captures, filesystem slack, alternate data streams, and nested containers. Record every extraction command and intermediate hash.

## Mobile Challenges

Analyze APK, IPA, or mobile traffic locally. Inventory manifests, exported components, permissions, embedded URLs, hard-coded secrets, certificate configuration, local databases, deep links, and client-side checks. Use a disposable emulator or device profile. Treat network endpoints as challenge scope only and preserve traffic captures with credentials removed from the final report.

Android coverage includes manifests, activities, services, broadcast receivers, content providers, intents, exported components, deep links, WebViews, native libraries, assets, resources, SQLite, SharedPreferences, keystores, certificate pinning, and obfuscation. iOS coverage includes Info.plist, URL schemes, entitlements, keychain usage, local storage, frameworks, Objective-C or Swift metadata, and network configuration.

## Hardware, ICS, and OT-Themed Challenges

Use the supplied simulator, firmware, packet capture, or local fixture. Identify the protocol, message framing, state machine, safety interlocks, and intended test boundary. Prefer read-only state queries and offline firmware analysis. Do not send control commands to real devices or public infrastructure. For protocol puzzles, build a local parser and replay only the minimum message sequence needed to prove the challenge condition.

Hardware coverage includes firmware extraction, file systems, boot logs, UART/JTAG clues, EEPROM dumps, radio captures, logic-analyzer traces, CAN, BLE, Zigbee, RFID, USB descriptors, and embedded web interfaces. ICS coverage includes Modbus, S7, DNP3, OPC UA, BACnet, MQTT, and custom telemetry only when supplied by the challenge. Treat physical-control semantics as safety-sensitive even in simulated data.

## Blockchain and Smart-Contract Challenges

Work against the supplied local chain, emulator, or explicitly scoped instance. Identify accounts, balances, contract addresses, ABI, compiler assumptions, access-control roles, and transaction state. Reproduce the baseline transaction locally before testing one invariant or authorization hypothesis. Never broadcast transactions to a public chain or use real funds.

Coverage checklist:

- Solidity, Vyper, EVM bytecode, proxy patterns, storage layout, events, modifiers, access control, arithmetic assumptions, signature verification, reentrancy, callbacks, flash-loan-like state, oracles, token standards, and initialization.
- Non-EVM chains only when the challenge supplies tooling or documentation.
- Keep private keys, mnemonic phrases, and RPC URLs out of public notes.

## AI/ML-Themed Challenges

Keep model and dataset analysis local unless the challenge explicitly provides a scoped endpoint. Inventory prompt or input format, preprocessing, model version, output constraints, and state. Test one controlled input at a time and avoid sending challenge data or secrets to third-party model APIs. Distinguish model behavior from application authorization and verify outputs independently.

Coverage includes prompt injection, tool-use boundaries, retrieval data leakage, classifier evasion, data poisoning in supplied datasets, model inversion in toy settings, unsafe deserialization in ML pipelines, notebook secrets, feature preprocessing bugs, and evaluation harness mistakes. Keep tests deterministic and avoid uploading challenge data to external model providers.

## Coding, Miscellaneous, and Game-Focused Challenges

Read the protocol or prompt as a specification. Implement a small parser with strict framing, timeouts, and error handling. For games or interactive services, model state transitions and use harmless inputs before optimizing. Keep automated solvers deterministic and log inputs, outputs, and the reason each move was chosen.

Coding coverage includes parsers, graph search, dynamic programming, constraint solving, SAT/SMT-style modeling, pathfinding, scheduling, compression, checksums, protocol automation, and streaming inputs. Game coverage includes rules engines, RNG analysis, state search, replay logs, map parsing, collision or physics assumptions, and scoreboard protocols. Do not automate against unrelated public game servers.

## Challenge Completion

A completed challenge record contains the archive hash or instance identifier, the local environment, the hypothesis chain, the minimal solver or proof, the flag format check, and the evidence path. Do not include active challenge files, private flags, challenge secrets, or copied proprietary writeups in a public repository.
