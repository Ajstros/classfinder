"""Pull data from classfinder and filter out to see what relevant classes are offered next semester."""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import argparse
from datetime import datetime
from io import StringIO

DEFAULT_OUTPUT_PATH = "classes.csv"
DEFAULT_MAJOR_CLASSES_PATH = "major_classes.csv"
DEFAULT_TAKEN_CLASSES_PATH = "taken_classes.csv"

def get_year_term(day: datetime) -> tuple[int, str]:
    """Get the year and term for a specific day.

    Parameters
    ----------


    Returns
    -------
    year, term : int, str
        The day's year and term (fall, summer, spring, j-term). E.g. ("2024", "fall")
    """

    year = day.year
    month = day.month
    if month == 1:
        term = 'j-term'
    elif month <= 5:
        term = 'spring'
    elif month <= 8:
        term = 'summer'
    else:
        term = 'fall'

    return year, term

def term_str_to_code(term_string: str) -> int:
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

def get_classes(year: int, term: str, subjects: list[str]) -> pd.DataFrame:
    """Get the classes for a specific year and term.

    Parameters
    ----------
    year : int
        The year to search classes for.
    term : str
        The string version of the term to search classes for. Case insensitive. fall, summer, spring, j-term.
    subjects : list[str]
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
            json_data = pd.read_json(StringIO(elem.script.text))
            description = json_data.drop_duplicates('name')['description'].iat[0].strip()
            class_dict["Course"].append(course)
            class_dict["Section"].append(course_section)
            class_dict["Title"].append(title)
            class_dict["Description"].append(description)
    classes_df = pd.DataFrame(class_dict)
    return classes_df

def read_major_classes(major_classes_file_path: str=DEFAULT_MAJOR_CLASSES_PATH) -> list[str]:
    """Read the classes that apply to a major from a CSV list in the file path given.

    Parameters
    ----------
    major_classes_file_path : str
        Path to the CSV containing a list of major classes. E.g. "ETLS 676,ETLS 679".

    Returns
    -------
    major_classes : list[str]
        A list of the major classes from the CSV. E.g. ["ETLS 676", "ETLS 679"].
    """

    with open(major_classes_file_path, 'r') as f:
        lines = f.readline()
    return lines.strip().split(',')

def read_taken_classes(taken_classes_file_path: str=DEFAULT_TAKEN_CLASSES_PATH) -> list[str]:
    """Read the classes that you have taken from a CSV list in the file path given.

    Parameters
    ----------
    taken_classes_file_path : str
        Path to the CSV containing a list of taken classes. E.g. "ETLS 676,ETLS 679".

    Returns
    -------
    taken_classes : list[str]
        A list of the taken classes from the CSV. E.g. ["ETLS 676", "ETLS 679"].
    """

    with open(taken_classes_file_path, 'r') as f:
        lines = f.readline()
    return lines.strip().split(',')

def select_major_classes(classes_df: pd.DataFrame, major_classes_file_path: str=DEFAULT_MAJOR_CLASSES_PATH) -> pd.DataFrame:
    """Select only the classes that apply to a major from a DataFrame of classes.

    Parameters
    ----------
    classes_df : pd.DataFrame
        DataFrame of classes including the Course number, the class Title, and its Description.
    major_classes_file_path : str
        Path to the CSV containing a list of major classes. E.g. "ETLS 676,ETLS 679".

    Returns
    -------
    major_classes_only_df : pd.DataFrame
        DataFrame of classes that apply to a major from the given classes including the Course number, the class Title, and its Description. Note this DataFrame is copied out of the given DataFrame.
    """

    major_classes = read_major_classes(major_classes_file_path)
    return classes_df.loc[classes_df["Course"].isin(major_classes)].copy()

def select_not_taken_classes(classes_df: pd.DataFrame, taken_classes_file_path: str=DEFAULT_TAKEN_CLASSES_PATH) -> pd.DataFrame:
    """Select only the classes that have not been taken from a DataFrame of classes.

    Parameters
    ----------
    classes_df : pd.DataFrame
        DataFrame of classes including the Course number, the class Title, and its Description.
    taken_classes_file_path : str
        Path to the CSV containing a list of taken classes. E.g. "ETLS 676,ETLS 679".

    Returns
    -------
    taken_classes_only_df : pd.DataFrame
        DataFrame of classes that have not been taken from the given classes including the Course number, the class Title, and its Description. Note this DataFrame is copied out of the given DataFrame.
    """

    taken_classes = read_taken_classes(taken_classes_file_path)
    return classes_df.loc[~classes_df["Course"].isin(taken_classes)].copy()

def get_major_classes(year: int, term: str, subjects: list[str], major_classes_file_path: str=DEFAULT_MAJOR_CLASSES_PATH) -> pd.DataFrame:
    """Get only the classes that apply to a major from the classfinder site.

    Parameters
    ----------
    year : int
        The year to search classes for.
    term : str
        The string version of the term to search classes for. Case insensitive. fall, summer, spring, j-term.
    subjects : list[str]
        A list of subject codes to search for. E.g. ["ETLS", "SEIS"].
    major_classes_file_path : str
        Path to the CSV containing a list of major classes. E.g. "ETLS 676,ETLS 679".

    Returns
    -------
    major_classes_only_df : pd.DataFrame
        DataFrame of classes that apply to a major from the given classes including the Course number, the class Title, and its Description.
    """

    full_df = get_classes(year=year, term=term, subjects=subjects)
    return select_major_classes(full_df, major_classes_file_path)


DEFAULT_YEAR, DEFAULT_TERM = get_year_term(datetime.today())
DEFAULT_SUBJECTS = ["ETLS", "SEIS"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        prog='ClassFinder',
                        description='Pull data from classfinder and filter out to see what relevant classes are offered next semester.',
    )
    parser.add_argument('-o', '--output', default=DEFAULT_OUTPUT_PATH, help='output CSV file to write DataFrame to')
    parser.add_argument('-y', '--year', default=DEFAULT_YEAR, help='year to find classes for')
    parser.add_argument('-t', '--term', choices=['fall', 'summer', 'spring', 'j-term'], default=DEFAULT_TERM, help='year to find classes for')
    parser.add_argument('-s', '--subjects', default=DEFAULT_SUBJECTS, help='subjects to find classes from')
    parser.add_argument('-q', '--quiet', action='store_true', help='suppress all printing. Still outputs to a CSV')
    parser.add_argument('-m', '--major', nargs='?', const=DEFAULT_MAJOR_CLASSES_PATH, help='find only classes that apply to a major. Uses the given CSV filename to read major classes')
    parser.add_argument('-f', '--filter-taken', nargs='?', const=DEFAULT_TAKEN_CLASSES_PATH, help='find only classes not yet taken. Uses the given CSV filename to read taken classes')
    parser.add_argument('--no-sections', action='store_true', help='do not include the sections column in the CSV or the printed output. Courses with multiple sections will be listed only once')

    args = parser.parse_args()
    year = args.year
    term = args.term
    subjects = args.subjects

    if args.major is not None:
        if not args.quiet:
            print(f'Showing only major classes. Reading major classes from {args.major}')
        df = get_major_classes(year, term, subjects, args.major)
    else:
        df = get_classes(year, term, subjects)

    if args.filter_taken is not None:
        if not args.quiet:
            print(f'Showing only non-taken classes. Reading taken classes from {args.filter_taken}')
        df = select_not_taken_classes(df, args.filter_taken)

    if args.no_sections:
        df.drop(columns='Section', inplace=True)
        df.drop_duplicates(inplace=True)

    df.to_csv(args.output)

    if not args.quiet:
        print(f'{term.title()} {year}\n')
        print(df)
