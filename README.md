# PDF-Text-Extraction


1.0 General Description
The data boom and mass digital-sensitization post the late 2010s brought with it an imminent need to digitize data and make it readily accessible to businesses and organizations. Today, access to data in electronic form is critical to a business' workflow. Although most businesses have switched to an online model of data extraction, there is a massive chunk who haven't. There is also the task of digitizing old archival data in the form of physical invoices, bills and other paperwork. In most mid to small scale organizations, this task is being done manually, with a human typing relevant data into the system. Data extraction engines do exist which extract text from image data, but most of them do not possess a method to parse the same into a structured and usable format.

The objective of this project is to create a data extraction platform for users to conveniently obtain data in a structured format from uploaded files (mainly invoices, bills and other documents). The user would be required to upload a scanned pdf(s) of a document to the platform. Ideally, the platform would process the uploaded document, mark regions of interest in the processed file and then proceed to extract text from it using an OCR (Optical Character Recognition) Engine. Finally, it would parse the extracted text to structure the data into a JSON file, which would be sent back to the user to download.

1.1 How the program is structured:
The front-end is the interface through which the user uploads the pdf document(s) and then post-extraction, downloads the JSON file for the same.
Once the documents are uploaded to the server, the program which inculcates the use of parallelism, creates a child process for each file uploaded and proceeds.
Each document is converted to a set of images and this set is then iterated over to pre-process the image. Pre-processing the image reduces it to a more manageable size, converts the image to grayscale and applies filters to reduce noise and detect edges in the image.
Each of the processed images are then passed through a contour detection script to detect regions of interest in the image.
Each detected region of interest is then iterated over and made to undergo the text extraction process through the OCR Engine.
This returns a .txt file of all extracted text which is then sent over to the parsing code segment
The text file is then parsed using regular expressions which returns all the pre defined keys with their values parsed using the program.
The key value pairs are subsequently formatted into a JSON object and sent over to the API.


<h5>To understand better read the Documentation






