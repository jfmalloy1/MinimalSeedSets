using Distributed

#Parallel setup
addprocs(8)
println("Num Processors ", nprocs())

@everywhere begin
using Pkg
Pkg.activate(".")
using BioXP
#using ProgressMeter
using Random
using JSON

    # using BenchmarkTools
## Master file from ecg (with dgs added from `add_dgs_to_master` .py files)
rstructs_path = "../BioXP/test/data/master_from_redges-og-submission.json"

function MSS(f)
    println(f)
    tids_path = "data/MW/"*f
    tids = readlines(tids_path)
    #Reverse list (to match reverse universality of sid_sets)
    tids = reverse(tids)
    #tids = readkeyedids(targets_path)[tid_name]
    rstructs = readmaster(rstructs_path)
    #print(rstructs)

    #Find rids
    rids = collect(keys(rstructs))
    #print(rids)

    #Find ordered seed sets
    ss_path = "data/MW/"*f
    sid_sets = readlines(ss_path)
    #Reverse the list (least universal as the first seed to be removed)
    sid_sets = reverse(sid_sets)


    #
    # #TEST: Select first 10 compounds from tids and sid_sets
    # tids = tids
    # sid_sets = sid_sets

    write_path = "output/Pmw"*f[4:13]*"/"

    if !ispath(joinpath(write_path))
        mkpath(joinpath(write_path))
    end

    find_minimal_seed_set(rstructs,
        rids,
        sid_sets,
        tids=tids,
        write_path=write_path)


    formatbioxpoutput("output/Pmw"*f[4:13]*"/", "output/Pmw"*f[4:13]*"/")
end
end

function parallel_wrapper(dirs)
    for f in dirs
        MSS(f)
    end
end

println("Molecular Weight MSS")

dirs = readdir("data/MW")
pmap(MSS, dirs[1:9])

# #for f in readdir("data/MW")
# parallel_wrapper(dirs)

#
# println("Universality MSS")
# for f in readdir("data/Universality")
#     MSS(f)
# end
