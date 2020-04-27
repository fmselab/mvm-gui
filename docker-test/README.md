# How to build and use docker image for MVM gui testing

The goal is to have a software testing environment as similar as possibile to the real one.

The **raspbian** image is based on **debian** \(10.3 at the moment\). 

The production image uses python 3.7 and pacakges provided by the distribution. The *pyyaml* package that comes with debian 10.3 is version 3.13 and cannot be used because it does not implement the method *FullLoader* (present since 5.1). 
To have the same version installed in production it is necessary to rebuild package from debian 11, it is not possibile to simple install it because it depends from python 3.8. To accomplish the rebuild in a coherent way without leaving useless packages into the image the build is made using [multistage method](https://docs.docker.com/develop/develop-images/multistage-build/).

## Creating the image
As reported in docker site [instructions](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/) it's better to create separate directories for dockerfiles and context.

Build the image with the command
```
docker build -t mvm-gui-test -f dockerfiles/Dockerfile context/
```

## Running tests

Download the testing repo 
```
git clone https://github.com/fmselab/mvm-gui.git
```
and run the tests
```
docker run --rm -ti -v $PWD/mvm-gui:/mvm-gui -e MVMGUI_BASEDIR=/mvm-gui -w /mvm-gui/gui mvm-gui-test pytest testfile.py
```

