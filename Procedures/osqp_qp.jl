using QPSReader
using Logging
using OSQP
using SparseArrays
using LinearAlgebra

function run_qps_files()

    org_stdout = stdout;

    listQpProblems = "Procedures/qp_problem_list.txt";
    fileNames = readlines(listQpProblems);
    qps_dir = "QP_Problems/";;
    for fileName in fileNames
        # skipping the comments
        if fileName[1] == '*'
            continue;
        end
        # only for QPS files
        if split(fileName, '.')[end] != "qps"
            continue;
        end

        # redirecting the stdout to a log file
        qpsTestName = fileName[1:length(fileName)-4];
        println("qpsTestName = ", qpsTestName);
        logfile = open("Solvers_Logs/OSQP/QP/" * "osqp_" * qpsTestName * ".log", "w");
        redirect_stdio(stdout=logfile);

        # reading the QPS file
        qpsFilePath = qps_dir * fileName;
        qps = readqps(qpsFilePath);

        # OSQP accepts the QP problems with the following format:
        # min/max    q'x + x'Qx
        # s.t.       l <= Ax <= u
        q = qps.c;
        P = sparse(qps.qcols, qps.qrows, qps.qvals, qps.nvar, qps.nvar);
        l = [qps.lcon; qps.lvar];
        u = [qps.ucon; qps.uvar];
        Acon = sparse(qps.arows, qps.acols, qps.avals, qps.ncon, qps.nvar);
        A = [Acon; sparse(Matrix(1.0I, qps.nvar, qps.nvar))];

        # passing the problem to OSQP
        model = OSQP.Model();
        OSQP.setup!(model; P=P, q=q, A=A, l=l, u=u);
        results = OSQP.solve!(model);

        # closing the log file
        Base.Libc.flush_cstdio();
        redirect_stdio(stdout=org_stdout);
        close(logfile);
    end

end

run_qps_files();
println("Returned to main function.");