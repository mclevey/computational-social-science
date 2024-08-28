# Contributor Guide

> Hi! 👋 This is: CURRENTLY A COLLECTION OF RANDOM NOTES TO HELP ME REMEMBER WHAT I NEED TO DO... I'LL BE CLEANING UP AND UPDATING SOON!

---

# WORK IN PROGRESS!

Public links to slides:

- [Day 1, Introduction](https://www.johnmclevey.com/computational-social-science-python-intro/day-1.html)
- [Day 2, Obtaining Data](https://www.johnmclevey.com/computational-social-science-python-intro/day-2.html)
- [Day 3, Computational Text Analysis](https://www.johnmclevey.com/computational-social-science-python-intro/day-3.html)
- [Day 4, Computational Network Analysis](https://www.johnmclevey.com/computational-social-science-python-intro/day-4.html)
- [Day 5, Simulation and Agent-based Modelling](https://www.johnmclevey.com/computational-social-science-python-intro/day-5.html)
- [Day 6, Projects](https://www.johnmclevey.com/computational-social-science-python-intro/day-6.html)

**These are all currently in development.**

# MISC NOTES

## Package Name

`icss` and `icsspy` have both neen rejected by `pypi` because there are packages with similar names. Think of something else (or don't).

# `poetry` + `conda` in the pipeline

This seems to make `conda` run `graph-tool` in the `poetry` environment for `icsspy`.

```zsh
poetry shell
conda create --name gt -c conda-forge graph-tool -y
source $(conda info --base)/etc/profile.d/conda.sh
conda activate gt
pip install -e . # run from project root
conda deactivate
cd pipelines/youtube
pdpp run
```

Will need to update install instructions, etc. Will finish testing first.

# Quarto Slides with Port Forwarding

If you are working on the Quarto slides (e.g., `day-1.qmd`) from `buffy`, then you can just call

```zsh
quarto preview day-1.qmd
```

and Quarto automatically handles the port forwarding. It will open a browser and use localhost with the correct ssh port and display the slides. It's super fast and nice. 😁

---

---

# Computing Setup

## Accounts

- GitHub
- Google (YouTube API, Colab Compute)

## Required Software

- terminal + text editor
- package manager -> git, docker, quarto, pipx
- pipx -> poetry

### macOS

Install the [homebrew](https://brew.sh) package manager if you don't already have it.

```zsh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

You can install the core dependencies individually:

```zsh
brew install git
brew install docker
brew install quarto
brew install pipx
pipx ensurepath
```

Or you can install them together alongside some other useful but inessential tools with:

<!--
`brew leaves > setup/leaves.txt`
remove lines that students do not need
 -->

```zsh
xargs -a setup/leaves.txt brew install
pipx ensurepath
```

### Linux (Debian / Ubuntu)

```zsh
sudo apt update
sudo apt install pipx
pipx ensurepath
```

- [ ] Add Linux pacakges.txt or whatever

For Linux, see the [Quarto documentation](https://quarto.org/docs/download/tarball.html).

### Windows

- [ ] Add Windows

Now that the foundational tools are installed, let's setup our virtualization tools.

### Poetry

```zsh
pipx install poetry # install poetry
poetry install # install project dependencies
poetry run download-models # download language models
```

- [ ] Add other language models in pipeline to `download-models` script
- [ ] Add logging to the `download-models` script

While `poetry` is a great tool for managing Python dependencies, it is not designed to manage other aspects of our computing environment. Some packages, such as `graph-tool` are... There are a few good ways to manage this, including using a conda environment or a Docker container. Either is a great choice.

## Poetry + Conda

To install and manage additional dependencies using a `conda environment`, run

```zsh
conda create --name gt -c conda-forge graph-tool
conda activate gt
```

When you first enter the `gt` environment, you can install the project dependencies with

```zsh
poetry install
```

- [ ] Is the installation of packages into the conda environment the source of problems for pdpp?
- [ ] Do I want a modified version of `gt` for this specific course? YAML could be in `setup/`

## Poetry + Docker

Another option is to use Docker of a `conda` environment. `Docker` is a complex but powerful tool that enables us to create consistent and _fully_ reproducible development environments for computational social science. To use it, you'll need to [install `Docker` on your local machine](https://www.docker.com/products/docker-desktop/).

Once you have `Docker` installed, `clone` the project repo and `cd` into the project root directory.

```zsh
git clone git@github.com:mclevey/computational-social-science-python-intro.git
cd computational-social-science-python-intro
```

You can then build the `docker image` and give it the name `gesis` (or whatever you want) by running

```zsh
docker build -f Dockerfile -t gesis .
```

> **Permissions**
>
> If you run into permissions issues, you can use `sudo`
>
> ```zsh
> sudo docker build -f Dockerfile -t gesis .
> ```
>
> However, it is better to add your user to the `Docker` group. You can do that by:
>
> ```zsh
> sudo groupadd docker
> sudo usermod -aG docker $USER
> ```
>
> Apply the new membership in the `docker` group by logging out and logging back in, or by running `newgrp docker`. If you run `groups`, you should see `docker` listed. You can now run `docker` commands (e.g., `poetry run enter-docker`) without having to `sudo`.

When the image finishes building, you'll want to enter the container to install additional dependencies and execute code by using the `docker run` command. The full command you want to run is a bit gross, but it does some important stuff...

```zsh
docker run -it --rm -v "$(pwd)":/app -w /app gesis zsh
```

The key is to be able to access your local project files without having to copy them into the container. Instead, we can mount the project directory as a volume inside our container. This is important; copying everything into the container is easy, but it's slow and makes the containers larger. More importantly, any changes you make to your project files will violate the `docker cache` and trigger a full rebuild the next time you run `docker`! Life's too short. Just mount a volume.

If you run the following command _from the project root directory_ (i.e., the same folder containing the `Docker` file), then it will mount the project directory as `/app` inside the container.

If you're curious, here's what each component of the above command means:

- `docker` is the application we are running, and `run` is the `docker` command that runs our container;
- `-it` specifies that we want to run the container in _interactive mode_ from a terminal emulator;
- `--rm` automatically removes the container when it exits;
- `-v "$(pwd)":/app` mounts the current directory (`$(pwd)`) to `/app` inside the container;
- `-w /app` sets the working directory inside the container to `/app`
- `gesis` is the name of the Docker image we want to run (and so could also be something else); and finally
- `zsh` is the command to run inside the container, in this case, starting a `zsh` shell.^[If you prefer, you could run `bash` instead.]

You can avoid having to remember (and type) this command in a variety of ways, the easiest being to run the script `poetry run enter-docker` from the project root directory (which triggers `script/enter_docker.py`).

```zsh
poetry run enter-docker
```

Once you are inside the container, you can install the Python packages and their dependencies with:

```zsh
poetry install
```

If you have already run `poetry install` outside of the container, you're already good to go, as Docker is mounting this directory.

- [ ] Should I go back to copying the install files into the last layer, though? Does this work the same way? Check.

You can navigate through the project files from the command line while inside the container, and you can run code using `poetry run <SOME-COMMAND>`. For example, let's run the YouTube pipeline in `pipelines/youtube`. You need to initialize this pipeline the first time you run it with:

```zsh
cd examples/youtube # go to the pipeline directory
poetry run pdpp init # initialize pdpp (ignore the warning)
./import.sh --source config.yaml # copy project settings into _import_
```

After that, you can execute the pipeline with:

```zsh
poetry run pdpp run
```

The process is the same for the `abm` pipelines.

# Remote Computing

- GitHub + Google Colab seems better than the straight Colab solution
- This approach requires using notebooks; lessons will be in notebooks anyway

# Additional Resources

- See [graph-tool.skewed.de](https://graph-tool.skewed.de) for other installation options, including other package managers such as `homebrew`, `pacman`, etc.
- HuggingFace stuff
- Books, etc.

# Contributing

- Issues, etc.
- Welcome contributions, yada yada yada

## Additional Development Setup

### Git and Coding Conventions

#### Pre-commit hooks

This repository is setup with `pre-commit-hooks` specified in `.pre-commit-config.yaml`. It uses:

- **black**: Formats Python code to adhere to the PEP 8 style guide. This ensures consistency in code formatting across the project, making it more readable and maintainable.
- **flake8**: Lints Python code for style violations and logical errors. Useful for catching coding errors and enforcing coding standards to maintain code quality.
- **isort**: Sorts and organizes Python imports. Keeps import statements consistent and clean, which helps in maintaining code readability.
- **trim trailing whitespace**: Removes trailing whitespace from the end of lines. Helps in maintaining clean code by avoiding unnecessary whitespaces.
- **fix end of files**: Ensures that all files end with a newline. This helps in maintaining consistency across the codebase and prevents issues with certain text editors and tools.
- **check toml**: Validates TOML files for syntax errors. Ensures that TOML configuration files are correctly formatted and free of syntax issues.
- **check yaml**: Validates YAML files for syntax errors. Ensures that YAML configuration files are correctly formatted and free of syntax issues.
- **detect private key**: Scans for private keys that may have been accidentally committed. Prevents sensitive keys from being exposed in the repository, enhancing security.
- **check for added large files**: Ensures that no large files are added to the repository. This helps in keeping the repository lightweight and avoids unnecessarily large commits.
- **check for broken symlinks**: Checks for broken symbolic links in the repository. Ensures that all symlinks point to valid targets, avoiding issues with missing files or directories.
- **check for merge conflicts**: Detects unresolved merge conflict markers in files. Prevents committing code that contains merge conflict markers, which could lead to errors and confusion.
- **check that executables have shebangs**: Verifies that all executable scripts have a proper shebang (`#!`) line. This ensures that the scripts are correctly identified and run with the appropriate interpreter.
<!-- - **prettier**: Formats CSS, SCSS, HTML, JSON, and MD to ensures consistent style and enhance readability. -->

<!-- - **pylint**: Analyzes Python code for errors, enforces a coding standard, and looks for code smells. Helps improve code quality by identifying potential issues early. -->
<!-- - **bandit**: Checks Python code for security issues. Useful for identifying and mitigating security risks in the codebase. -->

To install the project `pre-commit-hooks`, run:

```zsh
poetry run pre-commit install
```

Once installed, the hooks will be run anytime you attempt to `commit` files to the repo. To run the `pre-commit-hooks` on all files outside of a `git commit`,

```zsh
poetry run pre-commit run --all-files
```

or for specific files:

```zsh
pre-commit run --files scripts/enter_docker.py scripts/render_slides.py
```

It is also possible to run a specific hook (e.g., `flake8`) on all files,

```zsh
pre-commit run flake8 --all-files
```

or specific files:

```zsh
pre-commit run flake8 --files scripts/enter_docker.py scripts/render_slides.py
```

Some configuration for the pre-commit-hooks can be found in `.pre-commit-config.yaml` and the `pyproject.toml`, others in dotfiles in the project repo (e.g., `.black.toml`, `.flake8`, `.isort.cfg`). Consult the [pre-commit-hooks](https://pre-commit.com/#usage) documentation for more information.

<!-- > **Note** > [pylint](https://github.com/pylint-dev/pylint) is slow because it infers typing. It's annoying to use slow tools in 2024, but it's worth it when `pylint` catches typing-related errors that other linters miss. In this project, `pylint` is configured to ignore coding conventions (Category C) and will not suggest ways to improve code through refactoring (category R). -->

### Scripts (Installed in Poetry)

- General overview of what this is / how it works with `poetry`

#### `poetry run download-models`

- Add the HuggingFace models here

#### `poetry run enter-docker`

Runs an awkward Docker command that mounts the current directory into `/app`, enters the container interactively, starts `zsh`

#### `poetry run draw-graphical-models`

Produces PDF and PNG versions of all `.gv` files in the `graphical_models/` subdirectory.

#### `poetry run render-slides`

Runs `quarto render` on `*.qmd` files in the `slides/` subdirectory.

### `pdpp` Pipelines

- `cd` into the pipeline
- `poetry run pdpp run` to run the full pipeline
- see the [pdpp repo](https://github.com/UWNETLAB/pdpp?tab=readme-ov-file) for more information

# License

# TEMPORARY MISC NOTES

## Simulation and ABM Content

Code to run the threshold and bounded-confidence ABMs is in `course-materials/day-5-simulation`. The `agents.py` and `model.py` files for the models are in the package now, at `icsspy/abms/threshold` and `icsspy/abms/bounded-confidence`.

```zsh
cd course-materials/day-5-simulation
poetry run pdpp run
```

There are tasks to run both the threshold and bounded-confidence models. Others can be added.

- [ ] TODO: Add analysis and visualization tasks
- [ ] TODO: Move into examples alongside YouTube
