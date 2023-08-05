# Configuration Filenames

Any of the following can be used as the `verchew` configuration filename:

* `.verchew.ini`
* `verchew.ini`
* `.verchew`
* `.verchewrc`

# Custom Project Root

To call `verchew` from an arbitrary directory, pass it the path to the root of your project:

```sh
$ verchew --root=<path/to/project>
```

# Configuration Generation

In a new project, a sample configuration file can be generated:

```sh
$ verchew --init
```

Update the generated file to match your project's system dependencies, including an optional `message` where helpful.
    
# Custom Version Arguments

If one of your system dependencies using an argument other than `--version` to display its version information, this can be changed in the configuration file using the `cli_version_arg` setting:

```ini
[Graphviz]

cli = dot
cli_version_arg = -V
version = 2.
```

# Optional Programs

If one of your system dependencies is optional or you only want to show a warning for incompatible versions, include the `optional` setting:

```ini
[Terminal Notifier]

cli = terminal-notifier
version = 1.8
optional = true
```

# Exit Codes

When `verchew` runs, it will always return an exit code of 0 to avoid interrupting continuous integration. To force a non-zero exit code on failure, use the `--exit-code` option:

```sh
$ verchew --exit-code
```
