# Web and Application Security Playbook

Use this guide for authorized lab applications and APIs. It is designed for hypothesis-driven validation, not broad production scanning. Keep request volume low, retain request and response evidence, and redact credentials and tokens.

## Application Intake

Record the canonical URL, host header, port, TLS status, redirect chain, authentication state, user roles, input surfaces, and challenge or machine scope. Capture one baseline response per route before mutating parameters.

```bash
curl --silent --show-error --max-time 10 \
  -D evidence/home.headers \
  -o evidence/home.body \
  http://<host>:<port>/
```

Map routes from links, forms, JavaScript, API documentation, robots files, source code, exposed documentation, package manifests, redirects, certificates, and response headers. Treat every hostname discovered in content as a lead that requires scope confirmation.

Create an application inventory with:

- Base URLs, virtual hosts, ports, TLS names, and redirects.
- Technology clues from headers, cookies, static paths, error pages, HTML, JavaScript, package files, and source maps.
- Authentication states, user roles, and privilege boundaries.
- Input surfaces: query strings, paths, fragments, forms, JSON, XML, multipart bodies, headers, cookies, WebSocket messages, GraphQL queries, file uploads, and background jobs.
- Storage and execution boundaries: database, filesystem, object storage, template engine, shell, XML parser, browser, queue worker, cache, webhook, and outbound HTTP client.

## Hostname, Virtual Host, and Subdomain Enumeration

Only enumerate names within the authorized scope. Start from local evidence before external lookups: TLS certificates, redirects, HTML links, JavaScript bundles, API docs, robots files, application config, source code, Git remotes, and error messages.

For a machine or lab target, prefer small, bounded virtual-host checks against the in-scope IP and record the exact wordlist and Host header used. Stop when the target shows rate limits, wildcard behavior, or unrelated infrastructure.

```bash
ffuf -w <small-wordlist> -u http://<target>/ \
  -H 'Host: FUZZ.<domain>' \
  -timeout 5 -rate 20 -ac \
  -o evidence/vhost-ffuf.json -of json
```

For public or cloud-style challenge scopes, confirm that subdomain enumeration is explicitly allowed before querying DNS, certificate transparency, or third-party indexes. Do not enumerate unrelated parent domains, organization assets, or real customer infrastructure.

## Testing Order

1. Identify the request and response contract.
2. Test authentication and authorization separately.
3. Identify parser, filesystem, interpreter, template, database, and outbound-request boundaries.
4. Use a benign marker or known local fixture.
5. Compare status, size, headers, body, timing, and side effects.
6. Validate only the smallest behavior that proves the hypothesis.
7. Stop before destructive payloads, broad fuzzing, or scope expansion.

## Input and Trust-Boundary Matrix

| Boundary | Questions | Benign first test |
| --- | --- | --- |
| Object identifier | Can one role access another role’s object? | Compare two known lab objects with separate accounts. |
| File path | Is input normalized and constrained to an allowed root? | Request a known, non-sensitive fixture in the application directory. |
| URL or host | Does the server make outbound requests? | Use a lab-controlled endpoint or a local fixture if provided. |
| Template expression | Is input interpreted by a server-side template? | Use an arithmetic marker that has no side effect. |
| Command argument | Is input passed to an interpreter or shell? | Use a harmless identity or version query only when the lab requires execution testing. |
| Database query | Is input concatenated or parameterized? | Compare quote handling and a known true or false condition. |
| XPath query | Is XML path selection built from user input? | Compare quote handling and a known true or false predicate. |
| XML parser | Are external entities, DTDs, or parser options enabled? | Parse a benign local XML sample first and inspect parser configuration. |
| Serialized state | Is integrity or type validation enforced? | Decode locally and compare a controlled field without changing privilege. |
| Upload or parser | What file type, metadata, and transformation path is used? | Upload a benign file with controlled metadata and observe processing. |
| Browser sink | Does user-controlled data reach HTML, JavaScript, URL, or CSS contexts? | Use a harmless marker and inspect encoding in the rendered context. |
| Cache key | Can one user's response affect another user's cache entry? | Compare cache headers and vary behavior with benign parameters. |

## Web Vulnerability Coverage

Use this catalog to choose the next hypothesis. It is not a payload database and not a license to brute force. For every class, record the exact route, role, input, baseline response, changed response, and minimum safe proof.

### Authentication and Account Flows

Check registration, login, logout, password reset, invite links, email changes, MFA setup, remember-me cookies, session fixation, session rotation, lockout, and role assignment. Verify whether tokens expire, whether old sessions remain valid after password changes, and whether server-side authorization matches client-visible claims.

### Authorization and IDOR

