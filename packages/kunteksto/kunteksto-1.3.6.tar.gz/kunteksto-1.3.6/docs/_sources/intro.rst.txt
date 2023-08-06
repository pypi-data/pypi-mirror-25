=============================
Introduction and Installation
=============================

Purpose
=======

**Kunteksto** (ˈkänˌteksto) [#f1]_ is a tool to translate simple CSV formatted data files into computable, semantically enhanced knowledge representations. As a foundation for **crowd sourced**, *automated knowledge base construction*; it provides a path for existing data sets to be used in conjuntion with the emerging *datacentric, model first* approach in analysis, general artificial intelligence and decision support systems. This approach opens the door for the change to a *datacentric* world as opposed to the *application-centric* one we have now. This new approach enables automatic interoperability avoiding the data quality issues created through data cleaning and massaging. 

The importance of how this simplifies query and analysis capabilities and improves data quality is discussed in foundational `S3Model <https://datainsights.tech/S3Model>`_ documentation and references. However, detailed understanding of S3Model is not required to understand and use the power of Kunteksto. Addtional information on the datacentric movement can be found below [#f2]_

Target Audience
---------------
Kunteksto design is based around the ability for *domain experts* from any field, with very little programming ability to quickly annotate data extracts to improve the usability of the data.  Data engineers and data scientists can also benefit from Kunteksto in the same ways as domain experts. It just takes a bit more research to discover the semantics that the original domain experts usually have at hand.

Requirements
============

- Python 3.6 or later. See: `Downloads <https://www.python.org/downloads/>`_  

.. _install:

Installation
============

Cross-Platform on Anaconda
--------------------------

This is the **preferred environment** for a tool like Kunteksto because it integrates easily with systems for domain experts, data engineers and data scientists.

- `Download and install <https://www.continuum.io/downloads>`_ Anaconda Python 3.6+ for your platform.
- More detailed Anaconda instructions are `here <https://docs.continuum.io/anaconda/install/>`_  if you prefer.
- If you are using Linux or Mac OSX, follow the `instructions for your platform <http://lxml.de/installation.html>`_ for **lxml** installation. 


- Open a terminal window and create a conda environment. On Windows it is best to open an *Anaconda Prompt* terminal from the Anaconda menu: 

.. code-block:: sh

    conda create -p kunteksto python=3 pycurl ujson

- Change to the directory

.. code-block:: sh
    
    cd kunteksto

.. _activate: Activate


- Activate the environment according to the instructions shown by Anaconda in the terminal window.

**Windows**

.. code-block:: sh

    activate <path/to/directory> 

**or Linux/MacOSX**

.. code-block:: sh

    source activate <path/to/directory> 

- install Kunteksto

.. code-block:: sh

    pip install kunteksto

These four quick steps creates a virtual environment in the subdirectory *kunteksto*. When it is created conda displays how to activate the environment. Once activated then Kunteksto is installed in the subdirectoy along with the environment. 

The last step is to do the :ref:`tutor`



Windows
-------

Details coming soon. Preferably use the Anaconda instructions above. 


Mac OSX
-------
Follow the `instructions for your platform <http://lxml.de/installation.html>`_ for lxml installation. 

Details coming soon. Preferably use the Anaconda instructions above. 


Linux
-----

Install Python and SQLiteBrowser as directed by the links above. 

Follow the `instructions for your platform <http://lxml.de/installation.html>`_ for lxml installation. 

Now that that is settled.  The rest is easy.  

.. note::

    **Option 1:**

    Use the Anaconda instructions above. 

.. note::

    **Option 2:**

    Just create a virtual environment for Python 3.6 or later, using your favorite tool; conda, virtualenv, etc. 

    .. code-block:: sh

        conda create -p kunteksto python=3

    Activate your virtual environment and navigate to the *kunteksto* directory. Then install kunteksto using pip.

    .. code-block:: sh
     
        pip install kunteksto

    After several minutes of installing all the cool stuff, you'll be ready to begin the tutorial. 


	Go to the :ref:`tutor` 


Update to a New Version
=======================

When you want to upgrade to a new version of Kunteksto you can just use the line below in your terminal where you have activated the virtual environment. 

.. code-block:: sh

    pip install  kunteksto --upgrade --no-cache-dir


What are all the files for?
===========================

Depending on how and where you installed Kunteksto you will see a varying number of files and subdirectories. Many of them may be part of the Anaconda environment so we won't be covering those.

Referenced from the *kunteksto* directory created at install time:

Files
-----

- README.md
    A brief explaination of Kunteksto's purpose and links to background information.

- kunteksto.conf
    The required configuration file for Kunteksto.

- LICENSE.txt
    A copy of the copyright notice and license.


Directories
-----------

- example_data
    Where you will find information and sample data files for the tutorials. There is also an example of the completed Demo database, model and data in the archive Demo_with_semantics.zip. 

- output
    The default location of all generated output from Kunteksto. This can be changed either via the configuration file or via the commandline. 

- catalogs
    Where Kunteksto places XML catalog files that are used in in the data validation process.

- s3model
    Support files required for operation.

    - s3model.owl - the core S3Model ontology.
    - s3model_3_0_0.xsd - the reference model schema version 3.0.0
    - s3model_3_0_0.rdf - the extracted semantics from the reference model schema version 3.0.0
    - s3model_3_0_0.xsl - a stylesheet providing visualization in a browsser of the reference model schema version 3.0.0
    - dm-description.xsl - a stylesheet providing visualization in a browser of any S3Model data model. Just place it in the same directory with the dm-{uuid}.xsd file and open the schema in a browser. 



.. rubric:: Footnotes

.. [#f1] S3Model is called the Esperanto of information management. Kunteksto is the Esperanto translation for *Context*. See `Wikipedia <https://simple.wikipedia.org/wiki/Esperanto>`_ for more information about the Esperanto language.

.. [#f2] 
    -  `The Estes Park Group <http://estesparkgroup.org/>`_ 
    -  `The Data-centric Manifesto <http://datacentricmanifesto.org/>`_  
    -  `Data-centric companies will devour competitors <https://goo.gl/xDcpZM>`_ 
    -  `The Data-Centric Revolution: Gaining Traction <https://goo.gl/zdRLm9>`_ 
    -  `The limits of deep learning <https://blog.keras.io/the-limitations-of-deep-learning.html>`_ 
    -  `The future of deep learning <https://blog.keras.io/the-future-of-deep-learning.html>`_