        # Item custom fields
        for cf in item_cfs:
            if "custom_fields" not in new_item:
                new_item['custom_fields'] = []

            # Is the item defined in the data?
            if cf in item:

                # Only continue if it's defined
                if item[cf] not in ['',None]:    

                    # Add to list of custom fields if haven't seen VALUE yet
                    do_add = True
                    if cf in seen: 
                        if item[cf] in seen[cf]:
                            do_add = False
                    else:
                        seen[cf] = []                    

                    if do_add is True:               
                        new_item['custom_fields'].append({'key': cf, 
                                                          'value': item[cf] })
                        seen[cf].append(item[cf])
 

OriginalAttributesSequence: [(0400, 0550)  Modified Attributes Sequence   1 item(s) ---- 

(0400, 0563) Modifying System                    LO: 'LAITEK'
(0400, 0564) Source of Previous Values           LO: 'SOURCE PACS'
(0400, 0565) Reason for the Attribute Modificati CS: 'CORRECT'
(0400, 0550)  Modified Attributes Sequence   1 item(s) ---- 
   (0010, 0010) Patient's Name                      PN: 'Xxxxxxxxxxxxx'
   ---------
(0400, 0562) Attribute Modification DateTime     DT: '20170114111221'
(0400, 0563) Modifying System                    LO: 'LAITEK'
(0400, 0564) Source of Previous Values           LO: 'SOURCE PACS'
(0400, 0565) Reason for the Attribute Modificati CS: 'CORRECT'(0400, 0550)  Modified Attributes Sequence   1 item(s) ---- 
   (0010, 0020) Patient ID                          LO: 'Xxxxxxxxxxxx'
   ---------
(0400, 0562) Attribute Modification DateTime     DT: '20170114111221'
(0400, 0563) Modifying System                    LO: 'LAITEK'
(0400, 0564) Source of Previous Values           LO: 'SOURCE PACS'
(0400, 0565) Reason for the Attribute Modificati CS: 'CORRECT']


(0032, 1064)  Requested Procedure Code Sequence   1 item(s) ---- 
   (0008, 0100) Code Value                          LO: 'DXCH1P'
   (0008, 0102) Coding Scheme Designator            SH: 'AGFA'
   (0008, 0103) Coding Scheme Version               SH: '1'

SOPClassUID: Grayscale Softcopy Presentation State Storage
StationName: suhpla155
StudyDescription: CHEST 1 VIEW PORTABLE

>>> dcm.__dict__
{'file_meta': (0002, 0000) File Meta Information Group Length  UL: 220
(0002, 0001) File Meta Information Version       OB: b'\x00\x01'
(0002, 0002) Media Storage SOP Class UID         UI: Grayscale Softcopy Presentation State Storage
(0002, 0003) Media Storage SOP Instance UID      UI: 1.2.840.113619.2.201.17165130155.8082.1206391107751.2.315
(0002, 0010) Transfer Syntax UID                 UI: Explicit VR Little Endian
(0002, 0012) Implementation Class UID            UI: 1.3.6.1.4.1.29565.0.3.6.2
(0002, 0013) Implementation Version Name         SH: 'DCMSYS_RTR_362'
(0002, 0016) Source Application Entity Title     AE: 'SHC_ARCHIVE', '_pixel_array': None, '_parent_encoding': 'iso8859', 'is_little_endian': True, 'fileobj_type': <built-in function open>, 'preamble': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', 'timestamp': 1504138594.712588, '_pixel_id': None, 'filename': '/data/2175270/1.2.840.113619.2.201.17165130155.8082.1206391107751.2.315', 'is_implicit_VR': False}

>>> bytes2hex(preamble)
'00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'


