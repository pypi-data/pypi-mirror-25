pysap
=====

[pysap](https://www.coresecurity.com/corelabs-research/open-source-tools/pysap)
is a Python library that provides modules for crafting and sending packets
using SAP's NI, Message Server, Router, RFC, SNC, Enqueue and Diag protocols.
The modules are build on top of [Scapy](http://www.secdev.org/projects/scapy/)
and are based on information acquired at researching the different protocols
and services.


Features
--------

* Dissection and crafting of the following network protocols:

    * SAP Network Interface (NI)
    * SAP Diag
    * SAP Enqueue
    * SAP Router
    * SAP Message Server (MS)
    * SAP SNC

* Client interfaces for handling the following file formats:

    * SAP SAR archive files

* Library implementing SAP's LZH and LZC compression algorithms.

* Automatic compression/decompression of payloads with SAP's algorithms.

* Client, proxy and server classes implemented for some of the protocols.

* Example scripts to illustrate the use of the different modules and protocols.


:copyright: (c) 2012-2017 by Martin Gallo, Core Security.
:license: GNU General Public License v2 or later (GPLv2+).


