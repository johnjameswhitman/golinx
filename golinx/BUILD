# TODO(john): Consider adding a python toolchain as described in the link below.
# As it stands, these rules execute using the system `python`, regardless of
# whether that points to python2 or python3.
# https://github.com/bazelbuild/rules_python/blob/master/docs/python.md#py_runtime_pair

load("@rules_python//python:python.bzl", "py_binary", "py_library", "py_test")
load("@pip_reqs//:requirements.bzl", "requirement")

py_binary(
    name = "main",
    srcs = ["main.py"],
    deps = [
        requirement("Flask"),
        requirement("absl-py"),
    ],
)
