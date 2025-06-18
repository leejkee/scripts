---

## CLI Tool: Text File Encoding Converter

This is a versatile command-line interface (CLI) tool designed to convert the encoding of text files. All converted files will be saved in the `output/` directory, located within the script's current working directory.

---

### Quick Start

#### Single File Conversion

To convert a single file, use the `-f` or `--file` option:

```shell
python convert-encoding-tool.py -f <input_file>
```

**Example:**

```bash
python convert-encoding-tool.py -f my_document.txt
```

This will convert `my_document.txt` (assuming its original encoding is GBK) to UTF-8 and save the new file as `output/my_document_utf8.txt`.

#### Directory Search (Current Directory)

To convert multiple files within a specified directory (non-recursively), use the `-d` or `--directory` option. You can also use `-F` or `--filter` to specify file patterns.

```shell
python convert-encoding-tool.py -d ./ -F "*.lrc"
```

**Example:**

```bash
python convert-encoding-tool.py -d ./ -F "*.txt" "*.csv"
```

This command will find all `.txt` and `.csv` files directly within the current directory (`./`), convert their encoding (from GBK to UTF-8 by default), and save the converted files into the `output/` directory (e.g., `output/your_file_utf8.txt`).

---

### Parameter Usage

Here's a detailed explanation of all available parameters:

* **`-f`, `--file <path>`**
    * **Description:** Specifies the path to a **single text file** you want to convert. This option is mutually exclusive with `-d` (you can use one or the other, but not both).
    * **Required:** Yes (along with `-d`, exactly one must be provided).
    * **Example:** `-f "C:\Users\John\Documents\report.log"`

* **`-d`, `--directory <path>`**
    * **Description:** Specifies the **directory** containing the text files you wish to convert in batch mode. The tool will process files directly within this directory, but it **will not** traverse into subdirectories. This option is mutually exclusive with `-f`.
    * **Required:** Yes (along with `-f`, exactly one must be provided).
    * **Example:** `-d "/home/user/my_lyrics"`

* **`-o`, `--output <path>`**
    * **Description:** Defines the **output destination** for the converted files.
        * **For single file mode (`-f`):** This specifies the **exact path and filename** for the converted file.
        * **For directory mode (`-d`):** This specifies the **base directory** where all converted files will be saved.
    * **Default Behavior (if not specified):**
        * **For `-f`:** The converted file will be saved in the **same directory** as the input file, with the target encoding appended to its name (e.g., `original_file_utf8.txt`).
        * **For `-d`:** A new subdirectory named `converted_<target_encoding>` (e.g., `converted_utf8`) will be created **inside the input directory** (`-d` specified path), and all converted files will be placed there.
    * **Example (single file):** `-f input.txt -o converted.txt`
    * **Example (directory):** `-d ./my_docs -o ./processed_output`

* **`-s`, `--source-encoding <encoding>`**
    * **Description:** Specifies the **original encoding** of your input file(s). This tells the tool how to correctly read the source files.
    * **Default:** `gbk`
    * **Example:** `-s "shift_jis"`

* **`-t`, `--target-encoding <encoding>`**
    * **Description:** Specifies the **desired encoding** for the output file(s). This is the encoding the converted files will be written in.
    * **Default:** `utf-8`
    * **Example:** `-t "latin-1"`

* **`-F`, `--filter <pattern> [<pattern> ...]`**
    * **Description:** Used exclusively with directory mode (`-d`) to **filter which files** get converted. You can provide one or more glob patterns (e.g., `*.txt`, `song*.lrc`). Only files whose names match at least one of the provided patterns will be processed.
    * **Default:** `['*.txt', '*.lrc', '*.srt', '*.csv', '*.log']` (processes common text file types).
    * **Note:** This argument is **ignored** when using single file mode (`-f`).
    * **Example:** `--filter "*.html" "*.css"`

---