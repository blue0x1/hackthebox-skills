# Hack The Box Skills for Claude and Codex

![logo](https://academy.hackthebox.com/images/logo.svg)

A practical, safety-first skill pack for authorized lab work across Machines, Challenges, Sherlocks, ProLabs, and Academy-style exercises with Claude and Codex.

> **Important:** This is an unofficial community project. Hack The Box and related names are trademarks of their respective owners. Use these skills only against HTB-owned or HTB-provided lab targets, or systems for which you have explicit written authorization.

## What This Repository Provides

The repository contains two complementary skills:

| Skill | Best suited for | Emphasis |
| --- | --- | --- |
| `hackthebox-claude` | Interactive work with Claude | Conversational checkpoints, hypothesis tracking, careful scope confirmation, and evidence-backed explanations. |
| `hackthebox-codex` | Terminal and code-centric work with Codex | Local-first artifact analysis, reviewable scripts, bounded execution, captured output, and reproducible changes. |

Both skills use the same original playbooks for machine methodology, web applications, privilege boundaries, Windows and Active Directory, challenges, Sherlock investigations, forensics, malware analysis, SSH pivoting, and nimux integration. The platform-specific instructions are intentionally separate so each agent can follow the conventions of its host environment without losing the shared safety model. The package is organized for progressive disclosure: load the entrypoint first, then read only the reference needed for the current case.

## Reference Catalog

The entrypoints route to detailed references using progressive disclosure:

| Reference | Coverage |
| --- | --- |
| `core-methodology.md` | Mode selection, difficulty profiles, authorization, evidence, graph edges, and stop conditions. |
| `machine-playbooks.md` | Easy through Insane machines, Linux, Windows, Active Directory, lateral movement, and completion criteria. |
| `challenge-playbooks.md` | Web, crypto, reversing, pwn, forensics, OSINT, stego, mobile, hardware, blockchain, AI/ML, coding, miscellaneous, ICS, and game-focused work. |
| `sherlock-playbooks.md` | DFIR, SOC, malware analysis, threat hunting, threat intelligence, cloud investigations, timelines, and question ledgers. |
| `pivoting-and-ssh.md` | ProxyJump, SOCKS, local and remote forwards, multi-hop routing, file transfer, verification, and cleanup. |
| `ad-and-windows.md` | SMB, LDAP, Kerberos, WinRM, RDP, MSSQL, AD CS, delegation, ACLs, GPOs, secrets, and replication guardrails. |
| `web-application.md` | Web and API mapping, authentication, authorization, path handling, uploads, parsers, and source review. |
| `privilege-escalation.md` | Linux, Windows, service, scheduled-task, credential, container, and kernel-boundary analysis. |
| `forensics-and-malware.md` | Artifact integrity, Windows and Linux evidence, memory, disk, PCAP, timelines, and isolated malware triage. |
| `exploit-review.md` | Safe review and adaptation of supplied or public proof-of-concept code. |
| `tooling-and-output.md` | Bounded commands, structured output, naming, hashing, failures, and evidence bundles. |
| `nimux-usage.md` and `nimux-command-surface.txt` | User-supplied nimux installation paths: release binary, Debian package, Docker, BlackArch, Arch AUR, and Nimble, plus version checks and command families. |

## Repository Layout

```text
.
├── AGENTS.md
├── CLAUDE.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── SECURITY.md
├── .github/workflows/validate.yml
├── skills/
│   ├── hackthebox-claude/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   └── templates/
│   └── hackthebox-codex/
│       ├── SKILL.md
│       ├── references/
│       └── templates/
└── tools/validate_skills.py
```

## Installation and Use

Clone the repository:

```bash
git clone https://github.com/blue0x1/hackthebox-skills.git
cd hackthebox-skills
```

Validate the package before installing:

```bash
python3 tools/validate_skills.py
```

### Install for Codex

Copy the Codex skill into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R skills/hackthebox-codex ~/.codex/skills/
```

If you want Codex to use the project-level safety instructions automatically, keep `AGENTS.md` in the root of the workspace where you run Codex. For a different workspace, copy it there:

```bash
cp AGENTS.md /path/to/your/workspace/
```

Then start Codex from that workspace and ask it to use the Hack The Box skill for authorized lab work.

### Install for Claude

Copy the Claude skill into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills
cp -R skills/hackthebox-claude ~/.claude/skills/
```

If you want Claude to use the project-level safety instructions automatically, keep `CLAUDE.md` in the root of the workspace where you run Claude. For a different workspace, copy it there:

```bash
cp CLAUDE.md /path/to/your/workspace/
```

Then restart or reload Claude so it can discover the new skill.

### Manual Installation

If your client uses a custom skill directory, copy only the matching skill folder:

```bash
# Codex-oriented workflow
cp -R skills/hackthebox-codex /path/to/client/skills/

# Claude-oriented workflow
cp -R skills/hackthebox-claude /path/to/client/skills/
```

Each installed skill directory must include `SKILL.md`, `references/`, and `templates/`.

Start each lab by confirming the target, scope, challenge or machine name, objective, and constraints. The skills are designed to guide the workflow; they do not replace the HTB VPN, target access, or tools installed in the user’s environment.

A typical request might look like this:

```text
I have explicit authorization to work on the HTB machine at <TARGET>.
Use the Hack The Box skill to enumerate it conservatively, save evidence under
htb/<target>/, and stop before any scope expansion or unreviewed payload.
```

Do not provide a target address, credential, flag, or private artifact in a public issue. Use placeholders in examples and redact sensitive values in reports.

## Safety Model

The skills enforce a narrow, evidence-led workflow:

1. Confirm authorization and exact scope before network activity.
2. Prefer local analysis and read-only inspection.
3. Use bounded scans, small wordlists, explicit timeouts, and one hypothesis at a time.
4. Review downloaded code before execution and avoid destructive behavior.
5. Preserve raw output separately from summaries.
6. Minimize collection of credentials, flags, private files, and unrelated data.
7. Distinguish observed facts from inferences and unverified hypotheses.

This project intentionally excludes machine-specific write-ups, active challenge solutions, Sherlock evidence packages, credentials, flags, VPN files, persistence mechanisms, malware, and destructive testing instructions. It also does not scrape, reproduce, summarize, compile, or derive an AI dataset or knowledge base from HTB content.

## Research and Compliance

The methodology was informed by official high-level platform documentation and by the user-supplied nimux installation and command-surface references. The repository does not copy or compile public HTB writeups. Current publication permissions and AI-use restrictions must be checked against the [HTB Platform Rules](https://help.hackthebox.com/en/articles/12325897-hack-the-box-platform-rules) before sharing any lab-specific solution. See `skills/hackthebox-claude/references/source-map.md` for the source map and compliance notes.

## Contributing

Contributions are welcome when they improve clarity, reproducibility, accessibility, or safety. Read `CONTRIBUTING.md` before opening a pull request. Add sanitized examples and service-agnostic guidance rather than spoilers for individual HTB targets.

## Validation

Run the repository validator locally from the project root:

```bash
python3 tools/validate_skills.py
```

The continuous-integration workflow runs the same checks on pushes and pull requests. Validation checks frontmatter, line limits, required resources, placeholder remnants, and common credential or private-key patterns. It does not attempt to scan or exploit any target.

## Contributors

- [blue0x1](https://github.com/blue0x1)

## License

This repository is released under the MIT License. See `LICENSE`.
