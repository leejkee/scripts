import argparse
import os
import fnmatch # For fuzzy matching with globs like *.txt

# --- Custom Exception Classes ---
class FileConversionError(Exception):
    """Base exception for file conversion errors."""
    pass

class FileNotFoundError(FileConversionError):
    """Raised when the input file is not found."""
    pass

class EncodingError(FileConversionError):
    """Raised when there's an issue with file encoding (decode or lookup)."""
    pass

# --- Core File Conversion Logic ---
def convert_single_file(input_filepath: str, output_filepath: str, source_encoding: str = 'gbk', target_encoding: str = 'utf-8'):
    """
    Converts a text file's encoding from source_encoding to target_encoding.

    Args:
        input_filepath (str): Path to the input file.
        output_filepath (str): Path to save the converted output file.
        source_encoding (str): Encoding of the input file (default: 'gbk').
        target_encoding (str): Desired encoding for the output file (default: 'utf-8').

    Raises:
        FileNotFoundError: If the input file does not exist.
        EncodingError: If there's an issue decoding with source_encoding or if
                       target_encoding is unsupported.
        FileConversionError: For other unexpected errors during conversion.
    """
    if not os.path.exists(input_filepath):
        raise FileNotFoundError(f"Error: Input file '{input_filepath}' not found.")

    try:
        with open(input_filepath, 'r', encoding=source_encoding) as infile:
            content = infile.read()

        with open(output_filepath, 'w', encoding=target_encoding) as outfile:
            outfile.write(content)

    except UnicodeDecodeError as e:
        raise EncodingError(f"Error decoding '{input_filepath}' with '{source_encoding}'. Detail: {e}")
    except LookupError as e:
        raise EncodingError(f"Error: Unsupported encoding '{source_encoding}' or '{target_encoding}'. Detail: {e}")
    except Exception as e:
        raise FileConversionError(f"An unexpected error occurred during conversion of '{input_filepath}': {e}")

