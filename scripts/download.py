from bs4 import BeautifulSoup
from os import makedirs
from os.path import join, exists
from markdown import markdown
import re
import gdown


if __name__ == "__main__":
    with open("../README.md", "r") as f:
        soup = BeautifulSoup(markdown(f.read()), "html.parser")
    
    for link in soup.findAll('a', {"href" : re.compile("^./")}):
        course = link.get_text()
        path = join("../", link.get("href"))
        readme = join(path, "README.md")

        print(course)
        if not exists(readme):
            print("\tREADME missing")
            continue
        else:
            print("\tREADME found")
            with open(readme, "r") as f:
                s = BeautifulSoup(markdown(f.read()), "html.parser")
            
            texts = {l.get_text():l.get("href") for l in s.findAll('a', {"href" : re.compile("^https://drive.google.com/")})}
            if len(texts) > 0:
                print(f"\t\t{len(texts)} Google Drive links found")
                for name, url in texts.items():
                    tbdir = join(path, "textbooks")
                    if not exists(tbdir):
                        makedirs(tbdir)
                    filename = join(tbdir, f"{name}.pdf")

                    if not exists(filename):
                        id = re.search("[-\w]{25,}",url).group(0)
                        download_link = f"""https://drive.google.com/uc?id={id}&export=download"""
                        gdown.download(download_link, filename, quiet=False)
                    else:
                        print(f"\t{name} already exists")
            else:
                print("\tNo Google Drive links found")
        print()
