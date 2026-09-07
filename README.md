# Website for CSC 413 at the University of Toronto Mississauga (Fall 2026)

🔗 https://utm-csc413.github.io/2026F-website/

## Quarto Website Setup Guide

This guide will help you set up, compile, and deploy the CSC413 course website using Quarto.

### 1. Install Quarto

Visit the offical [Quarto website](https://quarto.org/docs/get-started/) to download and install Quarto. Make sure to follow the installation instructions for your operating system (Windows, macOS, Linux). You can verify the installation by running:

``` bash
quarto --version
```

### 2. Clone the Repository

Clone this repository to your local machine:

``` bash
git clone https://github.com/utm-csc413/2026F-website.git
cd 2026F-website
```

### 3. Set Up R (required for slides with executable R code)

Slides under `slides/` run R code and depend on a large set of packages pinned in `renv.lock` via [renv](https://rstudio.github.io/renv/).

1. Install R (this project was last synced against R 4.4.3, but any recent R 4.x should work).
2. Install a Fortran compiler — some packages (e.g. `rms`, `mvtnorm`) build from source and need one:
   - **macOS**: install the official [R development tools](https://mac.r-project.org/tools/) (provides `gfortran` at `/opt/gfortran`, the path R expects). If you use Homebrew's `gfortran` (`brew install gcc`) instead, tell R where to find it by creating `~/.R/Makevars`:
     ``` make
     FC = /opt/homebrew/bin/gfortran
     F77 = /opt/homebrew/bin/gfortran
     FLIBS = -L/opt/homebrew/lib/gcc/current -lgfortran -lquadmath -lm
     ```
     (adjust the `gcc` lib path to match your `brew --prefix gcc`)
   - **Windows**: install [Rtools](https://cran.r-project.org/bin/windows/Rtools/) matching your R version.
   - **Linux**: install via your package manager, e.g. `sudo apt install gfortran`.
3. From the repo root, install and restore the pinned packages:
   ``` r
   install.packages("renv")
   renv::restore()
   ```
   This installs every package in `renv.lock` at its pinned version, including the two GitHub-only packages (`colorblindr`, `emo`).

### 4. Set Up Python (required for `lecs/w10/lec10.qmd`)

One lecture (`lecs/w10/lec10.qmd`) runs executable PyTorch code cells via a dedicated Jupyter kernel named `myenv`. Set it up with:

``` bash
python3 -m venv myenv
myenv/bin/pip install torch numpy ipykernel
myenv/bin/python -m ipykernel install --user --name myenv --display-name "Python (myenv)"
```

Quarto will automatically pick up the `myenv` kernel when rendering that file.

> **Note:** `renv.lock` only tracks R package versions — it does not cover the R interpreter/compiler toolchain (like `gfortran` above) or this Python environment, so both need to be set up separately.

### 5. Compile the Website and Run Locally

To compile the source files (.qmd, .md) into a HTML website, run the following command after navigating to the cloned repository:

``` bash
quarto render
```

This will generate the HTML files from the source files and will be placed in the \_site/ directory by default (configurable in \_quarto.yml).

Then to preview the website locally with live reload:

``` bash
quarto preview
```

This command will start a local development server, allowing you to view the website in your browser (e.g. `http://localhost:4200`).

More details on rendering can be found in the [Quarto documentation](https://quarto.org/docs/websites/).

### 6. Deploy to GitHub Pages

To publish the compiled site directly to GitHub Pages, run the following command:

``` bash
quarto publish gh-pages
```

This command will push the contents of the `_site/` directory to the `gh-pages` branch of the repository, making it available at `https://utm-csc413.github.io/2026F-website/`.

## Colors

-   website background: #D9E3E4
-   headings: #5B888C

## Attribution

Much of the content is based on [STA 210 - Fall 2021](https://github.com/sta210-fa21/) by Dr. Maria Tackett and [STA210](https://sta210-s22.github.io/website/) by Dr. Mine Çetinkaya-Rundel.

<hr>

<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" alt="Creative Commons License" style="border-width:0"/></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>.