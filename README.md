# vdts 🕐🕑⭕🕓

vdts is a library and cli for verifying that items in a time series occur at
regular time intervals.

It started out as a tool specifically used to check and report on if a set of
files with dates in their names occur at regular time intervals with no 
missing and/or extra files.

For example, this is very useful for verifying that there are no missing
statements in a directory for monthly financial statements.

It can still be used to do that. But underneath, we've isolated the core
functionality—the module may also be used as a python code library now.

> Fun fact: "vdts" originally was an abbreviation for "Verify Directory Time
> Series"

## How to Install

This package is still in development and will be deployed to Pypi soon. Watch
out for the pypi release shield to appear at the top of this file.

## Quick Start Guide

### CLI

Once the package is installed, you should have access to a command line script
`vdts` from your python environment's bin directory, which should be in your
user PATH.

To check if there are any gaps in monthly statements with file names that look
like `statement-%Y%m%d.pdf` in the current directory, you can run:

```sh
vdts . 'statement-%Y%m%d\.pdf'
```

To check all the way up until today (to see if you need to go to your bank's
online portal to download statements), you can run:

```sh
vdts -n . 'statement-%Y%m%d\.pdf'
```

Now let's say you have an investment account that provides quarterly
statements. You can check by running:

```sh
vdts -i q -n . 'investment_account_\d{8}-%Y%m%d\.pdf'
```

For further instructions on how to use the CLI, just run

```sh
vdts -h
```

### Library

Details about the library will come soon!

## API Documentation

TODO: I still need to finalize the API for the library offering of vdts
