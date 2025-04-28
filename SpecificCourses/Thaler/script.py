"""
SpecializedSliceScript_ProofsArgumentsZeroKnowledge.py

VERSION 1.0 (CourseInACan Protocol)

This script slices "Proofs, Arguments, and Zero-Knowledge" by Justin Thaler (2022)
into chapter-based PDFs following CourseInACan structure.
"""

import sys
import os
import random
import re
from PyPDF2 import PdfReader, PdfWriter

def sanitize(text):
    """Remove special characters and spaces for filenames."""
    return re.sub(r'[^A-Za-z0-9_]', '', text.replace(' ', ''))

# Define slices manually:
slices = [
    (119, 131, 1, 1, "Introduction", "Introduction"),
    (132, 147, 2, 2, "PowerofRandomness", "PowerofRandomness"),
    (148, 165, 3, 3, "DefinitionsandTechnicalPreliminaries", "DefinitionsandTechnicalPreliminaries"),
    (166, 235, 4, 4, "InteractiveProofs", "InteractiveProofs"),
    (236, 253, 5, 5, "PubliclyVerifiableArguments", "PubliclyVerifiableArguments"),
    (254, 291, 6, 6, "FrontEnds", "FrontEnds"),
    (292, 310, 7, 7, "FirstSuccinctArgument", "FirstSuccinctArgument"),
    (311, 336, 8, 8, "MIPsandSuccinctArguments", "MIPsandSuccinctArguments"),
    (337, 357, 9, 9, "PCPsandSuccinctArguments", "PCPsandSuccinctArguments"),
    (358, 397, 10, 10, "InteractiveOracleProofs", "InteractiveOracleProofs"),
    (398, 412, 11, 11, "ZeroKnowledgeProofsandArguments", "ZeroKnowledgeProofsandArguments"),
    (413, 442, 12, 12, "ProtocolsandCommitments", "ProtocolsandCommitments"),
    (443, 462, 13, 13, "ZeroKnowledgeviaCommitAndProve", "ZeroKnowledgeviaCommitAndProve"),
    (463, 495, 14, 14, "PolynomialCommitmentsDiscreteLog", "PolynomialCommitmentsDiscreteLog"),
    (496, 536, 15, 15, "PolynomialCommitmentsPairings", "PolynomialCommitmentsPairings"),
    (537, 547, 16, 16, "WrapUpofPolynomialCommitments", "WrapUpofPolynomialCommitments"),
    (548, 578, 17, 17, "LinearPCPsandSuccinctArguments", "LinearPCPsandSuccinctArguments"),
    (579, 606, 18, 18, "SNARKCompositionandRecursion", "SNARKCompositionandRecursion"),
    (607, 628, 19, 19, "BirdsEyeViewofPracticalArguments", "BirdsEyeViewofPracticalArguments")
]

# Set the page offset between logical and physical pages
PAGE_OFFSET = -110

def main():
    if len(sys.argv) != 2:
        print("Usage: python SpecializedSliceScript_ProofsArgumentsZeroKnowledge.py <input.pdf>")
        sys.exit(1)

    input_file = sys.argv[1]
    reader = PdfReader(input_file)

    random_number = random.randint(10000, 99999)
    output_dir = f"output_{random_number}"
    os.makedirs(output_dir, exist_ok=True)

    for logical_start, logical_end, ch_start, ch_end, title_first, title_last in slices:
        pdf_writer = PdfWriter()
        real_start = logical_start + PAGE_OFFSET - 1  # Adjust for 0-indexing
        real_end = logical_end + PAGE_OFFSET - 1

        logical_page_count = logical_end - logical_start + 1
        if logical_page_count > 140:
            print(f"WARNING: Slice for chapters {ch_start}-{ch_end} ({title_first} to {title_last}) is {logical_page_count} pages long (exceeds 140).")

        for page_num in range(real_start, real_end + 1):
            pdf_writer.add_page(reader.pages[page_num])

        title_first_clean = sanitize(title_first)
        title_last_clean = sanitize(title_last)

        if ch_start == ch_end:
            filename = f"CHAPTER_{ch_start}_{title_first_clean}.pdf"
        else:
            filename = f"CHAPTER_{ch_start}_{ch_end}_{title_first_clean}_{title_last_clean}.pdf"

        output_path = os.path.join(output_dir, filename)

        with open(output_path, 'wb') as f_out:
            pdf_writer.write(f_out)

        print(f"Created {output_path}")

if __name__ == "__main__":
    main()