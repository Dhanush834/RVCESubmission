import requests  # Server interaction
import time  # Timers for waiting time estimation
import argparse  # Command line switch handling
import json  # Structured data formatting and transfer
import sys

# List of all computationally intensive models. Either manually pick from this list, or specify to use ALL_MODELS directly
ALL_MODELS = ["dili", "cyto", "carcino", "immuno", "mutagen", "nr_ahr", "nr_ar", "nr_ar_lbd", "nr_aromatase", "nr_er", "nr_er_lbd", "nr_ppar_gamma", "sr_are", "sr_hse", "sr_mmp", "sr_p53", "sr_atad5"]

# PROGRAM LOGIC
# ---------------------------------
parser = argparse.ArgumentParser(description="Query the PROTOX API")
parser.add_argument("-t", "--mtype", help="Default: name. specify 'name' (pubchem search using the compound name) or 'smiles' (canonical smiles) as your input data type",
                    type=str, choices=['name', 'smiles'], default="name")
parser.add_argument("-m", "--models", help="Default: acute_tox,tox_targets. specify models and data points to compute. Options are (to be separated by ,): acute_tox,tox_targets and the additional toxicity models dili,cyto,carcino,immuno,mutagen,nr_ahr,nr_ar,nr_ar_lbd,nr_aromatase,nr_er,nr_er_lbd,nr_ppar_gamma,sr_are,sr_hse,sr_mmp,sr_p53 and sr_atad5. You can use all additional models using ALL_MODELS, but be mindful it incurs high calculation times",
                    type=str, default="acute_tox,tox_targets")
parser.add_argument("searchterms", help="The actual strings to search for (comma-separated). May be pubchem name (default) or SMILES (use -t smiles).", type=str)
parser.add_argument("-o", "--outfile", help="Default: results.csv. specify where to output your retrieved data (csv format)",
                    type=str, default="results.csv")
parser.add_argument("-r", "--retry", help="Default: 5. Retry limit to attempt to retrieve data. Increase this in case of large, unpredictable queries",
                    type=int, default=5)
parser.add_argument("-q", "--quiet", help="Suppress all non-error output from the script", action="store_true")

args = parser.parse_args()

input_type = args.mtype
models = args.models.split(',')
searchterms = args.searchterms.split(',')
outfile = args.outfile
retry_limit = args.retry
quiet = args.quiet

try:
    data_file = open(outfile, "w")
except IOError:
    print("Could not open specified outfile")
    sys.exit()

task_id_list = []


def log(msg):
    if not quiet:
        print(msg)


def request_data(inputs):
    log("Enqueing request " + inputs + ", with models :")

    if "ALL_MODELS" in models:
        models.remove("ALL_MODELS")
        models.extend(ALL_MODELS)

    log(models)
    r = requests.post("http://tox.charite.de/protox_II/src/api_enqueue.php", data={'input_type': input_type, 'input': inputs, 'requested_data': json.dumps(models)})  # encode array, the rest are single strings
    if r.status_code == 200:  # Data response

        # Data query response. Add response to our task_id_list
        log("Received qualified response with id")
        task_id_list.append(r.text)  # See if this works.

        # Set up wait time before next query
        if 'Retry-After' in r.headers:
            wait_time = int(r.headers['Retry-After']) + 1  # Wait depending on how long the server thinks it needs
        else:
            wait_time = 10  # Something went wrong with transmission, just wait 10s by default

        log("Waiting for " + str(wait_time) + " s till next request")

        time.sleep(wait_time)

    elif r.status_code == 429:  # Too many requests. Slow down/wait
        log("Server responds: Too many requests. Slowing down query slightly")
        if 'Retry-After' in r.headers:
            wait_time = int(r.headers['Retry-After']) + 1  # Wait depending on how long the server thinks it needs
        else:
            wait_time = 10  # Something went wrong with transmission, just wait 10s by default

        log("Waiting for " + str(wait_time) + " s till next request")
        time.sleep(wait_time)
        # WOULD HAVE TO RE-SUBMIT?

    elif r.status_code == 403:  # Daily quota exceeded. Aborting operation for now.
        data_file.write(",Daily Quota Exceeded")  # Input as well
        print("Daily Quota Exceeded. Terminating process.")
        exit(0)

    else:  # Server gone away or different issues, outputting here
        print("ERROR: Server issue")
        print(r.status_code, r.reason)


for inputs in searchterms:
    request_data(inputs)

# Once done, retrieve data from the server. Repeat queries every 30s until all data has been retrieved. Append to an outfile if given
log("All queries have been enqueued. Starting result retrieval...")
time.sleep(2)

result_objects = []

while task_id_list:  # As long as we still have elements to get:
    response_list = []
    first_response = True
    for task_id in task_id_list:
        log("Asking for " + task_id)
        r = requests.post("http://tox.charite.de/protox_II/src/api_retrieve.php", data={'id': task_id})
        if r.status_code == 200:  # Data response
            if r.text == "":
                print("Warning: Empty response")
            else:
                response_list.append(task_id)
                result_objects.append(json.loads(r.text))
                log("Received queue id: " + task_id + "\n")
        elif r.status_code == 404:  # Not found, not computed or finished yet. Do nothing
            if first_response:
                log("No response yet. Likely cause: computation unfinished (retrying...)")
                print(r.text)
                first_response = False
        else:  # Other codes are not permitted
            print("Unexpected return from server")
            print(r.status_code, r.reason)
            sys.exit()

    task_id_list = [item for item in task_id_list if item not in response_list]  # Remove all found id's
    if task_id_list:
        log("Some queries still pending. Retrying in 30s")
        time.sleep(30)  # Wait 30s before another run if there's still work to do

data_file.write(json.dumps(result_objects))
data_file.close()

print("Completed all operations. Your results are in " + outfile)
