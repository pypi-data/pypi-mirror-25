import click

from pytally import tallylog

log = None

@click.group()
@click.option('--logfile', default='tallylog.txt')
def cli(logfile):
    global log
    log = tallylog.TallyLog(logfile)

@click.command(help='adds line to tallylog')
@click.argument('line')
def add(line):
    log.add(line)

@click.command(help='prints log')
def lines():
    for line in log.lines:
        click.echo(line)

@click.command(help='prints lines without tag')
def tagless_lines():
    for line in log.tagless_lines:
        click.echo(line)

@click.command(help='prints line with given tag')
@click.argument('tag')
def line(tag):
    try:
        click.echo(log.line(tag), err=True)
    except tallylog.TagNotFound:
        handle_tag_not_found(tag)

@click.command(help='adds tag to the given line')
@click.argument('line')
@click.argument('tag')
def tag(line, tag):
    try:
        log.tag(line, tag)
    except tallylog.NoSuchLineFound:
        handle_line_not_found(line)

@click.command(help='remove tag')
@click.argument('tag')
def remove_tag(tag):
    log.remove_tag(tag)

@click.command(help='moves given tag to line. Removes old tags')
@click.argument('from_line')
@click.argument('to_line')
def move_tag(from_line, to_line):
    try:
        log.move_tag(from_line, to_line)
    except tallylog.NoSuchLineFound:
        handle_line_not_found(line)
    except tallylog.TagNotFound:
        handle_tag_not_found(tag)

@click.command(help='moves tag to up')
@click.argument('tag')
def move_tag_up(tag):
    try:
        log.move_tag_up(tag)
    except tallylog.CannotMoveTag:
        click.echo(f'"{tag}" cannot be moved. It is on first line', err=True)
        exit(-1)
    except tallylog.TagNotFound:
        handle_tag_not_found(tag)

@click.command(help='moves tag to down')
@click.argument('tag')
def move_tag_down(tag):
    try:
        log.move_tag_down(tag)
    except tallylog.CannotMoveTag:
        click.echo(f'"{tag}" cannot be moved. It is on last line', err=True)
        exit(-1)
    except tallylog.TagNotFound:
        handle_tag_not_found(tag)

@click.command(help='removes first line')
def remove_first_line():
    log.remove_first()

@click.command(help='changes tag to other')
@click.argument('old_tag')
@click.argument('new_tag')
def change_tag(old_tag, new_tag):
    try:
        log.change_tag(old_tag, new_tag)
    except tallylog.TagNotFound:
        handle_tag_not_found(old_tag)

@click.command(help='Removes the line matching with argument. Removed line can contain tag')
@click.argument('line')
def remove_line(line):
    try:
        log.remove_line(line)
    except tallylog.NoSuchLineFound:
        handle_line_not_found(line)

cli.add_command(add)
cli.add_command(lines)
cli.add_command(line)
cli.add_command(tag)
cli.add_command(remove_tag)
cli.add_command(move_tag)
cli.add_command(move_tag_up)
cli.add_command(move_tag_down)
cli.add_command(remove_first_line)
cli.add_command(change_tag)
cli.add_command(tagless_lines)
cli.add_command(remove_line)

def handle_tag_not_found(tag):
    click.echo(f'Tag "{tag}" was not found!', err=True)
    exit(-1)


def handle_line_not_found(line):
    click.echo(f'Line "{line}" was not found!', err=True)
    exit(-1)



if __name__ == '__main__':
    cli()

