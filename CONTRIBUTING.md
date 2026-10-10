# Contributing

These rules apply to every repository of the `eoc-llm-tooling` organization. A repository's own
`README.md` and `CLAUDE.md` add what is specific to it, such as its check command.
Participation in issues, pull requests and comments follows the
[code of conduct](CODE_OF_CONDUCT.md).

## Reporting a bug

Open an issue with the **Bug report** form. Report a security vulnerability privately instead, as
[SECURITY.md](SECURITY.md) describes.

Issues, comments and pull request descriptions are public as soon as they are posted. Leave out
secrets, tokens, keys, paths from your own machine, IP or MAC addresses, internal host names and
the names of repositories that are not public; use placeholders.

## How issues are handled

Every issue has a type: **Bug**, **Feature** or **Task**. An epic is a Feature whose work is
split into sub-issues.

### Bugs

The description of a bug is the report. It records what was observed, what was expected, how to
reproduce it, the evidence and the impact, and it is edited afterwards only to correct or narrow
the report. Everything that follows happens in comments: questions, reproduction attempts,
hypotheses and measurements. Two comments mark the milestones:

- **Cause confirmed** — the mechanism and the evidence that confirms it. A maintainer pins it to
  the top of the issue.
- **Resolution** — the pull request or commit that fixed it, and how the fix was verified. It is
  posted when the issue closes, unless the closing pull request already states both.

| State | Shown by |
|---|---|
| Reported | an open issue |
| Cause confirmed | the pinned **Cause confirmed** comment |
| Fix in progress | a pull request linked in the issue's Development panel |
| Fixed | closed as *completed*, with the **Resolution** |
| Not fixed | closed as *not planned* (won't fix, or not a bug, with the reason in a comment) or as a *duplicate* of the issue named |

Severity is set by a maintainer as a label:

| Label | Meaning |
|---|---|
| `severity:blocker` | the component cannot be used, or data is lost or exposed |
| `severity:major` | a documented guarantee or main function fails; a workaround may exist |
| `severity:minor` | a secondary function misbehaves, or the behaviour is noisy or misleading |
| `severity:cosmetic` | wording, formatting or presentation only |

A repository may keep a problem log in `docs/issues.md`. Maintainers add a record there for a
blocker or major bug when its issue closes, condensed from the issue, which it links.

### Features and tasks

The description of a feature or task is its plan: summary, the need it serves, scope, what is out
of scope, acceptance criteria, dependencies and open decisions. It is kept current; a decision
reached in the comments is carried into the description.

### Labels, milestones and needs

- `area:<part>` labels name the part of a repository an issue concerns; each repository has its
  own set.
- `decision-needed` marks an issue waiting for a maintainer's decision.
- Milestones are the phases of a repository's `docs/roadmap.md`.
- Where a repository keeps `docs/needs.md`, an issue names the need it serves on a
  `Traces to:` line, with the need's ID (for example `ABC-N-001`).

## Pull requests

- Work on a branch and open a pull request against `main`; never push to `main`.
- Run the check command named in the repository's `CLAUDE.md`, and commit only when it passes.
- Write commit messages and the pull request title as
  [Conventional Commits](https://www.conventionalcommits.org/): `type(scope): description`,
  imperative, lowercase, no trailing period. The title becomes the merge commit's message.
- Keep the branch linear: rebase onto `main` instead of merging it in.
- In the description, state what changed and how it was tested, list any test that could not be
  run, and end with `Closes #<n>` for the issue it resolves.
- Docs, code comments and commit messages describe what the repository is and does, not how a
  change was made or found.
- Tests use fixtures written for the repository, or public codebases.
- A new dependency, or a source fetched at build time, carries a license compatible with MIT.
  Raise a copyleft one in the pull request instead of adding it.

## License

Contributions are licensed under the MIT license of the repository they are made to.
