# Yet Another Roguelike (YARL)

Yet Another Roguelike built for [RoguelikeDev Does The Complete Roguelike Tutorial 2026](https://www.reddit.com/r/roguelikedev/comments/1vd9noj/roguelikedev_does_the_complete_roguelike_tutorial/) by following [Yet Another Roguelike Tutorial](https://rogueliketutorials.com/tutorials/tcod/v2/).

## Installation

Download a bundle from [GitHub
releases](https://github.com/mnemotic/yarl2026/releases/latest) or from
[itch.io](https://mnemotic.itch.io/yarl), extract, and run `yarl.exe` (on
Windows) or `yarl` (on Linux).

## Packaging

### PyInstaller

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
