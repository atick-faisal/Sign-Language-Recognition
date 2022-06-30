import sys
import getopt

from typing import List


def parse_args(argv) -> List[str]:
    arg_exp_name = "stack_cnn"
    arg_data_dir = "data/dataset/raw"
    arg_model_dir = "models/"
    arg_help = "{0} -e <exp_name> -d <data_dir> -m <model_dir>".format(argv[0])

    try:
        opts, _ = getopt.getopt(
            argv[1:], "he:d:m:", ["help", "exp_name=", "data_dir=", "model_dir="])
    except:
        print("parsing error!")
        return arg_exp_name, arg_data_dir, arg_model_dir

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)
            sys.exit(2)
        elif opt in ("-e", "--exp_name"):
            arg_exp_name = arg
        elif opt in ("-d", "--data_dir"):
            arg_data_dir = arg
        elif opt in ("-m", "--model_dir"):
            arg_model_dir = arg

    return arg_exp_name, arg_data_dir, arg_model_dir
