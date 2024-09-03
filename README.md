🤗🤗 2024 GESIS Fall Seminar

# Introduction to Computational Social Science with Python

Dr. **John McLevey**<br>University of Waterloo<br>Waterloo, ON, Canada<br>[johnmclevey.com](https://www.johnmclevey.com)<br><john.mclevey@uwaterloo.ca>

Hi! This repository contains a Python package and course materials for my [GESIS Fall Seminar](https://www.gesis.org/en/gesis-training/what-we-offer/fall-seminar-in-computational-social-science) course **Introduction to Computational Social Science with Python**. This course is taught in parallel with Dr. [Johannes Gruber](https://www.johannesbgruber.eu), who is teaching a similar [introductory course in R](https://github.com/JBGruber/computational-social-science-r/tree/main). You'll find the course overview and details below, along with details instructions on how to setup your computing environment.

- [Course Description](#course-description)
- [Course Schedule](#course-schedule)
- [Download the Course Materials](#download-the-course-materials)
- [Using the Course Materials](#using-the-course-materials)
- [Required Software](#required-software)
  - See the [Setup Guide](setup/setup-guide.md) for more a detailed guide

# Course Description

The Digital Revolution has produced unprecedented amounts of data that are relevant for researchers in the social sciences, from online surveys to social media user data, travel and access data, and digital or digitized text data. How can these masses of raw data be turned into understanding, insight, and knowledge? The goal of this course is to introduce you to Computational Social Science with Python, a powerful programming language that offers a wide variety of tools, used by journalists, data scientists and researchers alike. Unlike many introductions to programming, e.g., in computer science, the focus of this course is on how to explore, obtain, wrangle, visualize, model, and communicate data to address challenges in social science. The course emphasizes the theoretical and ethical aspects of CSS while covering topics such as web scraping (obtaining data from the internet), data cleaning and visualization, computational text analysis, machine learning, network analysis, and agent-based modeling. The course will be held as a blended learning workshop with video lectures focused on theoretical background and demonstrations accompanied by live sessions where students can ask questions and work through projects together.

> **Working knowledge of Python is an asset, but is not required.** There is an optional "Introduction to Python" module that you should review before beginning this course.


# Course Schedule

GESIS Fall Seminar in Computational Social Science<br>
August 30 - September 6, 2024

| time  | Session                                      | Tutorial Repositories                                                                                                                        | Videos      |
| ----- | -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| Day 1 | Introduction to Computational Social Science | [setup guide](setup/setup-guide.md)                                                                                                      | Moodle Site |
| Day 2 | Obtaining Data                               | [tutorials](https://github.com/gesis24csspy/obtaining-data-from-the-web) | Moodle Site |
| Day 3 | Computational Text Analysis                  | [tutorials](https://github.com/gesis24csspy/analyzing-text-data)       | Moodle Site |
| Day 4 | Computational Network Analysis               | [tutorials](https://github.com/gesis24csspy/modelling-networks) | Moodle Site |
| Day 5 | Social Simulation & Agent-based Models       | [tutorials](https://github.com/gesis24csspy/agent-based-modelling)                                                                                         | Moodle Site |
| Day 6 | Project Work Day                 |                                                                                       | Moodle Site |

- Optional Additional Modules
  - **[Introduction to Python](https://github.com/gesis24csspy/introduction-to-python)**
    - Python Programming: The Basics
    - Python Programming: Data Structures, Functions, and Files
    - Processing Structured Data with Pandas
  - **Obtaining Data from the Web**
    - Scraping the Web (Coming soon...)
    - Working with APIs (Coming soon...)


# Access the Course Materials (GitHub CodeSpaces)

> **Please consult the detailed [setup guide](setup/setup-guide.md) for more information.** If you run into any problems, I'll help you get them sorted in the live sessions or on the course forums on the Moodle site.

# Required Accounts and Software

You will need a GitHub account to use the course materials in GitHub CodeSpaces. That's all you need, but you may want to download and install VS Code on your machine instead of working with VS Code in your browser. See the [setup guide](setup/setup-guide.md) for detailed instructions.

<!--
Detailed instructions to come soon.

I am currently ironing out the details of adopting devcontainers, Docker, and GitHub CodeSpaces. All course module repositories are [available here](https://github.com/orgs/gesis24csspy/repositories). -->



<!--
## VS Code

The easiest way to get the course material is to clone this repository. If you aren’t already familiar with git, I recommend doing this via VS Code. Once you've downloaded VS Code and set it up according to the setup guide, you can clone the repo by

1. clicking the "Source Control" button on the left,
2. selecting "Clone Repository",
3. pasting the GitHub repository when prompted by VS Code, and finally
4. selecting a folder on your computer to store the repo.

The screenshots below should help you find what you're looking for if this is your first time doing this.

![](setup/vs-code-clone-1.png)

![](setup/vs-code-clone-2.png)

Once you tell VS Code to open the repo, you're ready to go! You should see the repository contents in the file browser on the left.

![](setup/vs-code-clone-3.png)

## From the Command Line

Alternatively, you can close the repository from the command line.

```zsh
git clone https://github.com/mclevey/computational-social-science.git
cd computational-social-science-python
```

# Using the Course Materials

You'll find that content in the `notebooks/` directory, or linked directly in the [Course Schedule table above](#course-schedule).

The source code for the lecture slides is available in the [slides](slides) directory. Once you've installed Quarto, you can display the slides yourself by running the following commands from the command line:

```zsh
cd slides
```

- Lecture 1 Slides: `quarto preview day-1.qmd`
- Lecture 2 Slides: `quarto preview day-2.qmd`
- Lecture 3 Slides: `quarto preview day-3.qmd`
- Lecture 4 Slides: `quarto preview day-4.qmd`
- Lecture 5 Slides: `quarto preview day-5.qmd`
- Lecture 6 Slides: `quarto preview day-6.qmd`

Quarto will compile the source code and open the slides in a browser tab. Note that some lectures may take a while to compile, especially if you have code execution on. If you do have code execution on, you'll need to activate the course virtual environment before running the Quarto commands. More information about this is available in [the setup guide](setup/setup-guide.md).


# Required Software

See the [setup guide](setup/setup-guide.md) for detailed instructions on how to setup the required software for this course.

- [VS Code](https://code.visualstudio.com) (text editor / IDE)
- Python 3.11+ (via [Miniconda](https://docs.anaconda.com/miniconda/))
- [Quarto](https://quarto.org)

# Course Virtual Environment

There is a virtual environment you can use to easily access all the packages we will use in this course. Please follow the instructions in the [setup guide](setup/setup-guide.md).

# Contributing to the Course Development

These course materials are available for reuse under the [CC BY-SA 4.0 license](LICENSE). If you would like to contribute to course development, you can consult the [contributor guide](setup/contributor-guide.md).
-->
