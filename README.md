# FakeFS

This fun project has been created as a response to a series of questions
in the [/r/learnpython](https://www.reddit.com/r/learnpython) subreddit.

I took it as an inspiration and tried to develop a fake filesystem
with several commands which would actually do something
*almost* real.

> **Note** I quite like Python 3.10 new features so it's required.

## Basic Assupmtions

Filesystem has a name as there might be several filesystems mounted in an OS
at the same time.

Filesystem is used to keep objects called **nodes****. There might be several
types of nodes - at least **folders** (aka directories) and **files**.

Each node can have at most one parent.

### Folders ###

**Folders** are containers which can contain another **folders** or **files**.

**Path** is a sequence of names of nodes  leading to a particular node.

### Files ###

**Files** contain actual data (contents) but no nodes.

## Operations

As in a real filesystem, I want to provide the user with a set of useful
operations. These operations have their traditional names:

## Folder Oprations

| Operation | Description                                         |
|-----------|------------                                         |
| cd        | Change current folder                               |
| cp        | Copy a node to another folder (tricky - deep copy!) |
| ls        | List folder contents, i.e. nodes in the folder      |
| mkdir     | Create a new folder (*make directory*)              |
| mv        | Move a node to another folder                       |
| pwd       | Get current folder path                             |
| rmdir     | Remove an empty folder (*remove directory*)         |
| tree      | Display filesystem nodes in a tree                  |

## File operations

| Operation | Description                 |
|-----------|------------                 |
| cat       | Display file contents       |
| edit      | Set file contents           |
| rm        | Remove file from filesystem |
| touch     | Create an empty file        |

# Data Structures

Filesystem is a tree-like structure by nature.

When think about the design, several operations were considered important:

- cd - It's used to traverse the filesystem both up and down which means
    a data structure should support this.
- path search - Paths can be either absolute or relative. Used in almost
    any command to find a node.

The following decisions were made to reflect the above ideas:

- A folder will keep a list of its **child nodes**. Or preferably a dictionary
    will be used since it allows indexing by node name while providing methods
    to get a list of names as well as a list of values.
- A node will keep a reference to its parent.

It's technically possible to implement all of this using Python dictionaries
but my personal preference here are classes.

> So this is the end of a small brainstorming and now it's time to get into
> the implementation and do some work. Take a look at the code.