# cenyslovensko-bindings

Python bindings for the [cenyslovensko-api/core](https://github.com/cenyslovensko-api/core) RPC server.

## Requirements

- Python 3.10+
- [Rust / cargo](https://rustup.rs/) — needed to build the RPC server binary
- [CMake 3.20+](https://cmake.org/download/)

## Getting started

Everything is driven through CMake — it clones the core repo, compiles the binary, and installs the Python package in one go:

```bash
cmake -S . -B build
cmake --build build
```

This will:
1. Clone `cenyslovensko-api/core` and compile the RPC server binary with cargo
2. Install the binary to `../cenyslovensko_client/bin`
3. Run `pip install -e ".[test]"` for the Python package

To pin a specific release tag instead of `main`:

```bash
cmake -S . -B build -DCORE_TAG=v0.1.14
cmake --build build
```

To update the binary to the latest `main`:

```bash
cmake --build build --target core_rpc_server
```

## Usage

```python
from cenyslovensko_client import CenyslovenskoVersionRpcClient, CenyslovenskoProductRpcClient

# version
with CenyslovenskoVersionRpcClient() as client:
    print(client.get_version())

# product
with CenyslovenskoProductRpcClient() as client:
    product = client.get_product("abc-123")
    print(product)
```

### Binary resolution order

When no `command` is passed to a client, the binary is located in the following order:

1. `CENYSLOVENSKO_RPC_SERVER_BIN` environment variable
2. `../cenyslovensko_client/bin/cenyslovensko_rpc_server` (installed by CMake)
3. `cenyslovensko_rpc_server` on `PATH`

```bash
# override at runtime
CENYSLOVENSKO_RPC_SERVER_BIN=/path/to/binary python your_script.py
```

## Development

### Running tests

```bash
cmake --build build --target test
```

### CMake options

| Variable         | Default                                          | Description                            |
|------------------|--------------------------------------------------|----------------------------------------|
| `CORE_REPO`      | `https://github.com/cenyslovensko-api/core.git` | Git URL of the core repo               |
| `CORE_TAG`       | `main`                                           | Git tag, branch, or commit to build    |
| `BIN_NAME`       | `cenyslovensko_rpc_server`                       | Cargo package / binary name            |
| `BIN_OUTPUT_DIR` | `../cenyslovensko_client/bin`                     | Where the binary is installed          |

## CI / CD

| Workflow | Trigger | What it does |
|----------|---------|--------------|
| **Test** | push / PR to `main` | Runs `cmake -S . -B build && cmake --build build && cmake --build build --target test` on Ubuntu and macOS |
| **Publish** | GitHub release published | Builds sdist + wheel, publishes to PyPI via OIDC trusted publishing |

[Dependabot](https://docs.github.com/en/code-security/dependabot) is configured to open weekly PRs for GitHub Actions and Python dependency updates.
