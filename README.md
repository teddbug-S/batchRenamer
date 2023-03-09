# A powerful but simple batch renamer.
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

### Methods
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
   
 - `replace` replaces a substring or match in old file name with new one, returns a list of new strings without renaming fetched files.
 Case sensitivity is enabled (`match_case`) by default and number of times to replace (`count`) defaults to 1.
   ```python
   print(renamer.fetched_files) # assuming files have names ['E-01', 'E-02', 'E-03']
   new_names = renamer.replace('E-', 'Episode ')
   print(new_names) # -> ['Episode 1', 'Episode 2', 'Episode 3']
   ```
   
 - `expand_template` generates new names from `template`, this method automatically generates the values (sequences) according to the template but you can specify custom sequences for both numeric and alphabetic.
 ```python
  new_names = renamer.expand_template(upper=True) # auto-generated sequence, upper for upper case letter sequence
  print(new_names) #  ['Merlin 01', 'Merlin 02', 'Merlin 03']
  
  new_names = renamer.expand_template(a_seq=a_seq, n_seq=n_seq) # generate with custom sequences
  print(new_names) # ['Merlin 02', 'Merlin 04', 'Merlin 06']
 ```
 
 - `rename` rename fetched files with `names` supplied as argument, useful when replacing a substring the `replace` method or after expanding the template with `expand_template`
 ```python
 renamer.rename(new_names)
 ```

### Renaming Template Placeholders
 Templates can contain character constants that you want to include in file
 name, e.g. `data_file_%n`, this will include the string `data_file` including
 a substitution of the `%n` placeholder into a number sequence.

 Placeholders: each placeholder should begin with a `%` symbol as in the example above
  
  - `n`: for a number sequence, files will be counted and `%n` 
         will be substituted for each file count. 
         Automatically, counting starts from zero (0) and will end at count of
         last file with a step of one (1).

         e.g. 'Merlin - Episode %n' -> 'Merlin - Episode 1', 'Merlin - Episode 2', ...

         This behaviour can be customized by supplying the `--start` and `--step`
         options to what you want.

  - `a`: for an alphabetic sequence i.e abc... or ABC...
         e.g. 'Section - %a' -> 'Section a', 'Section b', ...
         'Section - %a' -> 'Section A', 'Section B', ... 

  - `d`: this placeholder substitutes into the new name the old name of each file when supplied, it 
         is useful if you want to include the old names in the new name. 

         e.g. Template: 'Data %d'
            Old files: [ 'Column One', 'Column Two', ... ]
            New names: 'Data Column One', 'Data Column Two', ...