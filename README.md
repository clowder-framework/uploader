This container allows you to upload a folder to clowder. The following command will create a dataset with the given n upload all the files and folders in the data folder to the specified dataset. This assumes you run the container on the same machine as clowder.

```
docker run -ti --rm \
  --network clowder_clowder \
  --env CLOWDER_KEY=<yourkey> \
  --env DATASET_NAME=<mydataset>
  --volume ${PWD}/data:/data \
  clowder/uploader
```

You can customize the container using the following variables:
- **CLOWDER_URL** : the url of clowder (without the final /)
- **CLOWDER_KEY** : the key of the user who will own the uploaded files.
- **DATA** : the path of the folder mounted in the container (if no dataset name is given it will use the name of the folder)
- **DATASET_ID** : if given, the files be uploaded to this dataset.
- **DATASET_NAME** : the name of the dataset, this dataset will be created.
- **LINK_PATH** : see below

## LINK_PATH

Instead of uploading the files to clowder, you can tell clowder about files that exist already in a folder visible to clowder. You will need to make sure this folder is mounted inside the container of clowder. Next you run the uploaded with LINK_PATH to be the path inside the clowder container where the files are located. The uploader will now tell clowder about these files and clowder will create entries for them. It will not upload/copy the files. This is useful in the case that you have an external process that created a large folder with files that clowder can see.

## MULTIPLE EXECUTIONS

This program does not check if the dataset already exist and will recreate the dataset. It will also not check to see if the folder and files already exist, and will re-upload them. This script does not mirror the data.


