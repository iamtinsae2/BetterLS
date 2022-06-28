#!/usr/bin/env python3
import os
import click
import tabulate
from utils import sizeof_fmt

# Returns list of files and directories present
# in the given path
def list_dir(path: str) -> list[tuple]:
  dirs = sorted(os.listdir(path), key=str.lower)
  ret = []

  for idx, item in enumerate(dirs):
    full_path = os.path.join(path, item)
    try: 
      size = os.stat(full_path).st_size
    except:
      size = 0

    if os.path.isdir(full_path):
      type = "DIR"
    elif os.path.islink(full_path):
      type = "SYMBOLIC"
    elif os.path.ismount(full_path):
      type = "MOUNT"
    elif os.path.isfile(full_path):
      type = "FILE"
    else:
      type = "UNKNOWN"

    ret.append((idx, item,  sizeof_fmt(size), type))

  return ret

# PRETTIFY
def prettify(paths):
  ret = []

  for path in paths:
    idx, name, size, path_type = path
    if path_type == 'FILE':
      path = map(lambda a: click.style(a, fg="yellow"), path)
    elif path_type == 'DIR':
      path = map(lambda a: click.style(a, fg="green"), path)
    elif path_type == 'SYMBOLIC':
      path = map(lambda a: click.style(a, fg="magenta"), path)
    elif path_type == 'MOUNT':
      path = map(lambda a: click.style(a, fg="blue"), path)

    ret.append(path)

  return ret

@click.command()
@click.argument("path", default=os.getcwd())
def main(path):
  out = list_dir(path)

  headers = ("#", "NAME", "SIZE", "TYPE")
  
  click.echo(tabulate.tabulate(prettify(out), headers=headers, tablefmt="fancy_outline"))

  pass

if __name__ == '__main__':
  main()
