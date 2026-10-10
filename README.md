# .github

Default community files of the `eoc-llm-tooling` organization.

| File | Holds |
|---|---|
| [CONTRIBUTING.md](CONTRIBUTING.md) | how issues are reported and handled, and the rules for pull requests |
| [SECURITY.md](SECURITY.md) | how to report a vulnerability privately |
| [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | the Contributor Covenant 3.0, with the address that receives reports |
| [.github/ISSUE_TEMPLATE/](.github/ISSUE_TEMPLATE/) | the Bug, Feature and Task issue forms |
| [.github/pull_request_template.md](.github/pull_request_template.md) | the pull request description |
| [labels.yml](labels.yml) | the labels every repository carries |
| [labels/](labels/) | the labels of one repository, in `<repository>.yml` |
| [tools/sync_labels.py](tools/sync_labels.py) | applies the label files to the organization's repositories |
| [profile/README.md](profile/README.md) | the organization's profile page |

GitHub shows each of these files in every repository of the organization that has no file of the
same type itself. A repository with its own `.github/ISSUE_TEMPLATE/` folder uses none of the
forms here. The defaults are not part of a repository's clone, download or history: they live in
this repository only.

The code of conduct is the Contributor Covenant's text under its own license, CC BY-SA 4.0, as
the file states; everything else here is MIT-licensed.

`labels.yml` lists each shared label's name, color and description; `labels/<repository>.yml`
lists the labels of that repository only, such as its `area:` labels. `tools/sync_labels.py`
creates and updates them in every repository of the organization that has issues, and with
`--prune` deletes labels the files do not define. It prints the changes without making them
unless run with `--apply`, and reaches GitHub through `gh` with the token in `GH_TOKEN`:

```bash
GH_TOKEN=<token> uv run tools/sync_labels.py --prune            # show the changes
GH_TOKEN=<token> uv run tools/sync_labels.py --prune --apply    # make them
```

The token needs read and write access to issues in the organization's repositories.
