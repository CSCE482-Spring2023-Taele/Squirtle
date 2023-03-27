# -*- coding: utf-8 -*-
"""Citation Model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1y5EFkfybkBdeRbwqnpqBnUyvXj7tNJ49
"""

import re

# true positives
    # (Hancock, 1983)
    # (Collins, Williams 2019)
    # (Jenkyn et al., 2020)
    # (Kingma and Ba, 2014)
  
# edge cases
    # (Wu et al., 2019a)
    # (Cohen et al., 2010; Lin, 2008; Schuemie et al., 2004)

# cases of "lastName (2018)" should not be classified

def get_citations(citation_list: list, text: str) -> None:
    for partial_citation in citation_list:
        while (text.find(partial_citation) != -1):
            # for each partial citation, trace backwards to find first parenthesis

def find_citations(text: str) -> None:
    # search for occurances of years ranging from 1600 to 2100
    # if a closing parenthesis or semicolon follows, then we predict there is an in-text citation
        # trace backwards to first occurance of opening parenthesis or semicolon
    years_with_paren = re.findall(r"(\d{4}\))", text)
    years_with_semicolon = re.findall(r"(\d{4};)", text)
    years_with_letter_paren = re.findall(r"(\d{4}\w\))", text)
    years_with_letter_semicolon = re.findall(r"(\d{4}\w;)", text)
    print(years_with_paren)
    print(years_with_semicolon)
    print(years_with_letter_paren)
    print(years_with_letter_semicolon)

    citations = []
    


if __name__ == "__main__":
    find_citations("This is a year (name 2020b), and here is another 1983a;. Next year is 2024) and this year is 2023;")