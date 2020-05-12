load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("@bazel_tools//tools/build_defs/repo:git.bzl", "new_git_repository")

# Set up Python environment
http_archive(
    name = "rules_python",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.0.1/rules_python-0.0.1.tar.gz",
    sha256 = "aa96a691d3a8177f3215b14b0edc9641787abaaa30363a080165d06ab65e1161",
)
# load("@rules_python//python:pip.bzl", "pip_import")
# load("@rules_python//python:pip.bzl", "pip_repositories")
load("@rules_python//python:repositories.bzl", "py_repositories")

py_repositories()

# pip_install() doesn't handle transitive dependencies. From a couple of github
# issues it seems like third-party rules do it, so I'm switching to `rules_python_external`.
# - https://github.com/bazelbuild/rules_python/issues/35
# - https://github.com/bazelbuild/rules_python/issues/125
# - https://github.com/dillon-giacoppo/rules_python_external (still recommends closed-reqs)
# # Uses system's `python` command (suggest using pyenv to point this at python3).
# # Also, not that requirements.txt must contain all transitive dependencies!
# pip_import(
#    name = "pip_reqs",
#    requirements = "//:requirements.txt",
# )
# load("@pip_reqs//:requirements.bzl", "pip_install")
# pip_install()

rules_python_external_version = "3aacabb928a710b10bff13d0bde49ceaade58f15"

http_archive(
    name = "rules_python_external",
    sha256 = "5a1d7e6e4bab49dcdd787694f0f5d52ac5debdfc1852981a89cc414e338d60dc", # Fill in with correct sha256 of your COMMIT_SHA version
    strip_prefix = "rules_python_external-{version}".format(version = rules_python_external_version),
    url = "https://github.com/dillon-giacoppo/rules_python_external/archive/{version}.zip".format(version = rules_python_external_version),
)

# Install the rule dependencies
load("@rules_python_external//:repositories.bzl", "rules_python_external_dependencies")
rules_python_external_dependencies()

load("@rules_python_external//:defs.bzl", "pip_install")
pip_install(
    name = "py_deps",
    requirements = "//:requirements.txt",
)