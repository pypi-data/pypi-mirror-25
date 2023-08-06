pymd5
=====

Recursively calculate and display MD5 file hashes for all files rooted in a directory.

Description
-----------
Hashes are calculated for all files rooted in the given directory. Hashes and file paths (relative to given directory) are output to stdout, problem files reported on stderr. File paths are output in alphabetical order, and don't include the name of the top-level directory.

Output matches that of md5sum(1): "{md5-hash} \*{relative file path}", e.g: ::

    7df5132659452a47ec54aa7158995e21 *pymd5.py

Functions
---------
.. raw:: html

    <pre>
    <strong>calculate_hashes</strong>(dirpath)
        Calculate MD5 hashes for all files rooted in `dirpath`.
    </pre>

Command-line usage
------------------
.. raw:: html

    <pre><strong>pymd5</strong> [-h|--help] DIRPATH</pre>
