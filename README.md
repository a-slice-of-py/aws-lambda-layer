# LayLa
LayLa is a simple Python project to initialize a Lambda layer ready for build and deploy via aws-sam.

## Usage
You can use `layla.py` as a standalone script or via the provided Makefile.

Available `make` commands:
- `init`: initialize .layla layer folder
- `build`: build layer via aws-sam
- `deploy`: deploy layer via aws-sam
- `clean`: clean everything built with LayLa

## Configuration
Before exploit the Makefile, you will likely have to change some config variables in `config.mk`.

Available variables:
- _LANGUAGE_, interpreter language (default `python`)
- _SCRIPT_, script to be executed (default `layla.py`)
- _SAM_CMD_, location of aws-sam cmd (default `"C:\Program Files\Amazon\AWSSAMCLI\bin\sam.cmd"`)
- _LAYLA_DIR_, name of the LayLa build directory (default `.layla`)
- _LAYER_NAME_, layer name (default `hello_layla`)
- _CONTENTS_, Python libraries to be included in the layer (default `pandas pyjanitor`)
- _STACK_NAME_, CloudFormation stack name (default `layla-stack`)
- _S3_BUCKET_, s3 bucket in which aws-sam artifacts must be stored (default `layla-bucket`)
- _AWS_REGION_, name of aws region (default `eu-central-1`)

## Dependencies
You need `make` and `aws-sam` to properly exploit LayLa functionalities.

## Authors
* **Silvio Lugaro** - *Advanced Analytics team, Iren S.p.A.*, 2020