docker build --tag avm:latest .
docker run --rm -v "${PWD}:/opt/avm"  -it avm:latest
