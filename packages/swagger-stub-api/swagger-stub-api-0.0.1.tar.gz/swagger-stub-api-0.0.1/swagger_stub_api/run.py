import click

from .app import app


@click.command()
@click.option('--port', default=3000, help='port')
@click.option('--host', default="0.0.0.0", help='host')
@click.option('--swagger_path', default="swagger.yaml", help='path to swagger file')
def main(port, host, swagger_path):
    app.config["SWAGGER_PATH"] = swagger_path
    app.run(host=host, port=port)


if __name__ == "__main__":
    main()