Test horizontal and vertical access separately with two lab accounts or supplied roles. Compare object IDs, UUIDs, slugs, filenames, tenant IDs, organization IDs, GraphQL node IDs, numeric offsets, and indirect references. Do not access unrelated user data beyond the minimum proof needed in the lab.

### Injection Families

For SQL, NoSQL, LDAP, XPath, OS command, template, expression language, header, and mail injection, first identify the interpreter boundary from errors, behavior, or source code. Use benign true or false comparisons, controlled markers, and local reproduction where possible. Treat time-based, file-writing, command execution, and out-of-band checks as approval-gated actions.

### Cross-Site Scripting and Browser Contexts

Track the browser context before testing: HTML text, attribute, URL, JavaScript string, JSON script block, CSS, Markdown renderer, rich-text editor, PDF converter, or email template. Use harmless markers to verify reflection, storage, encoding, and sanitization. Avoid payloads that steal cookies, call third-party services, or affect other users.

### Request Forgery and Outbound HTTP

For SSRF, webhook, URL preview, import, avatar, PDF, XML, and callback features, identify allowlists, DNS resolution behavior, redirect handling, IP filtering, and protocol support. Prefer a lab-controlled endpoint or local fixture. Do not target cloud metadata, internal hosts, or adjacent networks unless explicitly in scope and approved.

### File, Path, and Archive Handling

Cover path traversal, local file inclusion, remote file inclusion, unsafe downloads, archive extraction, symlink handling, image processing, filename collisions, Unicode normalization, extension checks, and MIME sniffing. Start with known non-sensitive files and application fixtures. Do not read secrets or private files unless they are the explicit lab objective.

### Uploads and Content Processing

Check extension filtering, MIME validation, magic bytes, metadata processing, storage location, post-upload access controls, transformation jobs, antivirus hooks, thumbnailers, document converters, and whether uploads are served from the same origin. Use benign files first. Executable uploads, web shells, and parser crash probes require explicit lab justification.

### XML, XPath, and XXE

Identify XML inputs from content types, SOAP, SAML, SVG, RSS, DOCX, XLSX, config import, and API errors. In source, inspect parser flags for DTDs, external entities, network access, XInclude, schema validation, and entity expansion limits. For XPath, trace user input into query construction and compare controlled predicates. Avoid external entity callbacks unless the lab explicitly permits an out-of-band proof.

### Serialization, Tokens, and Cryptography Boundaries

Inspect cookies, JWTs, signed URLs, API keys, CSRF tokens, encrypted blobs, pickles, Java serialization, PHP serialization, YAML, and framework-specific session formats. Decode locally when safe. Check algorithm confusion, missing verification, weak secrets, replay, expiry, audience, issuer, nonce, and privilege claims. Do not brute force secrets except with explicit challenge scope and bounded local wordlists.

### API, GraphQL, and WebSocket Testing

Build a route and message table. Cover REST, GraphQL, RPC, gRPC gateways, WebSockets, Server-Sent Events, webhooks, and background jobs. Test schema exposure, authorization per object, mass assignment, pagination limits, batch operations, nested object authorization, content-type confusion, and inconsistent validation between client and server.

### Client-Side and JavaScript Analysis

Review JavaScript bundles, source maps, route definitions, API clients, feature flags, hidden endpoints, environment variables, error telemetry, and build artifacts. Treat discovered URLs, credentials, or tokens as leads requiring server-side verification, not proof. Do not use real third-party keys or call external services.

### CORS, CSRF, Clickjacking, and Browser Policy

Check CORS origin reflection, credentialed requests, preflight behavior, CSRF token scope, SameSite cookies, origin and referer validation, frame controls, content security policy, referrer policy, and mixed-content behavior. Validate with minimal same-site or lab-controlled origins only.

### Cache, Proxy, and Header Handling

Inspect cache headers, reverse proxy behavior, host header routing, forwarded headers, request smuggling indicators, response splitting, open redirects, and password reset URL generation. Keep tests small and stop before ambiguous behavior could affect other users or shared infrastructure.

### Dependency, Framework, and Known-CVE Triage

Identify frameworks, plugins, package versions, lockfiles, container images, CMS themes, and exposed admin panels. Prefer source and version evidence over blind probing. When a known CVE appears relevant, read the advisory, confirm affected version and configuration, and adapt only the minimal safe check needed for the lab.

## Authentication and Session Analysis

Record login request shape, cookie attributes, CSRF behavior, token format, role claims, session rotation, and logout invalidation. Use separate lab accounts when available to test authorization. Do not steal or publish another person’s session. Do not send session data to external services.

When a client-side token appears signed or encrypted, decode only the representation needed to understand its fields. Verify server-side authorization independently; a decoded role field is not proof that the server trusts it.

