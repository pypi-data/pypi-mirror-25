'''
standards.py: standards for the identifiers API

Copyright (c) 2017 Vanessa Sochat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

# Sources (lists) of valid identifiers
identifier_sources = ['stanford','Stanford MRN', 'StanfordMRN']
item_sources = ['pacs','Stanford PACS', 'GE PACS', 'GE PACS Accession Number', 'Lab Result']

# Regular expressions # '1961-07-27T00:00:00Z'
timestamp = '\d{4}-\d{2}-[A-Za-z0-9]{5}:\d{2}:\d{2}Z$'

# Swagger api
spec = "https://app.swaggerhub.com/apiproxy/schema/file/susanweber/UID/1.0.0/swagger.json"

# Valid actions to be taken for deidentification (in dicom/config.json)

valid_actions = ['blanked',    # use API response to code the item. If no response is provided, blank it.
                 'coded',    # blank the response (meaning replace with an empty string)
                 'original', # do not touch the original header value
                 'removed']  # completely remove the field and value from the data/header


