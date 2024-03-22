SML docs repository
===

## Requirements
* Hatch >= 19.4

## Commands

* `hatch run dev:build`
    Build Sphinx documentation into `build/html` docs
* `hatch run dev:watch`
    Starts Sphinx autobuilder - HTTP hosting with auto rebuild and reload
* `hatch run dev:check`
    Checks quality of documentation using linters

## Linters
* `sphinx-lint`
* `Vale` with `Alex` package
