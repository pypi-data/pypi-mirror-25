"""Commands for getting information about datasets."""

import sys
import click

from dtoolcore import DataSet
from dtoolcore.compare import (
    diff_identifiers,
    diff_sizes,
    diff_content,
)

from dtool_cli.cli import (
    dataset_uri_argument,
    dataset_uri_validation,
)


@click.command()
@dataset_uri_argument
@click.argument("reference_dataset_uri", callback=dataset_uri_validation)
def diff(dataset_uri, reference_dataset_uri):
    """Report the difference between two datasets.

    1. Checks that the identifiers are identicial
    2. Checks that the sizes are identical
    3. Checks that the hashes are identical

    If a differences is detected in step 1, steps 2 and 3 will not be carried
    out. Similarly if a difference is detected in step 2, step 3 will not be
    carried out.

    When checking that the hashes are identical the hashes for the first
    dataset are recalculated using the hashing algorithm of the reference
    dataset.
    """

    def echo_header(desc, ds_name, ref_ds_name, prop):
        click.secho("Different {}".format(desc), fg="red")
        click.secho("ID, {} in '{}', {} in '{}'".format(
            prop, ds_name, prop, ref_ds_name))

    def echo_diff(diff):
        for d in diff:
            line = "{}, {}, {}".format(d[0], d[1], d[2])
            click.secho(line)

    ds = DataSet.from_uri(dataset_uri)
    ref_ds = DataSet.from_uri(reference_dataset_uri)

    num_items = len(list(ref_ds.identifiers))

    ids_diff = diff_identifiers(ds, ref_ds)
    if len(ids_diff) > 0:
        echo_header("identifiers", ds.name, ref_ds.name, "present")
        echo_diff(ids_diff)
        sys.exit(1)

    with click.progressbar(length=num_items,
                           label="Comparing sizes") as progressbar:
        sizes_diff = diff_sizes(ds, ref_ds, progressbar)
    if len(sizes_diff) > 0:
        echo_header("sizes", ds.name, ref_ds.name, "size")
        echo_diff(sizes_diff)
        sys.exit(2)

    with click.progressbar(length=num_items,
                           label="Comparing hashes") as progressbar:
        content_diff = diff_content(ds, ref_ds, progressbar)
    if len(content_diff) > 0:
        echo_header("content", ds.name, ref_ds.name, "hash")
        echo_diff(content_diff)
        sys.exit(3)
