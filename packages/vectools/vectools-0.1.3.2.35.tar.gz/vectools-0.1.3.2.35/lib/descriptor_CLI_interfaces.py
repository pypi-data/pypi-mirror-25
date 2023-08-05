import argparse
import sys
import numpy as np
from lib.inputoutput import ParseVectors
from lib.inputoutput import ParseFasta
from lib.inputoutput import VectorFormats
from lib.inputoutput import _shared_params
from lib.inputoutput import COLUMN_TITLE_FOR_OUTPUT_MATRICES
from lib.inputoutput import VectorIO
from lib.inputoutput import  _slice_list
import re
# -*- coding: utf-8 -*-
"""
##########################################################################################
This module is used for computing the Autocorrelation descriptors based different
 properties of AADs.You can also input your properties of AADs, then it can help you
to compute Autocorrelation descriptors based on the property of AADs. Currently, You
can get 720 descriptors for a given protein sequence based on our provided physicochemical
properties of AADs. You can freely use and distribute it. If you hava  any problem,
you could contact with us timely!
References:
[1]: http://www.genome.ad.jp/dbget/aaindex.html
[2]: Feng, Z.P. and Zhang, C.T. (2000) Prediction of membrane protein types based on
the hydrophobic index of amino acids. J Protein Chem, 19, 269-275.
[3]: Horne, D.S. (1988) Prediction of protein helix content from an autocorrelation
analysis of sequence hydrophobicities. Biopolymers, 27, 451-477.
[4]: Sokal, R.R. and Thomson, B.A. (2006) Population structure inferred by local
spatial autocorrelation: an Usage from an Amerindian tribal population. Am J
Phys Anthropol, 129, 121-131.
Authors: Dongsheng Cao and Yizeng Liang.
Date: 2010.11.22
Email: oriental-cds@163.com

#import lib.descriptors as descriptors

"""

STD_AMINO_ACIDS = [
    "A", "R", "N", "D", "C",
    "E", "Q", "G", "H", "I",
    "L", "K", "M", "F", "P",
    "S", "T", "W", "Y", "V"
]

'''
Additional papers.
propy: a tool to generate various modes of Chou's PseAAC.
http://bioinformatics.oxfordjournals.org/content/31/8/1307.short
repDNA: a Python package to generate various modes of feature vectors for DNA sequences by incorporating
user-defined physicochemical properties and sequence-order effects
Protein remote homology detection by combining Chou's distance-pair pseudo amino acid
composition and principal component analysis
Rcpi: R/Bioconductor package to generate various descriptors of proteins, compounds, and their interactions
ProFET: Feature engineering captures high-level protein functions
class AminoAcidProperty:
    def __init__(self, name, properties):
        self.name = name
        self.properties = properties
'''
# http://www.ncbi.nlm.nih.gov/pubmed/23426256
# http://code.google.com/p/protpy/
'''
def get_residue_percentate(residue_str, ProteinSequence, entry_len):
    """
    This function takes a string of letters, a dictonary with single letter aa abreviateion keys
    mapping to their occurence in a fasta entry and entry_len - an integer counting the total number of entires.
    in the fasta file.
    """
    residue_count = 0
    for aa in residue_str:
        residue_count += ProteinSequence.count(aa)
    return float(residue_count)/float(entry_len)
'''
# @TODO: Use this in testing http://www.ebi.ac.uk/Tools/seqstats/emboss_pepstats/
# ======================================================================================================================
# Nucleic Acid Descriptors.
# ======================================================================================================================
# http://bioinformatics.oxfordjournals.org/content/early/2015/01/12/bioinformatics.btu857.short
# def bilinearindices(parse):
#    # @TODO: Implement this...
#    # This might work for nucleic acids too.
#    # http://onlinelibrary.wiley.com/doi/10.1111/j.1742-4658.2010.07711.x/full
#    x = 0


