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

Map routes from links, forms, JavaScript, API documentation, robots files, source code, and observed redirects. Treat every hostname discovered in content as a lead that requires scope confirmation.

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
| Serialized state | Is integrity or type validation enforced? | Decode locally and compare a controlled field without changing privilege. |
| Upload or parser | What file type, metadata, and transformation path is used? | Upload a benign file with controlled metadata and observe processing. |

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
