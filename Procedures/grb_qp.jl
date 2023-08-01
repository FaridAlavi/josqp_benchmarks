using QPSReader
using Logging
using OSQP
using SparseArrays
using LinearAlgebra

function run_qps_files()

    org_stdout = stdout;

    listQpProblems = "Procedures/qp_problem_list.txt";
    fileNames = readlines(listQpProblems);
    qps_dir = "QP_Problems/";

    for fileName in fileNames
        # skipping the comments
        if fileName[1] == '*'
            continue;
        end
        # only for QPS files
        if split(fileName, '.')[end] != "qps"
            continue;
        end
        # info
        print("Solving problem " * fileName * "... ");
        
        try
            # solving the problem of the QPS file
            qpsFilePath = qps_dir * fileName;
            run(`gurobi_cl $(qpsFilePath)`);
            defLogFileName = "gurobi.log";
            dstLogFileName = "Solvers_Logs/Gurobi/QP/" * "grb_" * chop(fileName, tail=4) * ".log";
            mv(defLogFileName, dstLogFileName, force=true);
        catch
            println("Error in solving problem " * "fileName");
        end
    end

end

run_qps_files();
println("Solving QP problems with Gurobi finished.");