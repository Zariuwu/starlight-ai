#!/usr/bin/env python3
"""
Starlight portable runtime main script.
This script loads configuration and starts the agent.
"""
import json
import os
import sys


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main(root_path):
    # Load manifest and launcher config
    manifest = load_json(os.path.join(root_path, 'manifest.json'))
    launcher_conf = load_json(os.path.join(root_path, 'system', 'config', 'launcher.json'))
    assistant_conf = load_json(os.path.join(root_path, 'agents', 'core', 'starlight_assistant.json'))
    # Print out loaded configs for debugging
    print("Starlight runtime initialized.")
    print("Manifest:", manifest)
    print("Launcher Config:", launcher_conf)
    print("Assistant Config:", assistant_conf)
    # Execute on_plug_in automation (stub)
    on_plug = load_json(os.path.join(root_path, 'tasks', 'automations', 'on_plug_in.json'))
    print("Running automation:", on_plug['name'])
    for step in on_plug['steps']:
        print("Executing step:", step)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        root = sys.argv[1]
    else:
        # Assume current working directory is root of Starlight
        root = os.getcwd()
    main(root)
