"""Pull data from classfinder and filter out to see what relevant classes are offered next semester."""

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

DEFAULT_OUTPUT_PATH = "classes.csv"
DEFAULT_MAJOR_CLASSES_PATH = "major_classes.csv"
DEFAULT_TAKEN_CLASSES_PATH = "taken_classes.csv"

def term_str_to_code(term_string):
    """Convert term string to code for URL.

    Parameters
    ----------
    term_string : str
        The string version of the term. Case insensitive. fall, summer, spring, j-term.

    Returns
    -------
    term_code : int
        The corresponding URL code for the input term string.
    """

    term_dict = {
        'fall' : 40,
        'summer' : 30,
        'spring' : 20,
        'j-term' : 10,
    }
    return term_dict[term_string.lower()]

def get_classes(year, term, subjects):
    """Get the classes for a specific year and term.

    Parameters
    ----------
    year : int
        The year to search classes for.
    term : str
        The string version of the term to search classes for. Case insensitive. fall, summer, spring, j-term.
    subjects : List[str]
        A list of subject codes to search for. E.g. ["ETLS", "SEIS"].

    Returns
    -------
    classes_df : pd.DataFrame
        DataFrame of the classes found including the Course number, the class Title, and its Description.
    """

    term_code = term_str_to_code(term)
    url = f"https://classes.aws.stthomas.edu/index.htm?year={year}&term={term_code}&schoolCode=ALL&levelCode=ALL&selectedSubjects={','.join(subjects)}#advancedSearch"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    subject_course_elems = soup.find_all("div", class_=["course", "cf"])

    class_dict = {"Course": [], "Section": [], "Title": [], "Description": []}
    current_subject = ''

    for elem in subject_course_elems :
        if 'cf' in elem['class']:
            # Subject
            current_subject = elem.text.strip().split(':')[0]
        else:
            # Course
            course_number, course_section = elem.span.text.split('-')
            course = f'{current_subject} {course_number}'
            title = elem.strong.text
            json_data = json.loads(elem.script.text, strict=False)
            description = json_data['description'].strip()
            class_dict["Course"].append(course)
            class_dict["Section"].append(course_section)
            class_dict["Title"].append(title)
            class_dict["Description"].append(description)
    classes_df = pd.DataFrame(class_dict)
    return classes_df

def read_major_classes(major_classes_file_path=DEFAULT_MAJOR_CLASSES_PATH):
    """Read the classes that apply to a major from a CSV list in the file path given.

    Parameters
    ----------
    major_classes_file_path : str
        Path to the CSV containing a list of major classes. E.g. "ETLS 676, ETLS 679".

    Returns
    -------
    major_classes : List[str]
        A list of the major classes from the CSV. E.g. ["ETLS 676", "ETLS 679"].
    """

    with open(major_classes_file_path, 'r') as f:
        lines = f.readline()
    return lines.strip().split(',')

def select_major_classes(classes_df, major_classes_file_path=DEFAULT_MAJOR_CLASSES_PATH):
    """Select only the classes that apply to a major from a DataFrame of classes.

    Parameters
    ----------
    classes_df : pd.DataFrame
        DataFrame of classes including the Course number, the class Title, and its Description.
    major_classes_file_path : str
        Path to the CSV containing a list of major classes. E.g. "ETLS 676, ETLS 679".

    Returns
    -------
    major_classes_only_df : pd.DataFrame
        DataFrame of classes that apply to a major from the given classes including the Course number, the class Title, and its Description. Note this DataFrame is copied out of the given DataFrame.
    """

    major_classes = read_major_classes(major_classes_file_path)
    return classes_df[classes_df["Course"].isin(major_classes)].copy()

def get_major_classes(year, term, subjects, major_classes_file_path=DEFAULT_MAJOR_CLASSES_PATH):
    """Get only the classes that apply to a major from the classfinder site.

    Parameters
    ----------
    major_classes_file_path : str
        Path to the CSV containing a list of major classes. E.g. "ETLS 676, ETLS 679".

    Returns
    -------
    major_classes_only_df : pd.DataFrame
        DataFrame of classes that apply to a major from the given classes including the Course number, the class Title, and its Description.
    """

    full_df = get_classes(year=year, term=term, subjects=subjects)
    return select_major_classes(full_df, major_classes_file_path)

if __name__ == "__main__":
    year = 2024
    term = 'fall'
    subjects = ["ETLS", "SEIS"]
    major_df = get_major_classes(year, term, subjects)
    major_df.to_csv(DEFAULT_OUTPUT_PATH)
    print(major_df)
