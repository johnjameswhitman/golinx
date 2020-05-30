# TODO(john): Consider adding a python toolchain as described in the link below.
# As it stands, these rules execute using the system `python`, regardless of
# whether that points to python2 or python3.
# https://github.com/bazelbuild/rules_python/blob/master/docs/python.md#py_runtime_pair

load("@rules_python//python:python.bzl", "py_binary", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")
load(
    "@io_bazel_rules_docker//container:container.bzl",
    "container_image",
)
load("@io_bazel_rules_docker//python3:image.bzl", "py3_image")

package(
    default_visibility = ["//golinx:__subpackages__",]
)

py_library(
    name = "utils",
    srcs = ["utils.py"],
    deps = [
        requirement("Flask"),
    ],
)

py_binary(
    name = "main",
    srcs = ["main.py"],
    data = [
        ":templates",
        ":static",
    ],
    deps = [
        "//golinx/controllers:link_controller",
        "//golinx/models:db",
        requirement("Flask"),
        requirement("absl-py"),
    ],
)

filegroup(
    name = "static_assets",
    srcs = glob([
        "static/*",
        ])
)

filegroup(
    name = "templates",
    srcs = glob([
        "templates/*.html",
        "templates/**/*.html",
        ])
)


py_binary(
    name = "server",
    srcs = ["server.py"],
    data = [
        ":templates",
        ":static",
    ],
    deps = [
        requirement("Flask"),
        requirement("absl-py"),
        # requirement("gevent"),
        requirement("bjoern"),
        "//golinx/models:db",
        "//golinx/controllers:link_controller",
    ],
)

# Testing Docker Image
py3_image(
    name = "golinx_py",
    srcs = ["server.py"],
    data = [
        ":templates",
        ":static",
    ],
    base = "@official_python3//image",
    # As a docker-ism, you want your smallest, most-frequently changing layers
    # listed last, because layers are cached and if you change an earlier layer
    # then later layers will have to be rebuilt.
    layers = [
        requirement("Flask"),
        requirement("absl-py"),
        requirement("gevent"),
        "//golinx/models:db",
        "//golinx/controllers:link_controller",
    ],
    main = "server.py",
    args = [
        "--port=5080",
        "--init_db",
    ],
)

container_image(
    name = "container",
    base = ":golinx_py",
    ports = [
        "5080",
        "5082",
    ]
)