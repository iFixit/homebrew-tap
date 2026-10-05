#!/usr/bin/env python3
"""Generate the formula from the four versioned release checksums."""
import argparse
import hashlib
from pathlib import Path
import re

TARGETS = ('darwin-arm64', 'darwin-x64', 'linux-arm64', 'linux-x64')


def render_formula(version, checksums):
    if not re.fullmatch(r'\d+\.\d+\.\d+', version):
        raise ValueError('Expected a stable numeric version, for example 0.0.1')
    for target in TARGETS:
        if not re.fullmatch(r'[a-f0-9]{64}', checksums[target]):
            raise ValueError(f'Invalid SHA-256 for {target}')
    base = f'https://github.com/iFixit/ifixit-cli/releases/download/v{version}/ifixit-v{version}'
    platforms = []
    for os_name, target_os in (('macos', 'darwin'), ('linux', 'linux')):
        branches = []
        for arch, target_arch in (('arm', 'arm64'), ('intel', 'x64')):
            target = f'{target_os}-{target_arch}'
            branches.append(f'''    on_{arch} do
      url "{base}-{target}.tar.gz"
      sha256 "{checksums[target]}"
    end''')
        platforms.append(f'  on_{os_name} do\n' + '\n'.join(branches) + '\n  end')
    return f'''class Ifixit < Formula
  desc "Repair guides and household maintenance from your terminal"
  homepage "https://github.com/iFixit/ifixit-cli"
  version "{version}"
  license :cannot_represent

{chr(10).join(platforms)}

  def install
    # Keep Homebrew from moving the archive license out of libexec.
    cp "LICENSE", prefix/"LICENSE"
    libexec.install Dir["*"]
    bin.install_symlink libexec/"bin/ifixit"
    bash_completion.install libexec/"share/bash-completion/completions/ifixit"
    zsh_completion.install libexec/"share/zsh/site-functions/_ifixit"
  end

  test do
    ENV["IFIXIT_NO_WELCOME"] = "1"
    ENV["IFIXIT_CREDENTIALS_PATH"] = testpath/"credentials.json"
    ENV["IFIXIT_TOKEN"] = ""
    ENV["IFIXIT_PROFILE"] = ""
    assert_match "USAGE", shell_output("#{{bin}}/ifixit --help")
    assert_match '"status": "dry-run"', shell_output(
      "#{{bin}}/ifixit advanced guides getGuide 1 --dry-run --json",
    )
    assert_match "complete", shell_output("#{{bin}}/ifixit advanced completion bash")
    assert_match "#compdef", shell_output("#{{bin}}/ifixit advanced completion zsh")
    assert_predicate libexec/"bin/node", :executable?
    assert_path_exists libexec/"release.json"
    assert_path_exists libexec/"LICENSE"
    assert_path_exists libexec/"NODE-LICENSE"
  end
end
'''


def verified_checksums(version, directory):
    result = {}
    for target in TARGETS:
        filename = f'ifixit-v{version}-{target}.tar.gz'
        text = (directory / f'{filename}.sha256').read_text().strip()
        match = re.fullmatch(r'([a-f0-9]{64}) [ *]' + re.escape(filename), text)
        if not match:
            raise ValueError(f'Invalid checksum document for {filename}')
        archive = directory / filename
        with archive.open('rb') as stream:
            hasher = hashlib.sha256()
            for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                hasher.update(chunk)
            digest = hasher.hexdigest()
        if digest != match[1]:
            raise ValueError(f'Checksum mismatch for {filename}')
        result[target] = digest
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('version')
    parser.add_argument('artifacts', type=Path)
    args = parser.parse_args()
    checksums = verified_checksums(args.version, args.artifacts)
    Path('Formula/ifixit.rb').write_text(render_formula(args.version, checksums))
