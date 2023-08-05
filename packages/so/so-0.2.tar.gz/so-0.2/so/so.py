import click

@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name', help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo('Hello %s!' % name)


@click.command()
@click.option('--spring', type=click.Choice(['boot', 'mvc']))    # 限定值
def choose(spring):
    click.echo('spring: %s' % spring)

if __name__ == '__main__':
    choose()
    hello()