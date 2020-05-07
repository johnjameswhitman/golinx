load("@rules_python//python:python.bzl", "py_library")
load("@pip_reqs//:requirements.bzl", "requirement")

package(
    default_visibility = ["//golinx:__subpackages__",]
)

py_library(
    name = "link",
    srcs = ["link.py"],
    deps = [
        "//golinx:utils",
        requirement("Flask"),
    ],
)
