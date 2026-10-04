import argparse
import json

from .api import build, inspect


def main():
    parser = argparse.ArgumentParser(description='Bounded straight-path access on explicit mm STEP inputs')
    sub = parser.add_subparsers(dest='command', required=True)
    for command in ('build', 'inspect', 'demo'):
        p = sub.add_parser(command)
        if command != 'demo':
            p.add_argument('input')
        else:
            p.add_argument('--offline', required=True, action='store_true')
        p.add_argument('--output', required=True)
        p.add_argument('--timeout', type=float, default=120)
        p.add_argument('--memory-mb', type=int, default=2048)
    args = parser.parse_args()
    try:
        if args.command == 'demo':
            from .demo import demo
            code, report = demo(args.output, timeout=args.timeout, memory_mb=args.memory_mb)
        else:
            operation = build if args.command == 'build' else inspect
            code, report = operation(args.input, args.output, timeout=args.timeout, memory_mb=args.memory_mb)
        print(json.dumps({'status': report['status'], 'exit_code': code, 'output': args.output}))
        return code
    except (ValueError, OSError) as error:
        print(json.dumps({'status': 'inconclusive', 'error': str(error)}))
        return 2
