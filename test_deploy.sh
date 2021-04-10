#!/bin/bash
echo "Update project to version "$1
docker build -f Dockerfile -t enterprise .
#docker build -f Dockerfile-deploy -t project-deploy .
docker tag enterprise:latest rscicomp/cloud-computations:$1
docker push rscicomp/cloud-computations:$1
kubectl run enterprisevmcloud --image=rscicomp-docker-registry/cloud-computations:$1
echo "Done updating project to version "$1
