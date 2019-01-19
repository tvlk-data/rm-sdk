**Raring Meerkat Python SDK**

Configuration
--------------

RM-SDK needs RMConfig object during the construction
Please check the RM_SDK.RMConfig class for better understanding

RMConfig object consists of

1. RM_GRAPHQL_API_URL (This variable is required which points to the graphql api)
2. MODEL_UPLOAD_URI (This variable is requries for models files upload)
3. AUTH0_CONFIG 

Installation
-------------

pip install git+https://git@github.com/tvlk-data/rm-sdk.git@{version_no}

You can get the versions from here:

https://github.com/tvlk-data/rm-sdk/releases

Creating Documentation
----------------------


Due to the fact that not all machine have the same specification to build the documentation,
we can use `Makefile` to build a Docker image and use the image to build documentation.


$ make docker-build

$ docker run -it -v $(PWD):/tmp/tmp rm-sdk:latest  bash

$ cd docs

$ make html
