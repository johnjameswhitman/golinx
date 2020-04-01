load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("@bazel_tools//tools/build_defs/repo:git.bzl", "new_git_repository")


# Set up Python environment
http_archive(
    name = "rules_python",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.0.1/rules_python-0.0.1.tar.gz",
    sha256 = "aa96a691d3a8177f3215b14b0edc9641787abaaa30363a080165d06ab65e1161",
)
load("@rules_python//python:pip.bzl", "pip_import")
load("@rules_python//python:pip.bzl", "pip_repositories")
load("@rules_python//python:repositories.bzl", "py_repositories")

py_repositories()

# Uses system's `python` command (suggest using pyenv to point this at python3).
pip_import(
   name = "pip_reqs",
   requirements = "//:requirements.txt",
)
load("@pip_reqs//:requirements.bzl", "pip_install")
pip_install()


# Pull down repo with modified PDFkit until I can get my changes merged.
# PDFKIT_BUILD = """
# load("@rules_python//python:python.bzl", "py_library")
# 
# py_library(
#     name = "pdfkit",
#     srcs = glob(["pdfkit/*.py"]),
#     visibility = ["//visibility:public"],
# )
# """
# 
# new_git_repository(
#     name = "pdfkit_timeout",
#     remote = "https://github.com/johnjameswhitman/python-pdfkit.git",
#     branch = "master",
#     build_file_content = PDFKIT_BUILD,
# )
