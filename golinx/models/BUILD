load("@rules_python//python:python.bzl", "py_binary", "py_library", "py_test")
load("@pip_reqs//:requirements.bzl", "requirement")

package(
    default_visibility = ["//golinx:__subpackages__",]
)

py_library(
    name = "db",
    srcs = ["db.py"],
    data = [
            "schema.sql",
            "data/seed_links.csv",
            "data/seed_users.csv",
    ],
    deps = [
        ":link",
        ":user",
        requirement("Flask"),
    ],
)

py_library(
    name = "model",
    srcs = ["model.py"],
)

py_library(
    name = "link",
    srcs = ["link.py"],
    deps = [
        ":model",
    ],
)

py_library(
    name = "user",
    srcs = ["user.py"],
    deps = [
        ":model",
    ],
)

