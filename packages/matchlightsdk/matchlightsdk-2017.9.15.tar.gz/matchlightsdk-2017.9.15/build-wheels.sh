#!/bin/bash
# Adapted from:
# https://raw.githubusercontent.com/sdispater/pendulum/master/build-wheels.sh
PACKAGE_NAME=matchlightsdk
PYTHON_VERSIONS="cp27-cp27m cp35-cp35m"


build_wheels() {
  echo "Compiling wheels"
  for python in ${PYTHON_VERSIONS}; do
      cd /io
      /opt/python/${python}/bin/pip install -r requirements/build.txt
      /opt/python/${python}/bin/python setup.py sdist \
        --dist-dir wheelhouse --formats=gztar
      /opt/python/${python}/bin/pip wheel \
        --no-index --no-deps --wheel-dir wheelhouse wheelhouse/*.tar.gz
      cd -
  done

  echo "Bundling external shared libraries into the wheels"
  for whl in /io/wheelhouse/*.whl; do
      auditwheel repair $whl -w /io/wheelhouse/
  done
}


install() {
  echo "Installing packages and test"
  for python in ${PYTHON_VERSIONS}; do
      /opt/python/${python}/bin/pip install ${PACKAGE_NAME} \
        --no-index -f /io/wheelhouse
      find ./io/tests | grep -E "(__pycache__|\.pyc$)" | xargs rm -rf
      /opt/python/${python}/bin/py.test /io/tests
      find ./io/tests | grep -E "(__pycache__|\.pyc$)" | xargs rm -rf
  done
}


main() {
  build_wheels
  install
}


main "$@"
