import sys
import argparse
import importlib
from .contrib import bottle


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default=8080,
                        help="Port to bind on.")
    parser.add_argument("--host", default="0.0.0.0",
                        help="Host to bind.")
    parser.add_argument("--echo", action="store_true",
                        help="Module echo, return the current http request detail.")
    parser.add_argument("--echo-prefix", default="/_y3k/",
                        help="The path prefix for echo module")
    parser.add_argument("--mock",
                        help="Enable mocking data via a json file.")
    parser.add_argument("--mock-prefix", default="",
                        help="The path prefix for all mocking data.")
    parser.add_argument("--static", default="",
                        help="Serve static files with specified directory.")
    parser.add_argument("--static-prefix", default="/",
                        help="The path prefix for serving static files with --static.")
    parser.add_argument("--static-serve-dir", action="store_true",
                        help="Serve directories as a list.")
    parser.add_argument("--zip", default="",
                        help="Serve a zip file as static directory.")
    parser.add_argument("--zip-prefix", default="/",
                        help="The path prefix for the serving file with --zip.")   
    parser.add_argument("--interact", action="store_true",
                        help="Attach to a interactive console.")
    parser.add_argument("--interact-path", default="/_y3k/interact",
                        help="The path for interactive console.")
    parser.add_argument("--version", action='store_true', default=False,
                        help="Show version and exit.")

    args = parser.parse_args()
    return args


def main():
    args = vars(parse_args())
    if args['version']:
        from . import __VERSION__
        print("ynm3k %s" % __VERSION__)
        return
    if args['echo']:
        from . import echo
        object_echo = echo.ModuleEcho(args['echo_prefix'])
    if args['interact']:
        from . import interact
        object_interact = interact.ModuleInteract(args['interact_path'])
    if args['static']:
        from . import static
        object_static = static.ModuleStatic(args['static_prefix'],
                                            path=args['static'],
                                            serve_dir=args['static_serve_dir'])
    if args['zip']:
        from .modules import zip_serve
        object_zip = zip_serve.ModuleZipServe(args['zip_prefix'],
                                              path=args['zip'])
    if args['mock']:
        from . import mock
        object_mock = mock.ModuleMock(args['mock_prefix'], args['mock'])
    bottle.run(host=args['host'], port=int(args['port']),
               debug=True)


if __name__ == '__main__':
    main()
