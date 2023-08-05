Allure Adaptor for Robot Framework
==================================

.. contents::
   :local:

Introduction
------------

The Allure Adaptor for Robot Framework is a Library that can be included
in the Robot scripts to generate `Allure <http://allure.qatools.ru/>`_
compatible XML files which can then be used to generate the Allure HTML
reports. These reports provide a clear and dynamic overview of the status
of the test run through several graphs and a time line overview of the run
itself.

.. image:: https://img.shields.io/pypi/v/robotframework-allurereport.svg?label=version
   :target: https://pypi.python.org/pypi/robotframework-allurereport
   :alt: Latest version

.. image:: https://img.shields.io/pypi/dm/robotframework-allurereport.svg
   :target: https://pypi.python.org/pypi/robotframework-allurereport
   :alt: Number of downloads
   
.. image:: 
    https://img.shields.io/badge/license-MIT-blue.svg   
    :target: https://raw.githubusercontent.com/kootstra/robotframework-allurereport/master/LICENSE.txt
    :alt: License

.. image:: https://robotframework-slack.herokuapp.com/badge.svg
   :target: https://robotframework-slack.herokuapp.com
   :alt: Slack channel

Features
--------

-   Steps in Allure Framework are aligned to Keyword in Robot Framework.
-   Test Suites map to Allure Test Cases are the same at both xml formats of 
    Robot Framework and Allure.
-   Feature and Stories are implemented as robot framework Tags story:name and
    feature:name format.
-   External Issues Id's are supported as Robot Framework tags and an option to 
    define a regular expression for their recognition.
-   Link to the Issue Management system (For example JIRA) can be configured. 
-   The Allure adapter output is on top of the standard Robot Framework and does 
    not replace it. 
-   Initialisation is done as a Robot Framework Library or as a Command Line 
    Listener. Listener is preferred over the Library when in conflict.
-   Parallelisation is supported, both manually started Robot Framework instances 
    as well as using `Pabot <https://github.com/mkorpela/pabot>`_ (version 0.32+).
-   Supports overriding of Test Case status with: failed, broken, canceled, 
    pending or passed by using Tags.
-   Extends the number of Severity options to: blocker, critical, normal, minor 
    or trivial through use of Robot Framework Tags
-   The Allure Library is compatible with the Libspec API used by editors as for 
    example `RED <https://github.com/nokia/RED>`_
-   Supports nesting of keywords. 
-   Provides Robot Framwork Environment information in the Environment section 
    (versions, CLI arguments, OS type).
-   Screenshots created by the Selenium2Library are supported.


Installation
------------
Prerequisites:
^^^^^^^^^^^^^ 
The Allure adapter for Robotframework has a number of requirements that need to
be in place:
-   Python. In testing 2.7 has been used. 
-   `Allure Pytest Adaptor <https://github.com/allure-framework/allure-python>` 
    who'se foundation Python classes are used. It will be installed if not present.
-   Robot Framework versions 2.8.5 and 3.0 have been used in testing. Since Robot 
    Framework can be installed outside of `pip` this is not automatically installed.
-   `Allure Command line <http://wiki.qatools.ru/display/AL/Allure+Commandline>`
    is needed to convert the Allure adapter for Robot Framework output files to 
    the final HTML format.
-   The Allure command line application requires Java Runtime Environment of 1.7
    higher to function properly.

Steps
^^^^^^^^^^^^^^
Use PIP::

    pip install robotframework-allurereport


Clone the project repository from GitHub. After that you can install
the framework with::

    python setup.py install

Usage
-------
The Allure adapter can be started as Library from within a Robot Framework test 
suite or when Robot Framework is started as a command line switch.

Library
^^^^^^^
Below is a example Robot Framework suite file. The AllureLibrary is added in the
Settings section of the file. When it's loaded it adds the listener to Robot
Framework.

Optionally an argument can be provided to have the Allure adapter store its 
files in a different folder from the normal Robot Framework log files. 

.. code:: robotframework

    Library           AllureReportLibrary     C:\\Temp\\Allure

Below a more complete example:

