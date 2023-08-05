
What is Tox?
--------------------


.. image:: https://img.shields.io/pypi/v/tox.svg
   :target: https://pypi.org/project/tox/
.. image:: https://img.shields.io/pypi/pyversions/tox.svg
  :target: https://pypi.org/project/tox/
.. image:: https://travis-ci.org/tox-dev/tox.svg?branch=master
    :target: https://travis-ci.org/tox-dev/tox
.. image:: https://img.shields.io/appveyor/ci/RonnyPfannschmidt/tox/master.svg
    :target: https://ci.appveyor.com/project/RonnyPfannschmidt/tox


Tox is a generic virtualenv management and test command line tool you can use for:

* checking your package installs correctly with different Python versions and
  interpreters

* running your tests in each of the environments, configuring your test tool of choice

* acting as a frontend to Continuous Integration servers, greatly
  reducing boilerplate and merging CI and shell-based testing.

For more information and the repository please checkout:

- home and docs: https://tox.readthedocs.org

- repository: https://github.com/tox-dev/tox



Changelog (last 5 releases - `full changelog <https://github.com/tox-dev/tox/blob/master/CHANGELOG>`_)
======================================================================================================


2.8.2 (2017-10-09)
------------------

- `#466 <https://github.com/tox-dev/tox/issues/466>`_: stop env var leakage if popen failed with resultjson or redirect

2.8.1 (2017-09-04)
------------------

- `#p599 <https://github.com/tox-dev/tox/pull/599>`_: fix problems with implementation of `#515 <https://github.com/tox-dev/tox/issues/515>`_.
         Substitutions from other sections were not made anymore if they were not in `envlist`.
         Thanks to Clark Boylan (@cboylan) for helping to get this fixed (`#p597 <https://github.com/tox-dev/tox/pull/597>`_).

2.8.0 (2017-09-01)
-------------------

- `#276 <https://github.com/tox-dev/tox/issues/276>`_: Remove easy_install from docs (TL;DR: use pip).
        Thanks Martin Andrysík (@sifuraz).
- `#301 <https://github.com/tox-dev/tox/issues/301>`_: Expand nested substitutions in tox.ini
        Thanks @vlaci.
        Thanks to Eli Collins (@eli-collins) for creating a reproducer.
- `#315 <https://github.com/tox-dev/tox/issues/315>`_: add --help and --version to helptox-quickstart
        Thanks @vlaci.
- `#326 <https://github.com/tox-dev/tox/issues/326>`_: Fix OSError 'Not a directory' when creating env on Jython 2.7.0.
        Thanks Nick Douma (@LordGaav).
- `#429 <https://github.com/tox-dev/tox/issues/429>`_: Forward MSYSTEM by default on Windows
        Thanks Marius Gedminas (@mgedmin) for reporting this.
- `#449 <https://github.com/tox-dev/tox/issues/449>`_: add multi platform example to the docs.
        Thanks Aleks Bunin (@sashkab) and @rndr.
- `#474 <https://github.com/tox-dev/tox/issues/474>`_: Start using setuptools_scm for tag based versioning.
- `#484 <https://github.com/tox-dev/tox/issues/484>`_: Renamed `py.test` to `pytest` throughout the project
        Thanks Slam (@3lnc).
- `#504 <https://github.com/tox-dev/tox/issues/504>`_: With `-a`: do not show additional environments header if there are none
        Thanks @rndr.
- `#515 <https://github.com/tox-dev/tox/issues/515>`_: Don't require environment variables in test environments where they
        are not used.
        Thanks André Caron (@AndreLouisCaron).
- `#517 <https://github.com/tox-dev/tox/issues/517>`_: Forward NUMBER_OF_PROCESSORS by default on Windows to fix
        `multiprocessor.cpu_count()`.
        Thanks André Caron (@AndreLouisCaron).
- `#518 <https://github.com/tox-dev/tox/issues/518>`_: Forward `USERPROFILE` by default on Windows.
        Thanks André Caron (@AndreLouisCaron).
- `#p528 <https://github.com/tox-dev/tox/pull/528>`_: Fix some of the warnings displayed by pytest 3.1.0.
         Thanks Bruno Oliveira (@nicoddemus).
