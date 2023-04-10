class jsontohtml:
    def __init__(self, json_filename, remove_citations):
        self.filename = json_filename
        self.citation_flag = remove_citations

    def json2html(self):
        import json
        file = self.filename
        f = open(file,)
        pdf = json.load(f)

        structured = {}

        # length of total text elements
        x = len(pdf["elements"])
        if "Text" in pdf["elements"][0]:
            section = pdf["elements"][0]["Text"]
            section = section[:-1]
            structured[section] = ""
        else:
            section = ""

        # looping through text elements
        for i in range(x-1):
            if "Text" in pdf["elements"][i]:
                if pdf["elements"][i]["Path"].find("Document/H") != -1:
                    section = pdf["elements"][i]["Text"]
                    section = section[:-1]
                if pdf["elements"][i]["Path"].find("Document/P") != -1:
                    structured[section] = structured.get(section, "") + pdf["elements"][i]["Text"]
                if pdf["elements"][i]["Path"].find("Document/Title") != -1:
                    section = pdf["elements"][i]["Text"]
                    structured[section] = ""

        f.close()
        html = '''<html>
        <head>
        <title>Output HTML File</title>
        <link rel="preconnect" href="https://fonts.googleapis.com/%22%3E/n<link rel="preconnect" href="https://fonts.gstatic.com/" crossorigin>\n<link href="https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap" rel="stylesheet">\n<style>\n@import url(https://fonts.googleapis.com/css2?family=Noto+Serif&family=Roboto:wght@300;400&family=VT323&display=swap);\nhtml {\nfont-family: "Noto Serif", serif;\n}\nbr {\ndisplay: block;\nmargin: 4% 0;\ncontent: "";\n}\na {\ncolor: #1857b6;\ntransition: color .25s ease-out;\nfont-size: 1.15rem;\n}\na:hover {\ncolor: #11223d;\ntext-decoration: none\n}\nh1,h2 {\ncolor: #11223d;\n}\np {\nfont-size: 1.5rem;\n}\nh2 {\nfont-size: 2rem;\n}\nhr {\ncolor: #11223d;\nheight: 0.15%;\nbackground-color: #11223d;\nwidth: 100%;\n}\n</style>
        </head> 
        <body style="display: flex;">
        <div style="min-width: 15%; max-width: 15%; margin: 0 2%; overflow: auto;">
        <h1>Table of contents</h1>
        '''

        for i in structured:
            html = html + "<a href=\"#" + i + "\">" + i + "</a>\n <br>\n"
        html = html + "</div>\n" + "<div style=\"overflow: auto; height: auto; border-left: solid; padding-left: 2%; padding-right: 2%\">"

        for i in structured:
            html = html + "<div id=\"" + i + "\">\n"
            html = html + "<h2>" + i + "</h2>\n  <p>" + structured[i] + "</p>\n"
            html = html + "</div>\n"
        html = html + "</div>"
        html = html + """</body>
        </html>"""

        if not self.citation_flag:
            return html
        return self.classify_citations(html)
    
    def classify_citations(self,text):
        import re
        print('Removing Citations')
        # print(text)
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
                        starting_index = -1
                        ending_index = -1
        citations = list(set(citations))
        for citation in citations:
            normalized_citation = '<!--' + citation + '-->'
            text = text.replace(citation, normalized_citation)
        return text
