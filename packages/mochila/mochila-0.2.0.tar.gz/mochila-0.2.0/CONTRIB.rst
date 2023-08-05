CODING CONVENTIONS
==================

Look at the existing source for guidance and keep PEP8 in mind.

REPOSITORY
==========

MOchila uses Git as it version control system and Git Flow as the branching model.

Branch naming
~~~~~~~~~~~~~

Branch should be named using the issue/bug number, using the following naming::

    feature/<issue #>

Other prefixes can be used to indicate the area the branch applies to: *fix*. *doc*, etc.

Commit Messages
~~~~~~~~~~~~~~~
Next we describe the commit message conventions that should be used for all commits to the repository. The reasons for
this conventions:
- integration to YouTrack
- automatic processing of git log
- simple navigation through git history

Format of  the commit message:
------------------------------

::

    <type>(<scope>): <subject>

    <body>

    <footer>

Example commit message:
-----------------------

::

    mod(uml): Add a factory for UML Property Descriptors

    Added a metaclass to handle UML Property Instantiation. The metaclass assigns
    the appropriate __set__ and __get__ method implementations.

    #P-15 Fixed
    Need to describe the steps for testing.

Message subject (first line):
-----------------------------
The first line should be a short description of the commit:

- Cannot be longer than 70 characters.
- Uses the imperative, present tense: “change” not “changed” nor “changes”
- The type and scope should always be lowercase.
- The second line is always blank

Allowed ``<type>`` values:
##########################
- **feat**: New feature (user)
- **fix**: Specific bugfix (user)
- **docs**: Changes to the documentation
- **refactor**: Refactoring production code, e.g. rename a class, move a file
- **style**: Formatting - No production code change
- **test** Adding missing tests - No production code change
- **chore**: Clean up, remove commented code, etc. - No production code change
- **bump**: Bump version - No production code change

Allowed ``<scope>`` values:
###########################
The ``<scope>`` should match the subsystem (component) affected by the commit. It can be empty if the change is global
or affects multiple components, in which case the parenthesis are omitted.


Message body:
-------------
The body should provide a meaningful commit message includes motivation for the change, and contrasts its implementation
with previous behaviour:

- Lines should be wrapped at 80 characters.
- Uses the imperative, present tense: “change” not “changed” nor “changes”

Message footer:
---------------
Referencing issues (YouTrack Integration)
#########################################
Issues are referenced according to the YouTrack VCS integration::

    #issueId <command 1> <command 2> ... <command n>
    <issue comment text>

For a detailed explanation of the command interface please refer to: `YouTrack Commands <https://www.jetbrains.com/help/youtrack/standalone/7.0/Commands.html>`_

Issue state commands include:
#############################
- *fixed*
- *in progress*
- *reopened*
- *incomplete*
- *to be discussed*
- *verified*

The ´<issue comment text>´ is added to the issue as a comment.

Breaking changes:
#################
All breaking changes have to be mentioned in footer with the description of the change, justification and migration notes.::

    BREAKING CHANGE:

    `port-runner` command line option has changed to `runner-port`, so that it is
    consistent with the configuration file syntax.

    To migrate your project, change all the commands, where you use `--port-runner`
    to `--runner-port`.


------------

Commit Messages are based on `Karma Git Commit Msg Convention <http://karma-runner.github.io/latest/dev/git-commit-msg.html>`_.