- `#p547 <https://github.com/tox-dev/tox/pull/547>`_: Add regression test for `#137 <https://github.com/tox-dev/tox/issues/137>`_
         Thanks Martin Andrysík (@sifuraz).
- `#p553 <https://github.com/tox-dev/tox/pull/553>`_: Add an XFAIL test to reproduce upstream bug `#203 <https://github.com/tox-dev/tox/issues/203>`_
         Thanks Bartolomé Sánchez Salado (@bartsanchez).
- `#p556 <https://github.com/tox-dev/tox/pull/556>`_: Report more meaningful errors on why virtualenv creation failed
         Thanks @vlaci.
         Also thanks to Igor Sadchenko (@igor-sadchenko) for pointing out a
         problem with that PR before it hit the masses :)
- `#575 <https://github.com/tox-dev/tox/issues/575>`_: Add announcement doc to end all announcement docs
        (using only CHANGELOG and Github issues since 2.5 already)
- `#p580 <https://github.com/tox-dev/tox/pull/580>`_: Do not ignore Sphinx warnings anymore
         Thanks Gábor Bernát (@gaborbernat).
- `#585 <https://github.com/tox-dev/tox/issues/585>`_: Expand documentation to explain pass through of flags from deps to pip
        (e.g. -rrequirements.txt, -cconstraints.txt)
        Thanks Alexander Loechel (@loechel).
- `#588 <https://github.com/tox-dev/tox/issues/588>`_: Run pytest wit xfail_strict and adapt affected tests.

2.7.0 (2017-04-02)
------------------

- `#p450 <https://github.com/tox-dev/tox/pull/450>`_: Stop after the first installdeps and first testenv create hooks
  succeed. This changes the default behaviour of `tox_testenv_create`
  and `tox_testenv_install_deps` to not execute other registered hooks when
  the first hook returns a result that is not `None`.
  Thanks Anthony Sottile (@asottile).

- `#271 <https://github.com/tox-dev/tox/issues/271>`_ and `#464 <https://github.com/tox-dev/tox/issues/464>`_: Improve environment information for users.

  New command line parameter: `-a` show **all** defined environments -
  not just the ones defined in (or generated from) envlist.

  New verbosity settings for `-l` and `-a`: show user defined descriptions
  of the environments. This also works for generated environments from factors
  by concatenating factor descriptions into a complete description.

  Note that for backwards compatibility with scripts using the output of `-l`
  it's output remains unchanged.

  Thanks Gábor Bernát (@gaborbernat).

- `#464 <https://github.com/tox-dev/tox/issues/464>`_: Fix incorrect egg-info location for modified package_dir in setup.py.
  Thanks Selim Belhaouane (@selimb).

- `#431 <https://github.com/tox-dev/tox/issues/431>`_: Add 'LANGUAGE' to default passed environment variables.
  Thanks Paweł Adamczak (@pawalad).

- `#455 <https://github.com/tox-dev/tox/issues/455>`_: Add a Vagrantfile with a customized Arch Linux box for local testing.
  Thanks Oliver Bestwalter (@obestwalter).

- `#454 <https://github.com/tox-dev/tox/issues/454>`_: Revert `#407 <https://github.com/tox-dev/tox/issues/407>`_, empty commands is not treated as an error.
  Thanks Anthony Sottile (@asottile).

- `#446 <https://github.com/tox-dev/tox/issues/446>`_: (infrastructure) Travis CI tests for tox now also run on OS X now.
  Thanks Jason R. Coombs (@jaraco).

2.6.0 (2017-02-04)
------------------

- add "alwayscopy" config option to instruct virtualenv to always copy
  files instead of symlinking. Thanks Igor Duarte Cardoso (@igordcard).

- pass setenv variables to setup.py during a usedevelop install.
  Thanks Eli Collins (@eli-collins).

- replace all references to testrun.org with readthedocs ones.
  Thanks Oliver Bestwalter (@obestwalter).

- fix `#323 <https://github.com/tox-dev/tox/issues/323>`_ by avoiding virtualenv14 is not used on py32
  (although we don't officially support py32).
  Thanks Jason R. Coombs (@jaraco).

- add Python 3.6 to envlist and CI.
  Thanks Andrii Soldatenko (@andriisoldatenko).

- fix glob resolution from TOX_TESTENV_PASSENV env variable
  Thanks Allan Feldman (@a-feld).


