# Copyright 2021 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

import logging
import os.path
import tempfile

from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import ExtractPDFOptions
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_renditions_element_type import \
    ExtractRenditionsElementType
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_element_type import ExtractElementType
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.pdfops.extract_pdf_operation import ExtractPDFOperation


logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

class ExtractAPI:
    def __init__(self, pdf_filename, pdf_file_buf_stream):
        self.filename = pdf_filename
        self.buf_stream = pdf_file_buf_stream
    
    def adobe_extract(self):
        try:
            # get base path.
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            #write_path = tempfile.gettempdir()
            # Initial setup, create credentials instance.
            credentials = Credentials.service_account_credentials_builder() \
                .from_file(base_path + "/pdfservices-api-credentials.json") \
                .build()

            # Create an ExecutionContext using credentials and create a new operation instance.
            execution_context = ExecutionContext.create(credentials)
            extract_pdf_operation = ExtractPDFOperation.create_new()

            # Set operation input from a source file.
            #source = FileRef.create_from_local_file(base_path + "/resources/2020.acl-main.207.pdf")
            source = FileRef.create_from_stream(self.buf_stream, 'application/pdf')
            extract_pdf_operation.set_input(source)

            # Build ExtractPDF options and set them into the operation
            extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
                .with_elements_to_extract([ExtractElementType.TEXT, ExtractElementType.TABLES, ]) \
                .with_elements_to_extract_renditions([ExtractRenditionsElementType.TABLES,
                                                    ExtractRenditionsElementType.FIGURES]) \
                .build()
            extract_pdf_operation.set_options(extract_pdf_options)

            # Execute the operation.
            result: FileRef = extract_pdf_operation.execute(execution_context)

            # Save the result to the specified location.
            result.save_as(base_path + '/' + self.filename[:-4] + ".zip")

            return base_path + '/' + self.filename[:-4] + ".zip"
        
        except (ServiceApiException, ServiceUsageException, SdkException):
            logging.exception("Exception encountered while executing operation")
