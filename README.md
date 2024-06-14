# Classfinder in Python
Grab the available classes for a specified year and term. Optionally filter by only classes for my degree (MSEE, embedded track, defined in `major_classes.csv`). Optionally filter out classes I have already taken (defined in `taken_classes.csv`).

# Usage

```bash
$ python .\classfinder.py -h                                                                           
usage: ClassFinder [-h] [-o OUTPUT] [-y YEAR] [-t {fall,summer,spring,j-term}] [-s SUBJECTS] [-q] [-m [MAJOR]] [-f [FILTER_TAKEN]] [--no-sections]

Pull data from classfinder and filter out to see what relevant classes are offered next semester.

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output CSV file to write DataFrame to
  -y YEAR, --year YEAR  year to find classes for
  -t {fall,summer,spring,j-term}, --term {fall,summer,spring,j-term}
                        year to find classes for
  -s SUBJECTS, --subjects SUBJECTS
                        subjects to find classes from
  -q, --quiet           suppress all printing. Still outputs to a CSV
  -m [MAJOR], --major [MAJOR]
                        find only classes that apply to a major. Uses the given CSV filename to read major classes
  -f [FILTER_TAKEN], --filter-taken [FILTER_TAKEN]
                        find only classes not yet taken. Uses the given CSV filename to read taken classes
  --no-sections         do not include the sections column in the CSV or the printed output. Courses with multiple sections will be listed only once
```

# Example

With `major_classes.csv` in the current directory, containing:

```csv
ETLS 676,ETLS 679,ETLS 630,ETLS 631,ETLS 678,ETLS 675,ETLS 699,ETLS 620,ETLS 621,ETLS 739,ETLS 744,ETLS 745,ETLS 746,ETLS 747,ETLS 748,ETLS 750,ETLS 751,ETLS 753,ETLS 795,ETLS 810,SEIS 631,SEIS 663,SEIS 763,SEIS 764,ETLS 881
```

and `taken_classes.csv` in the current directory, containing:

```csv
ETLS 676,ETLS 675,ETLS 699
```

We can get the following.

```bash
$ python .\classfinder.py -y 2024 -t fall  -m -f --no-sections
Showing only major classes. Reading major classes from major_classes.csv
Showing only non-taken classes. Reading taken classes from taken_classes.csv
Fall 2024

      Course                          Title                                        Description
15  ETLS 620          Communication Systems  Introduction to Fourier analysis of noise and ...
19  ETLS 678     Applications of AI in Engr  Introduction to wearable sensor systems, appli...
30  ETLS 739     EV Market and Technologies  A one semester graduate course exploring the k...
31  ETLS 744  Power Systems and Smart Grids  An introduction to the practical aspects of po...
32  ETLS 748    Renewable Energy Generation  Energy is one of the most important issues of ...
33  ETLS 753   Power Sys Protection & Relay  This course covers the fundamentals of and the...
54  SEIS 631  Data Preparation and Analysis  This course provides a broad introduction to t...
60  SEIS 663  Introduction to Cybersecurity  This overview course will provide the foundati...
69  SEIS 763               Machine Learning  Machine Learning builds computational systems ...
71  SEIS 764        Artificial Intelligence  Artificial Intelligence has made significant s...
```
