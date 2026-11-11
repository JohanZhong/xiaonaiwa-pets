# Security

The installer runs locally, reads bundled files, verifies hashes and copies only the two required desktop files per pet. It has no network requests, auto-update mechanism or elevated-privilege requirement.

Use this repository's Release assets, verify `SHA256SUMS.txt`, and inspect scripts before running them. Do not run commands from unsolicited issues or comments.

For a vulnerability that could expose secrets or overwrite unrelated files, use GitHub's private vulnerability reporting if available; otherwise contact the maintainer through the profile without disclosing secrets in a public issue. Supported release line: 1.x.