def _yield_string_slices(input_string, slice_string):
    """
    :param matrix:
    :param slice_string: The string describing how to slice import strings.
    :param keep:
    :return:
    """
    allowed_chars = set("0123456789,:%")
    number_of_columns = len(input_string)
    comma_separated_values = slice_string.split(",")
    sliced_input_str = ""

    l = locals()

    for el in comma_separated_values:
        sliced_input_str = ""
        assert set(el) - allowed_chars == set()
        # Convert percent to numbers.

        original_el = "" + el

        if "%" in el:
            while True:
                percent_match = re.search(r"\.*(\d+)%\.*", el)

                if percent_match is None:
                    break
                else:
                    percent_index = int(percent_match.groups()[0]) / 100.0
                    replace_str = str(int(number_of_columns * percent_index))
                    el = re.sub(percent_match.group(0), replace_str, el)

        build_str = "sliced_input_str = input_string[%s]" % el
        exec(build_str, globals(), l)  # , globals(), _locals
        yield original_el, l['sliced_input_str']

def _handlefastanametorowname(fasta_name, delim):
    """This function is meant to prevent errors cause by using complicated fasta names as row names.
    For example if the matrix delimiter is commas and a fasta name contains a comma this would
    throw off the column naming.
    The initial split is meant to keep the sizes down.
    :param fasta_name:
    :param delim:
    :return:
    """
    return fasta_name.strip().split()[0].split(delim)[0].lstrip(">")


def _input_fasta_params(parser):
    """
    Handle the common tasks needed for vectorization

    I am a bit conflicted about the best design style for creating vectors. It would be more efficient
    to make a composite vector as i.e. AACOMP-DIPEP but this kind of goes against the rest of the
    design scheme.

    At the moment I will plan for users to make composite vectors with the zip function
    can use the zip function to combine the vectors.

    :param vector_types:
    :return:
    @TODO Make a format output object. Can handel which formats are available and their descriptions.
    """

    inputfast_handler_obj = ParseFasta()
    vec_format_obj = VectorFormats()

    parser.add_argument('infiles', nargs='*')
    # nargs='?',
    # type=argparse.FileType('r'),
    # default=sys.stdin

    parser.add_argument('-o', '--output_format', type=str, required=False,
                        choices=vec_format_obj.getavailableformats(),
                        default=vec_format_obj.getdefaultformat(),
                        help='')

    parser.add_argument('-f', '--input_format', dest="input_format", type=str, required=False,
                        choices=inputfast_handler_obj.getavailableformats(),
                        default=inputfast_handler_obj.getdefaultformat(),
                        help='')

    parser.add_argument("--standard_chars_only",
                        action="store_false",
                        help="Fail if a non-standard char is found")


