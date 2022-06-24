import json
import os
import requests
import requests_toolbelt


LINK_PATH=os.getenv("LINK_PATH", "")

CLOWDER_URL=os.getenv("CLOWDER_URL", "http://clowder:9000")
CLOWDER_KEY=os.getenv("CLOWDER_KEY", "r1ek3rs")


# upload a single file to the folder. IF LINK_PATH is set it will just link the file to clowder,
# otherwise it will upload the file to clowder.
def upload_file(dataset_id, folder_id, filepath, basepath):
    filename = os.path.basename(filepath)
    if LINK_PATH:
        clowderpath = filepath.replace(basepath, LINK_PATH)
        data = requests_toolbelt.MultipartEncoder(
            fields={'file': json.dumps({"path": clowderpath})}
        )
    else:
        data = requests_toolbelt.MultipartEncoder(
            fields={'file': (filename, open(filepath, 'rb'))}
        )
    headers = {
        'X-Api-Key': CLOWDER_KEY,
        'Content-Type': data.content_type
    }

    url = f"{CLOWDER_URL}/api/uploadToDataset/{dataset_id}"
    if folder_id:
        url = url + f"?folder_id={folder_id}"
    resp = requests.post(url, data=data, headers=headers)
    resp.raise_for_status()
    return resp.json()['id']


# create a folder in a dataset (potentially as subfolder) and returns the id of the folder.
def create_folder(dataset_id, foldername, folder_id=None):
    headers = {
        'X-Api-Key': CLOWDER_KEY,
        'Content-Type': 'application/json'
    }
    if folder_id:
        data = {
            "name": foldername,
            "parentId": folder_id,
            "parentType": "folder"
        }
    else:
        data = {
            "name": foldername,
            "parentId": dataset_id,
            "parentType": "dataset"
        }
    resp = requests.post(f"{CLOWDER_URL}/api/datasets/{dataset_id}/newFolder",
                         data=json.dumps(data), headers=headers)
    resp.raise_for_status()
    return resp.json()['id']


def create_dataset(name):
    headers = {
        'X-Api-Key': CLOWDER_KEY,
        'Content-Type': 'application/json'
    }
    data = {
        "name": name,
    }
    resp = requests.post(f"{CLOWDER_URL}/api/datasets/createempty", data=json.dumps(data), headers=headers)
    resp.raise_for_status()
    return resp.json()['id']


# upload all files in a folder, and optionally recurse folder
def upload_folder(dataset_id, folder_id, folder, basepath):
    for name in os.listdir(folder):
        filename = os.path.join(folder, name)
        if os.path.isfile(filename):
            upload_file(dataset_id, folder_id, filename, basepath)
        elif os.path.isdir(filename):
            # create folder
            subfolder_id = create_folder(dataset_id, name, folder_id)

            # upload all files in folder
            upload_folder(dataset_id, subfolder_id, filename, basepath)


def main():
    # create dataset if needed
    datafolder = os.getenv("DATA", "/data")
    dataset_id = os.getenv("DATASET_ID")
    if not dataset_id:
        dataset_name = os.getenv("DATASET_NAME")
        if not dataset_name:
            dataset_name = os.path.basename(datafolder)
        dataset_id = create_dataset(dataset_name)

    # loop through root
    upload_folder(dataset_id, None, datafolder, datafolder)

    print(f"{CLOWDER_URL}/datasets/{dataset_id}")


if __name__ == '__main__':
    main()
