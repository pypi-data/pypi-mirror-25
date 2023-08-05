=========
pysingfel
=========

Python version of `singfel <https://github.com/eucall-software/singfel>`_, which is a C++ package calculating the propagation of the scattered light signal (including incoherent effects) to the detector plane.

Benchmark
=========

+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
|             |                  C++                    |               pysingfel                 |
+=============+=============+=============+=============+=============+=============+=============+
| No. of dp   | 100         | 200         | 400         | 100         | 200         | 400         |
+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
| Time (s)    | 72.514      | 143.179     | 283.113     | 75.768      | 150.969     | 302.367     |
+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
| Ave time (s)| 3.626       | 3.579       | 3.539       | 3.788       | 3.774       | 3.780       |
+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
Here 'dp' means diffraction pattern. On average pysingfel is only about 5.3% slower than the C++ version, thanks for the just-in-time optimization provided by `Numba <https://numba.pydata.org/>`_ library.

Usage
=====

1. **Integrated inside the** `simex_platform <https://github.com/eucall-software/simex_platform>`_. A python script named radiationDamageMPI has the same interface as the excutive radiationDamageMPI in the C++ version and could be used in the same way. Therefore simex_platform doesn't need to change.

2. **Calculate diffraction patterns directly from Protein Data Bank (.pdb) file.** See `test_particle.test_calFromPDB()` for more infomation.

