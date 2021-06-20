import json

def _textbook(subject: str, chapter: str):
    def drivify_link(tag: str):
        return f"https://drive.google.com/drive/folders/{tag}?usp=sharing"

    with open("C:/Users/Shlok/J.A.R.V.I.SV2021/json_files/drive_links.json", "r") as f:
        subjects: dict[str: dict[str:str]] = json.load(f)
    if subject:
        chapters: dict = subjects.get(subject.title())
        if chapter:
            # embed = await set_timestamp(Embed(title=f"`{subject.title()}`", description="",
            #                                   colour=Colour.random(), url=drivify_link(subjects.get("link"))))
            chapters: str = chapters.get(chapter.title())
            if chapters:
                # embed.title = None
                # embed.description = f"[`{chapter.title()}`]({chapters})"
                pass

_textbook("Math", "polynomials")
