"""Pull data from classfinder and filter out to see what relevant classes are offered next semester."""

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

OUTPUT_FILE = "classes.csv"

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
    class_dict : pd.DataFrame
        DataFrame of the classes found including the Course number, the class Title, and its Description.
    """

    term_code = term_str_to_code(term)
    url = f"https://classes.aws.stthomas.edu/index.htm?year={year}&term={term_code}&schoolCode=ALL&levelCode=ALL&selectedSubjects={','.join(subjects)}#advancedSearch"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    subject_course_elems = soup.find_all("div", class_=["course", "cf"])

    class_dict = {"Course": [], "Title": [], "Description": []}
    current_subject = ''

    for elem in subject_course_elems :
        if 'cf' in elem['class']:
            # Subject
            current_subject = elem.text.strip().split(':')[0]
        else:
            # Course
            course = f'{current_subject} {elem.span.text}'
            title = elem.strong.text
            json_data = json.loads(elem.script.text, strict=False)
            description = json_data['description'].strip()
            class_dict["Course"].append(course)
            class_dict["Title"].append(title)
            class_dict["Description"].append(description)
    df = pd.DataFrame(class_dict)
    return df

if __name__ == "__main__":
    year = 2024
    term = 'fall'
    subjects = ["ETLS", "SEIS"]
    df = get_classes(year, term, subjects)
    df.to_csv(OUTPUT_FILE)
