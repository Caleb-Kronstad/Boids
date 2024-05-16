import cx_Freeze as freeze # import cx freeze

executables = [freeze.Executable("main.py")] # executable files
freeze.setup(
    name = "DucksAndBoids",
    options = {"build_exe": { "packages":["pygame","numpy","random","sys","math"],
                              "include_files":[
                                  "resources"
                                  ]}},
    executables = executables
) # setup exe build