def ncomposition_command_line(parser):
    """ Calculates the n-composition of a FASTA sequence (default: amino acid composition).
    # @TODO: Input file as row id. Should be added in

    This can be used to calculate the K-tuple nucleotide composition (PseKNC)

    #Examples:
    $ cat example.fasta
    >test1
    ATGC
    >test2
    CCGG
    >test3
    AAAA
    >test4
    GCGCGCGCGCCCGGCGCGCCGG

    $ vectools ncomp -o TSV -f FASTA -crd , -l 1 -a <(echo "A,T,G,C") example.fasta
    row_title,A,C,G,T
    >test1,0.25,0.25,0.25,0.25
    >test2,0.0,0.5,0.5,0.0
    >test3,1.0,0.0,0.0,0.0
    >test4,0.0,0.5,0.5,0.0

    """
    # Parse input related to fasta files.
    _input_fasta_params(parser)

    # Get standard vector related arguments.
    _shared_params(
        parser,
        enable_column_titles="Generate column-titles in the output file",
        enable_row_titles="Generate row-titles in the output file"
    )

    # Function specific command line arguments.
    parser.add_argument(
        "-l", '--kmer-len',
        type=int,
        default=1,
        choices=range(1, 5),
        help="The length of peptide k-mer to use. 1 = amino acid composition, 2 = dipeptide, ..., etc.")

    parser.add_argument(
        '--split',
        default=None,
        help="Slice sequences into specified chunks and return composition of each chunk.")

    parser.add_argument(
        "-a", '--alphabet',
        #type=file,
        default=None,
        help="Standard 20 amino acids, or a file with a vector containing the alphabet to use in each.")

    parser.add_argument(
        '--groups',
        #type=file,
        default=None,
        help="Standard 20 amino acids, or a file with a vector containing the alphabet to use in each.")

    # Collect arguments.
    args = parser.parse_args()

    # Store the alphabet used to generate n-composition vectors.
    if args.alphabet is None:
        alphabet = STD_AMINO_ACIDS
    else:
        alphabet = open(args.alphabet).read().strip().split(args.delimiter)
        # alphabet = [i for i in open(args.alphabet).read().strip()]

    # This might help seed up execution.
    from lib.descriptors import NComposition

    # Create a descriptor generating object.
    ncomp_obj = NComposition(args.kmerlen, alphabet, args.roundto)

    # Handle row and column titles.
    # out_column_titles = None
    # if args.column_titles:
    #     # Return the column titles.
    #     out_column_titles = ncomp_obj.getcoltitles()
    #    if args.row_titles:
    #        # If we also have row titles offset add a row title to the column titles.
    #        out_column_titles = [COLUMN_TITLE_FOR_OUTPUT_MATRICES] + out_column_titles

    # Initialize VectorIO object.
    vp = VectorIO(
        delimiter=args.delimiter,
        has_col_names=args.column_titles,
        has_row_names=args.row_titles
    )

    # Set column titles. If column flag is not set, not column title will be output.
    vp.set_column_titles(ncomp_obj.getcoltitles())

    # Set the input format
    fasta_parser_obj = ParseFasta(input_format=args.input_format)

    # Iterate over the fasta entries in the fasta file.
    for fasta_title, sequence in fasta_parser_obj.generatefastaobjects(args.infiles):
        # Calculate N composition of the added sequence.
        vp.iterative_out(
            _handlefastanametorowname(fasta_title, args.delimiter),  # row title
            ncomp_obj.calculate(sequence),                           # Descriptor Vector
            roundto=args.roundto
        )


def transitions_command_line(parser):
    """

    :param parser:
    :return:
    """
    # Parse input related to fasta files.
    _input_fasta_params(parser)

    # Get standard vector related arguments.
    _shared_params(
        parser,
        enable_column_titles="Generate column-titles in the output file",
        enable_row_titles="Generate row-titles in the output file"
    )

    # Function specific command line arguments.
    parser.add_argument(
        '--split',
        default=None,
        help="Slice sequences into specified chunks and return composition of each chunk.")

    parser.add_argument(
        "-l", '--kmer-len',
        type=int,
        default=1,
        choices=range(1, 5),
        help="The length of peptide k-mer to use. 1 = amino acid composition, 2 = dipeptide, ..., etc.")

    parser.add_argument(
        "-a", '--alphabet',
        default=None,
        help="Standard 20 amino acids, or a file with a vector containing the alphabet to use in each.")

    parser.add_argument(
        '--all',
        action="store_false",
        help="Return a vector containing the amounts of all transition types.")

    # @TODO: Add groups. i.e. physico-chem transiitons using non-intersecting sets.
    # Collect arguments.
    args = parser.parse_args()

    # Store the alphabet used to generate n-composition vectors.
    if args.alphabet is None:
        alphabet = STD_AMINO_ACIDS
    else:
        alphabet = open(args.alphabet).read().strip().split(args.delimiter)

    from lib.descriptors import Transition

    descriptor_obj = Transition(alphabet, kmer_len=args.kmer_len, sum_transitions=args.all)

    # Initialize VectorIO object.
    vp = VectorIO(
        delimiter=args.delimiter,
        has_col_names=args.column_titles,
        has_row_names=args.row_titles
    )

    # Set column titles. If column flag is not set, not column title will be output.
    vp.set_column_titles(descriptor_obj.getcoltitles())

    # Set the input format
    fasta_parser_obj = ParseFasta(input_format=args.input_format)

    # Iterate over the fasta entries in the fasta file.
    for fasta_title, sequence in fasta_parser_obj.generatefastaobjects(args.infiles):
        # Calculate N composition of the added sequence.
        vp.iterative_out(
            _handlefastanametorowname(fasta_title, args.delimiter),  # row title
            descriptor_obj.calculate(sequence),  # Descriptor Vector
            roundto=args.roundto
        )


