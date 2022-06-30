import sys
import getopt


def parse_args(argv):
    arg_data_dir = "data/dataset/raw"
    arg_model_dir = "models/"
    arg_help = "{0} -d <data_dir> -m <model_dir>".format(argv[0])

    try:
        opts, _ = getopt.getopt(
            argv[1:], "hd:m:", ["help", "data_dir=", "model_dir="])
    except:
        return arg_data_dir, arg_model_dir

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)
            sys.exit(2)
        elif opt in ("-d", "--data_dir"):
            arg_data_dir = arg
        elif opt in ("-m", "--model_dir"):
            arg_model_dir = arg

    return arg_data_dir, arg_model_dir
