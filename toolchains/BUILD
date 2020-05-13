# This is borrowed from here and modified to point to the python iterpreter
# used by the official python image:
# https://github.com/bazelbuild/rules_docker/blob/master/toolchains/BUILD
load("@bazel_tools//tools/python:toolchain.bzl", "py_runtime_pair")

package(default_visibility = ["//visibility:public"])

py_runtime(
    name = "default_container_py3_runtime",
    interpreter_path = "/usr/local/bin/python",
    python_version = "PY3",
)

py_runtime_pair(
    name = "default_container_py_runtime_pair",
    py3_runtime = ":default_container_py3_runtime",
)

# A toolchain to run python outputs inside a container.
# If you are using a custom base for py_image which has python tools in a
# different location, you must register that toolchain prior to the
# registration of this one in @io_bazel_rules_docker//python:image.bzl
toolchain(
    name = "golinx_py_toolchain",
    exec_compatible_with = [
        "@io_bazel_rules_docker//platforms:run_in_container",
    ],
    toolchain = ":default_container_py_runtime_pair",
    toolchain_type = "@bazel_tools//tools/python:toolchain_type",
)