def grouped_n_composition_command_line(parser):
    """

    :param parser:
    :return:
    """
    # out_row_titles = None
    # out_column_titles = None
    # These data structures define the operations and order to perform them in,
    # It is important to preserve this,  especially when adding column titles.
    # Therefore, this are use to produce column titles and to calculate each feature.
    # defines the groups' names and member amino acids.

    # Parse input.
    _input_fasta_params(parser)
    # Handle standard parameters.
    _shared_params(parser)

    parser.add_argument(
        "-l", '--kmer-len',
        type=int,
        default=1,
        choices=range(1, 5),
        help="The length of peptide k-mer to use. 1 = amino acid composition, 2 = dipeptide, ..., etc.")

    parser.add_argument(
        '--groups',
        default=None,
        help="A file containing the characters to describe with features.")

    parser.add_argument(
        '--dist',
        default=None,
        help="""
        Specify the range of sequence to create vectors from. Inspired by the descriptors split-composition
        25{0},25{0}-26,-25{0} and distribution {0}25{1}{2}{0}50{1}{2}{0}75{1}{2}{0}100{1}
        """.format(":", "%%", ","))
    # .format(colon="c")
    # 25,25{colon}-26,-25{colon} and distribution 25%{colon},50%{colon},75%{colon},100%{colon}

    args = parser.parse_args()

    from lib.descriptors import GroupedPropertiesNComposition

    # Initialize descriptor object.
    grouped_ncomp = GroupedPropertiesNComposition(args.groups, kmer_len=args.kmer_len)

    # Initialize fasta parser object, used for parsing fasta files and fasta-vector files.
    fasta_parser_obj = ParseFasta(input_format=args.input_format)

    # Initialize VectorIO object.
    vp = VectorIO(
        delimiter=args.delimiter,
        has_col_names=args.column_titles,
        has_row_names=args.row_titles
    )

    # Set column titles. If column flag is not set, not column title will be output.
    vp.set_column_titles(grouped_ncomp.get_column_titles())

    original_column_titles = vp.get_column_titles()
    updated_column_titles = []

    first_print = True
    # Generate vectors from fasta file or fasta vec.
    for fasta_title, sequence in fasta_parser_obj.fastasequencegenerator(args.infiles):
        # Calculate N composition of the added sequence.

        # @TODO: Add other vector format outputs, should be possible to output vector.
        row_title = _handlefastanametorowname(fasta_title, args.delimiter)
        # _yield_string_slices
        if args.dist is None:
            vec = grouped_ncomp.calculate(sequence)
            first_print = False
        else:
            vec = np.array([])
            for col_type, sub_seq in _yield_string_slices(sequence, args.dist):

                tmp_vec = grouped_ncomp.calculate(sub_seq)
                vec = np.concatenate((vec, tmp_vec), axis=0)

                if first_print:
                    # Need to update column names.
                    for original_col_title in original_column_titles:
                        updated_column_titles.append(original_col_title+"x"+col_type)

        if first_print:
            vp.set_column_titles(updated_column_titles)
            first_print = False

        vp.iterative_out(row_title, vec, roundto=args.roundto)























