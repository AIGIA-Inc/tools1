import os
import pathlib
import shutil
import pprint

#絶対パスで取得
PATH_ROOT: str = str(pathlib.Path(__file__).resolve().parent)
PATH_PRODUCT: str = PATH_ROOT + "/product"

def build_directory(directoryname: str) -> str:
    target: str = PATH_ROOT + directoryname
    if not (os.path.exists(target)):
        os.mkdir(target)
    return target


def build_file(filename: str)-> str:
    result = ""
    source: str = PATH_ROOT + filename #絶対パスで取得
    target: str = PATH_PRODUCT + filename

    try:
    #    os.remove(target) #プロダクト内のファイルを削除
        shutil.copy2(source, target) #ディレクトリ下へコピー
    except:
        result= target +" error."

    return result


if __name__ == "__main__":
    build_directory("/product")
    pprint.pprint(list(map(build_directory, ["/product/templates",
                                     "/product/static",
                                     "/product/aig_accounts",
                                     "/product/aig_shots",
                                     "/product/config"
                                     ])))
    pprint.pprint(list(map(build_file, ["/main.py",
                                        "/setup.py",
                                        "/mongocopy.py",
                                        "/requirements.txt",
                                        "/config/default.json",
                                        "/static/.gitkeep",
                                "/aig_accounts/__init__.py",
                                "/aig_accounts/accounts.py",
                                "/aig_accounts/payment.py",
                                "/aig_shots/__init__.py",
                                "/aig_shots/shots.py",
                                "/aig_shots/download_shots.py",
                                "/templates/accounts.j2",
                                "/templates/accounts_tree.j2",
                                "/templates/base.j2",
                                "/templates/error.j2",
                                "/templates/guests.j2",
                                "/templates/index.j2",
                                "/templates/test.j2",
                                "/templates/studios.j2",
                                "/templates/shots.j2",
                                "/templates/totalling.j2",
                                "/templates/totallings.j2",
                                ])))