# --- Argument Parsing Logic ---
def parse_arguments():
    """
    Parses command-line arguments for the file encoding conversion tool.

    Returns:
        argparse.Namespace: An object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="A versatile tool to convert text file encodings, supporting single file or batch directory processing.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-f", "--file",
        help="Path to a single file to convert.",
        type=str
    )
    group.add_argument(
        "-d", "--directory",
        help="Path to a directory for batch conversion. Only files in this directory (non-recursive) will be processed.\n"
             "Defaults to the current working directory if not specified with -f or -d (though one must be provided).", # Clarified default
        default=os.getcwd(), # Default for -d if it were optional, but it's in a required mutual exclusive group.
        type=str
    )

    parser.add_argument(
        "-o", "--output",
        help="Output path for single file mode (-f): Specifies the direct output file path.\n"
             "For directory mode (-d): Specifies the base output directory.\n"
             "Defaults:\n"
             "  - For -f, original filename with '_target_encoding' suffix in its original directory.\n"
             "  - For -d, a 'converted_<target_encoding>' subdirectory within the input directory.",
        type=str
    )

    parser.add_argument(
        "-s", "--source-encoding",
        help="The current encoding of input file(s). Defaults to 'gbk'.",
        default="gbk",
        type=str
    )

    parser.add_argument(
        "-t", "--target-encoding",
        help="The target encoding for converted file(s). Defaults to 'utf-8'.",
        default="utf-8",
        type=str
    )

    parser.add_argument(
        "-F", "--filter",
        help="For directory mode (-d): A glob pattern to filter files (e.g., '*.txt', '*.lrc', 'song*.txt').\n"
             "Defaults to all files with common text extensions (*.txt, *.lrc, *.srt, *.csv, *.log).\n"
             "Specify multiple patterns like '--filter \"*.txt\" --filter \"*.lrc\"'.\n"
             "Note: This argument is ignored in single file mode (-f).",
        nargs='*', # Allows zero or more arguments
        default=['*.txt', '*.lrc', '*.srt', '*.csv', '*.log'],
        type=str
    )

    return parser.parse_args()

# --- Unified File Processing Logic ---
def process_file_conversion(args):
    """
    Handles both single file and batch directory conversion based on parsed arguments.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.
    """
    source_encoding = args.source_encoding
    target_encoding = args.target_encoding
    sanitized_target_encoding = target_encoding.replace('-', '') # For default naming

    input_files_to_process = []
    output_base_dir = None # This will be determined dynamically

    if args.file:
        input_filepath = args.file
        if not os.path.isfile(input_filepath):
            print(f"Error: Input file '{input_filepath}' not found or is not a file.")
            return

        input_files_to_process.append(input_filepath)

        print(f"\n--- Converting Single File ---")
        print(f"Input: '{input_filepath}'")

        if args.output:
            output_filepath_for_single = args.output
            output_base_dir = os.path.dirname(output_filepath_for_single) # Get the directory part
            if not output_base_dir: # If only a filename was given, use current dir
                output_base_dir = os.path.dirname(input_filepath)
        else:
            name, ext = os.path.splitext(input_filepath)
            output_filepath_for_single = f"{name}_{sanitized_target_encoding}{ext}"
            output_base_dir = os.path.dirname(output_filepath_for_single)

        print(f"Output path: '{output_filepath_for_single}'")

    elif args.directory:
        input_dir = args.directory
        if not os.path.isdir(input_dir):
            print(f"Error: Directory '{input_dir}' not found or is not a directory.")
            return

        if args.output:
            output_base_dir = args.output
        else:
            output_base_dir = os.path.join(input_dir, f"converted_{sanitized_target_encoding}")
        
        print(f"\n--- Batch Conversion Started ---")
        print(f"Input Directory: '{input_dir}'")
        print(f"Output Directory: '{output_base_dir}'")
        print(f"Filter Pattern(s): {', '.join(args.filter)}")

        for filename in os.listdir(input_dir):
            filepath = os.path.join(input_dir, filename)
            if os.path.isfile(filepath): 
                is_match = False
                for pattern in args.filter:
                    if fnmatch.fnmatch(filename, pattern):
                        is_match = True
                        break
                if is_match:
                    input_files_to_process.append(filepath)

        if not input_files_to_process:
            print(f"No files found matching the filter(s) in '{input_dir}'.")
            return
            
    try:
        os.makedirs(output_base_dir, exist_ok=True)
        print(f"Created output directory: '{output_base_dir}' (if it didn't exist)")
    except OSError as e:
        print(f"Error: Could not create output directory '{output_base_dir}': {e}")
        return

    print(f"Source Encoding: '{source_encoding}'")
    print(f"Target Encoding: '{target_encoding}'")
    print(f"--------------------------------\n")

    files_converted = 0
    files_skipped = 0
    files_failed = 0

    for input_filepath in input_files_to_process:
        filename = os.path.basename(input_filepath)
        print(f"Processing '{filename}'...")

        try:
            current_output_filepath = ""
            if args.file:
                current_output_filepath = output_filepath_for_single
            else:
                name, ext = os.path.splitext(filename)
                output_filename = f"{name}_{sanitized_target_encoding}{ext}"
                current_output_filepath = os.path.join(output_base_dir, output_filename)

            if os.path.abspath(input_filepath) == os.path.abspath(current_output_filepath):
                print(f"  Skipped: Output file '{current_output_filepath}' would overwrite input. Adjust output path or directory.")
                files_skipped += 1
                continue

            convert_single_file(input_filepath, current_output_filepath, source_encoding, target_encoding)
            files_converted += 1
            print(f"  Converted successfully to '{os.path.basename(current_output_filepath)}'")

        except FileConversionError as e:
            files_failed += 1
            print(f"  Failed: {e}")
        except Exception as e:
            files_failed += 1
            print(f"  An unhandled error occurred: {e}")
    
    print(f"\n--- Conversion Summary ---")
    print(f"Files Processed: {len(input_files_to_process)}")
    print(f"Files Converted: {files_converted}")
    print(f"Files Skipped: {files_skipped}")
    print(f"Files Failed: {files_failed}")
    print(f"--------------------------\n")

# --- Script Entry Point ---
if __name__ == "__main__":
    try:
        args = parse_arguments()
        process_file_conversion(args)
    except SystemExit:
        pass # argparse handles --help and invalid arguments
    except Exception as e:
        print(f"An unexpected top-level error occurred: {e}")