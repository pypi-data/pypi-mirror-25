#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
"""
sfftk.notes.edit

Copyright 2017 EMBL - European Bioinformatics Institute
Licensed under the Apache License, Version 2.0 (the "License"); 
you may not use this file except in compliance with the License. 
You may obtain a copy of the License at 

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an 
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, 
either express or implied. 

See the License for the specific language governing permissions 
and limitations under the License.
"""



from collections import namedtuple
import re
import shlex
import shutil
import sys, os

import h5py

from .. import schema
from ..core.configs import get_configs
from ..core.parser import parse_args
from ..core.print_tools import print_date
from ..notes.view import HeaderView, NoteView
from ..sff import handle_convert

"""
:TODO: allow user to modify/view hierarchy through segmentation annotation toolkit 
"""

configs = get_configs()

    
__author__ = "Paul K. Korir, PhD"
__email__ = "pkorir@ebi.ac.uk, paul.korir@gmail.com"
__date__ = "2017-04-07"


# externalReference
ExternalReference = namedtuple('ExternalReference', ['type', 'otherType', 'value'], verbose=False)


class NoteAttr(object):
    def __init__(self, initval=None, name='var'):
        self.val = initval
        self.name = name
    def __get__(self, obj, _):
        return self.val
    def __set__(self, obj, val):
        self.val = val
        

"""
:TODO: attribute type checking
"""
class BaseNote(object):
    """Note base class"""
    def __init__(self):
        self._extRefList = list()
    
    @property
    def externalReferences(self):
        return self._extRefList
    
    @externalReferences.setter
    def externalReferences(self, value):
        for v in value:
            self._extRefList.append(v)


