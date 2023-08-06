import click

from swagger_stub_api.app import app


@click.command()
@click.option("--port", default=3000, type=click.INT, help="Port used when running application")
@click.option("--host", default="0.0.0.0", type=click.STRING, help="Host used when running application")
@click.argument("swagger_path", type=click.STRING)
def main(port, host, swagger_path):
    app.config["SWAGGER_PATH"] = swagger_path
    app.run(host=host, port=port)


if __name__ == "__main__":
    main()
