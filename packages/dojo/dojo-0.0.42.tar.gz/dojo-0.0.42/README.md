A data framework encapsulating common data warehousing patterns and best practices, including:

 - Defining and scheduling jobs locally, on Google Cloud Dataflow, and on Google Cloud ML Engine
 - Schemas on datasets and integrity of inputs and outputs
 - Versioned datasets in storage, never updated
 - Batch and incremental processing of sources and datasets
 - Dataset dependencies


# Getting started

```
source script/env
script/up
script/test
script/distribute
```

##### Generate your decryption key:

```
dojo encrypt
```
or use a pre-exsiting key:
```
$ export DOJO_DECRYPT_KEY=yourkey
```

##### Run your job

```
dojo run <job_name> --runner cloud --env production
```

```
dojo --help
```