class AbstractGlobalNote(BaseNote):
    """GlobalNote 'abstract' class that defines private attributes and methods"""
    name = NoteAttr('name')
    softwareName = NoteAttr('softwareName')
    softwareVersion = NoteAttr('sofwareVersion')
    softwareProcessingDetails = NoteAttr('softwareProcessingDetails')
    filePath = NoteAttr('filePath')
    details = NoteAttr('details')
    externalReferenceId = NoteAttr('externalReferenceId')
    
    def add_to_segmentation(self, segmentation):
        """Add attributes to a segmentation
        
        :param segmentation: an EMDB-SFF segmentation
        :type segmentation: ``sfftk.schema.SFFSegmentation``
        :return segmentation: an EMDB-SFF segmentation
        :rtype segmentation: ``sfftk.schema.SFFSegmentation``
        """
        # name
        if self.name is not None:
            segmentation.name = self.name
        # software name
        if self.softwareName is not None:
            segmentation.software.name = self.softwareName
        # software version
        if self.softwareVersion is not None:
            segmentation.software.version = self.softwareVersion
        # software processing details
        if self.softwareProcessingDetails is not None:
            segmentation.software.processingDetails = self.softwareProcessingDetails
        # file path
        if self.filePath is not None:
            segmentation.filePath = self.filePath
        # details
        if self.details is not None:
            segmentation.details = self.details
        # global external references
        if self.externalReferences:
            if not segmentation.globalExternalReferences:
                segmentation.globalExternalReferences = schema.SFFGlobalExternalReferences()
            for gExtRef in self.externalReferences:
                segmentation.globalExternalReferences.add_externalReference(
                    schema.SFFExternalReference(
                        type=gExtRef.type,
                        otherType=gExtRef.otherType,
                        value=gExtRef.value,
                        )
                    )
        return segmentation

    def edit_in_segmentation(self, segmentation):
        """Edit attributes in a segmentation
        
        :param segmentation: an EMDB-SFF segmentation
        :type segmentation: ``sfftk.schema.SFFSegmentation``
        :return segmentation: an EMDB-SFF segmentation
        :rtype segmentation: ``sfftk.schema.SFFSegmentation``
        """
        # name
        if self.name is not None:
            segmentation.name = self.name
        # software name
        if self.softwareName is not None:
            segmentation.software.name = self.softwareName
        # software version
        if self.softwareVersion is not None:
            segmentation.software.version = self.softwareVersion
        # software processing details
        if self.softwareProcessingDetails is not None:
            segmentation.software.processingDetails = self.softwareProcessingDetails
        # file path
        if self.filePath is not None:
            segmentation.filePath = self.filePath
        # details
        if self.details is not None:
            segmentation.details = self.details
        # external references
        if not segmentation.globalExternalReferences:
            segmentation.globalExternalReferences = schema.SFFGlobalExternalReferences()
        start_index = self.externalReferenceId
        # first replace
        # then insert any additional
        replaced = False
        for gExtRef in self.externalReferences:
            # replace
            if not replaced and segmentation.globalExternalReferences:
                segmentation.globalExternalReferences.replace_externalReference(
                    schema.SFFExternalReference(
                        type=gExtRef.type,
                        otherType=gExtRef.otherType,
                        value=gExtRef.value,
                        ),
                    start_index,
                    )
                replaced = True
            # insert
            else:
                segmentation.globalExternalReferences.insert_externalReference(
                    schema.SFFExternalReference(
                        type=gExtRef.type,
                        otherType=gExtRef.otherType,
                        value=gExtRef.value,
                        ),
                    start_index,
                    )
            start_index += 1
        return segmentation

    def del_from_segmentation(self, segmentation):
        """Delete attributes from a segmentation
        
        :param segmentation: an EMDB-SFF segmentation
        :type segmentation: ``sfftk.schema.SFFSegmentation``
        :return segmentation: an EMDB-SFF segmentation
        :rtype segmentation: ``sfftk.schema.SFFSegmentation``
        """
        # name
        if self.name:
            segmentation.name = None
        # software name
        if self.softwareName:
            segmentation.software.name = None
        # software version
        if self.softwareVersion:
            segmentation.software.version = None
        # sofware processing details
        if self.softwareProcessingDetails:
            segmentation.software.processingDetails = None
        # file path
        if self.filePath:
            segmentation.filePath = None
        # details
        if self.details:
            segmentation.details = None
        # external references
        if self.externalReferenceId is not None:
            if segmentation.globalExternalReferences:
                try:
                    del segmentation.globalExternalReferences[self.externalReferenceId]
                except IndexError:
                    print_date("Failed to delete global external reference ID {}".format(self.externalReferenceId))
            else:
                print_date("No global external references to delete from.")
        return segmentation        
        

class GlobalArgsNote(AbstractGlobalNote):
    def __init__(self, args, *args_, **kwargs_):
        super(GlobalArgsNote, self).__init__(*args_, **kwargs_)
        self.name = args.name
        self.softwareName = args.software_name
        self.softwareVersion = args.software_version
        self.softwareProcessingDetails = args.software_processing_details
        self.filePath = args.file_path
        self.details = args.details
        if hasattr(args, 'external_ref_id'):
            self.externalReferenceId = args.external_ref_id
        if hasattr(args, 'external_ref'):
            if args.external_ref:
                for _type, _value in args.external_ref:
                    self._extRefList.append(
                        ExternalReference(
                            type=_type,
                            otherType='-',
                            value=_value
                            )
                        )

