#! /bin/bash

SCRIPTNAME="${0##*/}"
REQUIRED_CMDS=("python3" "pip3")
VIRTUAL_DIR="$HOME/.virtualenvs/s2orc-doc2json"

# Add colors to output
source ./colors.sh

warn() {
	#cout >&2 "$SCRIPTNAME: $*"
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

cout "Preparing environment for doc2json"
checkdeps "${REQUIRED_CMDS[@]}"

# Create virtual environemnt dir if not exist
python3 -m venv "$VIRTUAL_DIR"

# Install requirements and setup.py
source "$VIRTUAL_DIR/bin/activate"
cd ./s2orc-doc2json
pip3 install -r ./requirements.txt
python3 ./setup.py develop

cout "Open up another shell and:"
cmd "cd $HOME/Squirtle/s2orc-doc2json/scripts"
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
