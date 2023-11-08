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
        try:
            token_path = pathlib.Path(token_path)
        except (ValueError, TypeError):
            pass
        if token_path.is_file():
            token = token_path.open('r').read()
    pn.state.as_cached(
        key='api_token',
        fn=lambda: token,
    )
    pn.serve(
        APP_FILE,
        port=port,
        websocket_origin='*',
        show=False,
    )