class AbstractNote(BaseNote):
    """Note 'abstact' class that defines private attributes and main methods"""
    description = NoteAttr('description')
    numberOfInstances = NoteAttr('numberOfInstances')
    externalReferenceId = NoteAttr('externalReferenceId')
    complexId = NoteAttr('complexId')
    complexes = NoteAttr('complexes')
    macromoleculeId = NoteAttr('macromoleculeId')
    macromolecules = NoteAttr('macromolecules')
    
    def add_to_segment(self, segment):
        """Add the annotations found in this ``Note`` object to the ``schema.SFFSegment`` object
         
        :param segment: single segment in EMDB-SFF
        :type segment: ``sfftk.schema.SFFSegment``
        """
        # biologicalAnnotation
        if segment.biologicalAnnotation:
            print_date("Note: A biological annotation exists. You can edit it using 'sff notes edit'.")
        else:
            bA = schema.SFFBiologicalAnnotation()
            bA.description = self.description
            bA.numberOfInstances = self.numberOfInstances
            if self.externalReferences:
                if not bA.externalReferences:
                    bA.externalReferences = schema.SFFExternalReferences()
                for extRef in self.externalReferences:
                    bA.externalReferences.add_externalReference(
                        schema.SFFExternalReference(
                            type=extRef.type,
                            otherType=extRef.otherType,
                            value=extRef.value,
                            )
                        )
            segment.biologicalAnnotation = bA
        # complexesAndMacromolecules
        if segment.complexesAndMacromolecules:
            print_date("Note: Complexes and macromolecules exist. You can edit them using 'sff notes edit'.")
        else:
            cAM = schema.SFFComplexesAndMacromolecules()
            if self.complexes:
                complexes = schema.SFFComplexes()
                for c in self.complexes:
                    complexes.add_complex(c)
                cAM.complexes = complexes
            if self.macromolecules:
                macromolecules = schema.SFFMacromolecules()
                for m in self.macromolecules:
                    macromolecules.add_macromolecule(m)
                cAM.macromolecules = macromolecules
            segment.complexesAndMacromolecules = cAM
        return segment
    
    def edit_in_segment(self, segment):
        """Edit the annotations found in this ``Note`` object to the ``schema.SFFSegment`` object
         
        :param segment: single segment in EMDB-SFF
        :type segment: ``sfftk.schema.SFFSegment``
        """
        # biologicalAnnotation
        if not segment.biologicalAnnotation:
            print_date("Note: no biological anotation was found. You may edit only after adding with 'sff notes add'.")
        else:
            bA = segment.biologicalAnnotation
            if self.description:
                bA.description = self.description
            if self.numberOfInstances:
                bA.numberOfInstances = self.numberOfInstances
            if self.externalReferences:
                if not bA.externalReferences:
                    bA.externalReferences = schema.SFFExternalReferences()
                start_index = self.externalReferenceId
                # first replace
                # then insert any additional
                replaced = False  
                for extRef in self.externalReferences:
                    # replace
                    if not replaced and bA.externalReferences:
                        bA.externalReferences.replace_externalReference(
                            schema.SFFExternalReference(
                                type=extRef.type, 
                                otherType=extRef.otherType,
                                value=extRef.value,
                                ),
                            start_index,              
                            )
                        replaced = True
                    # insert
                    else:
                        bA.externalReferences.insert_externalReference(
                            schema.SFFExternalReference(
                                type=extRef.type, 
                                otherType=extRef.otherType,
                                value=extRef.value,
                                ),
                            start_index,              
                            )
                    start_index += 1
            segment.biologicalAnnotation = bA
        # complexesAndMacromolecules
        if not segment.complexesAndMacromolecules:
            print_date("Note: no complexes and macromolecules were found. You may edit only after adding with 'sff notes add'.")
        else:
            cAM = segment.complexesAndMacromolecules
            # complexes
            if self.complexes:
                if cAM.complexes: # complexes already present
                    for i in xrange(len(self.complexes)):                            
                        if i == 0: # there are complexes but editing the first item mentioned
                            try:
                                cAM.complexes.replace_complex_at(self.complexId + i, self.complexes[i])
                            except IndexError:
                                cAM.complexes.add_complex(self.complexes[i])
                        else: # all other new complexes are inserted after pushing others down
                            try:
                                cAM.complexes.insert_complex_at(self.complexId + i, self.complexes[i])
                            except IndexError:
                                cAM.complexes.add_complex(self.complexes[i])
                else: # no complexes 
                    complexes = schema.SFFComplexes()
                    for c in self.complexes:
                        complexes.add_complex(c)
                    cAM.complexes = complexes
            # macromolecules
            if self.macromolecules:
                if cAM.macromolecules: # macromolecules already present
                    for i in xrange(len(self.macromolecules)):
                        if i == 0: # there are macromolecules but editing the first item mentioned
                            try:
                                cAM.macromolecules.replace_macromolecule_at(self.macromoleculeId + i, self.macromolecules[i])
                            except IndexError:
                                cAM.macromolecules.add_macromolecule(self.macromolecules[i])
                        else: # all other new macromolecules are inserted after pushing others down
                            try:
                                cAM.macromolecules.insert_macromolecule_at(self.macromoleculeId + i, self.macromolecules[i])
                            except IndexError:
                                cAM.macromolecules.add_macromolecule(self.macromolecules[i])
                else: # no macromolecules
                    macromolecules = schema.SFFMacromolecules()
                    for m in self.macromolecules:
                        macromolecules.add_macromolecule(m)
                    cAM.macromolecules = macromolecules
            segment.complexesAndMacromolecules = cAM
        return segment
    
    def del_from_segment(self, segment):
        """Delete the annotations found in this ``Note`` object to the ``schema.SFFSegment`` object
         
        :param segment: single segment in EMDB-SFF
        :type segment: ``sfftk.schema.SFFSegment``
        """
        # biologicalAnnotation
        if not segment.biologicalAnnotation:
            print_date("No biological anotation found! Use 'add' to first add a new annotation.")
        else:
            bA = segment.biologicalAnnotation
            if self.description:
                bA.description = None
            if self.numberOfInstances:
                bA.numberOfInstances = None
            if self.externalReferenceId is not None: # it could be 0, which is valid but False
                if bA.externalReferences:
                    try:
                        del bA.externalReferences[self.externalReferenceId] # externalReferences is a list
                    except IndexError:
                        print_date("Failed to delete external reference of ID {}".format(self.externalReferenceId))
                else:
                    print_date("No external references to delete from.")
            segment.biologicalAnnotation = bA
        # complexesAndMacromolecules
        if not segment.complexesAndMacromolecules:
            print_date("No complexes and macromolecules found! Use 'add' to first add a new set.")
        else:
            cAM = segment.complexesAndMacromolecules
            # complexes
            if self.complexId is not None:
                if cAM.complexes:
                    try:
                        cAM.complexes.delete_at(self.complexId)
                    except IndexError:
                        print_date("Failed to delete macromolecule of ID {}".format(self.complexId))
                else:
                    print_date("No complexes to delete from.")
            # macromolecules
            if self.macromoleculeId is not None:
                if cAM.macromolecules:
                    try:
                        cAM.macromolecules.delete_at(self.macromoleculeId)
                    except IndexError:
                        print_date("Failed to delete macromolecule of ID {}".format(self.macromoleculeId))
                else:
                    print_date("No macromolecules to delete from.")
            segment.complexesAndMacromolecules = cAM
        return segment


