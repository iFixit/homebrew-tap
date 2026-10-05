# iFixit Homebrew tap

Install and upgrade the iFixit CLI without a separate Node.js installation:

```sh
brew install ifixit/tap/ifixit
brew upgrade ifixit/tap/ifixit
```

The formula installs the complete standalone release under `libexec` and links
its launcher into Homebrew's `bin`. It also installs bash and zsh completion.
Homebrew owns upgrades. Credentials stay in your home directory.

## Support

Native installation CI covers macOS 15 on Intel and Apple Silicon, and Ubuntu
22.04 on x64 and ARM64. Homebrew itself must support your host; its requirements
can be stricter than the archive's Node runtime baseline. Older macOS versions,
custom Homebrew prefixes, and other distributions are not part of this tap's
installation test matrix. See [Homebrew support tiers](https://docs.brew.sh/Support-Tiers).

The standalone runtime baseline is macOS 11+ or GNU/Linux with glibc 2.28+ and
kernel 4.18+, plus the usual GCC runtime libraries. This is an archive baseline,
not a promise that Homebrew supports those systems. Alpine/musl, Windows, and
32-bit systems are outside the formula's scope.

## Release updates

`Update iFixit formula` checks the latest published stable CLI release every six
hours and supports `repository_dispatch` (`ifixit-release`) and manual runs.
Drafts and prereleases are excluded. Before creating an update PR it verifies
all four downloaded archive checksums and their GitHub attestations. It never
merges its own PR. Native tests are explicitly dispatched because PRs created
using `GITHUB_TOKEN` do not start another workflow automatically.

The CLI's release notification workflow can dispatch immediately after publication.
Its `HOMEBREW_TAP_TOKEN` must be a narrowly scoped GitHub App or fine-grained token
with access to this repository. The scheduled fallback needs no cross-repository
credential once CLI releases are public. Enable Actions to create PRs in this tap.

Tests exercise installation, completions, symlinks, a read-only Cellar, and
`brew upgrade` from an older formula version of the same verified archive.
A later release should also be tested as a real version-to-version upgrade.

## Initial activation

The initial formula pins the archives built and tested for CLI v0.0.1. Merge
and advertise installation only after that release is publicly downloadable
with its GitHub attestations and this tap's native installation checks pass.
The CLI repository is currently private; its release attestation job requires
public visibility or a GitHub plan that supports private attestations.
