# デバッグ用の関数。引数に文字列を指定するとTestsディレクトリ（ローカルのみ）内にファイルを作成。
def debug_file(s):
    path = "tests/output.txt"
    with open(path, mode="w") as f:
        f.write(s)
