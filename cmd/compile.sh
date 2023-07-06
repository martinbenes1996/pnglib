
# remove previous releases
rm -rf build/ dist/ pnglib.egg-info/ __pycache__/
rm -rf pnglib/cpnglib/*.so

# compile
python setup.py bdist --verbose
retVal=$?
if [ $retVal -ne 0 ]; then
    exit $retVal
fi

# get dynamic libs
cp $(find build/lib* -maxdepth 0)/pnglib/cpnglib/*.so pnglib/cpnglib/

python run.py
