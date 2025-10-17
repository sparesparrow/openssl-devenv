#!/usr/bin/env python3
"""
Update VS Code IntelliSense paths from Conan dependencies

Usage:
    python update-intellisense.py [build_folder]
"""

import json
import subprocess
import sys
from pathlib import Path

def get_conan_include_paths(build_folder="build"):
    """Extract include paths from Conan info"""
    result = subprocess.run(
        ["conan", "info", "..", "--paths"],
        cwd=build_folder,
        capture_output=True,
        text=True,
        check=True
    )

    paths = []
    for line in result.stdout.split('\n'):
        if 'package_folder:' in line:
            pkg_path = line.split(':', 1)[1].strip()
            paths.append(f"{pkg_path}/**")

    return paths

def update_cpp_properties(include_paths):
    """Update c_cpp_properties.json"""
    vscode_dir = Path(".vscode")
    vscode_dir.mkdir(exist_ok=True)

    cpp_props_file = vscode_dir / "c_cpp_properties.json"

    template = {
        "configurations": [
            {
                "name": "Linux",
                "includePath": [
                    "${workspaceFolder}/**"
                ] + include_paths,
                "defines": [],
                "compilerPath": "/usr/bin/gcc",
                "cStandard": "c17",
                "cppStandard": "c++17",
                "intelliSenseMode": "linux-gcc-x64",
                "compileCommands": "${workspaceFolder}/build/compile_commands.json"
            }
        ],
        "version": 4
    }

    if cpp_props_file.exists():
        with open(cpp_props_file, 'r') as f:
            existing = json.load(f)
        existing.update(template)
        template = existing

    with open(cpp_props_file, 'w') as f:
        json.dump(template, f, indent=2)

    print(f"✓ Updated {cpp_props_file}")
    print(f"  Added {len(include_paths)} Conan include paths")

def main():
    build_folder = sys.argv[1] if len(sys.argv) > 1 else "build"

    print(f"Extracting Conan paths from {build_folder}...")
    paths = get_conan_include_paths(build_folder)

    print("Updating VS Code IntelliSense...")
    update_cpp_properties(paths)

    print("\n✅ IntelliSense updated successfully")
    print("Reload VS Code window for changes to take effect")

if __name__ == "__main__":
    main()
