# Setup instructions

- create virtualenv
  path/to/python3.6virtualenv .
- install the requirements
  ./bin/pip install -r requirements.txt
  ./bin/pip install -e src/onna.canonical

(you'll need to manually install guillotina_ttw this way...)

# or, buildout install

Buildout will work with guillotina_ttw automatically

- install buildout:
  ./bin/pip install zc.buildout

- then run buildout:
  ./bin/buildout

# to run

When the project was based on `plone.server`, the `pserver` command was used.
That command has changed to `g` or `guillotina`.

An example command would be::

  ./bin/g -c config-stage.json


# Troubleshooting

## elasticsearch docker not running in jenkins

Run this command to fix the jenkins setup to make it work:
  for i in $(gcloud compute instances list | awk '/gke-jenkins/ {print $1}') ; do gcloud compute ssh $i -- "sudo sysctl -w vm.max_map_count=262144"; done



# Run cloud storage tests


## gcloud

Uses environ variables to specific private info to be able to do test::

    GCLOUD_CREDENTIALS=Intra-3863b7170883-storage.json \
    GCLOUD_BUCKET=storage-dev.atlasense.com \
    GCLOUD_PROJECT=graceful-earth-112011 \
    ./bin/pytest libsrc/guillotina_gcloudstorage/guillotina_gcloudstorage


## s3

    S3CLOUD_BUCKET=stage-kops-onnaplatform-com-state-store \
    S3CLOUD_ID=AKIAJC6ION7GHD32QLEQ \
    S3CLOUD_SECRET=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 \
    ./bin/pytest libsrc/guillotina_s3storage/guillotina_s3storage



# Running Molotov stress tests

If you want to use statsd: http://molotov.readthedocs.io/en/latest/installation/

To run statsd with docker: `make run-statsd`

Then, just run molotov like you normally would::

    ./bin/molotov molotov.py -w 5 -d 15  -x -c -v --statsd


# Enterprise labels

Enterprise labels on resource data is used to help the machine learning engine
properly train on data.

You create labels and labels set in the admin dashboard.

Then, use the `@alllabels` endpoint to get all your labels and uuids.

Finally, when creating your Resource, provide the labels with your payload like::

    "onna.canonical.behaviors.machine_learning.IMachineLearning": {
      "labels": [{
        "label": "<uid of label>",
        "proba": 1,
        "type": "enterprise",
        "confirmed": true
      }]
    }
