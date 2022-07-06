import fileinput
import json
import shutil


def make_single_post(template_file, variables, name):
    newfilename = "posts/" + name + "/post.html"
    shutil.copyfile(template_file, newfilename)
    for var in variables:
        print(var, variables[var])
        with fileinput.FileInput(newfilename, inplace=True, backup=".bak") as file:
            for line in file:
                print(line.replace("VARIABLE::" + var, variables[var]), end="")
                pass
            pass
    return 0


def make_all_posts():
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
