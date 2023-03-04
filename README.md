## A powerful but simple batch renamer.
Rename multiple files or directories elegantly with rich features such as
  - fully customizable numeric sequence
  - upper or lowercase alphabetic sequence
  - replace substrings in old name with new one (works with pattern matching)
  - able to reuse old file name in new one

## Usage

### As A Library
import and initialize the `BatchRenamer` class by providing the
`path` where files reside, `pad` (int) amount of padding with zeros 
to use in numeric sequence when numbering files, `template` template to be used in
new file names.

```python
# initialize the class
renamer = BatchRenamer(path="Desktop/Movies", pad=1, template="Merlin %n")
```

#### Methods
 - `fetch_files` call with no arguments to fetch the files residing in `path` or files to rename.
   ```python
   # fetch files to rename
   renamer.fetch_files() # assuming three (3) files were fetched 
    ```
   
 - `generate_a_seq` generate an alphabetic sequence which stops at number of files fetched,
                    could be upper or lower case by setting the `upper` argument to `True` defaults to 
                    `False`.
   ```python
   a_seq = renamer.generate_a_seq()
   A_seq = renamer.generate_a_seq(upper=True)
   
   print(a_seq) # ['a', 'b', 'c']
   print(A_seq) # ['A', 'B', 'C']
   ```
   
 - `generate_n_seq` generate a numeric sequence, also generates elements equal to number of files fetched
                    but can be customized by specifying the `step` and where sequence should `start` 
   ```python
   n_seq = renamer.generate_n_seq(start=2, step=2) # start and step defaults to 1
   print(n_seq) # -> ['2', '4', '6']
   ```
   
 - `replace` replaces a substring or match in old file name with new one, returns a list of new strings
             without renaming fetched files.
             Case sensitivity is enabled (`match_case`) by default and number of times to replace (`count`) defaults to 1.
   ```python
   print(renamer.fetched_files) # assuming files have names ['E-01', 'E-02', 'E-03']
   new_names = renamer.replace('E-', 'Episode ')
   print(new_names) # -> ['Episode 1', 'Episode 2', 'Episode 3']
   ```
   
 - `rename` rename fetched files using provided `template`, this method automatically generates the values (sequences)
            according to the template but you can specify custom sequences for both numeric and alphabetic
   ```python
   renamer.rename(upper=True) # rename with auto-generated sequence, upper for upper case letter sequence
   renamer.rename(a_seq=a_seq, n_seq=n_seq) # rename with custom sequences
   ```
 
 - `_rename` rename fetched files with `names` supplied as argument, useful when replacing a substring or
   a match with the `replace` method
   ```python
   renamer._rename(new_names)
   ```