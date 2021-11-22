import os
import pathlib
import shutil

PATH_ROOT = str(pathlib.Path(__file__).resolve().parent)
PATH_PRODUCT = PATH_ROOT + "/product"


def build_directory(directoryname):
    target = PATH_ROOT + directoryname
    if not (os.path.exists(target)):
        os.mkdir(target)
    return directoryname


def build_file(filename):
    shutil.copy2(PATH_ROOT + filename, PATH_PRODUCT + filename)
    return filename


if __name__ == "__main__":
    build_directory("/product")
    print(list(map(build_directory, ["/product/templates", "/product/static"])))
    print(list(map(build_file, ["/main.py",
                                "/requirement.txt",
                                "/aig_accounts/__init__.py",
                                "/aig_accounts/accounts.py",
                                "/aig_accounts/download_accounts.py",
                                "/aig_accounts/payment.py",
                                "/aig_shots/__init__.py",
                                "/aig_accounts/shots.py",
                                "/aig_accounts/download_shots.py",
                                "/templates/accounts.html",
                                "/templates/accounts_tree.html",
                                "/templates/base.html",
                                "/templates/error.html",
                                "/templates/guests.html",
                                "/templates/index.html",
                                "/templates/shots.html",
                                "/templates/totalling.html",
                                "/templates/totallings.html",
                                ])))
