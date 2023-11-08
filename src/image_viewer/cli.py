from __future__ import annotations
import pathlib

import click
import panel as pn

from . import APP_FILE

@click.command()
@click.option('-p', '--port', help='port',
              default=0, type=int)
@click.option('--token-path', help='token auth path',
              default=None, type=str)
def serve(port: int, token_path: str | None):
    token = None
    if token_path is not None:
        # Don't handle any errors so that an
        # invalid token path stops the launch
        token_path = pathlib.Path(token_path)
        with token_path.open('r') as fp:
            token = fp.read()
            print('Using token auth')
    if token is None:
        print('No token auth')
    pn.state.as_cached(
        key='api_token',
        fn=(lambda: token),
    )
    pn.serve(
        APP_FILE,
        port=port,
        websocket_origin='*',
        show=False,
    )
