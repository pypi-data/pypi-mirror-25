SSPYRS
======

Summary
-------
The SSPYRS (SQL Server Python Reporting Services) library is a lightweight interface for interacting with and retrieving data from SSRS reports. The core functionality of the library is straightforward. Perform authentication to an SSRS server, initialize a session, and then retrieve the report data from that session. Report data can be interacted with via raw XML, but has predefined methods to organize it into Pandas DataFrame objects.

Compatability
-------------
The SSPYRS library works primarily from the XML export functionality of SSRS. However, this neither XML nor CSV exports are provided in the express versions of SQL Server. The library does include direct download functions for the Excel export included in the express version, however it will not read the data directly into memory.

SSPYRS has been validated to work with SSRS 2008 R2, SSRS 2014, and SSRS 2016 under most server settings.


Usage and Documentation
=======================



