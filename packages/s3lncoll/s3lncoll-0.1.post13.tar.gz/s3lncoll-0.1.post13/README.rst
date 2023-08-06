s3lncoll
========

Read files from S3 as defined by a key prefix and map them by lines to
a set of optionally gzip compressed output files in S3, with the
output files limited by (pre-compressed) file size.  The string "{}"
in the output key will be substituted with the (zero-based) index of
the output files.

::

  s3lncoll: Line stream s3 files into ~uniform lumps in S3
  
  Usage: s3lncoll {{arguments}} {{options}}
  
  Arguments:
    from [text]  S3 URL prefix to clump
      to [text]    S3 URL for target clump ('{}' will be the count)
      
      Options:
        -h, --help             Show this help message and exit
        -H, --HELP             Help for all sub-commands
        -D, --debug            Enable debug logging
        -d, --delete           Delete source files/keys
        -j, --json             Validate each line as JSONM
        -q, --quiet            Be quiet, be vewy vewy quiet
        -V, --version          Report installed version
        -z, --compress         Ccompress (gzip) the target(s)
        -b, --blocksize [int]  Maximum size of pre-compressed output files in bytes. (default: 1048576)
