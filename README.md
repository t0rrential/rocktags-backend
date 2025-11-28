# rocktags-backend

fastapi + findmy.py backend for rocktags.

## how to use:

### 1. run the image on your own machine

```
docker run -it --name findmy -p 6970:6970 -v findmydata:/mnt/storage findmy:latest
```

## alternatively: run on GCP

### 1. generate files

Before we can deploy the container, we need to get `account.json` and `ani_libs.bin` from a local instance.

Make a new python script in this folder with the following:

```
import asyncio

from _login import get_account_async

STORE_PATH = "account.json"

ANISETTE_SERVER = None

ANISETTE_LIBS_PATH = "ani_libs.bin"

acc = await get_account_async(STORE_PATH, ANISETTE_SERVER, ANISETTE_LIBS_PATH)

await acc.close()
acc.to_json(STORE_PATH)
```

Run this script and log in through the command terminal. `account.json` and `ani_libs.json` should now be in there.

### 2. set up bucket

On GCP, create a new bucket and upload `account.json` and `ani_libs.json`. 

### 3. set up cloud run

Deploy this container to GCP Cloud Run. To set up the service, use these settings:

| Setting               | value |
|-----------------------|-------|
| Container Port        | 6970  |
| Execution Environment | Gen 2 |

You can configure the other settings as you like.

Make sure your Cloud Run service account has access to the bucket, and then mount the bucket as a volume under `/mnt/storage`.

## how to use

rocktags-backend sets up a backend on `0.0.0.0:6970`. 

Send a `POST` request with the following in the json body:

```
{
  "trackers": [
    {
      "name": {name of tracker},
      "privateKey": {tracker private key}
    }
  ]
}

```

Note that `trackers` is an array of the `name` and `privateKey` fields.

The response will look like this:

```
{
    {tracker name}: {
        "latitude": int,
        "longitude": int,
        "timestamp": iso format,
        "status": int
    }
}
```