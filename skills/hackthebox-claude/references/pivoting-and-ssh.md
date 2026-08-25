# Pivoting and SSH Reference

Use these patterns only when the pivot host and internal destinations are explicitly in scope. A pivot is not permission to reach every route visible from the pivot. Record the operator host, pivot host, internal destination, protocol, listener address, local and remote ports, account, key or credential source, start time, and cleanup command before deployment.

## Pivot Approval Record

```text
Authorization: <ticket, lab scope, or user confirmation>
Operator host: <operator-host>
Pivot host: <pivot-host>
Internal destination: <internal-host-or-subnet>
Allowed protocol and port: <protocol>/<port>
Tunnel type: ProxyJump | SOCKS | local forward | remote forward
Listener binding: <loopback-or-approved-interface>
Evidence directory: <path>
Cleanup plan: <process and temporary file removal>
```

Bind listeners to loopback by default. Do not expose a SOCKS listener or forwarded port to a shared network unless the lab explicitly requires it.

## Direct SSH Baseline

Validate the account and host before adding forwarding. Prefer key authentication with explicit identity selection and strict host-key handling.

```bash
ssh \
  -o IdentitiesOnly=yes \
  -o ServerAliveInterval=30 \
  -o ServerAliveCountMax=3 \
  -o ConnectTimeout=10 \
  -i ~/.ssh/<lab-key> \
  <user>@<pivot-host> \
  'whoami && hostname && id'
```

If password authentication is required, use the client’s protected prompt or an approved secret store. Do not put passwords in shell history, scripts, process arguments, or public notes.

## ProxyJump for One Hop

Use `ProxyJump` when the internal host accepts SSH and the pivot can reach it. The operator connects to the internal host through the pivot without opening a general-purpose proxy.

```bash
ssh \
  -J <pivot-user>@<pivot-host> \
  -o IdentitiesOnly=yes \
  -o ConnectTimeout=10 \
  -i ~/.ssh/<lab-key> \
  <internal-user>@<internal-host> \
  'whoami && hostname && ip route'
```

If the pivot and internal host use different keys, configure them explicitly:

```sshconfig
Host lab-pivot
    HostName <pivot-host>
    User <pivot-user>
    IdentityFile ~/.ssh/<pivot-key>
    IdentitiesOnly yes
    ServerAliveInterval 30
    ServerAliveCountMax 3

Host lab-internal
    HostName <internal-host>
    User <internal-user>
    IdentityFile ~/.ssh/<internal-key>
    IdentitiesOnly yes
    ProxyJump lab-pivot
    ConnectTimeout 10
```

Then verify with:

```bash
ssh lab-internal 'whoami; hostname; ip route'
```

Do not disable host-key checking as a troubleshooting shortcut. If a lab host is redeployed, remove only the affected lab entry from the operator’s known-hosts file after verifying the new fingerprint through the lab interface.

## Dynamic SOCKS Pivot

Use a loopback SOCKS listener when several explicitly scoped internal services must be reached through one pivot. The `-N` option avoids starting a remote shell; `-f` may be used only after authentication and forwarding have been verified interactively.

Start the tunnel:

```bash
ssh \
  -N \
  -D 127.0.0.1:<socks-port> \
  -o ExitOnForwardFailure=yes \
  -o ServerAliveInterval=30 \
  -o ServerAliveCountMax=3 \
  -o ConnectTimeout=10 \
  -i ~/.ssh/<lab-key> \
  <pivot-user>@<pivot-host>
```

Verify that the local listener exists and test one approved destination:

```bash
ss -lntp | grep ':<socks-port>'
curl --silent --show-error --max-time 10 \
  --socks5-hostname 127.0.0.1:<socks-port> \
  http://<internal-host>:<internal-port>/ \
  -o evidence/internal-response.txt
```

Use a proxy-aware client for the specific protocol. For example, a local tool may use:

```bash
proxychains4 -q ssh <internal-user>@<internal-host> 'whoami && hostname'
```

Prefer `socks5-hostname` when internal DNS names must resolve through the pivot. Do not assume every UDP protocol or every client supports SOCKS. Verify the client’s proxy behavior before interpreting a timeout as a target result.

## Local Port Forward

Use a local forward when one internal TCP service is needed. The operator’s loopback port maps to the internal destination as seen from the pivot.

```bash
ssh \
  -N \
  -L 127.0.0.1:<local-port>:<internal-host>:<internal-port> \
  -o ExitOnForwardFailure=yes \
  -o ServerAliveInterval=30 \
  -o ConnectTimeout=10 \
  -i ~/.ssh/<lab-key> \
  <pivot-user>@<pivot-host>
```

Verify with a bounded client request:

```bash
curl --silent --show-error --max-time 10 \
  http://127.0.0.1:<local-port>/ \
  -o evidence/forwarded-response.txt
```

