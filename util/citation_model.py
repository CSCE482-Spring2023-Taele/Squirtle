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
    citations = []
    for citation_index in citation_indexes:
        if text[citation_index - 1] == '(':
            starting_index = citation_index - 1
        elif ')' in text[citation_index + 4: citation_index + 10]:
            ending_index = citation_index + 4 + text[citation_index + 4: citation_index + 10].find(')') + 1
            citations.append(text[starting_index - 1: ending_index])
    for citation in citations:
        normalized_citation = '<!--' + citation + '-->'
        text = text.replace(citation, normalized_citation)
    print(text)
    return text
         
if __name__ == "__main__":
    classify_citations("Here is an example sentence here with a couple citations ((<>)Cohen et al., (<>)2010; (<>)Lin, (<>)2008; (<>)Schuemie et al., (<>)2004). Another fact came from there ((<>)Hancock, (<>)1983a).")
