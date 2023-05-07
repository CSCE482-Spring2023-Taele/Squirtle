# <img src="https://cdn.discordapp.com/attachments/933852328409313280/1093286323592368228/512px-Accessibility.svg.png" alt="logo" width=5% height=5% /> PDFMax Documentation
<img src="https://cdn.discordapp.com/attachments/1071203780294627470/1099894127723814922/image.png"/>

PDFMax is a solution offering an accessible reading experience for PDF users. Tailored for screen-reader users, this app converts a user's PDF file into HTML for a smooth reading experience. The team worked closely with experts to desing and implement features that aim to make PDF use for equitable for our blind users. 

- [Live App](https://pdfaccessibility-squirtle.uc.r.appspot.com)
- [Demo](https://www.youtube.com/watch?v=x_yqM2t75-0)

## Local Setup
- `git clone https://github.com/CSCE482-Spring2023-Taele/Squirtle.git`
- `pip install -r requirements.txt`
- run app with gunicorn using `gunicorn -w 9 --threads 10 flask_app:app`
- OR run app with Python using `python3 flask_app.py`

## User Instructions
- Upload a PDF file on the landing page. Select preference for citation-removal and image sonification. Hit submit. File processing might take >10s depending on file size.

## Code Documentation
### Templates

- [index.html](https://github.com/CSCE482-Spring2023-Taele/Squirtle/blob/master/templates/index.html) : Landing page containing the file upload form.
- [success.html](https://github.com/CSCE482-Spring2023-Taele/Squirtle/blob/master/templates/success.html) : Output page which displays the final HTML to the user.

## Request Handling
### Client requests are handled in [flask_app.py](https://github.com/CSCE482-Spring2023-Taele/Squirtle/blob/master/flask_app.py) inside `def home()`
### Request: 
- POST - Submission of a PDF file along with boolean parameters representing image sonification and citation removal toggle states.
### Responses:  
- 200 - Success. Generated HTML will be displayed to the user.
- 400 - Failed to Extract PDF. Failure caused during request made to the extraction agent. Potential cause - expired credential keys.
- 406 - Inavlid File Format. Occurs when a user uploads anything other than a `.pdf` file.
- 400 - Failed to generate HTML. Internal error occured during the HTML generation process. Might be tied to specific PDF types.
- 400 - Failed to sonify images. Internal error during image sonification. Try again.


## Server-Side Processes

### PDF Extraction Agent

This tool is responsible for extrating text, images, and tables from PDf files. As the first step in our processing pipeline, this process generates the JSON, PNG, and CSV files that are used later down the pipeline. The tool relies on a PDF parser and an Optical Character Recognition (OCR) library. When a user uploads text-based PDFs, the process defaults to the parser to extract information. This maximizes content accuracy. When the PDF is image-based/scanned the process opts for OCR. This helps ensure the app covers all types of PDFs.

#### Request
- GET - Request containing uploaded file and credentials.
#### Response
- 200 - Success. Returns content extracted from PDF in form of JSON, PNGs, and CSVs.
- 400 - Failure. Internal processing error or expired credentials.
### Image Sonification Model

This is an optional stage in our processing pipeline. If selected by the user, this step is responsible for generating sound files for the images present in a PDF. The tool uses fourier transformations to convert each pixel in an image to a sound wave. The result is a sound file that offers insights regarding the image. This tool is specifically designed to help blind users consume image content through sound.

#### Request
- PUT - Request containing path to .PNGs extracted.
#### Response
- 200 - Success. Generated .wav sound files saved to client's storage bucket.
- 400 - Failure. Internal error when generating sound files. 
### Citation Removal Model

This is an optional stage in our processing pipeline. If selected by the user, this model finds and removed in-text citations from text. This results in a smoother reading experience for users with screen-readers. Currently this model classifies and tags MLA, IEEE, and Legal citations.

#### Request
- UPDATE - Request containing extracted JSON.
#### Response
- 200 - Success. Successfuly removed in-text citations in given file.
- 400 - Failure. Internal error when trying to remove citations.
### HTML Generation Model

This is the final stage in our processing pipeline. Given the processed content (JSON, .PNGs, .CSVs, .WAVs) this model generates a fully accessible HTML file. This model preserves a 100% of the PDF content and a 100% of the content flow. The priority during this stage is to make the HTML fully compatible and navigable through a screen-reader.

#### Request
- GET - Request containing path to the extracted PDF content
#### Response
- 200 - Success. Generated HTML returned to the client.
- 400 - Failure. Internal error when parsing content.





