import logging
import yaml
from baselines import datasets
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

NON_DATASETS = set(["base"])
def find_available_datasets():
    return [func for func in dir(datasets)
            if not func.startswith("__") and not func in NON_DATASETS]

def main():
    logging.lastResort.setLevel(logging.INFO)
    logging.lastResort.setFormatter(logging.Formatter(
        '[%(levelname)s]\t%(asctime)s.%(msecs)dZ\t'
        '%(filename)s:%(funcName)s:%(lineno)d\t%(message)s',
        '%Y-%m-%dT%H:%M:%S'
    ))

    available_datasets = find_available_datasets()
    parser = ArgumentParser(
        description="Prepare datasets for experiments.",
        formatter_class=ArgumentDefaultsHelpFormatter
        )
    parser.add_argument("dataset_name", help="dataset name",
                        choices=available_datasets)
    parser.add_argument("output_dirpath", help="filepath to the directory containing jsonl files.")
    parser.add_argument("--config", default="config.yaml", help="filepath to the conf file (YAML).")
    args = parser.parse_args()

    with open(args.config) as yml:
        config = yaml.safe_load(yml)
    config = config["datasets"][args.dataset_name]
    dataset = getattr(datasets, args.dataset_name)(config)
    dataset.prepare(args)


if __name__ == '__main__':
    main()