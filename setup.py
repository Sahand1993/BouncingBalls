import cx_Freeze

executables = [cx_Freeze.Executable("visual.py")]

cx_Freeze.setup(
    name="BouncingBalls",
    options={"build_exe": {"packages":["pygame", "numpy"]}},
    executables = executables

    )