class ArgsNote(AbstractNote):
    def __init__(self, args, *args_, **kwargs_):
        super(ArgsNote, self).__init__(*args_, **kwargs_)
        self.description = args.description
        self.numberOfInstances = args.number_of_instances
        if hasattr(args, 'external_ref_id'):
            self.externalReferenceId = args.external_ref_id
        # externalReferences
        if hasattr(args, 'external_ref'): # sff notes del has no -E arg
            if args.external_ref:
                for _type, _value in args.external_ref:
                    self._extRefList.append(
                        ExternalReference(
                            type=_type,
                            otherType='-',
                            value=_value
                            )
                        )
        if hasattr(args, 'complex_id'):
            self.complexId = args.complex_id
        if hasattr(args, 'complexes'):
            self.complexes = args.complexes
        if hasattr(args, 'macromolecule_id'):
            self.macromoleculeId = args.macromolecule_id
        if hasattr(args, 'macromolecules'):
            self.macromolecules = args.macromolecules


class SimpleNote(AbstractNote):
    def __init__(
            self, description=None, numberOfInstances=None, externalReferenceId=None,
            externalReferences=None, complexId=None, complexes=None,
            macromoleculeId=None, macromolecules=None, *args, **kwargs
            ):
        super(SimpleNote, self).__init__(*args, **kwargs)
        self.description = description
        self.numberOfInstances = numberOfInstances
        self.externalReferenceId = externalReferenceId
        # externalReferences
        if externalReferences:
            for _type, _value in externalReferences:
                self._extRefList.append(
                    ExternalReference(
                        type=_type,
                        otherType='-',
                        value=_value
                        )
                    )
        self.complexId = complexId
        self.complexes = complexes
        self.macromoleculeId = macromoleculeId
        self.macromolecules = macromolecules


