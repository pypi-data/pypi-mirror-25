import argparse
import json
import glob
import logging
import time
import os
from os.path import dirname, abspath
import rhumbix_csv_uploader.payroll_processor as payroll_processor
import rhumbix_csv_uploader.work_order_processor as work_order_processor
import rhumbix_csv_uploader.job_cost_processor as job_cost_processor


payroll_pattern = "rhumbix_payroll*.csv"
work_order_pattern = "rhumbix_wo*.csv"
job_cost_pattern = "rhumbix_job_cost*.csv"
BATCH_LOOKUP_CYCLE_DELAY_SECONDS = 2
TWO_WEEKS_IN_SECONDS = 2 * 7 * 24 * 60 * 60


def clean_processed_folder(base_path):
    logging.info("Cleaning processed directory of expired files")
    processed_path = os.path.join(base_path, "processed")
    processed_path = os.path.join(processed_path, '')
    if not os.path.exists(processed_path):
        return
    paths = glob.glob("%s%s" % (processed_path, "*.csv"))
    for path in paths:
        if time.time() - os.path.getmtime(path) > TWO_WEEKS_IN_SECONDS:
            logging.info("Removing %s as it has expired", path)
            os.remove(path)


def move_file_to_processed(path):
    if os.path.exists(path):
        parent_path = (dirname(abspath(path)))
        processed_path = os.path.join(parent_path, "processed")
        if not os.path.exists(processed_path):
            # Create the processed directory
            os.makedirs(processed_path)
        processed_path = os.path.join(processed_path, os.path.basename(path))
        if os.path.exists(processed_path):
            logging.warning("Overwriting %s in processed directory!" % processed_path)
        os.rename(path, processed_path)
    else:
        logging.warning("move_file_to_processed received nonexistent file: %s" % path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csvs_directory")
    parser.add_argument('company_key', nargs='?')
    parser.add_argument('api_key', nargs='?')
    args = parser.parse_args()
    if args.company_key is None or args.api_key is None:
        config_dict = json.load(open('config.json'))
        args.company_key = config_dict["company_key"]
        args.api_key = config_dict["api_key"]

    args.csvs_directory = os.path.join(args.csvs_directory, '')

    logging.info("Processing directory %s with company_key=%s and api_key=%s" %
        (args.csvs_directory, args.company_key, args.api_key))

    clean_processed_folder(args.csvs_directory)

    payroll_paths = glob.glob("%s%s" % (args.csvs_directory, payroll_pattern))
    logging.info("Payroll files=%s" % payroll_paths)

    work_order_paths = glob.glob("%s%s" % (args.csvs_directory, work_order_pattern))
    logging.info("Workorder files=%s" % work_order_paths)

    job_cost_paths = glob.glob("%s%s" % (args.csvs_directory, job_cost_pattern))
    logging.info("Job Cost Files=%s" % job_cost_paths)


    payroll_batches = []
    for path in payroll_paths:
        logging.info("Processing payroll file: %s" % path)
        result = payroll_processor.process_csv(path, args.company_key, args.api_key)
        batch_key = result.json()["batch_key"]
        logging.info("Finished file:%s with batch id: %s" % (path, batch_key))
        payroll_batches.append({"path": path, "batch_key": batch_key})

    work_order_batches = []
    for path in work_order_paths:
        logging.info("Proccessing work order file: %s" % path)
        result = work_order_processor.process_csv(path, args.company_key, args.api_key)
        batch_key = result.json()["batch_key"]
        logging.info("Finished file:%s with batch id: %s" % (path, batch_key))
        work_order_batches.append({"path": path, "batch_key": batch_key})

    job_cost_batches = []
    for path in job_cost_paths:
        logging.info("Processing job cost file: %s" % path)
        result = job_cost_processor.process_csv(path, args.company_key, args.api_key)
        batch_key = result.json()["batch_key"]
        logging.info("Finished file:%s with batch id: %s" % (path, batch_key))
        job_cost_batches.append({"path": path, "batch_key": batch_key})

    logging.info("All csv files uploaded. Monitoring batch status...")
    # Wait for all the batches to get done. The [:] makes a temporary copy as the list is mutated
    while len(payroll_batches) + len(work_order_batches) + len(job_cost_batches) > 0:
        for batch in payroll_batches[:]:
            batch_key = batch["batch_key"]
            result = payroll_processor.get_batch_status(batch_key)
            body = result.json()
            logging.info("Batch id %s has status: %d %s" % (batch_key, result.status_code, body["status"]))
            if result.status_code == 200 and body["status"] == "COMPLETE":
                move_file_to_processed(batch["path"])
                payroll_batches.remove(batch)

        for batch in work_order_batches[:]:
            batch_key = batch["batch_key"]
            result = work_order_processor.get_batch_status(batch_key)
            body = result.json()
            logging.info("Batch id %s has status: %d %s" % (batch_key, result.status_code, body["status"]))
            if result.status_code == 200 and body["status"] == "COMPLETE":
                move_file_to_processed(batch["path"])
                work_order_batches.remove(batch)

        for batch in job_cost_batches[:]:
            batch_key = batch["batch_key"]
            result = job_cost_processor.get_batch_status(batch_key)
            body = result.json()
            logging.info("Batch id %s has status: %d %s" % (batch_key, result.status_code, body["status"]))
            if result.status_code == 200 and body["status"] == "COMPLETE":
                move_file_to_processed(batch["path"])
                job_cost_batches.remove(batch)

        time.sleep(BATCH_LOOKUP_CYCLE_DELAY_SECONDS)

    logging.info("All batches have completed processing")


if __name__ == "__main__":
    main()
