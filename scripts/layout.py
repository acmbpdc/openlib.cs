from bs4 import BeautifulSoup
from os import makedirs, listdir
from os.path import join, exists
from markdown import markdown
import re
import json
import yaml

if __name__ == "__main__":
    courses = [x for x in listdir("../courses")]
    for c in courses:
        input_file = join("../courses", c, "README.md")
        with open(input_file, "r") as f:
            raw = f.read()
            indices = [m.start() for m in re.finditer(r"#+ .*", raw)]
            texts = []
            for i, _ in enumerate(indices):
                s = indices[i]
                e = indices[i+1] if i+1 < len(indices) else len(raw)
                texts.append(raw[s:e])
            
            data = {}
            overview = ""
            for t in texts:
                html = markdown(t, extensions=['tables'])
                soup = BeautifulSoup(html, "html.parser")
                heading = soup.find(['h2'])
                if heading is not None:
                    ht = heading.text
                    if ht == "Overview":
                        overview = "\n\n".join(t.split("\n\n")[1:])
                        assert overview != ""
                    elif ht == "Textbooks":
                        data["textbooks"] = []
                        rows = soup.find('table').find('tbody').find_all('tr')
                        for row in rows:
                            row_t = [d.text for d in row.find_all('td')]
                            b = {}
                            
                            b["title"] = row_t[0]
                            b["authors"] = row_t[1]
                            m = re.search(r"(\d+[A-Za-z]+)\s*\((\d+)\)", row_t[2])
                            if m is not None:
                                b["edition"] = m.groups()[0]
                                b["year"] = m.groups()[1]
                            
                            data["textbooks"].append(b)
                        assert len(rows) == len(data["textbooks"])
                    elif ht != "Navigation":
                        links = []
                        for l in soup.find_all('a'):
                            link = {}
                            link["url"] = l.get("href") 
                            if l.find('em') is not None:
                                link["author"] = l.find('em').text
                                link["title"] = re.sub(f"""{link["author"]}$""", "", l.text)
                            else:
                                link["title"] = l.text
                            links.append(link)
                        data[ht.lower()] = links
            
            output_file = join("../courses", f"{c}.md")
            with open(output_file, "w") as of:
                of.write("---\n")
                of.write(yaml.dump(data, allow_unicode=True, default_flow_style=False, indent=4))
                of.write("---\n\n")
                of.write(overview)