def add_note(args):
    """Add annotation to a segment specified in args
    
    :param args: parsed arguments
    :type args: ``argparse.Namespace``
    """
    sff_seg = schema.SFFSegmentation(args.sff_file)
    # global changes
    if args.segment_id is None:
        # create a GlobalArgsNote object
        global_note = GlobalArgsNote(args)
        # add notes to segmentation
        sff_seg = global_note.add_to_segmentation(sff_seg)
        # show the updated header
        print HeaderView(sff_seg)
    else:
        found_segment = False
        for segment in sff_seg.segments:
            if segment.id in args.segment_id:
                note = ArgsNote(args)
                sff_seg.segment = note.add_to_segment(segment)
                print NoteView(sff_seg.segment, _long=True)
                found_segment = True
                break
        if not found_segment:
            print_date("Segment of ID(s) {} not found".format(", ".join(map(str, args.segment_id))))
    # export
    sff_seg.export(args.sff_file)
    return 0


def edit_note(args):
    """Edit annotation to a segment specified in args
    
    :param args: parsed arguments
    :type args: ``argparse.Namespace``
    """
    sff_seg = schema.SFFSegmentation(args.sff_file)
    # global changes
    if args.segment_id is None:
        # create a GlobalArgsNote object
        global_note = GlobalArgsNote(args)
        # edit the notes in the segmentation
        # editing name, software, filePath, details are exactly the same as adding
        # editing external references is different:
        # the externalReferenceId refers to the extRef to edit
        # any additionally specified external references (-E a b -E x y) are inserted after the edited index
        sff_seg = global_note.edit_in_segmentation(sff_seg)
        # show the updated header
        print HeaderView(sff_seg)
    else:
        found_segment = False
        for segment in sff_seg.segments:
            if segment.id in args.segment_id:
                note = ArgsNote(args)
                sff_seg.segment = note.edit_in_segment(segment)
                print NoteView(sff_seg.segment, _long=True)
                found_segment = True
                break
        if not found_segment:
            print_date("Segment of ID(s) {} not found".format(", ".join(map(str, args.segment_id))))
    # export
    sff_seg.export(args.sff_file)
    return 0


def del_note(args):
    """Delete annotation to a segment specified in args
    
    :param args: parsed arguments
    :type args: ``argparse.Namespace``
    """
    sff_seg = schema.SFFSegmentation(args.sff_file)
    # global changes
    if args.segment_id is None:
        # create a GlobalArgsNote object
        global_note = GlobalArgsNote(args)
        # delete the notes from segmentation
        sff_seg = global_note.del_from_segmentation(sff_seg)
        # show the updated header
        print HeaderView(sff_seg)
    else:
        found_segment = False
        for segment in sff_seg.segments:
            if segment.id in args.segment_id:
                note = ArgsNote(args)
                sff_seg.segment = note.del_from_segment(segment)
                print NoteView(sff_seg.segment, _long=True)
                found_segment = True
                break
        if not found_segment:
            print_date("Segment of ID(s) {} not found".format(", ".join(map(str, args.segment_id))))
    # export
    sff_seg.export(args.sff_file)
    return 0


def merge(args):
    """Merge two EMDB-SFF files
    
    :param args: parsed arguments
    :type args: ``argparse.Namespace``
    """
    # source
    if args.verbose:
        print_date("Reading in source: {}...".format(args.source))
    source = schema.SFFSegmentation(args.source)
    # destination
    if args.verbose:
        print_date("Reading in destination: {}...".format(args.destination))
    dest = schema.SFFSegmentation(args.destination)
    if args.verbose:
        print_date("Merging annotations...")
    dest.merge_annotation_from(source)
    # export
    if args.verbose:
        print_date("Writing output to {}".format(args.output))
    dest.export(args.output)
    if args.verbose:
        print_date("Done.")
    
    return 0


