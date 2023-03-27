import json

f = open("structuredData.json",)
pdf = json.load(f)

structured = {}

# length of total text elements
x = len(pdf["elements"])
section = pdf["elements"][0]["Text"]
structured[section] = ""

# looping through text elements
for i in range(x-1):
    if "Text" in pdf["elements"][i]:
        if pdf["elements"][i]["Path"].find("Document/H")!=-1:
            section = pdf["elements"][i]["Text"]
        if pdf["elements"][i]["Path"].find("Document/P")!=-1:
            structured[section] = structured.get(section, "") + pdf["elements"][i]["Text"]

f.close()

k = open("Output.html", "w", encoding="utf-8")
html = '''<html>
<head>
<title>Output HTML File</title>
</head> 
<body>
<h1>           
'''

#html = html + pdf["title"] + "</h1>\n"

for i in structured:
    html = html + "<h2>" + i + "</h2>\n  <p>" + structured[i] + "</p>\n"

html = html + """</body>
</html>"""

k.write(html)
k.close()
