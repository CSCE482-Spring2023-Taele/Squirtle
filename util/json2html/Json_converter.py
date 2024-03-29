import re
import json
from prettytable import PrettyTable
from xlsx2html import xlsx2html
from eyecite import get_citations

class jsontohtml:
    def __init__(self, foldername, remove_citations, sonify_images, secretStr):
        self.directory = foldername
        self.filename = foldername + "/structuredData.json"
        self.citation_flag = remove_citations
        self.sonify_flag = sonify_images
        self.secretStr = secretStr

    def json2html(self):
        file = self.filename
        f = open(file,)
        pdf = json.load(f)

        structured = {}

        # length of total text elements
        x = len(pdf["elements"])
        section = ""

        # looping through text elements
        for i in range(x-1):
            if "Text" in pdf["elements"][i]:
                if pdf["elements"][i]["Path"].find("Document/H") != -1:
                    section = pdf["elements"][i]["Text"]
                    section = section[:-1]
                if pdf["elements"][i]["Path"].find("/P") != -1 and pdf["elements"][i]["Path"].find("Table") == -1:
                    if not pdf["elements"][i]["Text"].endswith(". "):
                        structured[section] = structured.get(section, "") + pdf["elements"][i]["Text"]
                    else:   
                        structured[section] = structured.get(section, "") + pdf["elements"][i]["Text"] + "<br><br>"
                if pdf["elements"][i]["Path"].find("Document/Title") != -1:
                    section = pdf["elements"][i]["Text"]
                    structured[section] = ""
            if pdf["elements"][i]["Path"].find("Figure") != -1:
                structured[pdf["elements"][i]["filePaths"][0]] = ""
            if pdf["elements"][i]["Path"].find("Table") != -1:
                structured[pdf["elements"][i].get("filePaths",[""])[0]] = ""
                


        f.close()
        html = '''<html>
        <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js" integrity="sha512-q/dWJ3kcmjBLU4Qc47E4A9kTB4m3wuTY7vkFJDTZKjTs8jhyGQnaUrxa0Ytd0ssMZhbNua9hE+E7Qv1j+DyZwA==" crossorigin="anonymous"></script>
        <script>
            window.onbeforeunload = function () {
                socket.emit('disconnect');
            }
            var socket = io();
                socket.on('connect', function() {
            });
        </script>
        <title>Output HTML File</title>
        <link rel="preconnect" href="https://fonts.googleapis.com/%22%3E/n<link rel="preconnect" href="https://fonts.gstatic.com/" crossorigin> <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap" rel="stylesheet"> <style> @import url(https://fonts.googleapis.com/css2?family=Noto+Serif&family=Roboto:wght@300;400&family=VT323&display=swap); @import url(https://fonts.googleapis.com/css2?family=Courgette&family=Space+Grotesk:wght@300;400&display=swap); html { font-family: "Noto Serif", serif; } br { display: block; margin: 4% 0; content: ""; } a { color: #1857b6; transition: color .25s ease-out; font-size: 1.15rem; } a:hover { color: #11223d; text-decoration: none } h1,h2 { color: #11223d; } p { font-size: 1.5rem; } h2 { font-size: 2rem; } hr { color: #11223d; height: 0.15%; background-color: #11223d; width: 100%; } .app_header { background: #11223d; padding: 12px 16px; position: fixed; width: 100%; display: flex; justify-content: space-between; z-index: 10; } .button { line-height: 20px; padding: 6px 12px; text-decoration: none; border: 1px solid #9ac2ff; color: #9ac2ff; display: block; border-radius: 4px; margin-left: 12px; font-size: 1.1rem; white-space: nowrap; transition: all .25s ease-out; } </style>
        </head> 
        <body style="display: flex; margin: 0;">
        <header class="app_header">
            <div>
                <a href="/" class="button">Home</a>
            </div>
            <div style="font-size: 2rem; color: white; font-family:'Courgette', cursive;">pdf max</div>
            <img src="https://cdn.discordapp.com/attachments/933852328409313280/1093286323592368228/512px-Accessibility.svg.png" style="width: 2.5%; margin-right: 2.5%;"/>
        </header>
        <div style="min-width: 15%; max-width: 15%; margin: 5% 2%; overflow: auto;">
        <h1>Table of contents</h1>
        '''

        for i in structured:
            if (i.find("figures/fileoutpart") == -1) and (i.find("tables/fileoutpart") == -1):
                html = html + "<a href=\"#" + i + "\">" + i + "</a>\n <br>\n"
        html = html + "</div>\n" + "<div style=\"overflow: auto; height: auto; border-left: solid; padding: 5% 2%;\">"

        for i in structured:
            if i.find("figures/fileoutpart") != -1:
                html = html + "<div id=\"" + i + "\">\n"
                imagepath = self.secretStr + "/" + i
                html = html + "<img src=\"" + "{{url_for('static', filename = '" + imagepath + "')}}\"" + ">"
                if self.sonify_flag:
                    soundpath = imagepath[:-3] + "wav"
                    html = html + "<audio controls>\n" + "<source src=\"" + "{{url_for('static', filename = '" + soundpath + "')}}\"" + " type=\"audio/wav\" >\n" + "</audio>"
                html = html + "</div>\n" + "<br>"
            elif i.find("tables/fileoutpart") != -1:
                tablepath = self.directory + "/" + i
                out_stream = xlsx2html(tablepath)
                out_stream.seek(0)
                html = html + "<div id=\"" + i + "\">\n"
                html = html + out_stream.read().replace('_x000D_', "")
                html = html + "</div>\n" + "<br>"
            else:
                html = html + "<div id=\"" + i + "\">\n"
                html = html + "<h2>" + i + "</h2>\n  <p>" + structured[i] + "</p>\n"
                html = html + "</div>\n"
        html = html + "</div>"
        html = html + """</body>
        </html>"""

        
        if not self.citation_flag:
            return html.replace("(<>)","")
        return self.classify_citations(html)
    
    def classify_citations(self,text):
        print('Removing Citations')
        citation_indexes = [m.start() for m in re.finditer('\(<>\)', text)]
        starting_index = -1
        ending_index = -1
        text_length = len(text)
        citations = []
        if len(citation_indexes) != 0:
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
        print('CITATION MODEL --- Number of (name year)-style citations found: ' + str(len(citations)))
        citations = list(set(citations))
        for citation in citations:
            # normalized_citation = '<!--' + citation + '-->'
            text = text.replace(citation, '')
        bracket_citations = []
        bracket_citation_indexes = [m.start() for m in re.finditer('\[\d\]', text)] + [m.start() for m in re.finditer('\[\d\d\]', text)] + [m.start() for m in re.finditer('\[\d\d\d\]', text)]
        if len(bracket_citation_indexes) != 0:
            for bracket_citation_index in bracket_citation_indexes:
                ending_bracket = text[bracket_citation_index:].find(']')
                if ending_bracket <= bracket_citation_index + 5:
                    bracket_citations.append(text[bracket_citation_index: bracket_citation_index + ending_bracket + 1])
        print('CITATION MODEL --- Number of [#]-style citations found: ' + str(len(bracket_citations)))
        bracket_citations = list(set(bracket_citations))
        if len(bracket_citations) != 0:
            for bracket_citation in bracket_citations:
                text = text.replace(bracket_citation, '')
        text = text.replace('(<>)', '')
        legal_citation_indexes = get_citations(text)
        legal_citations = []
        if len(legal_citation_indexes) != 0:
            for legal_citation_index in legal_citation_indexes:
                citation_span = legal_citation_index.full_span()
                legal_citations.append(text[citation_span[0] : citation_span[1]])
        print('CITATION MODEL --- Number of legal-style citations found: ' + str(len(legal_citations)))
        legal_citations = list(set(legal_citations))
        if len(legal_citations) != 0:
            for legal_citation in legal_citations:
                text = text.replace(legal_citation, '')
        return text
