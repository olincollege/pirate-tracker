---
title: README
jupyter: python3
---
<hr>

## How to Use
<hr>

## Visualizing Pirate Attacks Across the Globe
Online, we had pulled a PDF of all the pirate attacks/incidents that occured over the course of the 2024 year. Given this information, we were able to use an online library, `pdfplumber`, to help digest this information. 

Here is the function we had used to collect the text:
```sh
with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"
```
A massive flaw of `pdfplumber` was that the text collects line by line by line. Given this information, we have to further our rendering of the data by removing the headers and the
### 
Given a function that examines the text from a pdf


## Requirements

The `requirements.txt` file is blank and should be filled out with any project
dependencies. There is a Python package called `pipreqs` that autogenerates the
contents of the `requirements.txt` file based on the `import` statements in your
`.py` files. To get this, run

```
pip install pipreqs
```

Then, in the root of your project repository, run:

```
pipreqs --mode compat
```

If you already have a `requirements.txt`, the above command will ask you to
rerun the command with the `--force` flag to overwrite it.
