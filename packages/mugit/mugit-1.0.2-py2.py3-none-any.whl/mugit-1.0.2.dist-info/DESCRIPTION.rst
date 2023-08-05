mugit
=======

This is a tool for managing a workspace containing multiple git_ repositories.

Although generally all software architects agree that version control is
essential to software development, the community is split on what is best
for large-scale projects, especially those which heavily reuse components.
There are many different opinions (for example, see [#]_, [#]_, [#]_, and
[#]_) but they generally fall into one of two camps:

- monorepo — one monolithic repository containing everything

- multiple repos — split project into many repositories, each managing a
  single component

For those whose projects which adopt the philosophy of multiple repos, mugit
is used in concert with git_ to manage the overall project workspace.

The root directory of the workspace, itself managed as a git_ repository,
includes a *manifest* file.  This is an XML file describing which folders
in the workspace are themselves git_ repositories.  For each of these,
the manifest holds configuration metadata:

- upstream URL, from which to clone the repository and to where to
  push changes

- which branch to check out

- whether or not to keep the repository *pinned*, or pointed to a
  specific revision even if the branch changes (e.g. new commits are
  added upstream)

Multiple manifest files may exist in a project.  Typically one manifest
is used during normal development to keep all components up to date
on their configured branches, and another manifest (with all repositories
pinned) is used to mark what revisions of each component together
constitute the last release or snapshot of the overall project.

Installation
------------

- ``pip install mugit`` — download and install from PyPI

- ``pip install mugit-1.0.0-py2.py3-none-any.whl`` — install from local
  wheel file

- ``pip install -e .`` — install in `editable mode`_ from mugit
  source folder

Usage
-----

- ``mugit [COMMAND] --help`` — get more help overall or for a specific command

- ``mugit select [-c] <MANIFEST>`` — select manifest to use in other
  mugit commands

- ``mugit pull [-c]`` — clone missing repositories and fetch/rebase
  existing ones

- ``mugit status [-c] [-a]`` — generate report on the state of the workspace

  - Use ``-a`` to list all repositories, not just ones with changes.

- ``mugit update [-c]`` — update manifest to reflect current workspace state

- ``mugit add [-c] --all | <PATH>..`` — add repositories to the manifest

  - Specify repositories by path or use ``--all`` to automatically scan
    for them.

- ``mugit remove <PATH>..`` — remove repositories from the manifest

- ``mugit release <MANIFEST>`` — create or update a release/snapshot manifest

- ``mugit --version`` — display tool version information

Many mugit commands use `ANSI escape codes`_ to control cursor movement in
the console.  This works for most terminals, but some (most notably, the
Windows command prompt) may need help from the colorama_ library.
The commands which can make use of colorama_ accept the optional -c argument,
which if used, activates colorama_.

Creating a New Project
~~~~~~~~~~~~~~~~~~~~~~

When setting up a new project, use ``mugit select`` to choose the name
of the manifest.  The selected manifest is tracked in the ``.git/config``
of the root project repository.

After creating or cloning project components, use ``mugit add -a`` to
scan the workspace for repositories, adding an entry for each into
the manifest.  This creates the manifest XML file if it didn't exist
previously.  Note that newly created components will have no upstream
URL and will be skipped in all pulls and remote checks.

::

  mkdir FooBar
  cd FooBar
  git init
  mkdir Foo
  mkdir Bar
  git clone https://example.com/Utilites.git
  cd Foo
  git init
  git commit --allow-empty -m "Initial Revision"
  cd ../Bar
  git init
  git commit --allow-empty -m "Initial Revision"
  cd ..
  mugit select main
  mugit add -a
  git add main.xml
  git commit -m "Initial Revision"

To add individual components later, create or clone them, and then
pass their paths to ``mugit add`` to update the manifest.  Remember
to commit the manifest change to the root project repository.

::

  mkdir Spam
  cd Spam
  git init
  git commit --allow-empty -m "Initial Revision"
  cd ..
  mugit select main
  mugit add Spam
  git add main.xml
  git commit -m "Add Spam"

When a new component is initially published, use ``mugit update`` to
update the manifest to include the upstream URL.  Remember
to commit the manifest change to the root project repository.

::

  cd Foo
  git remote add origin https://example.com/foo.git
  git push --set-upstream origin master
  cd ..
  mugit update
  git add main.xml
  git commit -m "Foo now published at example.com"

Cloning an Upstream Project
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``mugit select`` followed by ``mugit pull`` to initially clone
all components in a project.

::

  git clone https://example.com/FooBar.git
  cd FooBar
  mugit select main
  mugit pull

Checking Status
~~~~~~~~~~~~~~~

Use ``mugit status`` whenever unsure about whether there are local
changes, or to check if there are other changes upstream.
Normally, only components found to have local or remote changes will
be reported.  Use the ``-a`` option to force  all components to be
included in the report.

::

  mugit status -a

Downloading Updates
~~~~~~~~~~~~~~~~~~~

Use ``mugit pull`` to fetch upstream changes.  The changes are first
fetched into the remote tracking branch.  The working branch is then
rebased onto the remote tracking branch, resulting in a fast-forward
(if there were no local changes) or a rebase (if there were local changes).

It's best to check the status with ``mugit status`` first to make sure
there are no local untracked or staged changes which might interfere
with a rebase.

::

  mugit status
  mugit pull


Making a Release
~~~~~~~~~~~~~~~~

Use ``mugit release`` to create a special copy of the selected
manifest where all components are *pinned*, or marked with their
current commit SHA1 code listed in the manifest.  This is useful
for recording the exact revisions of all components used to form
a specific snapshot or release of the project.

::

  mugit release release
  git add release.xml
  git commit -m "Release 1.12.7"
  git tag "1.12.7"

Checking Out a Release
~~~~~~~~~~~~~~~~~~~~~~

A generated manifest can be used later with ``mugit select`` to check out
the exact revisions of all components in the manifest that were
present when that manifest was generated, even if component branches
have moved in the interim.

Note that each component ise put into a *headless* state, even
if the revision checked out happens to still be at the head of the
configured branch.

::

  mugit select release

License/Warranty
----------------

This tool is made available under the MIT license.

::

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.

See the file `LICENSE.txt <https://bitbucket.org/digitalstirling/mugit/src/HEAD/LICENSE.txt>`_ for more information.

.. _ANSI escape codes: https://en.wikipedia.org/wiki/ANSI_escape_code
.. _colorama: https://pypi.python.org/pypi/colorama
.. _editable mode: https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs
.. _git: https://git-scm.com/

.. [#] https://gist.github.com/arschles/5d7ba90495eb50fa04fc
.. [#] https://gist.github.com/technosophos/9c706b1ef10f42014a06
.. [#] https://news.ycombinator.com/item?id=10007654
.. [#] http://blog.shippable.com/our-journey-to-microservices-and-a-mono-repository


