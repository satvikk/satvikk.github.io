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
        ] = '<span class="image featured"><img src="banner" alt="" /></span>'

    for var in variables:
        # print(var, variables[var])
        if var == "GITHUB":
            continue
        if var == "CONTENT":
            if variables[var] == "zero-markdown":
                variables[var] = '<zero-md src="post.md"></zero-md>'
            elif variables[var] == "iframe-pdf":
                ghline = ""
                if "GITHUB" in variables:
                    ghline = (
                        variables[var]
                        + f'<br>Checkout the github repository <a href="{variables["GITHUB"]}" target="_blank" style="color:#0366d6">here</a>'
                    )

                variables[var] = (
                    (
                        'To view the pdf directly in your browser: <a href="report.pdf" target="_blank" style="color:#0366d6">report.pdf</a>'
                        + ghline
                    )
                    + '<br><br><iframe src="report.pdf" width="100%" height="1000px"></iframe>'
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
