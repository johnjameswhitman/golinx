load("@rules_python//python:python.bzl", "py_library")
load("@pip_reqs//:requirements.bzl", "requirement")

package(
    default_visibility = ["//golinx:__subpackages__",]
)

py_library(
    name = "link_controller",
    srcs = ["link_controller.py"],
    data = [
        "//golinx:templates",
    ],
    deps = [
        "//golinx:utils",
        "//golinx/models:db",
        "//golinx/models:link_model",
        requirement("Flask"),
    ],
)
