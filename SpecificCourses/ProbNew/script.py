"""
SpecializedSliceScript_GrinsteadSnell.py

VERSION 1.0 (CourseInACan Protocol)

This script slices Grinstead and Snell's Introduction to Probability into chapter PDFs
according to the extracted Table of Contents.
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
# Each entry: (logical_start_page, logical_end_page, chapter_start_num, chapter_end_num, title_first, title_last)
slices = [
    (1, 40, 1, 1, "DiscreteProbabilityDistributions", "DiscreteProbabilityDistributions"),
    (41, 74, 2, 2, "ContinuousProbabilityDensities", "ContinuousProbabilityDensities"),
    (75, 132, 3, 3, "Combinatorics", "Combinatorics"),
    (133, 182, 4, 4, "ConditionalProbability", "ConditionalProbability"),
    (183, 224, 5, 5, "DistributionsandDensities", "DistributionsandDensities"),
    (225, 284, 6, 6, "ExpectedValueandVariance", "ExpectedValueandVariance"),
    (285, 304, 7, 7, "SumsofRandomVariables", "SumsofRandomVariables"),
    (305, 324, 8, 8, "LawofLargeNumbers", "LawofLargeNumbers"),
    (325, 364, 9, 9, "CentralLimitTheorem", "CentralLimitTheorem"),
    (365, 404, 10, 10, "GeneratingFunctions", "GeneratingFunctions"),
    (405, 470, 11, 11, "MarkovChains", "MarkovChains"),
    (471, 498, 12, 12, "RandomWalks", "RandomWalks")
]

# Set the page offset between logical and physical pages
PAGE_OFFSET = 8

def main():
    if len(sys.argv) != 2:
        print("Usage: python SpecializedSliceScript_GrinsteadSnell.py <input.pdf>")
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
