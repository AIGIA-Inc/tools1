import os
import pathlib
import shutil
import pprint

PATH_ROOT: str = str(pathlib.Path(__file__).resolve().parent)
PATH_PRODUCT: str = PATH_ROOT + "/product"


def build_directory(directoryname: str) -> str:
    target: str = PATH_ROOT + directoryname
    if not (os.path.exists(target)):
        os.mkdir(target)
    return target


def build_file(filename: str)-> str:
    source: str = PATH_ROOT + filename
    target: str = PATH_PRODUCT + filename
    os.remove(target)
    shutil.copy2(source, target)
    return target


if __name__ == "__main__":
    build_directory("/product")
    pprint.pprint(list(map(build_directory, ["/product/templates",
                                     "/product/static",
                                     "/product/aig_accounts",
                                     "/product/aig_shots"
                                     ])))
    pprint.pprint(list(map(build_file, ["/main.py","/setup.py","/mongocopy.py",
                                "/requirements.txt",
                                "/aig_accounts/__init__.py",
                                "/aig_accounts/accounts.py",
                                "/aig_accounts/download_accounts.py",
                                "/aig_accounts/payment.py",
                                "/aig_shots/__init__.py",
                                "/aig_shots/shots.py",
                                "/aig_shots/download_shots.py",
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
