import re

# test cases
# ((<>)Hancock, (<>)1983)
# ((<>)Collins, (<>)Williams (<>)2019)
# ((<>)Jenkyn et al., (<>)2020)
# ((<>)Kingma and Ba, (<>)2014)
# ((<>)Wu et al., (<>)2019a)
# ((<>)Cohen et al., (<>)2010; (<>)Lin, (<>)2008; (<>)Schuemie et al., (<>)2004)

# cases of "lastName (2018)" should not be classified
def classify_citations(text: str) -> str:
    print(text)
    citation_indexes = [m.start() for m in re.finditer('\(<>\)', text)]
    starting_index = -1
    ending_index = -1
    text_length = len(text)
    citations = []
    for citation_index in citation_indexes:
        # if a ( precedes the marker, we find the start of a citation
        if text[citation_index - 1] == '(':
            starting_index = citation_index - 1
        # else if ####) comes after the citation, we find the end of a citation
        if (citation_index + 9) <= text_length:
            if text[citation_index + 4 + 4] == ')': # index covers 4 for (<>) and 4 for the year
                ending_index = citation_index + 4 + 5 # take the index after the ending )
                if (ending_index - starting_index) <= 150: # if the found citation itself is less than 150 characters
                    citations.append(text[starting_index - 1: ending_index])
    for citation in citations:
        normalized_citation = '<!--' + citation + '-->'
        text = text.replace(citation, normalized_citation)
    print(text)
    return text
         
if __name__ == "__main__":
    classify_citations("Here is an example sentence here((<>) with(<>) a) couple citations ((<>)Cohen et al., (<>)2010; (<>)Lin, (<>)2008; (<>)Schuemie et al., (<>)2004). Another fact came from there ((<>)Hancock, (<>)1983).")
