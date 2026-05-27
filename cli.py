import argparse
import json
import sys
from pathlib import Path

CONFIG_PATH = Path.home() / ".cli-tool-lab.json"


def load_config():
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text())
    return {}


def save_config(config):
    CONFIG_PATH.write_text(json.dumps(config, indent=2))


def cmd_init(args):
    config = {"name": args.name, "version": "0.1.0", "settings": {}}
    save_config(config)
    print(f"Initialized config for {args.name}")


def cmd_set(args):
    config = load_config()
    config.setdefault("settings", {})[args.key] = args.value
    save_config(config)
    print(f"Set {args.key} = {args.value}")


def cmd_get(args):
    config = load_config()
    value = config.get("settings", {}).get(args.key)
    if value is None:
        print(f"Key '{args.key}' not found", file=sys.stderr)
        sys.exit(1)
    print(value)


def cmd_show(args):
    config = load_config()
    print(json.dumps(config, indent=2))


def cmd_status(args):
    config = load_config()
    if not config:
        print("No config found. Run 'cli-tool init <name>' first.")
        sys.exit(1)
    print(f"Project: {config.get('name', 'unknown')}")
    print(f"Version: {config.get('version', 'unknown')}")
    print(f"Settings: {len(config.get('settings', {}))} keys")


def main():
    parser = argparse.ArgumentParser(description="CLI Tool Lab")
    sub = parser.add_subparsers(dest="command")

    p_init = sub.add_parser("init", help="Initialize config")
    p_init.add_argument("name", help="Project name")
    p_init.set_defaults(func=cmd_init)

    p_set = sub.add_parser("set", help="Set a config key")
    p_set.add_argument("key", help="Config key")
    p_set.add_argument("value", help="Config value")
    p_set.set_defaults(func=cmd_set)

    p_get = sub.add_parser("get", help="Get a config key")
    p_get.add_argument("key", help="Config key")
    p_get.set_defaults(func=cmd_get)

    p_show = sub.add_parser("show", help="Show full config")
    p_show.set_defaults(func=cmd_show)

    p_status = sub.add_parser("status", help="Show project status")
    p_status.set_defaults(func=cmd_status)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)
    args.func(args)


if __name__ == "__main__":
    main()
