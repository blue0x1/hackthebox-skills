# Contributing

Thank you for helping improve the Hack The Box skills for Claude and Codex. Contributions should make authorized lab work more understandable, reproducible, and safe.

## Scope

Submit platform-neutral workflow improvements, service-enumeration guidance, sanitized templates, documentation fixes, validation improvements, and examples that do not reveal solutions for individual HTB targets. Keep Claude-specific behavior in `skills/hackthebox-claude/` and Codex-specific behavior in `skills/hackthebox-codex/`.

Do not submit credentials, flags, VPN configuration, target-specific private files, undisclosed vulnerabilities, persistence mechanisms, malware, denial-of-service instructions, credential-spraying workflows, active or protected solutions, or content copied from HTB materials. Do not scrape or transform HTB content into a dataset, knowledge base, training corpus, benchmark, evaluation set, or synthetic derivative. Use placeholders such as `<TARGET>`, `<LHOST>`, and `<LPORT>` in examples.

## Before Opening a Pull Request

Run the local validator:

```bash
python3 tools/validate_skills.py
```

Check that each skill has valid YAML frontmatter, remains under 500 lines, links only to files included in the package, and contains no placeholder TODO text or sensitive material. Keep raw lab evidence outside the repository. Confirm that any external reference is independently licensed, official platform guidance, or user-supplied material with permission to include.

## Pull Request Expectations

Explain the problem, the proposed change, and how it was tested. Prefer small, focused changes. If adding a service check, describe the observation it is intended to confirm and the safety boundary around it. If changing a template, include a sanitized example of the resulting format.

Maintainers may request wording changes when an example is too target-specific, overly aggressive, or difficult to reproduce safely.

## Code of Conduct

Be respectful, assume good faith, and keep technical discussion focused on improving the project. Do not request or publish other users’ credentials, flags, private write-ups, or target access details.
