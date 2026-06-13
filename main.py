"""Entry point for local and Render deployments.

This exposes the FastAPI app defined in server/main.py so that
`uvicorn main:app` works from the repository root.
"""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


SERVER_DIR = Path(__file__).resolve().parent / "server"
SERVER_MAIN = SERVER_DIR / "main.py"

if str(SERVER_DIR) not in sys.path:
    sys.path.insert(0, str(SERVER_DIR))

spec = spec_from_file_location("server_main", SERVER_MAIN)
server_main = module_from_spec(spec)
if spec and spec.loader:
    spec.loader.exec_module(server_main)
else:
    raise RuntimeError(f"Unable to load FastAPI app from {SERVER_MAIN}")

app = server_main.app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
