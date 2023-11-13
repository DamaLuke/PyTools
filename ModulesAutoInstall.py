# 检测并自动安装第三方包
def AutoInstall(libs):
    import importlib.util
    import pip

    if len(libs) != 0:
        for lib in libs:
            spec = importlib.util.find_spec(lib)
            if spec is None:
                pip.main(
                    [
                        "install",
                        "--user",
                        "-i",
                        "https://pypi.tuna.tsinghua.edu.cn/simple",
                        lib,
                    ]
                )
