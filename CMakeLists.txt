cmake_minimum_required(VERSION 3.20)
project(cenyslovensko_client NONE)

include(ExternalProject)

set(CORE_REPO "https://github.com/cenyslovensko-api/core.git"
    CACHE STRING "Git URL of the cenyslovensko-api/core repository")

set(CORE_TAG "main"
    CACHE STRING "Git tag / branch / commit of cenyslovensko-api/core to build")

set(BIN_NAME "cenyslovensko_rpc_server"
    CACHE STRING "Name of the RPC server binary to build from core")

set(BIN_OUTPUT_DIR "${CMAKE_SOURCE_DIR}/cenyslovensko_client/vendor"
    CACHE PATH "Directory where the compiled binary is installed")

find_program(CARGO_EXECUTABLE cargo REQUIRED
    HINTS "$ENV{HOME}/.cargo/bin"
    DOC "Rust cargo build tool")

find_package(Python3 3.10 REQUIRED COMPONENTS Interpreter)

message(STATUS "Found cargo:  ${CARGO_EXECUTABLE}")
message(STATUS "Found Python: ${Python3_EXECUTABLE} (${Python3_VERSION})")

set(_stamp_dir  "${CMAKE_BINARY_DIR}/_stamps")
set(_source_dir "${CMAKE_BINARY_DIR}/_core_src")

if(WIN32)
    set(_bin_suffix ".exe")
else()
    set(_bin_suffix "")
endif()

set(_release_bin  "${_source_dir}/target/release/${BIN_NAME}${_bin_suffix}")
set(_installed_bin "${BIN_OUTPUT_DIR}/${BIN_NAME}${_bin_suffix}")

ExternalProject_Add(core_rpc_server
    GIT_REPOSITORY  "${CORE_REPO}"
    GIT_TAG         "${CORE_TAG}"
    GIT_SHALLOW     TRUE
    SOURCE_DIR      "${_source_dir}"
    STAMP_DIR       "${_stamp_dir}"
    BINARY_DIR      "${_source_dir}"

    CONFIGURE_COMMAND ""
    BUILD_COMMAND
        "${CARGO_EXECUTABLE}" build --release -p "${BIN_NAME}"
        "--manifest-path" "${_source_dir}/Cargo.toml"
    INSTALL_COMMAND
        "${CMAKE_COMMAND}" -E make_directory "${BIN_OUTPUT_DIR}"
        COMMAND "${CMAKE_COMMAND}" -E copy "${_release_bin}" "${_installed_bin}"

    BUILD_ALWAYS FALSE
    LOG_DOWNLOAD TRUE
    LOG_BUILD    TRUE
)

set(_venv_dir  "${CMAKE_BINARY_DIR}/_venv")

if(WIN32)
    set(_venv_python "${_venv_dir}/Scripts/python.exe")
    set(_venv_pip    "${_venv_dir}/Scripts/pip.exe")
else()
    set(_venv_python "${_venv_dir}/bin/python")
    set(_venv_pip    "${_venv_dir}/bin/pip")
endif()

set(_venv_stamp   "${CMAKE_BINARY_DIR}/_stamps/venv.stamp")
set(_pip_stamp    "${CMAKE_BINARY_DIR}/_stamps/pip_install.stamp")

add_custom_command(
    OUTPUT  "${_venv_stamp}"
    COMMAND "${Python3_EXECUTABLE}" -m venv "${_venv_dir}"
    COMMAND "${CMAKE_COMMAND}" -E touch "${_venv_stamp}"
    COMMENT "Creating Python virtual environment"
)

add_custom_target(venv
    DEPENDS "${_venv_stamp}"
)

add_custom_command(
    OUTPUT  "${_pip_stamp}"
    COMMAND "${_venv_pip}" install -e "${CMAKE_SOURCE_DIR}[test]" --quiet
    COMMAND "${CMAKE_COMMAND}" -E touch "${_pip_stamp}"
    DEPENDS "${_venv_stamp}" "${CMAKE_SOURCE_DIR}/pyproject.toml"
    COMMENT "Installing Python package into venv (pip install -e .[test])"
)

add_custom_target(pip_install ALL
    DEPENDS "${_pip_stamp}"
)

add_custom_target(test
    COMMAND "${_venv_python}" -m pytest "${CMAKE_SOURCE_DIR}/tests" -v
    DEPENDS pip_install core_rpc_server
    WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}"
    COMMENT "Running Python tests"
)
