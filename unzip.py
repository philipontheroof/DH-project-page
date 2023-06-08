import os
import zipfile


def join_split_files(split_files, output_file):
    with open(output_file, "wb") as output:
        for file in split_files:
            with open(file, "rb") as file_input:
                output.write(file_input.read())


def extract_zipfile(file_path, output_dir):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)


split_files = ['./data/data.zip.001', './data/data.zip.002', './data/data.zip.003', './data/data.zip.004', './data/data.zip.005', './data/data.zip.006', './data/data.zip.007', './data/data.zip.008', './data/data.zip.009',
               './data/data.zip.010', './data/data.zip.011', './data/data.zip.012', './data/data.zip.013', './data/data.zip.014', './data/data.zip.015', './data/data.zip.016', './data/data.zip.017']  # Add your filenames here

output_file = './data/data.zip'
output_dir = 'data'

# Join the split zip files
join_split_files(split_files, output_file)

# Extract the single .zip file
extract_zipfile(output_file, output_dir)
