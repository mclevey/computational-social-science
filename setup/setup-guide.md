---
title: "Setup Guide"
description: "Instructions for accessing and using the course materials."
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
freeze: true
license: "CC BY-SA"
---

# Overview

1. Sign up for a free GitHub account
2. Follow [the gesis24csspy organization](https://github.com/gesis24csspy) for course materials
3. Go to one of the [course module repositories](https://github.com/gesis24csspy)
4. Click on "Code" > "CodeSpaces" > "Create CodeSpace on Main" to start a CodeSpace with VS Code in the browser
5. Open `tutorials/` and start running code!
6. Change the kernel to the `Poetry` environment

- **Optional:** Use your local installation of VS Code

# Step-by-Step Instructions

## Sign up for a free GitHub account

![Sign up for a free GitHub account](img/Screenshot%202024-09-02%20at%206.56.09 AM.png)

![Once you're in, you'll see a page that looks something like this.](img/Screenshot%202024-09-02%20at%207.03.27 AM.png)

![You can access all your CodeSpaces here.](img/Screenshot%202024-09-02%20at%207.04.10 AM.png)

![None CodeSpaces are running yet!](img/Screenshot%202024-09-02%20at%207.05.04 AM.png)

## Follow [the gesis24csspy organization](https://github.com/gesis24csspy) for course materials

![Course modules available from the gesis24csspy organization](img/Screenshot%202024-09-02%20at%207.08.46 AM.png)

## Go to one of the module repositories

![Course module repository for obtaining data from the web](img/Screenshot%202024-09-02%20at%207.07.50 AM.png)

## Click on "Code" > "CodeSpaces" > "Create CodeSpace on Main" to start a CodeSpace with VS Code in the browser

![Click on "Code" > "CodeSpaces" > "Create CodeSpace on Main" to start a CodeSpace with VS Code in the browser](img/Screenshot%202024-09-02%20at%207.11.27 AM.png)

![You'll see a screen like this for a while. Be patient while GitHub builds your environment! The first time will always take a while, but after that it will load relatively quickly.](img/Screenshot%202024-09-02%20at%207.12.23 AM.png)

![You're in!](img/Screenshot%202024-09-02%20at%207.15.15 AM.png)

Note that your environment might be a bit laggy for a few minutes because the VS Code extensions are still installing in the background.

## Open `tutorials/` and start running code!

You'll get an error the first time you try to run notebook code interactively. You need to change the kernel to the `Poetry` environment! After you do this, it should remember the setting for next time.

![](img/Screenshot%202024-09-02%20at%207.19.44 AM.png)

## Change the kernel to the `Poetry` environment

![Python can't find the requests module because it is running in the base Python installation by default. We need to activate the virtual environment.](img/Screenshot%202024-09-02%20at%207.23.19 AM.png)

Change the kernel to the Poetry virtual environment.

![Select the `Poetry` environment.](img/Screenshot%202024-09-02%20at%207.27.37 AM.png)

Run the code.

![Everything will work as expected once the `Poetry` environment is activated.](img/Screenshot%202024-09-02%20at%207.30.20 AM.png)

Once you have the correct environment, everything will just work.

## Optional Use your local installation of VS Code

![Open in Desktop VS Code.](img/Screenshot%202024-09-02%20at%207.33.25 AM.png)

Or

![Download the repository and open it in VS Code. If you have the Dev Containers extension installed, it will prompt you to open the repository in a container. Say yes!](img/Screenshot%202024-09-02%20at%207.37.04 AM.png)

![That's it!](img/Screenshot%202024-09-02%20at%207.38.15 AM.png)
