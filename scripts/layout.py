from bs4 import BeautifulSoup
from os import makedirs
from os.path import join, exists
from markdown import markdown
import re

if __name__ == "__main__":
    with open("../README.md", "r") as f:
        html = markdown(f.read())
    
    with open("./readme_format.md", "r") as f:
        readme_format = f.read()
    
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.findAll('a', {"href" : re.compile("^./")}):
        course = link.get_text()
        path = join("../", link.get("href"))
        readme = join(path, "README.md")
        print(course)
        
        # Create directory only if not exists
        if not exists(path):
            print("\tCreating directory")
            makedirs(path)
        else:
            print("\tDirectory already exists")
        
        # Create README only if not exists
        if not exists(readme):
            print("\tCreating README\n")
            with open(readme, "w") as f:
                f.write(readme_format.format(course=course))
        else:
            print("\tREADME already exists\n")
