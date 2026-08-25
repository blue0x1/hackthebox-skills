# Security Policy

## Supported Scope

This repository contains original procedural guidance for authorized labs plus user-supplied nimux documentation. It is not an authorization mechanism and does not grant permission to test any system. It must not be used to scrape, reproduce, summarize, compile, or derive an AI system, dataset, benchmark, or knowledge base from protected HTB content.

## Reporting a Repository Issue

Report exposed secrets, unsafe repository instructions, malicious changes, or a suspected supply-chain problem privately to the repository maintainers rather than opening a public issue. Do not include credentials, flags, VPN files, private keys, or target addresses in a public report.

If the repository does not yet have a private security contact configured, open a minimal public issue that says a private security report is needed, without including sensitive details.

## Safe Use

Use the skills only against HTB-owned or HTB-provided targets, or systems for which you have explicit written authorization. Follow the current HTB Platform Rules for target scope and publication permission. Keep scans bounded, avoid destructive behavior, review downloaded code before execution, and minimize collection of sensitive or unrelated data.

## Secrets

Never commit credentials, API keys, private keys, flags, VPN configuration, scan output containing sensitive data, or target-specific private artifacts. If a secret is committed accidentally, revoke or rotate it immediately, remove it from the working tree, and treat the repository history as exposed until it has been reviewed and rewritten appropriately.
