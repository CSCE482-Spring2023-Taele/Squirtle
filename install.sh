#! /bin/bash

SCRIPTNAME="${0##*/}"
REQUIRED_CMDS=("python3" "pip3")
VIRTUAL_DIR="$HOME/.virtualenvs/s2orc-doc2json"

# Add colors to output
source ./colors.sh

warn() {
	cerr "$SCRIPTNAME: $*"
}

iscmd() {
	command -v >&- "$@"
}

checkdeps() {
	local -i not_found=0
	for cmd; do
		if !(iscmd "$cmd"); then
			warn "command \"$cmd\" is not found"
			let not_found++
		fi
	done

	if [ $not_found -ne 0 ]; then
		warn "Install dependencies listed above to use $SCRIPTNAME"
		exit 1;
	fi
}

cout "Checking if python3 and pip3 are installed"
checkdeps "${REQUIRED_CMDS[@]}"

# Create virtual environemnt dir if not exist
python3 -m venv "$VIRTUAL_DIR"

# Install requirements and setup.py
source "$VIRTUAL_DIR/bin/activate"
cd ./s2orc-doc2json
cout "Installing Python dependencies"
pip3 install --quiet --ignore-installed --requirement ./requirements.txt
python3 ./setup.py develop 2>&1 >/dev/null
cd - 2>&1 >/dev/null

cout "Open up another shell and:"
cmd "cd $PWD/s2orc-doc2json/scripts"
cout "If running grobid for the first time:"
cmd "bash ./setup_grobid.sh"
cout "else:"
cmd "bash ./run_grobid.sh"
cout "Then in current shell:"
cmd "cd ./s2orc-doc2json"
cmd "source $VIRTUAL_DIR/bin/activate"
cmd "python3 doc2json/grobid2json/process_pdf.py -i tests/pdf/N18-3011.pdf -t temp/ -o output/"
cout "To deactivate virtual environment, close current shell or:"
cmd "deactivate"
