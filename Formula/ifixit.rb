class Ifixit < Formula
  desc "Repair guides and household maintenance from your terminal"
  homepage "https://github.com/iFixit/ifixit-cli"
  version "0.0.1"
  license :cannot_represent

  on_macos do
    on_arm do
      url "https://github.com/iFixit/ifixit-cli/releases/download/v0.0.1/ifixit-v0.0.1-darwin-arm64.tar.gz"
      sha256 "a7995569fa02479ac47b590b169d8f544b998e965ad2fde26bd9e4522927573d"
    end
    on_intel do
      url "https://github.com/iFixit/ifixit-cli/releases/download/v0.0.1/ifixit-v0.0.1-darwin-x64.tar.gz"
      sha256 "8316575856a74457ba606639b817e94b830a63a29b1e67e400860ed54aa40635"
    end
  end
  on_linux do
    on_arm do
      url "https://github.com/iFixit/ifixit-cli/releases/download/v0.0.1/ifixit-v0.0.1-linux-arm64.tar.gz"
      sha256 "aad23c78db26cec7df9ca160ad8167fffd9d46ea03bdcc78ff7f4cfae35140b2"
    end
    on_intel do
      url "https://github.com/iFixit/ifixit-cli/releases/download/v0.0.1/ifixit-v0.0.1-linux-x64.tar.gz"
      sha256 "c14204645e5dafd1f9a851b8d4fbff3f5c1420145da67513654ad2b6eff2c2fd"
    end
  end

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
    assert_match "USAGE", shell_output("#{bin}/ifixit --help")
    assert_match '"status": "dry-run"', shell_output(
      "#{bin}/ifixit advanced guides getGuide 1 --dry-run --json",
    )
    assert_match "complete", shell_output("#{bin}/ifixit advanced completion bash")
    assert_match "#compdef", shell_output("#{bin}/ifixit advanced completion zsh")
    assert_predicate libexec/"bin/node", :executable?
    assert_path_exists libexec/"release.json"
    assert_path_exists libexec/"LICENSE"
    assert_path_exists libexec/"NODE-LICENSE"
  end
end
