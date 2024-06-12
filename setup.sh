# Deleting previous venv and reinstalling

PYTHON_INTERPRETER=$(which python3)

if [ -z "$PYTHON_INTERPRETER" ]; then
    PYTHON_INTERPRETER=$(which python)
fi

if [ -z "$PYTHON_INTERPRETER" ]; then
    echo "Python interpreter not found"
    echo "Please install Python 3.7 or higher"
    echo "If you have Python 3.7 installed, ensure that it is in your PATH"
    exit 1
fi

rm -rf venv > /dev/null 2>&1
$PYTHON_INTERPRETER -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm