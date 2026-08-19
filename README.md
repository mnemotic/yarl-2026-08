# Yet Another Roguelike (YARL)

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Yet Another Roguelike built for [RoguelikeDev Does The Complete Roguelike Tutorial 2026](https://www.reddit.com/r/roguelikedev/comments/1vd9noj/roguelikedev_does_the_complete_roguelike_tutorial/) by following [Yet Another Roguelike Tutorial](https://rogueliketutorials.com/tutorials/tcod/v2/).

## Installation

Download a bundle from [GitHub
releases](https://github.com/mnemotic/yarl2026/releases/latest) or from
[itch.io](https://mnemotic.itch.io/yarl), extract, and run `yarl.exe` (on
Windows) or `yarl` (on Linux).

## Packaging

Requires `git`, `git lfs`, and `uv` to be installed.

1. Clone the project, including the assets.

    ```shell
    git clone https://github.com/mnemotic/yarl2026.git
    cd yarl2026
    git lfs pull
    ```

1. Install Python required by the project.

    ```shell
    uv install python
    ```

1. Install dependencies using `uv`. This will create a local virtual environment.

    ```shell
    uv sync --locked
    ```

1. Run PyInstaller.

    ```shell
    uv run pyinstaller yarl.spec --noconfirm
    ```

This will create a single directory bundle named `yarl` in `./dist`. This bundle
directory can be distributed to user.

## Release

1. Create a release branch, e.g. `release/v0.10.0` from `develop`.
1. Update project version using `uv`, either explicitly with `uv version 0.10.0`
   or by bumping with `uv version --bump <major|minor|patch>`.
1. Update `__version__` in `./src/yarl/__init__.py` to match the project version.
1. Commit with message, e.g. `chore: prepare release v0.10.0`.
1. Merge the release branch into `main` with fast-forward merge, e.g. `git
   switch main && git merge --ff-only release/v0.10.0`.
1. Tag the release with an annotated tag, e.g. `git tag -a v0.10.0 -m v0.10.0`
1. Push to GitHub, including tags, with `git push origin --tags`. GitHub
   workflow will create a draft release, build bundles and attach them to the
   draft release.
1. Add release notes to the draft release.
1. Publish the release. GitHub workflow will push the attached bundles to *itch.io*.
1. Merge the release branch into `develop` with fast-forward merge, e.g. `git
   switch develop && git merge --ff-only release/v0.10.0`. All three branches
   should now be at the same commit.

## License

This project is licensed under the **Apache License 2.0** - see the
[LICENSE](LICENSE) file for details.
