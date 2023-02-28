# Squirtle

## Development

Run `install.sh` to
- Ensure dependencies are installed
- Create virtual environment
- Install doc2json dependencies (`requirements.txt`)
- View instructions on how to run grobid and convert files


## Q&A

Problems users may run into

### Module not installed - bs4

```shell
Traceback (most recent call last):
	File "doc2json/grobid2json/process_pdf.py", line 5, in <module>
	from bs4 import BeautifulSoup
	ModuleNotFoundError: No module named 'bs4'
```

This probably means you are not in the virtual environemnt.
Follow the script instructions to activate the virtual environment before attempting to run.