def save(args):
    """Save changes made
    
    :param args: parsed arguments
    :type args: `argparse.Namespace`
    """
    temp_file = configs['__TEMP_FILE']
    if os.path.exists(temp_file):
        # temp_file: file.sff; args.sff_file: file.sff     copy
        # temp_file: file.hff; args.sff_file: file.hff     copy
        # temp_file: file.json; args.sff_file: file.json   copy
        if (re.match(r'.*\.sff$', temp_file, re.IGNORECASE) and re.match(r'.*\.sff$', args.sff_file, re.IGNORECASE)) or \
            (re.match(r'.*\.hff$', temp_file, re.IGNORECASE) and re.match(r'.*\.hff$', args.sff_file, re.IGNORECASE)) or \
            (re.match(r'.*\.json$', temp_file, re.IGNORECASE) and re.match(r'.*\.json$', args.sff_file, re.IGNORECASE)):
            print_date("Copying temp file {} to {}...".format(temp_file, args.sff_file))
            shutil.copy(temp_file, args.sff_file)
            print_date("Deleting temp file {}...".format(temp_file))
            os.remove(temp_file)
            assert not os.path.exists(temp_file)
        # temp_file: file.sff; args.sff_file: file.hff     convert
        # temp_file: file.sff; args.sff_file: file.json    convert
        # temp_file: file.hff; args.sff_file: file.sff     convert
        # temp_file: file.hff; args.sff_file: file.json    convert
        elif (re.match(r'.*\.sff$', temp_file, re.IGNORECASE) and (re.match(r'.*\.hff$', args.sff_file, re.IGNORECASE) or re.match(r'.*\.json$', args.sff_file, re.IGNORECASE))) or \
            (re.match(r'.*\.hff$', temp_file, re.IGNORECASE) and (re.match(r'.*\.json$', args.sff_file, re.IGNORECASE) or re.match(r'.*\.sff$', args.sff_file, re.IGNORECASE))):
            cmd = shlex.split("convert -v {} -o {}".format(temp_file, args.sff_file))
            _args = parse_args(cmd)
            handle_convert(_args) # convert
            print_date("Deleting temp file {}...".format(temp_file))
            os.remove(temp_file)
            assert not os.path.exists(temp_file)
        # temp_file: file.json; args.sff_file: file.sff    merge
        # temp_file: file.json; args.sff_file: file.hff    merge
        elif re.match(r'.*\.json$', temp_file, re.IGNORECASE) and (re.match(r'.*\.sff$', args.sff_file, re.IGNORECASE) or re.match(r'.*\.hff$', args.sff_file, re.IGNORECASE)):
            json_seg = schema.SFFSegmentation(temp_file)
            seg = schema.SFFSegmentation(args.sff_file)
            # merge
            seg.merge_annotation_from(json_seg)
            seg.export(args.sff_file)
            print_date("Deleting temp file {}...".format(temp_file))
            os.remove(temp_file)
            assert not os.path.exists(temp_file)
        else:
            print_date("Unknown file type: {}".format(args.sff_file))
    else:
        print_date("Missing temp file {}. First perform some edit actions ('add', 'edit', 'del') before trying to save.".format(temp_file))
    return 0


def trash(args):
    """Trash changes made
    
    :param args: parsed arguments
    :type args: `argparse.Namespace`
    """
    temp_file = configs['__TEMP_FILE']
    if os.path.exists(temp_file):
        print_date("Discarding all changes made in temp file {}...".format(temp_file), newline=False)
        os.remove(temp_file)
        assert not os.path.exists(temp_file)
        print_date("Done", incl_date=False)
    else:
        print_date("Unable to discard with missing temp file {}. No changes made.".format(temp_file))
    return 0