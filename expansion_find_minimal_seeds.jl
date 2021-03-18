import Pkg
Pkg.activate("/Users/John/Lab/BioXP")

#] add ProgressMeter

using BioXP
using ProgressMeter
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

    write_path = "output/mw"*f[4:13]*"/"

    if !ispath(joinpath(write_path))
        mkpath(joinpath(write_path))
    end

    find_minimal_seed_set(rstructs,
        rids,
        sid_sets,
        tids=tids,
        write_path=write_path)


    formatbioxpoutput("output/mw"*f[4:13]*"/", "output/mw"*f[4:13]*"/")
end

println("Molecular Weight MSS")
for f in readdir("data/MW")
    MSS(f)
end

println("Universality MSS")
for f in readdir("data/Universality")
    MSS(f)
end
