import subprocess
import os
import shutil



# HELPER: ARCHIVE ONLY IMPORTANT RESULT FILES

def archive_selected_files(wfn_file, source_dir, analysis_type, allowed_files):
    """
    Copy only selected result files into a system-named archive folder.

    Example:
        Cu_dimer.fchk →
        Cu_dimer/QTAIM/
        Cu_dimer/NCI/
    """
    base_path = os.path.dirname(wfn_file)
    system_name = os.path.splitext(os.path.basename(wfn_file))[0]

    archive_dir = os.path.join(base_path, system_name, analysis_type)
    os.makedirs(archive_dir, exist_ok=True)

    for fname in allowed_files:
        src = os.path.join(source_dir, fname)
        if os.path.isfile(src):
            shutil.copy2(src, os.path.join(archive_dir, fname))



# QTAIM ANALYSIS

def run_qtaim(wfn_file):
    """
    Run QTAIM analysis using Multiwfn 3.7
    """

    multiwfn_exe = r"C:\Users\hp\OneDrive\Desktop\Multiwfn_3.7_bin_Win64\Multiwfn.exe"

    workdir = os.path.join(os.path.dirname(wfn_file), "QTAIM_Output")
    os.makedirs(workdir, exist_ok=True)

    qtaim_input = (
        "2\n"
        "2\n"
        "3\n"
        "4\n"
        "5\n"
        "8\n"
        "-4\n"
        "6\n"
        "0\n"
        "-5\n"
        "6\n"
        "0\n"
        "7\n"
        "-1\n"
        "-10\n"
        "100\n"
        "2\n"
        "1\n"
        "mol.pdb\n"
    )

    inp_file = os.path.join(workdir, "qtaim.inp")
    with open(inp_file, "w") as f:
        f.write(qtaim_input)

    log_file = os.path.join(workdir, "multiwfn_qtaim.log")

    with open(inp_file, "r") as inp, open(log_file, "w") as log:
        subprocess.run(
            [multiwfn_exe, wfn_file],
            stdin=inp,
            stdout=log,
            stderr=log,
            cwd=workdir
        )

    # Archive scientifically important QTAIM results
    archive_selected_files(
        wfn_file,
        workdir,
        "QTAIM",
        allowed_files=[
            "mol.pdb",
            "paths.pdb",
            "CPs.pdb",
            "CPprop.txt"
        ]
    )

    return workdir



# NCI + RDG ANALYSIS (CLASSIC)

def run_nci(wfn_file):
    """
    Run classic NCI analysis using Multiwfn 3.7.

    Output files (Multiwfn default):
      - func1.cub
      - func2.cub
      - Output.txt
    """

    multiwfn_exe = r"C:\Users\hp\OneDrive\Desktop\Multiwfn_3.7_bin_Win64\Multiwfn.exe"

    workdir = os.path.join(os.path.dirname(wfn_file), "NCI_Output")
    os.makedirs(workdir, exist_ok=True)

    nci_input = (
        "20\n"
        "1\n"
        "2\n"
        "2\n"
        "3\n"
        "q\n"
    )

    inp_file = os.path.join(workdir, "nci.inp")
    with open(inp_file, "w") as f:
        f.write(nci_input)

    log_file = os.path.join(workdir, "multiwfn_nci.log")

    with open(inp_file, "r") as inp, open(log_file, "w") as log:
        subprocess.run(
            [multiwfn_exe, wfn_file],
            stdin=inp,
            stdout=log,
            stderr=log,
            cwd=workdir
        )

    # Archive scientifically important NCI results
    archive_selected_files(
        wfn_file,
        workdir,
        "NCI",
        allowed_files=[
            "func1.cub",
            "func2.cub",
            "Output.txt"
        ]
    )

    return workdir
