load("@rules_python//python:python.bzl", "py_library")
load("@py_deps//:requirements.bzl", "requirement")


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
        ":resource_controller",
        "//golinx:utils",
        "//golinx/models:db",
        "//golinx/models:base_model",
        "//golinx/models:link_model",
        requirement("Flask"),
    ],
)

py_library(
    name = "resource_controller",
    srcs = ["resource_controller.py"],
    deps = [
        requirement("Flask"),
    ],
)
