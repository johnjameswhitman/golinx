load("@rules_python//python:python.bzl", "py_binary", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

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
        ":link_model",
        ":user_model",
        requirement("Flask"),
    ],
)

py_library(
    name = "base_model",
    srcs = ["base_model.py"],
)

py_library(
    name = "link_model",
    srcs = ["link_model.py"],
    deps = [
        ":base_model",
    ],
)

py_library(
    name = "user_model",
    srcs = ["user_model.py"],
    deps = [
        ":base_model",
    ],
)
