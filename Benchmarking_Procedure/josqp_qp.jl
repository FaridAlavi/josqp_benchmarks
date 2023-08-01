using Logging

function run_qps_files()

    org_stdout = stdout;

    listQpProblems = "Benchmarking_Procedure/qp_problem_list.txt";
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
            run(`java -jar ./Benchmarking_Procedure/Bin/josqp.jar $(qpsFilePath)`);
            defLogFileName = "josqp.log";
            dstLogFileName = "./Solvers_Logs/JOSQP/QP/" * "josqp_" * chop(fileName, tail=4) * ".log";
            mv(defLogFileName, dstLogFileName, force=true);
        catch
            println("Error in solving problem " * fileName);
        end
    end

end

run_qps_files();
println("Solving QP problems with JOSQP finished.");