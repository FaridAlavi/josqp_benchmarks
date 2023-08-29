# JOSQP Benchmarking

This repository has been created to conduct a benchmark assessing the performance of the solver JOSQP in comparison to two other solvers, namely OSQP and Gurobi.

In our study, we consider two sets of QP problems:

1. [Maros-Meszaros](http://old.sztaki.hu/~meszaros/public_ftp/qpdata/) problem set
2. [QPLIB](https://qplib.zib.de/) problem set

## Running the Benchmark Problems

### Prerequisites

To run the benchmark problems on your local computer, ensure you have the following prerequisites in place:
* Gurobi must be installed with a valid license. Confirm that the command `gurobi_cl` is recognized in your terminal.
* Local installation of OSQP is required.
* Place the JAR file of the JOSQP solver in the `Procedures/bin` directory. Ensure the JAR file is named `josqp.jar`.
* Install Python 3 and Julia.

### Procedure

1. Unzip all the QP problems in the folder ```QP_Problems```.
2. Uncomment your targeted QP problems in ```Procedures/qp_problem_list.txt```. In that file, any line starting with a * is commented out.
3. Execute ```grb_qp.jl``` to solve the targeted problems with Gurobi.
4. Execute ```osqp_qp.jl``` to solve the targeted problems with OSQP.
5. Execute ```josqp_qp.jl``` to solve the targeted problems with JOSQP.

Please note that while performing the aforementioned procedures, your current working directory should be the parent directory of the `Procedures` folder.

6. Execute `analyzer.py` to generate a report of the outcomes. The report will be saved in `Results/report.txt`.

You can review individual log files in the `Solvers_Logs` directory.

## Results

### Maros-Meszaros Problem Set

[This table](/Results/report_MarosMeszaros.txt) table summarizes the results of Maros-Meszaros problem set. For the problems that could be solved correctly by all three solvers, the [shifted geometric mean](https://plato.asu.edu/ftp/shgeom.html) is as follows:

|                         | Gurobi | OSQP  | JOSQP |
| :---                    | :---:  | :---: | :---: |
| Arithmetic mean         | 0.28   | 3.59  | 1.74  |
| Shifted geometric mean  | 1.00   | 3.57  | 3.47  |

### QPLIB problem set

Within the QPLIB problem set, a subset of problems meets the requirements of the OSQP and JOSQP solvers (convex and quadratic cost function, linear constraints, and continuous variables). This table summarizes the outcomes for this specific subset. For problems successfully solved by all three solvers, the shifted geometric mean is as follows:

Within the QPLIB problem set, a subset of problems meets the requirements of the OSQP and JOSQP solvers (convex and quadratic cost function, linear constraints, and continuous variables). [This table](/Results/report_QPLIB.txt) summerized the outcomes for this specific subset. For the problems that could be solved correctly by all three solvers, the shifted geometric mean is as follows:

|                         | Gurobi | OSQP  | JOSQP |
| :---                    | :---:  | :---: | :---: |
| Arithmetic mean         | 4.86   | 7.09  | 3.92  |
| Shifted geometric mean  | 1.17   | 1.47  | 1.00  |

## Remarks

The formats of the following files have been updated to adhere to standard conventions:

* qforplan.qps -> Spaces in variable names have been replaced with underscores.
* qgfrdxpn.qps -> Bound names have been added.
* values.qps -> Bound names have been added.
* exdata.qps -> Bound names have been added.
