---
title: "Setup Guide"
description: "Introduction to Computational Social Science (Python), GESIS Fall Seminar 2024"
author:
  - name: John McLevey
    url: https://johnmclevey.com
    email: john.mclevey@uwaterloo.ca
    corresponding: true
    affiliations:
      - name: University of Waterloo
date: "08/26/2024"
date-modified: last-modified
categories:
  - Python
  - GESIS
  - computational social science
  - data science
tags:
  - Python
  - GESIS
  - computational social science
  - data science
bibliography: references.bib
reference-location: margin
citation-location: margin
toc: true
freeze: true
license: "CC BY-SA"
---

To set up your computing environment for this course, you will need to complete the following steps:

1. [Download and install the VS Code editor](#download-and-install-the-vs-code-editor)
2. [Download and install Git](#download-and-install-git)
3. [Download and install Miniconda Python](#download-and-install-miniconda-python)
4. [Download and install Pipx and Poetry](#download-and-install-pipx-and-poetry)
5. [Download and install Quarto](#download-and-install-quarto)
6. [Set up the Course Virtual Environment](#set-up-the-course-virtual-environment)

More details on each step are available below.

# Install Visual Studio Code (VS Code)

Step-by-Step Instructions:

1. **Download VS Code:**

   - Go to the [Visual Studio Code website](https://code.visualstudio.com/).
   - Click on the "Download for" button. It will automatically detect your operating system (Windows, macOS, or Linux).
   - Download the installer.

2. **Install VS Code:**

   - **macOS:** Open the downloaded `.dmg` file and drag the VS Code icon to the Applications folder.
   - **Linux:** Follow the installation instructions on the [Linux installation guide](https://code.visualstudio.com/docs/setup/linux).
   - **Windows:** Run the downloaded `.exe` file. Follow the installation prompts.

If your installer asks you if you want to add VS Code to your PATH, say yes. :)


3. **Open VS Code:**

   - Once installed, open VS Code.

4. **Install Recommended Extensions:**

   - **Python Development Tools:** When you open a Python file, VS Code will prompt you to install the Python extension. Accept the prompt to install.
   - **Jupyter Extension:** Search for "Jupyter" in the Extensions view (`Ctrl+Shift+X` or `Cmd+Shift+X` on macOS) and install it. This will allow you to work with Jupyter notebooks directly in VS Code.
   - **Quarto Extension:** Search for "Quarto" and install the extension to work with Quarto documents.
   - **Rainbow CSV:** Search for "Rainbow CSV" and install it. This extension highlights CSV files, making them easier to scan in VS Code, which comes in handy from time to time.

5. **Familiarize Yourself with VS Code:**
   - Make sure you can access the version control options on the left panel, which you can use to manage your Git repositories. I will discuss this in the live sessions.
   - Locate the integrated terminal at the bottom of the screen. You will use this terminal for running commands directly from within VS Code. I will also discuss this in the live sessions.

# Install Git

Git is a version control system that allows you to track changes in your code and collaborate with others. For this course, you'll use Git to access and update course materials. If you are using macOS or Linux, git it probably installed on your system already. You can check by opening the terminal and running `git --version`. If it is installed, you can skip to the next step.

Step-by-Step Instructions:

1. **Download Git:**

   - Go to the [Git website](https://git-scm.com/).
   - Click "Download" to get the latest version of Git for your operating system.

2. **Install Git:**

   - **macOS:** If it's not installed, you can install it after downloading it from the Git website. Alternatively you can use Homebrew: `brew install git`.
   - **Linux:** Use the package manager for your distribution. For Ubuntu, use: `sudo apt-get install git`.
   - **Windows:** Run the downloaded `.exe` file. Follow the installation prompts. When you reach the "Adjusting your PATH environment" option, select "Use Git from the command line and also from 3rd-party software."

3. **Configure Git:**

   - Open your terminal or command prompt and configure your Git username and email by running:
     ```bash
     git config --global user.name "Your Name"
     git config --global user.email "your.email@example.com"
     ```
   - This configuration is necessary for committing changes. Although you won't be commiting any changes in this course, it's useful to have this setup for the future!

4. **Verify Installation:**
   - Type `git --version` in your terminal to verify that Git was installed successfully.

# Install Miniconda (Python)

Miniconda is a minimal installer for Conda, a package manager that simplifies managing Python environments and packages. Miniconda is preferred over Anaconda because it is lightweight, and you can install only the packages you need.

Step-by-Step Instructions:

1. **Download Miniconda:**

   - Go to the [Miniconda website](https://docs.conda.io/en/latest/miniconda.html).
   - Choose the Python 3.x installer for your operating system.

2. **Install Miniconda:**

   - **macOS/Linux:** Open your terminal, navigate to the directory where the installer is located, and run:
     ```bash
     bash Miniconda3-latest-MacOSX-x86_64.sh  # for macOS
     bash Miniconda3-latest-Linux-x86_64.sh  # for Linux
     ```
   - **Windows:** Run the downloaded `.exe` file. Follow the prompts. Make sure to check the option to "Add Miniconda to my PATH environment variable."
   - Follow the prompts to complete the installation.

Steps 3 and 4 may not be necessary, but follow them if you are not able to use Python in VS Code as expected.

3. **Initialize Conda:**

   - After installation, open your terminal (or Command Prompt on Windows) and type:
     ```bash
     conda init
     ```
   - Close and reopen your terminal to apply the changes.

4. **Verify Installation:**
   - Check that Miniconda is installed and working by typing:
     ```bash
     conda --version
     ```

# Install Pipx and Poetry

Pipx is a tool to help you install and run Python applications in isolated environments. Poetry is a dependency management and packaging tool that simplifies project management. We're going to use pipx to install Poetry, which we will use alongside Conda for managing our dependencies.

Step-by-Step Instructions:

1. **Install Pipx:**

   - **Windows/macOS/Linux:**
     - Open your terminal and run:
       ```bash
       python -m pip install --user pipx
       python -m pipx ensurepath
       ```
     - Close and reopen your terminal to refresh the environment variables.

2. **Install Poetry:**
   - Once Pipx is installed, you can install Poetry using:
     ```bash
     pipx install poetry
     ```
   - Verify the installation by typing:
     ```bash
     poetry --version
     ```

# Install Quarto

Quarto is a scientific and technical publishing system built on Pandoc. It supports reproducible workflows, including Jupyter notebooks and R Markdown, which are widely used in this course.

Step-by-Step Instructions:

1. **Download Quarto:**

   - Go to the [Quarto website](https://quarto.org/).
   - Download the installer for your operating system (Windows, macOS, or Linux).

2. **Install Quarto:**

   - **macOS:** Open the downloaded `.pkg` file and follow the installation prompts.
   - **Linux:** Follow the instructions on the Quarto website for your distribution. For example, on Ubuntu, you can use:
     ```bash
     sudo apt-get install quarto
     ```
   - **Windows:** Run the downloaded `.exe` file and follow the installation prompts.


3. **Verify Installation:**

   - Check that Quarto is installed by typing:
     ```bash
     quarto --version
     ```

4. **Install Quarto VS Code Extension:**
   - Open VS Code, go to the Extensions view (`Ctrl+Shift+X` or `Cmd+Shift+X`), and search for "Quarto." Install the Quarto extension.

# Set up the Course Virtual Environment

Now that you have all the necessary tools installed, the final step is to set up the virtual environment for this course. This virtual environment will contain all the Python packages you'll need, ensuring that everyone in the course has a consistent setup.


Step-by-Step Instructions:

1. **Clone the Course Repository:**

   - Open your terminal and navigate to the directory where you want to store the course materials.
   - Clone the course repository using Git:
     ```bash
     git clone https://github.com/mclevey/computational-social-science
     ```
   - Navigate into the cloned repository:
     ```bash
     cd computational-social-science
     ```

::: { .callout-note }
This process has changed!

This process was different in an earlier version of these course materials. Please follow this version of the setup instructions instead of the previous version.
:::

2. **Create a Conda Environment:**

   - Create a new Conda environment with the name `gt` and install the `graph-tool` package into the environment:^[We are going to use the name `gt` because the environment I use in the lectures and tutorial videos is named `gt`. This keeps things consistent.]
     ```bash
     conda create --name gt -c conda-forge graph-tool
     ```

3. **Activate the Conda Environment:**
   - Activate your new environment:
     ```bash
     conda activate gt
     ```

4. **Install Additional Python Packages with Poetry:**

::: { .callout-note }
Complete these steps with your `gt` conda environment activated!
:::

   - From the root of the course materials directory (`cd computational-social-science`):
     ```bash
     poetry install
     ```
   - This command will install all the required dependencies into your activated `gt` environment.


If you encounter any issues, ensure that your environment is activated and that all packages are installed correctly.

# Conclusion

You have successfully set up your computing environment for the course! If you have any issues, please don't hesitate to reach out for help. I've also reserved time in our live session today to make sure everything has their systems set up and ready to go. :-)