.. code:: robotframework

    *** Settings ***
    Documentation     A test suite with a single test for valid login.
    ...
    ...               This test has a workflow that is created using keywords in
    ...               the imported resource file.
    Resource          resource.robot
    Library           AllureReportLibrary      //var//lib//Allure

    *** Test Cases ***
    Valid Login
        Open Browser To Login Page
        Input Username    demo
        Input Password    mode
        Submit Credentials
        Welcome Page Should Be Open
        [Teardown]    Close Browser

Command line switch
^^^^^^^^^^^^^^^^^^
For enabling the Allure adapter for a large set of suites files or simply for 
prefer to switch it on when needed, specifying a `listner <http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#listener-interface>`_ on the command line 
is the recommended approach.

The Listener is a class in the AllureLibrary Python module and can be directly 
accessed as `AllureLibrary.AllureListener` or in case the module is not installed
via PIP the full path to the `AllureListner.py` file.

The listener has 1 option argument to set the output folder. In the same way as 
the Library the full path to the folder where the files can be stored.:: 

    robot --listener AllureReportLibrary.AllureListener;C:\\tmp\AllureLog\ C:\tmp\\RobotScripts

Another example but then for `Pabot <https://github.com/mkorpela/pabot>`_. Since
it supports the regular Robot Framework command line switches as well the difference
is small.::

    pabot --processes 2 --listener AllureReportLibrary.AllureListener;C:\\tmp\AllureLog\ C:\tmp\\RobotScripts

Notes
-----

The Allure Adapter for Robotframework adheres to the Allure `Output Convention <https://github.com/allure-framework/allure1/wiki/Creating-Allure-Adapter#output-file-conventions>`.

-  Every XML file should be named like this: `{UUID}-testsuite.xml`,
   where `{UUID}` is a `universally unique identifier`_.
-  Every XML file should be valid when checked with the `Allure
   schema`_.
-  The output result of an Allure adapter should store not only XML
   files with information about tests, but also copies of all attached
   files.
-  Every `attachment`_ file should be named like this:
   `{HASH-SUM}-attachment.{EXT}`, where `{HASH-SUM}` is the
   cryptographic hash sum of the file contents (e.g. `MD5`_, `SHA1`_,
   `Whirlpool`_ and so on), `{EXT}` is the file extension
   corresponding to the `MIME type`_ in the XML file. We require
   cryptographic hash sums in order to avoid storing files with
   duplicate content.

.. _universally unique identifier: http://en.wikipedia.org/wiki/Uuid
.. _Allure schema: https://github.com/allure-framework/allure-core/blob/master/allure-model/src/main/resources/allure.xsd
.. _attachment: https://github.com/allure-framework/allure-core/wiki/Glossary#attachment
.. _MD5: http://en.wikipedia.org/wiki/MD5
.. _SHA1: http://en.wikipedia.org/wiki/SHA1
.. _Whirlpool: http://en.wikipedia.org/wiki/Whirlpool_%28cryptography%29
.. _MIME type: http://en.wikipedia.org/wiki/MIME


Further development
-------------------

With logging being influenced by a lot of different factors the present state
does not cover all options and permutations. Some notable examples that are 
slated for upcoming releases:

-   Screenshots are saved as a copy of the screenshots generated from
    Robot Framework. This requires the regular logging to happen in parallel. 
-   Command line settings for criticality and non-criticality are currently not
    used.
-   Suite Setup and Tear down may not behave as expected.
-   Interaction between the Library and Listener is currently not possible. The 
    Library on facilitates the initialisation, but not any interaction.
-   Although maybe last, certainly not least: documentation. 

License
-------

Allure Adaptor for Robot Framework is open source software provided under the 
`MIT License <https://opensource.org/licenses/MIT>`_. This software depends on 
`Allure Reporting <https://github.com/allure-framework/allure1>`_ and the 
Allure Python adapter. These two projects are also based on GitHub but are 
available under the `Apache 2.0 license <http://www.apache.org/licenses/>`_. 
Other dependent Python Modules are available but perhaps under other licenses. 
