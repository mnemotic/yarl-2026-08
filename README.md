# Yet Another Roguelike (YARL)

Yet Another Roguelike built for [RoguelikeDev Does The Complete Roguelike Tutorial 2026](https://www.reddit.com/r/roguelikedev/comments/1vd9noj/roguelikedev_does_the_complete_roguelike_tutorial/) by following [Yet Another Roguelike Tutorial](https://rogueliketutorials.com/tutorials/tcod/v2/).

## Installation

Currently, the best way to install YARL is to clone this repo and install it with `pipx`. This requires a local installation of Python 3.14+, Git with Git LFS, and `uv` and `pipx`.

More user-friendly solution coming soon (hopefully).

1. Clone the project, including the assets.

    ```shell
    git clone https://github.com/mnemotic/yarl-2026-08.git yarl
    cd yarl
    git lfs pull
    ```

1. Install dependencies with `uv`. This will create a local virtual environment.

    ```shell
    uv sync
    ```

1. Install with `pipx` for current user.

    ```shell
    pipx install --python=3.14 .
    ```

1. Run.

    ```shell
    yarl
    ```

## Packaging

### PyInstaller

1. Clone the project, including the assets.

    ```shell
    git clone https://github.com/mnemotic/yarl-2026-08.git yarl
    cd yarl
    git lfs pull
    ```

1. Install dependencies using `uv`. This will create a local virtual environment.

    ```shell
    uv sync
    ```

1. Activate the local virtual environment.

    ```shell
    source .venv/Scripts/activate
    ```

1. Run PyInstaller.

    ```shell
    pyinstaller \
        --noconfirm \
        --name=yarl \
        --add-data="src/yarl/assets/*:assets" \
        src/yarl/__main__.py
    ```