## Source and Configuration Review

When source code, debug output, stack traces, containers, or configuration files are supplied, analyze locally first. Search for route handlers, middleware, validation, file operations, subprocess calls, template rendering, database queries, secret loading, access-control checks, and error paths.

```bash
grep -RInE 'route|endpoint|subprocess|system\(|popen|eval\(|exec\(|render_template|SELECT|password|secret|token' <source-tree> \
  > evidence/source-keywords.txt || true
```

The keyword list is a starting point, not a vulnerability verdict. Read surrounding code and trace the data flow from input to sink.

For source-assisted analysis, build these notes before testing the live application:

- Entrypoints: routes, controllers, handlers, GraphQL resolvers, WebSocket handlers, queue consumers, CLI jobs, and template renderers.
- Trust boundaries: request parsing, authentication middleware, authorization checks, object lookup, deserialization, file handling, outbound requests, and database calls.
- Sensitive configuration: environment variables, secret loading, debug mode, storage paths, feature flags, signing keys, OAuth settings, SMTP settings, webhook URLs, and admin bootstrap logic.
- Dangerous sinks: SQL or NoSQL queries, XPath builders, LDAP filters, shell calls, template rendering, XML parsers, dynamic imports, eval-like behavior, file reads and writes, archive extraction, redirects, and HTTP clients.
- Missing tests or comments that reveal intended constraints.

Trace user-controlled values from source to sink. A finding is stronger when the code path, request, and observed behavior all agree.

## Git and Source Control Services

Git-backed services often become a web-to-source pivot in labs. Treat them as application surfaces first, then source repositories second.

Cover Gitea, GitLab, GitHub Enterprise, Bitbucket Server, cgit, GitWeb, plain `.git` exposure, package registries, CI logs, release assets, snippets, wikis, issues, merge requests, deploy keys, webhooks, runners, and container registries.

Checklist:

1. Confirm the host, product, version, and whether registration or anonymous browsing is allowed.
2. Map public projects, users, organizations, snippets, packages, releases, wiki pages, and issue trackers inside scope.
3. Review commit history for credentials, removed files, deployment scripts, config examples, and environment variable names.
4. Inspect CI/CD definitions such as `.gitlab-ci.yml`, GitHub Actions workflows, Drone, Woodpecker, Jenkinsfiles, and runner labels.
5. Check repository permissions with the supplied account only. Do not enumerate unrelated private repositories or users.
6. If clone access is authorized, clone to the evidence workspace, preserve the remote URL, and avoid pushing or opening pull requests.
7. Search locally for routes, secrets, dependencies, TODO notes, test fixtures, and deployment paths.
8. Treat discovered credentials as sensitive evidence. Validate only when necessary for the lab objective and never publish them.

For exposed `.git` directories, preserve a copy of retrieved objects and reconstruct locally. Do not hammer the server for every object path. Record exactly which files were accessible and why they are in scope.

## API Testing

Create a route table with method, path, authentication, required fields, response type, and authorization expectation. Use a small set of valid, invalid, missing, and boundary inputs. Preserve JSON structure and compare error messages without triggering rate limits.

For GraphQL or RPC interfaces, enumerate the schema only if the challenge exposes it and keep queries minimal. Do not use introspection or expensive queries against an uncontrolled service.

## File and Path Handling

Normalize path input before comparing it with the permitted directory. Check URL decoding, double decoding, separator variants, null bytes, symlinks, archive extraction, and alternate file names only when the application behavior and lab scope justify them. Use a known non-sensitive file as the first proof. Do not read system secrets or unrelated users’ files.

## Uploads and Parsers

Identify the storage path, filename generation, content-type handling, server-side transformation, post-upload access, and execution context. Use a benign file and inspect the resulting metadata or thumbnail. Do not upload executable content or a web shell unless the challenge explicitly requires controlled proof and the isolated target is in scope.

## Deserialization and Template Boundaries

Identify the serialization format, type restrictions, signing or encryption, and version assumptions. Reproduce parsing with a local copy first. For templates, demonstrate expression evaluation with a non-side-effect marker. Treat any command execution test as a separate approval-gated action.

## Browser-Assisted Actions

Use browser tooling only for the authorized lab application. Keep screenshots and request traces in the evidence directory. Before submitting a flag or altering application state, verify the target URL and request scope. Do not submit credentials, payments, or data to third-party services.

## Web Completion Criteria

A web finding is complete when the vulnerable boundary, input, authorization context, observed effect, and minimal remediation are documented. Include the baseline and comparison evidence, the exact route and method, the assumptions, and whether the behavior reproduces after a fresh session.
