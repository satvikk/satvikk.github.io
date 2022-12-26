"""
This script can be run to create post.html files for each topic. Variables in the ~/posts/template.html are replaced values from the ~/assets/python/variables.json.
Variables in template are defined by text written as VARIABLE::xyz . the value of xyz is replaced by json's xyz entry within each topic.
Run this script whenever you make changes to template. changes to individual post.html will be overwritten.
"""
import fileinput
import json
import shutil


def make_single_post(template_file, variables, name):
    """
    create a single post.html file
    Arguments:
        template_file: path to the template.html
        variables: a mapping dictionary of variables (keys) to be replaced in template by (values)
        name: topic name, eg: ctscan
    """
    newfilename = "posts/" + name + "/post.html"
    shutil.copyfile(template_file, newfilename)

    if "BANNER" not in variables:
        variables[
            "BANNER"
        ] = '<span class="image featured"><img src="banner.png" alt="" /></span>'
    elif variables["BANNER"] == "iframe-youtube":
        variables["BANNER"] = f'<iframe width="100%" src="{variables["YOUTUBE"]}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="aspect-ratio: 16 / 9;"></iframe><br><br>'
    elif variables["BANNER"] == "embed-canva":
        variables["BANNER"] = (
            '<div style="position: relative; width: 100%; height: 0; padding-top: 56.2500%; padding-bottom: 0; box-shadow: 0 2px 8px 0 rgba(63,69,81,0.16); margin-top: 1.6em; margin-bottom: 0.9em; overflow: hidden; border-radius: 8px; will-change: transform;">' +
            '<iframe loading="lazy" style="position: absolute; width: 100%; height: 100%; top: 0; left: 0; border: none; padding: 0;margin: 0;"' +
            f'src={variables["CANVA"]} allowfullscreen="allowfullscreen" allow="fullscreen">' +
            '</iframe></div>'
        )
        

    for var in variables:
        # print(var, variables[var])
        # if var == "GITHUB":
        #     continue

        if var == "CONTENT":
            if variables[var] == "zero-markdown":
                variables[var] = '<zero-md src="post.md"></zero-md>'
            elif variables[var] == "iframe-pdf":
                ghline = ""
                if "GITHUB" in variables:
                    ghline = f'<br>Checkout the github repository <a href="{variables["GITHUB"]}" target="_blank" style="color:#0366d6">here</a>'

                variables[var] = (
                    (
                        'To view the pdf directly in your browser: <a href="report.pdf" target="_blank" style="color:#0366d6">report.pdf</a>'
                        + ghline
                    )
                    + '<br><br><iframe src="report.pdf" width="100%" height="700px"></iframe>'
                )

        with fileinput.FileInput(newfilename, inplace=True, backup=".bak") as file:
            for line in file:
                print(line.replace("VARIABLE::" + var, variables[var]), end="")
                pass
            pass
    return 0


def make_all_posts():
    """
    Iteratively calls make_single for all topics defined within variables.json
    """
    variables_all = json.load(open("assets/python/variables.json"))["posts"]
    template_file = "posts/template.html"
    for post in variables_all:
        make_single_post(
            template_file=template_file, variables=variables_all[post], name=post
        )
        pass
    return 0


if __name__ == "__main__":
    make_all_posts()
    pass