For TLS or a protocol whose host identity matters, preserve the intended Host header or protocol name rather than concluding that a local address is the real service identity. Document both endpoints in the report.

## Remote Port Forward

Use a remote forward when an in-scope internal service must connect back to an operator listener. Confirm that the remote binding and callback direction are explicitly allowed. Bind the remote side to loopback unless the lab requires another interface.

Start a local test listener first:

```bash
socat -v TCP-LISTEN:<operator-port>,bind=127.0.0.1,reuseaddr,fork -
```

In another terminal, establish the reverse forward:

```bash
ssh \
  -N \
  -R 127.0.0.1:<remote-port>:127.0.0.1:<operator-port> \
  -o ExitOnForwardFailure=yes \
  -o ServerAliveInterval=30 \
  -o ConnectTimeout=10 \
  -i ~/.ssh/<lab-key> \
  <pivot-user>@<pivot-host>
```

From the approved remote context, connect to `127.0.0.1:<remote-port>` and verify that the operator receives only the expected test bytes. Do not expose the forward to unrelated users or use it for persistence.

## Multi-Hop Forwarding

For a chain of two or more pivots, prefer a `ProxyJump` chain for SSH destinations:

```bash
ssh \
  -J <user1>@<pivot1>,<user2>@<pivot2> \
  -o ConnectTimeout=10 \
  -i ~/.ssh/<lab-key> \
  <user3>@<internal-host> \
  'whoami && hostname'
```

For non-SSH services, create the tunnel from the nearest approved pivot or use a SOCKS chain only when each hop is documented. Test hop one, then hop two, then the destination. Never debug a multi-hop failure by broadening scan scope automatically.

## File Transfer Through a Pivot

Transfer only named, in-scope files. Use `scp` with `ProxyJump`, preserve hashes, and avoid recursive collection.

```bash
scp \
  -o ProxyJump=<pivot-user>@<pivot-host> \
  -o IdentitiesOnly=yes \
  -i ~/.ssh/<lab-key> \
  <internal-user>@<internal-host>:/path/to/<approved-file> \
  evidence/<approved-file>
sha256sum evidence/<approved-file> | tee evidence/<approved-file>.sha256
```

For a local forward to an SFTP service, keep the service bound to loopback:

```bash
ssh -N \
  -L 127.0.0.1:<local-port>:<internal-host>:22 \
  -o ExitOnForwardFailure=yes \
  -i ~/.ssh/<lab-key> \
  <pivot-user>@<pivot-host>

sftp -P <local-port> -i ~/.ssh/<internal-key> <internal-user>@127.0.0.1
```

Do not upload payloads, add keys, or modify remote files unless the lab objective and authorization explicitly permit it. Record uploaded filenames and remove them during cleanup when safe.

## Nimux SOCKS Pattern

The supplied `references/nimux-command-surface.txt` describes a native `nimux socks` feature and proxy-aware command usage. Treat local `nimux --help` and local documentation as authoritative for syntax. Use the same approval record as an SSH pivot, capture the printed SOCKS URL, process identifier, task name, and remote helper path, verify one internal destination, and clean up the helper when finished.

A safe conceptual sequence is:

```text
confirm pivot host and internal destination are in scope
→ approve helper deployment
→ deploy the smallest supported SOCKS helper
→ record listener, PID, task name, and remote path
→ verify one approved destination through the proxy
→ run narrow enumeration only
→ stop the helper and verify cleanup
```

Do not combine pivot deployment with credential spraying, broad CIDR scanning, persistence, or unrelated file collection.

## Verification and Failure Diagnosis

| Symptom | Check | Do not assume |
| --- | --- | --- |
| SSH authentication fails | Username, key permissions, host key, account rights, and target port | That the target is down or that another credential should be tried repeatedly. |
| Forward starts but client times out | Listener status, pivot route, internal host/port, and protocol support | That a timeout proves a filtered port or vulnerability. |
| SOCKS works by IP but not hostname | DNS resolution mode and client proxy settings | That the service is absent. |
| Multi-hop fails | Test each hop independently and inspect `ProxyJump` logs | That adding another tunnel will solve it. |
| Internal service returns an unexpected host | Host header, TLS SNI, virtual hosting, and application routing | That the response belongs to the intended target. |
| Tunnel drops | Keepalive, route stability, account limits, and lab instance state | That retrying indefinitely is harmless. |

## Cleanup

Record local tunnel PIDs and stop only the processes created for the lab. Close shells, remove temporary forwarding configuration, delete approved temporary uploads when safe, and confirm that no listener remains:

```bash
ss -lntp | grep -E ':(<socks-port>|<local-port>|<operator-port>)' || true
```

Do not kill unrelated processes or modify persistent SSH configuration without the user’s approval. Include the cleanup result and any residual state in the final report.
