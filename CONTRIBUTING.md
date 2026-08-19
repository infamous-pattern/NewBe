# Contributing to NewBe

Thank you for helping improve NewBe. Contributions should preserve its Wayland-first design, auditable user-scoped installation, and original visual identity.

## Before submitting a change

1. Create a focused branch from the current `main` branch.
2. Keep generated assets reproducible from their checked-in sources.
3. Do not add proprietary artwork, copied product icons, credentials, telemetry, remote installers, or system-wide mutations.
4. Run the complete verifier:

   ```bash
   ./scripts/verify.sh
   ```

5. Review `git diff --check` and confirm the installer and uninstaller remain reversible.

## Visual contributions

Follow `docs/DESIGN.md`, `docs/PALETTE.md`, and `docs/ICONS.md`. New artwork must be original or have clearly documented redistribution rights and provenance.

## Security reports

Do not file public issues containing vulnerability details. Follow `SECURITY.md` instead.

## Pull requests

Explain the user-visible outcome, list verification performed, and call out compatibility or migration concerns. Keep unrelated changes in separate pull requests.
