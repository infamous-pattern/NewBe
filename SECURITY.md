# Security Policy

## Supported versions

Security fixes are applied to the latest published NewBe release and the current `main` branch.

## Reporting a vulnerability

Please use the repository's private vulnerability-reporting form under **Security → Advisories → Report a vulnerability**. Do not disclose exploit details, private user data, credentials, or tokens in a public issue.

If private reporting is unavailable, open a minimal public issue requesting a private maintainer contact. Include no sensitive technical details in that issue.

Useful reports identify the affected release, impacted component, reproduction prerequisites, security impact, and any safe mitigation. Maintainers will acknowledge a complete report as soon as practical and coordinate remediation before public disclosure.

## Security boundaries

NewBe installation is user-scoped: it requires no root privileges and does not modify system files or GNOME settings automatically. Release archives include SHA-256 checksums and an internal per-file integrity manifest.
