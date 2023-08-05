import click

from ..config import Config


@click.command()
@click.option("use_global", "-g", "--global", is_flag=True,
              help="Use the global config (~/.adbons/.adbons.yml).")
@click.option("-d", "--set-device", type=click.STRING,
              help="Set a default device id.")
@click.option("-a", "--set-app", type=click.STRING,
              help="Set a default app id.")
@click.option("-c", "--clear",
              type=click.Choice([Config.SECTION_DEVICE, Config.SECTION_APP]),
              help="Clear the default value.")
@click.option("-s", "--show", is_flag=True,
              help="Show the set values.")
@click.pass_context
def config(ctx, use_global, set_device, set_app, clear, show):
    """Configurates adbons."""
    if set_device:
        Config.write_value(use_global, Config.SECTION_DEVICE,
                           Config.KEY_DEFAULT, set_device)
    if set_app:
        Config.write_value(use_global, Config.SECTION_APP,
                           Config.KEY_DEFAULT, set_app)
    if clear:
        Config.clear_value(use_global, clear, Config.KEY_DEFAULT)
    if show:
        config = Config.read_values(use_global)
        if config is None:
            raise click.ClickException("No config file found.")
        else:
            click.echo("%s config:" % ("Global" if use_global else "Local"))
            for key, value in config.items():
                if key is not None and value is not None:
                    default = "not set"
                    if bool(value) and bool(value[Config.KEY_DEFAULT]):
                        default = value[Config.KEY_DEFAULT]
                    click.echo("The default " + key + " is " + default)
