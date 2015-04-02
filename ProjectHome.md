There is no need to introduce the [OpenSSH](http://www.openssh.com) utility suite, that nowadays has a long success story.

The ssh-keydb project goal is to provide a way to easily manage the authorized\_keys files containing the OpenSSH public keys used for key-pair authentication. Assuming the keys are managed per-user, it is then possible to define roles and memberships on groups of machines for each individual.

The tool then allows to generate the authorized\_keys files and even to propagate them on the machines themselves.

## News ##

The first draft of the tool has been uploaded. It works from the command-line and provides a web front-end.

## Downloads ##

To obtain the tool, go to the [Source Checkout](http://code.google.com/p/ssh-keydb/source/checkout) page (recommended for now, since there is no stable release yet). The Python egg files are also available on the PyPI repository https://pypi.python.org/pypi/ssh-keydb.

## Documentation ##

Not available yet. Help is available from the command-line by running the tool without argument or with --help.

## Features ##

The list of currently available features:

  * Multiple public keys can be associated to the same user.
  * Multiple memberships for users based on public key, role, location and server groups. Each membership can be customized with arguments.
  * Per-server, per-login and per-location permissions definition.
  * Generation of the authorized\_keys file.
  * Overview of the user's profile. The chart shows the public keys, permissions, memberships and permissions of the user on a single chart.
  * Comes with a simple web front-end.

## Future Work ##

  * Combination with [Git](http://git-scm.com/) for deployment.
  * Handling of hostkeys
  * Dynamic meta-tags