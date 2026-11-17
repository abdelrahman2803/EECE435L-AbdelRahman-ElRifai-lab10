"""Deploy the application to a local release directory and verify it."""

import argparse
import hashlib
import json
import runpy
import shutil
from datetime import datetime, timezone
from pathlib import Path


def deploy(target, release):
    """Copy app.py, verify its greeting, and record a deployment manifest."""
    if not release or any(c not in "0123456789abcdefghijklmnopqrstuvwxyz"
                          "ABCDEFGHIJKLMNOPQRSTUVWXYZ-_" for c in release):
        raise ValueError("Release must contain only letters, digits, - or _")
    source = Path(__file__).resolve().with_name("app.py")
    release_dir = Path(target).resolve() / "releases" / release
    release_dir.mkdir(parents=True, exist_ok=True)
    deployed = release_dir / "app.py"
    shutil.copy2(source, deployed)
    application = runpy.run_path(str(deployed))
    greeting = application["greet"]("World")
    expected = "Hello, World from Abdel Rahman El Rifai!"
    if greeting != expected:
        raise RuntimeError("Deployed application failed its smoke test")
    manifest = {
        "release": release,
        "deployed_at_utc": datetime.now(timezone.utc).isoformat(),
        "application": str(deployed),
        "sha256": hashlib.sha256(deployed.read_bytes()).hexdigest(),
        "smoke_test": "passed",
        "output": greeting,
    }
    manifest_text = json.dumps(manifest, indent=2) + "\n"
    (release_dir / "manifest.json").write_text(manifest_text, encoding="utf-8")
    (Path(target).resolve() / "current.json").write_text(
        manifest_text, encoding="utf-8"
    )
    reports = Path("reports")
    reports.mkdir(exist_ok=True)
    (reports / "deployment.json").write_text(manifest_text, encoding="utf-8")
    print(greeting)
    print(f"Deployment smoke test passed: {deployed}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True)
    parser.add_argument("--release", required=True)
    arguments = parser.parse_args()
    deploy(arguments.target, arguments.release)
