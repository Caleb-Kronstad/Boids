import cx_Freeze as freeze # import cx freeze

executables = [freeze.Executable("main.py")] # executable files
freeze.setup(
    name = "DucksAndBoids",
    options = {"build_exe": { "packages":["pygame","numpy","random","sys","math"],
                              "include_files":[
                                  "resources/blue_arrow.png",
                                  "resources/circle_15px.png",
                                  "resources/circle_50px.png",
                                  "resources/ducky_large.png",
                                  "resources/ducky_medium.png",
                                  "resources/ducky_small.png",
                                  "resources/moving_water.png",
                                  "resources/walls.png",
                                  "resources/yellow_arrow.png"
                                  ]}},
    executables = executables
) # setup exe build