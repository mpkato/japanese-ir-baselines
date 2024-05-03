from baselines import datasets
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def find_available_datasets():
    return [func for func in dir(datasets)
            if not func.startswith("__")]

def main():
    available_datasets = find_available_datasets()
    parser = ArgumentParser(
        description="Prepare datasets for experiments.",
        formatter_class=ArgumentDefaultsHelpFormatter
        )
    parser.add_argument("dataset_name", help="dataset name",
                        choices=available_datasets)
    parser.add_argument("output_dirpath", help="filepath to the directory containing jsonl files.")
    args = parser.parse_args()

    getattr(datasets, args.dataset_name)(args)

if __name__ == '__main__':
    main()