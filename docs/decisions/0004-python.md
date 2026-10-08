# 0004. Python as the implementation language

- Status: accepted
- Date: 2026-10-08

## Context

Weft's dependencies expose Python interfaces. holonic is a Python library, sysml-toolkit ships Python bindings (decision 0002), and rdflib and pySHACL provide RDF handling and SHACL validation. specl, whose working rules Weft carries over, is also Python.

## Decision

Weft's library and command-line tools are written in Python. Code that belongs in the parser or checker is contributed to sysml-toolkit rather than reimplemented in Weft.

## Consequences

Weft's minimum Python version is at least 3.11, because holonic requires 3.11 or later. CI runs on Linux and Windows across the supported Python versions, following specl, where text I/O that assumed the locale encoding reached an adopter on a platform its CI did not run.
