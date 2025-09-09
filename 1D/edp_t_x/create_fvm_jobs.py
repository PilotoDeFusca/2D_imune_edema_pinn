import argparse
import os
from parametros_maquina import *



parser = argparse.ArgumentParser(description="", add_help=False)
parser = argparse.ArgumentParser()
parser.add_argument(
    "-n",
    "--n_iterations",
    type=int,
    action="store",
    dest="n_iterations",
    required=True,
    default=None,
    help="",
)
parser.add_argument(
    "-m",
    "--mode",
    type=str,
    action="store",
    dest="mode",
    required=True,
    default=None,
    help="",
)


def add_line(line, out, line_break=True):
    # Open the file in append & read mode ('a+')

    with open(out, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)

        # If file is not empty then append '\n'
        data = file_object.read(100)

        if len(data) > 0 and line_break:
            file_object.write("\n")

        # Append text at the end of file
        file_object.write(line)


def write_setup():
    if os.path.exists("jobs/fvm_comp.job"):
        os.remove("jobs/fvm_comp.job")

    else:
        print("The fvm job does not exist")

    add_line("#!/bin/bash", "jobs/fvm_comp.job")
    add_line(
        "#----------------------------------------------------------",
        "jobs/fvm_comp.job",
    )
    add_line("# Job name", "jobs/fvm_comp.job")
    add_line(
        "#PBS -N fvm_comp",
        "jobs/fvm_comp.job",
    )
    add_line(
        "#PBS -e error_files/fvm_comp.e",
        "jobs/fvm_comp.job",
    )
    add_line(
        "#PBS -o output_files/fvm_comp.o",
        "jobs/fvm_comp.job",
    )
    add_line(
        f"# Run time (hh:mm:ss) - {tempo_execução}",
        "jobs/fvm_comp.job",
    )
    add_line(
        f"#PBS -l walltime={tempo_execução}",
        "jobs/fvm_comp.job",
    )
    add_line(
        "#----------------------------------------------------------",
        "jobs/fvm_comp.job",
    )
    add_line(
        f"#PBS -l nodes=compute-{maquina}:ppn={numero_nucleos}",
        "jobs/fvm_comp.job",
    )
    add_line(
        "# Change to submission directory",
        "jobs/fvm_comp.job",
    )
    add_line(
        "cd $PBS_O_WORKDIR",
        "jobs/fvm_comp.job",
    )
    add_line(
        "cat $PBS_NODEFILE",
        "jobs/fvm_comp.job",
    )
    add_line(
        "# Launch Thiago-based executable",
        "jobs/fvm_comp.job",
    )
    add_line(
        f"export CUDA_VISIBLE_DEVICES={gpu_id}",
        "jobs/fvm_comp.job",
    )


if __name__ == "__main__":

    args = parser.parse_args()

    args_dict = vars(args)

    mode = args_dict["mode"]

    n_iterations = args_dict["n_iterations"]

    write_setup()

    if mode == "parallel":

        for i in range(n_iterations):

            if i != 0 and (i % len(v_gpu) == len(v_gpu) - 1 or i == n_iterations - 1):
                add_line(
                    "export CUDA_VISIBLE_DEVICES="
                    + v_gpu[i % len(v_gpu)]
                    + " && ~/../thiago.esterci/.conda/envs/torch-numba-11/bin/python3 fvm_comparison.py;",
                    "jobs/fvm_comp.job",
                )

            else:
                add_line(
                    "export CUDA_VISIBLE_DEVICES="
                    + v_gpu[i % len(v_gpu)]
                    + " && ~/../thiago.esterci/.conda/envs/torch-numba-11/bin/python3 fvm_comparison.py & ",
                    "jobs/fvm_comp.job",
                )

    elif mode == "serial":

        for i in range(n_iterations):
            add_line(
                "~/../thiago.esterci/.conda/envs/torch-numba-11/bin/python3 fvm_comparison.py;",
                "jobs/fvm_comp.job",
            )

    else:
        print("This mode was not implemented")
