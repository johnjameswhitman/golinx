load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("@bazel_tools//tools/build_defs/repo:git.bzl", "new_git_repository")

# ======== BEGIN PYTHON ========
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
# ======== END PYTHON ========

# ======== BEGIN DOCKER ========
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

# Download the rules_docker repository at release v0.14.1
http_archive(
    name = "io_bazel_rules_docker",
    sha256 = "dc97fccceacd4c6be14e800b2a00693d5e8d07f69ee187babfd04a80a9f8e250",
    strip_prefix = "rules_docker-0.14.1",
    urls = ["https://github.com/bazelbuild/rules_docker/releases/download/v0.14.1/rules_docker-v0.14.1.tar.gz"],
)

# OPTIONAL: Call this to override the default docker toolchain configuration.
# This call should be placed BEFORE the call to "container_repositories" below
# to actually override the default toolchain configuration.
# Note this is only required if you actually want to call
# docker_toolchain_configure with a custom attr; please read the toolchains
# docs in /toolchains/docker/ before blindly adding this to your WORKSPACE.
# BEGIN OPTIONAL segment:
# load("@io_bazel_rules_docker//toolchains/docker:toolchain.bzl",
#     docker_toolchain_configure="toolchain_configure"
# )
# docker_toolchain_configure(
#   name = "docker_config",
#   # OPTIONAL: Path to a directory which has a custom docker client config.json.
#   # See https://docs.docker.com/engine/reference/commandline/cli/#configuration-files
#   # for more details.
#   client_config="<enter absolute path to your docker config directory here>",
#   # OPTIONAL: Path to the docker binary.
#   # Should be set explcitly for remote execution.
#   docker_path="<enter absolute path to the docker binary (in the remote exec env) here>",
#   # OPTIONAL: Path to the gzip binary.
#   # Either gzip_path or gzip_target should be set explcitly for remote execution.
#   gzip_path="<enter absolute path to the gzip binary (in the remote exec env) here>",
#   # OPTIONAL: Bazel target for the gzip tool.
#   # Either gzip_path or gzip_target should be set explcitly for remote execution.
#   gzip_target="<enter absolute path (i.e., must start with repo name @...//:...) to an executable gzip target>",
#   # OPTIONAL: Path to the xz binary.
#   # Should be set explcitly for remote execution.
#   xz_path="<enter absolute path to the xz binary (in the remote exec env) here>",
#   # OPTIONAL: List of additional flags to pass to the docker command.
#   docker_flags = [
#     "--tls",
#     "--log-level=info",
#   ],

# )
# End of OPTIONAL segment.

# Plug in special python toolchain that points the interpreter to /usr/local/bin/python
# (the path used in the official python docker image).
register_toolchains("//toolchains:golinx_py_toolchain")

load(
    "@io_bazel_rules_docker//repositories:repositories.bzl",
    container_repositories = "repositories",
)
container_repositories()

# This is NOT needed when going through the language lang_image
# "repositories" function(s).
load("@io_bazel_rules_docker//repositories:deps.bzl", container_deps = "deps")

container_deps()

load(
    "@io_bazel_rules_docker//python3:image.bzl",
    _py3_image_repos = "repositories",
)

_py3_image_repos()

load(
    "@io_bazel_rules_docker//container:container.bzl",
    "container_pull",
)

container_pull(
    name = "py3_image_base_jjw",
    registry = "gcr.io",
    repository = "distroless/python3",
    tag = "latest",
)

container_pull(
    name = "official_python3",
    registry = "index.docker.io",
    repository = "python",
    tag = "3.7",
)
# ======== END DOCKER ========
