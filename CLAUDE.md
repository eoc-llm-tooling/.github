# CLAUDE.md

This repository holds the organization's default community files; [README.md](README.md) lists
them. It has no code.

## Before committing

- Run the check below and commit only when it passes.
- Never commit paths from your own machine, IP or MAC addresses, internal host names, tokens or
  keys; use the documented defaults or placeholders.
- Work on a branch and open a pull request; never push to `main`.
- Issues and pull requests follow the organization's
  [contribution rules](CONTRIBUTING.md).

```bash
uvx check-jsonschema --builtin-schema vendor.github-issue-forms .github/ISSUE_TEMPLATE/bug.yml .github/ISSUE_TEMPLATE/feature.yml .github/ISSUE_TEMPLATE/task.yml
uvx check-jsonschema --builtin-schema vendor.github-issue-config .github/ISSUE_TEMPLATE/config.yml
```

## Rules

- Keep [CONTRIBUTING.md](CONTRIBUTING.md) free of anything specific to one repository; a
  repository's own `README.md` and `CLAUDE.md` carry that.
- When a form's sections change, change the matching description in CONTRIBUTING.md in the same
  commit.
