Snakecharmer
============

| A package originally intended to use in Snakemake pipelines.
| Saves keystrokes and makes for more transparent rules.

Installation
~~~~~~~~~~~~

| Install the latest version with pip:
| ``pip install snakecharmer``

Usage
~~~~~

Snakecharmer can be used as a standalone command and as a Python module.

Usage as a standalone command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``snakecharmer -f`` (or ``snakecharmer --freeze-conda``): can be invoked
inside a non-root Conda environment and will create two files: -
``environment.yml``, containing the Conda config **without** the Pip
config; - ``requirements.txt``, containing the Pip config.

This is useful when some of the Pip packages are installed from
git+URLs, as Conda currently hiccups on them (it creates a YAML file
just fine, but later cannot parse such lines properly).

Usage as a Python module
^^^^^^^^^^^^^^^^^^^^^^^^

| ``snakecharmer.paired(wildcards, target_char="@", prefix=".", suffix="fa", with_unpaired=False)``:
| given wildcards with a name attribute, will provide filenames for
  forward, reverse and (if ``with_unpaired == True``) unpaired reads.
| For a file ``data/alignments/{name}.bam``, where ``name == "LibA_@"``,
  it will produce: ``./LibA_1.fa``, ``./LibB_2.fa`` if arguments are
  left at their defaults. - ``target_char`` controls which character in
  {name} to substitute; - ``prefix`` controls what to prepend to the
  names (usually a directory path); - ``suffix`` controls the extension.

| ``snakecharmer.Tools(rules, make_jobs=1)``:
| creates a namespace with paths to tool binaries.
| If a binary exists in $PATH, does nothing except point there.
| If a binary doesn't, looks for the provided fallback one.
| If the fallback binary doesn't exist, builds it in a specified
  subdirectory using a specified recipe. - ``rules``: description of
  tool names, aliases, fallbacks and recipes in YAML format; -
  ``make_jobs``: for rules without recipes, a simple ``make`` command is
  assumed; this controls how many jobs to give this command.

**A real-world example of a YAML with rules:**

.. code:: yaml

    masurca:
        executables:
          - match: masurca
            fallback: tools/masurca/bin/masurca
          - match: quorum_create_database
            fallback: tools/masurca/bin/quorum_create_database
          - match: quorum_error_correct_reads
            fallback: tools/masurca/bin/quorum_error_correct_reads
        wd: tools/masurca
        commands:
          - sh install.sh
        git_post:
          - ignore
    psmc:
        fallback: tools/psmc/psmc
        wd: tools/psmc
        git_post:
          - ignore

I promise I'll explain everything about the rules later.
