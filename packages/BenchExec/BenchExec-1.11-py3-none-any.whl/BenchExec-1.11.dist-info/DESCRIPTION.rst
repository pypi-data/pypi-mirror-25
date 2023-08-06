BenchExec
=========

A Framework for Reliable Benchmarking and Resource Measurement
--------------------------------------------------------------

|Build Status| |Code Quality| |Test Coverage| |Issue Stats| |Apache 2.0
License| |PyPI version|

**News**:

-  An extended version of our paper on BenchExec and its background gets
   published in `STTT <http://sttt.cs.uni-dortmund.de/index.html>`__,
   you can now read the preprint of `Reliable Benchmarking: Requirements
   and
   Solutions <https://www.sosy-lab.org/~dbeyer/Publications/2017-STTT.Reliable_Benchmarking_Requirements_and_Solutions.pdf>`__.
   In addition to the `previous version from
   SPIN'15 <https://www.sosy-lab.org/~dbeyer/Publications/2015-SPIN.Benchmarking_and_Resource_Measurement.pdf>`__,
   it also describes the container mode and how to present result data.
-  BenchExec 1.9 adds a `container
   mode <https://github.com/sosy-lab/benchexec/blob/master/doc/container.md>`__
   that isolates each run from the host system and from other runs
   (disabled by now, will become default in BenchExec 2.0).

BenchExec provides three major features:

-  execution of arbitrary commands with precise and reliable measurement
   and limitation of resource usage (e.g., CPU time and memory), and
   isolation against other running processes
-  an easy way to define benchmarks with specific tool configurations
   and resource limits, and automatically executing them on large sets
   of input files
-  generation of interactive tables and plots for the results

Contrary to other benchmarking frameworks, it is able to reliably
measure and limit resource usage of the benchmarked tool even if it
spawns subprocesses. In order to achieve this, it uses the `cgroups
feature <https://www.kernel.org/doc/Documentation/cgroup-v1/cgroups.txt>`__
of the Linux kernel to correctly handle groups of processes. For proper
isolation of the benchmarks, it uses (if available) Linux `user
namespaces <http://man7.org/linux/man-pages/man7/namespaces.7.html>`__
and an `overlay
filesystem <https://www.kernel.org/doc/Documentation/filesystems/overlayfs.txt>`__
to create a
`container <https://github.com/sosy-lab/benchexec/blob/master/doc/container.md>`__
that restricts interference of the executed tool with the benchmarking
host. BenchExec is intended for benchmarking non-interactive tools on
Linux systems. It measures CPU time, wall time, and memory usage of a
tool, and allows to specify limits for these resources. It also allows
to limit the CPU cores and (on NUMA systems) memory regions, and the
container mode allows to restrict filesystem and network access. In
addition to measuring resource usage, BenchExec can verify that the
result of the tool was as expected, and extract further statistical data
from the output. Results from multiple runs can be combined into CSV and
interactive HTML tables, of which the latter provide scatter and
quantile plots (have a look at our `demo
table <https://sosy-lab.github.io/benchexec/example-table/svcomp-simple-cbmc-cpachecker.table.html>`__).

BenchExec works only on Linux and needs a one-time setup of cgroups by
the machine's administrator. The actual benchmarking can be done by any
user and does not need root access.

BenchExec was originally developed for use with the software
verification framework `CPAchecker <https://cpachecker.sosy-lab.org>`__
and is now developed as an independent project at the `Software Systems
Lab <https://www.sosy-lab.org>`__ at the `Ludwig-Maximilians-Universität
München (LMU) <http://www.lmu.de>`__.

Links
~~~~~

-  `Documentation <https://github.com/sosy-lab/benchexec/tree/master/doc/INDEX.md>`__
-  `Demo <https://sosy-lab.github.io/benchexec/example-table/svcomp-simple-cbmc-cpachecker.table.html>`__
   of a result table
-  `Downloads <https://github.com/sosy-lab/benchexec/releases>`__
-  `Changelog <https://github.com/sosy-lab/benchexec/tree/master/CHANGELOG.md>`__
-  `BenchExec GitHub
   Repository <https://github.com/sosy-lab/benchexec>`__, use this for
   `reporting issues and asking
   questions <https://github.com/sosy-lab/benchexec/issues>`__
-  `BenchExec at PyPI <https://pypi.python.org/pypi/BenchExec>`__
-  *New*: Paper `Reliable Benchmarking: Requirements and
   Solutions <https://www.sosy-lab.org/~dbeyer/Publications/2017-STTT.Reliable_Benchmarking_Requirements_and_Solutions.pdf>`__
   about BenchExec (`supplementary
   webpage <https://www.sosy-lab.org/~dbeyer/benchmarking/>`__)

Authors
~~~~~~~

Maintainer: `Philipp Wendler <https://www.philippwendler.de>`__

Contributors:

-  `Dirk Beyer <https://www.sosy-lab.org/~dbeyer>`__
-  `Montgomery Carter <https://github.com/MontyCarter>`__
-  `Andreas Donig <https://github.com/adonig>`__
-  `Karlheinz
   Friedberger <https://www.sosy-lab.org/people/friedberger>`__
-  Peter Häring
-  `George Karpenkov <http://metaworld.me/>`__
-  `Mike Kazantsev <http://fraggod.net/>`__
-  Thomas Lemberger
-  Sebastian Ott
-  Stefan Löwe
-  Stephan Lukasczyk
-  `Alexander von
   Rhein <http://www.infosun.fim.uni-passau.de/se/people-rhein.php>`__
-  `Alexander
   Schremmer <https://www.xing.com/profile/Alexander_Schremmer>`__
-  `Andreas Stahlbauer <http://stahlbauer.net/>`__
-  `Thomas Stieglmaier <https://stieglmaier.me/>`__
-  and `lots of more people who integrated tools into
   BenchExec <https://github.com/sosy-lab/benchexec/graphs/contributors>`__

Users of BenchExec
~~~~~~~~~~~~~~~~~~

BenchExec was successfully used for benchmarking in all six instances of
the `International Competition on Software
Verification <https://sv-comp.sosy-lab.org>`__ (2012-2017) with a wide
variety of benchmarked tools and hundreds of thousands benchmark runs.

The developers of the following tools use BenchExec:

-  `CPAchecker <https://cpachecker.sosy-lab.org>`__, also for regression
   testing
-  `SMACK <https://github.com/smackers/smack>`__

If you would like to be listed here, `contact
us <https://github.com/sosy-lab/benchexec/issues/new>`__.

.. |Build Status| image:: https://travis-ci.org/sosy-lab/benchexec.svg?branch=master
   :target: https://travis-ci.org/sosy-lab/benchexec
.. |Code Quality| image:: https://api.codacy.com/project/badge/grade/d9926a7a5cb04bcaa8d43caae38a9c36
   :target: https://www.codacy.com/app/PhilippWendler/benchexec
.. |Test Coverage| image:: https://api.codacy.com/project/badge/coverage/d9926a7a5cb04bcaa8d43caae38a9c36
   :target: https://www.codacy.com/app/PhilippWendler/benchexec
.. |Issue Stats| image:: https://img.shields.io/issuestats/p/github/sosy-lab/benchexec.svg
   :target: http://issuestats.com/github/sosy-lab/benchexec
.. |Apache 2.0 License| image:: https://img.shields.io/badge/license-Apache--2-brightgreen.svg
   :target: https://www.apache.org/licenses/LICENSE-2.0
.. |PyPI version| image:: https://img.shields.io/pypi/v/BenchExec.svg
   :target: https://pypi.python.org/pypi/BenchExec


