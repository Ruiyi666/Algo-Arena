import os
import zipfile
import argparse

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), path))

def main():
    parser = argparse.ArgumentParser(description='Compresses directories into a zip file.')
    parser.add_argument('--source_dir', required=True, help='Directory of the source code to compress')
    parser.add_argument('--output_file', default=None, help='Name of the output zip file without extension')

    args = parser.parse_args()
    output_file = args.output_file if args.output_file else os.path.basename(os.path.normpath(args.source_dir))

    with zipfile.ZipFile(f'{output_file}.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipdir(args.source_dir, zipf)

if __name__ == "__main__":
    main()
