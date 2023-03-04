# MIT License
#
# Copyright (c) 2023 Divine Decimate Darkey ( D.Cube )
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import click
from batchRenamer import BatchRenamer, __version__


@click.group()
def main() -> bool:
    """
    A powerful but simple batch renamer.

    \b
    Rename multiple files or directories elegantly with
    rich features such as:
      - fully customizable numeric sequence
      - upper or lowercase alphabetic sequence
      - replace substrings in old name with new one (works with pattern matching)
      - able to reuse old file name in new one
    """
    ...


@main.command(short_help="rename files or directories")
@click.argument("path", type=click.Path(exists=True), required=True)
@click.argument("template", required=True)
@click.option('--start', default=0, help="start of the numeric sequence")
@click.option('--step', default=1, help="step to be taken in generating a numeric sequence")
@click.option('-p', '--pad', default=0, help="amount of padding to use in number sequence")
@click.option('-u', '--upper', default=False, is_flag=True, help="set if you want alphabetic sequence to be uppercase")
@click.option('-y', '--yes', default=False, is_flag=True, help="continue to rename files")
def rename(path, template: str, start: int, step: int, pad: int, upper: bool, yes: bool):
    """
    Templates can contain character constants that you want to include in file
    name, e.g. 'data_file_%n', this will include the string 'data_file' including
    a substitution of the '%n' placeholder into a number sequence.

    Placeholders: each placeholder should begin with a '%' symbol as in the example above

        - n: for a number sequence, files will be counted and '%n' 
             will be substituted for each file count. 
             Automatically, counting starts from zero (0) and will end at count of
             last file with a step of one (1).

             e.g. 'Merlin - Episode %n' -> 'Merlin - Episode 1', 'Merlin - Episode 2', ...

             This behaviour can be customized by supplying the `--start` and `--step`
             options to what you want.

        - a: for an alphabetic sequence i.e abc... or ABC... depending 
             on whether the `-u` `--upper` flag is set.

             e.g. 'Section - %a' -> 'Section a', 'Section b', ...
                 'Section - %a' -> 'Section A', 'Section B', ... (if `--upper` flag is set) 

        - d: this placeholder substitutes the old name of each file when supplied, it 
             is useful if you want to include the old names in the new name. 

             e.g.    Template: 'Data %d'
                    Old files: [ 'Column One', 'Column Two', ... ]

                    New names: 'Data Column One', 'Data Column Two', ...
    """

    renamer = BatchRenamer(path=path, template=template, pad=pad)
    renamer.fetch_files()  # fetch files from path
    # customize sequence if needed
    n_seq = None
    if start or step != 1:
        n_seq = renamer.generate_n_seq(start=start, step=step)
    
    names = renamer.expand_template(n_seq=n_seq, upper=upper)
    click.echo() # echo a blank line
    for old, new in zip(renamer.files, names):
        click.echo(click.style(f"  {old.name:16} -->\t {new}", fg='green'))

    # prompt user to proceed with renaming
    confirm = yes or click.confirm("\nContinue to rename files?")
    if confirm:
        renamer.rename(names)
        click.echo(f"\n({len(renamer.files)}) files renamed successfully.")
    else:
        click.echo(click.style("Operation aborted.", fg="red", bold=True))


@main.command('replace')
@click.argument('path', type=click.Path(exists=True))
@click.option('-o', '--old', default="", help="substring to be replaced")
@click.option('-n', '--new', default="", help="new string to replace match with.")
@click.option('-m', '--match-case', default=False, is_flag=True)
@click.option('-y', '--yes', default=False, is_flag=True, help="continue to rename files")
def replace(path, old, new, match_case, yes):
    """
    Replace a substring with a new one in file name.
    """
    renamer = BatchRenamer(path=path, template="")
    renamer.fetch_files() # fetch files from path

    names = renamer.replace(old, new, match_case=match_case)
    # echo blank line
    click.echo("")
    for o, n in zip(renamer.files, names):
        click.echo(click.style(f"{o.name:16} -->\t {n}", fg="yellow"))
    
    # prompt user to proceed with renaming
    confirm = yes or click.confirm("\nContinue to rename files?")
    if confirm:
        renamer.rename(names)
        click.echo(f"\n({len(renamer.files)}) files renamed successfully.")
    else:
        click.echo(click.style("Operation aborted.", fg="red", bold=True))


@main.command('version')
def version():
    """Prints version number and exit"""
    click.echo(click.style(f"\nBatchRenamer {__version__}", fg="yellow"))


if __name__ == '__main__':
    main()
