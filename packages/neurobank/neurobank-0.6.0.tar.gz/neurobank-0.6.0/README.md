# neurobank

**neurobank** is a simple, low-overhead data management system. It's designed for neural and behavioral data, but could be used for other kinds of experiments. The software helps you generate unique identifiers for your data resources, including stimuli, protocols, and recording units. No more guessing what version of a stimulus you presented in an experiment, where you stored an important recording, and whether you've backed it all up yet.  Your files are stored in a single directory hierarchy, and you get nice, human-readable, JSON-based metadata to organize your records and analysis workflows.

The data management strategy behind **neurobank** is simple: every resource gets a unique identifier and is stored in a canonical location. As long as you use the correct identifier, you can unambiguously locate the resource. What are resources? Resources include *sources*, which are used to control an experiment, and *data*, which result from running the experiment. Resources do not include things that evolve, like code, figures, or manuscripts. These should be managed in a version control system.

This software does two things: it assigns identifiers to resources, and it stores them in an filesystem-based archive. Optionally, it can interface with a centralized registry that stores your resources, their locations, and metadata. Using a registry gives you more flexibility in where you store resources and lets you search based on the metadata you store. See [django-neurobank](https://github.com/melizalab/django-neurobank) for an implementation of the registry that uses a postgres backend and the django REST framework.

## Installation

Install the **neurobank** Python package and its dependencies:

```bash
pip install neurobank
```

Initialize an archive. The archive has to live on a locally-accessible filesystem (however, it can be mounted over NFS, SSHFS, etc).

```bash
nbank init my-archive-path
```

You should edit the `README.md` and `project.json` files created in the archive directory to describe your project, set policies, and optionally specify a backend registry. You should also set permissions and default access control lists at this time so that files are added to the archive with the appropriate access restrictions (see [Best Practices](#best-practices) below).

## Registering and storing resources

Before you start an experiment, register all the resources you plan to use. For example, let's say you're presenting a set of acoustic stimuli to an animal while recording neural responses. To register the stimuli:

```bash
nbank -A my-archive-path register stimfile-1 stimfile-2 ...
```

Each stimulus will be given an identifier, moved to the archive, and (optionally) replaced by a link to the archived file.  The default policy is to keep the extension of the original file as a part of the new identifier, but this can be changed by editing `project.json` in the root of the archive. The command will output a JSON-encoded list of the resources that includes a mapping from the identifiers to the old filenames. You need to specify the archive loction either with the `-A` flag or by setting the `NBANK_PATH` environment variable.

In addition to giving source files an identifier, `nbank` calculates SHA1 hash values based on the contents of the file. If you're using a backend registry and attempt to register a source that's already in the archive, `nbank` will raise an error and let you know the identifier of the already-registered file.

Use the renamed stimulus files to run your experiment. If your data collection program doesn't store the names of the stimuli in the generated data files, you'll need to record the names manually. Usually it suffices to record the first part of the identifier, as the chances of a collision are extremely low.

After the experiment, deposit the data into the archive:

```bash
nbank -A my-archive-path deposit datafile-1 datafile-2 ...
```

As with the `register` command, `deposit` will assign a unique identifier to each resource and move the resource.

Resources may be regular files, directories or files that act as containers (e.g., ARF files, https://github.com/melizalab/arf). If you deposit containers or directories, you're responsible for organizing the contents and assigning any internal identifiers. The JSON output will contain the mappings from the original names to the new identifiers.

## Retrieving resources

The `register` and `deposit` commands both move resource files to the archive under the `resources` directory. Resources are further divided into subdirectories using the first two characters of the identifier. For example, if the identifier is `edd0ccae-c34c-48cb-b515-a5e6f9ed91bc.wav`, you'll find the file under `resources/ed`.

## Using a registry

The core functions of neurobank, identifier generation and resource archiving, do not require any kind of network connectivity. You can manage the identifiers however you choose, whether it's in a lab notebook, a text file, or a database of your own design.

For additional help in locating files, you can store catalogs (like those generated by the `register` and `deposit` commands) in the `metadata` directory of the archive. The command `nbank search` will search the catalog files for resources that match a search query. Currently only searching by the `name` field is supported. You can also look up the properties of an identifier with `nbank prop`. Bear in mind that this functionality is intended only for simple lookups. If you need a centralized representation of your resources you're better off using a real database and storing the canonical identifiers, which you can then pass to neurobank to locate.

You can edit this file to add additional information about the files or analysis units, and then store it in the archive metadata using the following command:

```bash
nbank catalog dataset.json target-catalog.json
```

This command will attempt to find `target-catalog.json` in the archive metadata directory. If it exists, the resources in `dataset.json` will be merged into the file. If there are duplicate identifiers, you'll be asked whether you want to keep the old metadata or merge in the new metadata. If `target-catalog.json` doesn't exist, `dataset.json` is simply copied to the metadata directory. You need to store the catalog in this way in order to use the search functions described in the next section.

## Policy settings

You can control how identifiers are generated (for example, to include the original filename or a shared suffix) and other policies for a data archive by editing the `project.json` file.

## Python interface


## Best Practices : Controlling access

One of the primary uses for neurobank is to allow multiple users to share a common set of data, thereby reducing the need for temporary copies and ensuring that a canonical, centralized backup of critical data can be maintained. In this case, the following practices are suggested for POSIX operating systems:

1. For each project, create a separate group and make the archive owned by the group. To give a user access to the data, add them to the group.
2. To restrict access to users not in the project group, set your umask to 027 before creating the archive.
3. Set the setgid (or setuid) bit on the subdirectories of the archive, so that files added to the archive become owned by the group. (`chmod 2770 resources metadata`). You may also consider setting the sticky bit so that files and directories can't be accidentally deleted.
4. If your filesystem supports it, set the default ACL on subdirectories so that added files are accessible only to the group. (`setfacl -d -m u::rwx,g::rwx,o::- resources metadata`).


## License

**neurobank** is licensed under the GNU Public License, version 2. That means you are free to use the code for anything you want, including a commerical work, but you have to provide the source code, including any modifications you make. You still own your data files and any associated metadata. See COPYING for more details.
