#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the results in Weights & Biases
"""
import argparse
import logging
import wandb
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):
    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################

    # Download input artifact
    logging.info("Downloading raw data.")
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    data = pd.read_csv(artifact_local_path)

    # Drop outliers
    logging.info(f"Filtering observation within ({args.min_price}, {args.max_price}) price interval")
    idx = data['price'].between(args.min_price, args.max_price)
    data = data[idx].copy()

    # Convert last_review to datetime
    logging.info("Converting last_review column value to datetime type")
    data['last_review'] = pd.to_datetime(data['last_review'])

    # Saving data to local file
    logging.info("Saving clean data to local file")
    data.to_csv("clean_sample.csv", index=False)

    # Upload cleaned data to WnB
    logging.info("Upload artifact with cleaned dataset")
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        desctiption=args.output_desctiption,
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This steps cleans the data")

    parser.add_argument(
        "--input_artifact",
        type=str,  ## INSERT TYPE HERE: str, float or int,
        help="raw data set",  ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_artifact",
        type=str,  ## INSERT TYPE HERE: str, float or int,
        help="Cleaned dataset",  ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_type",
        type=str,  ## INSERT TYPE HERE: str, float or int,
        help="type of output airtifact",  ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,  ## INSERT TYPE HERE: str, float or int,
        help="Description of cleaned data artifact",  ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,  ## INSERT TYPE HERE: str, float or int,
        help="Minimum price",  ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,  ## INSERT TYPE HERE: str, float or int,
        help="Maximum price",  ## INSERT DESCRIPTION HERE,
        required=True
    )

    args = parser.parse_args()

    go(args)
