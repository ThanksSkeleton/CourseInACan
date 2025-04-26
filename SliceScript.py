import sys
import os
import random
import re
from PyPDF2 import PdfReader, PdfWriter

def sanitize(text):
    return re.sub(r'[^A-Za-z0-9_]', '', text.replace(' ', ''))

# Define slices: (logical_start, logical_end, first_chapter_num, last_chapter_num, title_first, title_last)
slices = [
    (1, 74, 1, 2, "DiscreteProbabilityDistributions", "ContinuousProbabilityDensities"),
    (75, 132, 3, 3, "Combinatorics", "Combinatorics"),
    (133, 224, 4, 5, "ConditionalProbability", "DistributionsandDensities"),
    (225, 304, 6, 7, "ExpectedValueandVariance", "SumsofRandomVariables"),
    (305, 364, 8, 9, "LawofLargeNumbers", "CentralLimitTheorem"),
    (365, 404, 10, 10, "GeneratingFunctions", "GeneratingFunctions"),
    (405, 470, 11, 11, "MarkovChains", "MarkovChains"),
    (471, 498, 12, 12, "RandomWalks", "RandomWalks")
]

PAGE_OFFSET = 8

def main():
    if len(sys.argv) != 2:
        print("Usage: python slice_pdf.py <input.pdf>")
        sys.exit(1)

    input_file = sys.argv[1]
    reader = PdfReader(input_file)

    random_number = random.randint(10000, 99999)
    output_dir = f"output_{random_number}"
    os.makedirs(output_dir, exist_ok=True)

    for logical_start, logical_end, ch_start, ch_end, title_first, title_last in slices:
        pdf_writer = PdfWriter()
        real_start = logical_start + PAGE_OFFSET - 1  # 0-indexed
        real_end = logical_end + PAGE_OFFSET - 1      # inclusive

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
