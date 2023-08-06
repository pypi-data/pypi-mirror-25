#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
"""
sfftk.notes.view



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


import re
import sys
import textwrap

import h5py

from sfftk import schema
from sfftk.core.print_tools import print_date


__author__ = "Paul K. Korir, PhD"
__email__ = "pkorir@ebi.ac.uk, paul.korir@gmail.com"
__date__ = "2017-04-07"


def _add_index(L, pre="\t"):
    """Add indexes to items in L"""
    LL = list()
    i = 0
    for l in L:
        LL.append("{}{}: {}".format(pre, i, l))
        i += 1
    return LL


class View(object):
    DISPLAY_WIDTH = 110
    NOT_DEFINED = "-*- NOT DEFINED -*-"
    NOT_DEFINED_ALT = "N/A"
    LINE1 = '=' * DISPLAY_WIDTH
    LINE2 = '-' * DISPLAY_WIDTH
    LINE3 = '*' * DISPLAY_WIDTH


class NoteView(View):
    """NoteView class
    
    Display annotation for a single segment
    """
    def __init__(self, segment, _long=False):
        self._segment = segment
        self._long = _long
    @property
    def id(self):
        return self._segment.id
    @property
    def parentID(self):
        return self._segment.parentID
    @property
    def description(self):
        if self._segment.biologicalAnnotation.description:
            return textwrap.fill(self._segment.biologicalAnnotation.description, self.DISPLAY_WIDTH)
        else:
            return self.NOT_DEFINED
    @property
    def numberOfInstances(self):
        if self._segment.biologicalAnnotation.numberOfInstances:
            return self._segment.biologicalAnnotation.numberOfInstances
        else:
            return self.NOT_DEFINED_ALT
    @property
    def numberOfExternalReferences(self):
        return self._segment.biologicalAnnotation.numExternalReferences
    @property
    def externalReferences(self):
        if self._segment.biologicalAnnotation:
            string_list = list()
            string_list.append(
                "\t{:<20}\t{:<20}\t{:<20}".format(
                    "#  ontology",
                    "type",
                    "term",
                    )
                )
            string_list.append("\t" + "-" * (self.DISPLAY_WIDTH - len("\t".expandtabs())))
            i = 0
            for extRef in self._segment.biologicalAnnotation.externalReferences:
                string_list.append(
                    "\t{}: {:<20}\t{:<20}\t{:<20}".format(
                        i,
                        extRef.type,
                        extRef.otherType if extRef.otherType else '-',
                        extRef.value,
                        )
                    )
                i += 1
            return "\n".join(string_list)
        else:
            return "\t" + self.NOT_DEFINED
    @property
    def numberOfComplexes(self):
        return self._segment.complexesAndMacromolecules.numComplexes
    @property
    def complexes(self):
        if self._segment.complexesAndMacromolecules:
            return "\n".join(_add_index(self._segment.complexesAndMacromolecules.complexes))
        else:
            return "\t" + self.NOT_DEFINED
    @property
    def numberOfMacromolecules(self):
        return self._segment.complexesAndMacromolecules.numMacromolecules
    @property
    def macromolecules(self):
        if self._segment.complexesAndMacromolecules:
            return "\n".join(_add_index(self._segment.complexesAndMacromolecules.macromolecules))
        else:
            return "\t" + self.NOT_DEFINED
    @property
    def colour(self):
        if self._segment.colour.name:
            return self._segment.colour.name
        elif self._segment.colour.rgba:
            return self._segment.colour.rgba.value
        else:
            return self.NOT_DEFINED
    @property
    def segmentType(self):
        segment_type = list()
        if self._segment.contours:
            segment_type.append("contourList")
        if self._segment.meshes:
            print 'here'
            segment_type.append("meshList")
        if self._segment.shapes:
            segment_type.append("shapePrimitiveList")
        if self._segment.volume:
            segment_type.append("threeDVolume")
        # json EMDB-SFF files do not have geometrical data
        if not segment_type:
            return None
        else:
            return ", ".join(segment_type)
    def __str__(self):
        if self._long:
            string = """\
            \r{}
            \rID:\t\t{}
            \rPARENT ID:\t{}
            \rSegment Type:\t{}
            \r{}
            \rDescription:
            \r\t{}
            \rNumber of instances:
            \r\t{}
            \r{}
            \rExternal references:
            \r{}
            \r{}
            \rComplexes:
            \r{}
            \rMacromolecules:
            \r{}
            \r{}
            \rColour:
            \r\t{}\
            """.format(
                # ****
                self.LINE3,
                self.id,
                self.parentID,
                self.segmentType,
                # ---
                self.LINE2,
                self.description,
                self.numberOfInstances,
                # -----
                self.LINE2,
                self.externalReferences,
                # ----
                self.LINE2,
                self.complexes,
                self.macromolecules,
                # ----
                self.LINE2,
                self.colour,
                )
        else:
            string = "{:<7} {:<7} {:<40} {:>5} {:>5} {:>5} {:>5} {:^30}".format(
                self.id,
                self.parentID,
                self.description if len(self.description) <= 40 else self.description[:37] + "...",
                self.numberOfInstances,
                self.numberOfExternalReferences,
                self.numberOfComplexes,
                self.numberOfMacromolecules,
                "(" + ", ".join(map(str, map(lambda c: round(c, 3), self.colour))) + ")",
                )
        return string


class HeaderView(View):
    """HeaverView class
    
    Display EMDB-SFF header
    """
    def __init__(self, segmentation):
        self._segmentation = segmentation
    @property
    def name(self):
        if self._segmentation.name:
            return self._segmentation.name
        else:
            return self.NOT_DEFINED
    @property
    def version(self):
        return self._segmentation.version
    @property
    def software(self):
        return u"""\
        \r\tSoftware: {}
        \r\tVersion:  {}
        \rSoftware processing details: \n{}\
        """.format(
            self._segmentation.software.name if self._segmentation.software.name else self.NOT_DEFINED,
            self._segmentation.software.version if self._segmentation.software.version else self.NOT_DEFINED,
            textwrap.fill(
                u"\t" + self._segmentation.software.processingDetails \
                    if self._segmentation.software.processingDetails else "\t" + self.NOT_DEFINED, 
                self.DISPLAY_WIDTH
                ),
            ).encode('utf-8')
    @property
    def filePath(self):
        return self._segmentation.filePath
    @property
    def primaryDescriptor(self):
        return self._segmentation.primaryDescriptor
    @property
    def boundingBox(self):
        return self._segmentation.boundingBox.xmin, self._segmentation.boundingBox.xmax, \
            self._segmentation.boundingBox.ymin, self._segmentation.boundingBox.ymax, \
            self._segmentation.boundingBox.zmin, self._segmentation.boundingBox.zmax
    @property
    def globalExternalReferences(self):
        if self._segmentation.globalExternalReferences:
            string_list = list()
            string_list.append(
                "{:<20}\t{:<20}\t{:<20}".format(
                    "#  ontology",
                    "type",
                    "term",
                    )
                )
            string_list.append("\t" + "-" * (self.DISPLAY_WIDTH - len("\t".expandtabs())))
            i = 0
            for gExtRef in self._segmentation.globalExternalReferences:
                string_list.append(
                    "\t{}: {:<20}\t{:<20}\t{:<20}".format(
                        i,
                        gExtRef.type,
                        gExtRef.otherType if gExtRef.otherType else '-',
                        gExtRef.value,
                        )
                    )
                i += 1
            return "\n".join(string_list)
        else:
            return self.NOT_DEFINED
    @property
    def details(self):
        if self._segmentation.details:
            return u"\n".join(textwrap.wrap(self._segmentation.details, self.DISPLAY_WIDTH)).encode('utf-8')
        else:
            return self.NOT_DEFINED
    def __str__(self):
        string = """\
        \r{}
        \rEMDB-SFF v.{}
        \r{}
        \rSegmentation name:
        \r\t{}
        \rSegmentation software:
        \r{}
        \r{}
        \rPrimary descriptor:
        \r\t{}
        \r{}
        \rFile path:
        \r\t{}
        \r{}
        \rBounding box:
        \r\t{}
        \r{}
        \rGlobal external references:
        \r\t{}
        \r{}
        \rSegmentation details:
        \r\t{}\
        """.format(
            # ===
            self.LINE1,
            self.version,
            # ---
            self.LINE2,
            self.name,
            self.software,
            # ---
            self.LINE2,
            self.primaryDescriptor,
            # ---
            self.LINE2,
            self.filePath,
            # ---
            self.LINE2,
            self.boundingBox,
            # ---
            self.LINE2,
            self.globalExternalReferences,
            # ----
            self.LINE2,
            self.details,
            )
        return string


class TableHeaderView(View):
    def __str__(self):
        string = """\
        \r{}
        \r{:<7} {:<7} {:<40} {:>5} {:>5} {:>5} {:>5} {:^26}
        \r{}\
        """.format(
            View.LINE3,
            "id", 
            "parId",
            "description",
            "#inst",
            "#exRf",
            "#cplx",
            "#macr",
            "colour",
            View.LINE2
            )
        return string


def list_notes(args):
    """List all notes in an EMDB-SFF file
    
    :param args: parsed arguments
    :type args: ``argparse.Namespace``
    :return int status: 0 is OK, else failure
    """
    sff_seg = schema.SFFSegmentation(args.sff_file)
    """
    :TODO: make this optional
    :TODO: define the stream to use
    """
    if args.header:
        print HeaderView(sff_seg)
    note_views = [NoteView(segment, _long=args.long_format) for segment in sff_seg.segments]
    if args.sort_by_description:
        sorted_note_views = sorted(note_views, key=lambda n: n.description, reverse=args.reverse)
    else:
        sorted_note_views = sorted(note_views, key=lambda n: n.id, reverse=args.reverse)
    # table header
    print TableHeaderView()
    for note_view in sorted_note_views:
        print note_view
    return 0


def show_notes(args):
    """Show notes in an EMDB-SFF file for the specified segment IDs
    
    :param args: parsed arguments
    :type args: ``argparse.Namespace``
    :return int status: 0 is OK, else failure
    """
    sff_seg = schema.SFFSegmentation(args.sff_file)
    if args.header:
        print HeaderView(sff_seg)
    if args.segment_id is not None:
        if not args.long_format:
            print TableHeaderView()
        found_segment = False
        for segment in sff_seg.segments:
            if segment.id in args.segment_id:
                print NoteView(segment, _long=args.long_format)
                found_segment = True
        if not found_segment:
            print_date("No segment with ID(s) {}".format(", ".join(map(str, args.segment_id))))
    return 0