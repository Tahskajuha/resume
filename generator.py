from pathlib import Path
from PIL import Image
import argparse
import yaml


parser = argparse.ArgumentParser(description="Resume inputs")
parser.add_argument(
    "-P", "--projects", nargs="+", help="List of project IDs to be included"
)
parser.add_argument(
    "-S", "--skills", nargs="+", help="Predefined skillsets to be included"
)
parser.add_argument(
    "-s",
    "--extraskills",
    nargs="+",
    help="List of skills to be appended to the skillset in this instance",
)
args = parser.parse_args()


def read_jpeg(path: Path):
    with Image.open(path) as img:
        width, height = img.size

    data = path.read_bytes()

    return {
        "width": width,
        "height": height,
        "length": len(data),
        "hex": data.hex().upper(),
    }


def read_yaml(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def render_project(project):
    techout = " • ".join(project["technologies"])
    bulletout = "\n".join(f"\\item {bullet}" for bullet in project.get("bullets", []))
    return (
        rf"\timelineitem"
        rf"{{}}"
        rf"{{{project['start']} - {project['end']}}}"
        rf"{{{project['title']}}}"
        rf"{{{techout}}}"
        rf"{{{bulletout}}}"
        rf"{{{project.get('link', '')}}}"
    )


image = read_jpeg(Path("photo.jpeg"))
projects = []
for projectID in args.projects:
    p = read_yaml(Path("projects") / f"{projectID}.yml")
    projects.append(p)
skillsets = read_yaml(Path("skills.yml"))
skills = []
seen = set()
for name in args.skills or []:
    for skill in skillsets[name]:
        if skill not in seen:
            seen.add(skill)
            skills.append(skill)
for skill in args.extraskills or []:
    if skill not in seen:
        seen.add(skill)
        skills.append(skill)


projectsout = ""
for project in projects:
    projectsout += "\n" + render_project(project)
skillsout = ",".join(skills)


with open("template.tex", "r", encoding="utf-8") as f:
    tex = f.read()
tex = tex.replace("%<image width>%", str(image["width"]))
tex = tex.replace("%<image height>%", str(image["height"]))
tex = tex.replace("%<image byte length>%", str(image["length"]))
tex = tex.replace("%<image bytes hex encoded>%", image["hex"])
tex = tex.replace("%<skills list>%", skillsout)
tex = tex.replace("%<projects stuff>%", projectsout)

with open("build/resume.tex", "w", encoding="utf-8") as f:
    f.write(tex)
