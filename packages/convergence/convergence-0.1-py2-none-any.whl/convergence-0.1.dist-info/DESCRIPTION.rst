convergence
===========

A Python program to Perform Calculations Associated with a Grid
Convergence Study.

Introduction
------------

This is a port of verify.f90, a program provided as part of the NASA
Examining Spatial (Grid) Convergence tutorial.

http://www.grc.nasa.gov/WWW/wind/valid/tutorial/spatconv.html

Additional changes have been made to reflect the recommendations in:

Celik, I. B., Ghia, U., & Roache, P. J. (2008). Procedure for estimation
and reporting of uncertainty due to discretization in CFD applications.
Journal of fluids Engineering-Transactions of the ASME, 130(7).

This code was written by Mathew Topper between 2009 and 2011 as part of
the Supergen Marine Research Consortium project. I was younger then and
would do many things differently now. I am working on updating this code
to make the main class and functions more easy to use and also integrate
into other projects. Watch this space.

Installation
------------

The package requires no dependencies, but is currently only available
for Python 2.7.

The package can be installed by downloading the source code, and using a
terminal or command prompt as follows:

::

    cd /path/to/convergence
    python setup.py install

The package can also be downloaded from PyPI, again using a terminal or
command prompt:

::

    pip install convergence

Basic Usage
-----------

The package provides a command line interface which is the main (and
currently only sensible) way to use the package. The input data must be
a space delimeted text file with the first column being the grid spacing
and the second column being the metric of interest. An example can be
found in the *data* folder of the source code.

The program can then be executed as follows:

::

    grid-convergence /path/to/data/file

By default, the results of the program are written to a file called
*verify\_report.txt* in the calling directory. The file name can be
changed using the *-o* or *--out* command line options. The format of
the file is as follows:

::

    --- VERIFY: Performs verification calculations --- 

    Number of grids to be examined = 3 

         Grid Size     Quantity 

         1.000000      0.970500 
         2.000000      0.968540 
         4.000000      0.961780 


    Discretisation errors for fine grids:

           Grids |     e_approx |     e_extrap |      f_exact |   gci_coarse | 
     =========================================================================
           1 2 3 |     0.002020 |     0.000824 |     0.971300 |     0.003555 | 
     -------------------------------------------------------------------------

           Grids |     gci_fine |            p |          r21 |          r32 | 
     =========================================================================
           1 2 3 |     0.001031 |     1.786170 |     2.000000 |     2.000000 | 
     -------------------------------------------------------------------------


    Discretisation errors for coarse grids:

           Grids |     e_approx |     e_extrap |      f_exact |   gci_coarse | 
     =========================================================================
           1 2 3 |     0.006980 |     0.002842 |     0.971300 |     0.012287 | 
     -------------------------------------------------------------------------

           Grids |     gci_fine |            p |          r21 |          r32 | 
     =========================================================================
           1 2 3 |     0.003562 |     1.786170 |     2.000000 |     2.000000 | 
     -------------------------------------------------------------------------


    Asympototic ratio test:

               Grids | Asymptotic ratio | 
     ====================================
               1 2 3 |         0.997980 | 
     ------------------------------------


    --- End of VERIFY --- 

In the first table the input data is displayed. The second table shows
the fine analysis results for each trio of grids and the second table
shows the coarse analysis results for each trio. The final table shows
the asymptotic ratio.

The headers of the tables have the following meanings:

-  **Grids**: the trio of grids being analysed
-  **e\_approx**: approximate relative error
-  **e\_extrap**: extrapolated relative error
-  **f\_exact**: the estimated the zero grid spacing value
-  **gci\_coarse**: coarse grid convergence index
-  **gci\_fine** fine grid convergence index
-  **p**: order of convergence
-  **r21**: ratio of the middle to fine grid spacing
-  **r32**: ratio of the coarse to middle grid spacing

Known Analytical Result
-----------------------

If there is a known zero spacing value for the convergence study this
value can be added to the analysis using the *-a* or *--analytical*
command line option. To illustrate, the basic example would now become:

::

    grid-convergence /path/to/data/file -a 0.12345

Additional headers now appear in the fine and coarse analysis tables
with the following meanings:

-  **e\_analytic**: analytical relative error
-  **f\_analytic**: the analytical the zero grid spacing value
-  **f\_delta**: the different between the analytical and estimated zero
   grid spacing value


