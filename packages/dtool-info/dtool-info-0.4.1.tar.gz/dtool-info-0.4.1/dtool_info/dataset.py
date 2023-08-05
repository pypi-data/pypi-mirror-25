"""Commands for getting information about datasets."""

import sys

import click

import pygments
import pygments.lexers
import pygments.formatters

import dtoolcore
from dtoolcore.compare import (
    diff_identifiers,
    diff_sizes,
    diff_content,
)

from dtool_cli.cli import (
    dataset_uri_argument,
    dataset_uri_validation,
    storagebroker_validation,
    CONFIG_PATH,
)

item_identifier_argument = click.argument("item_identifier")


def validate_and_get_dataset(dataset_uri, err_message, err_code=1):
    try:
        dataset = dtoolcore.DataSet.from_uri(dataset_uri)
    except dtoolcore.DtoolCoreTypeError:
        click.secho(err_message, fg="red", err=True)
        sys.exit(err_code)
    return dataset


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

    ds = dtoolcore.DataSet.from_uri(dataset_uri)
    ref_ds = dtoolcore.DataSet.from_uri(reference_dataset_uri)

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


@click.command()
@click.argument("prefix", default="")
@click.argument("storage", default="file", callback=storagebroker_validation)
def ls(prefix, storage):
    """List datasets in a location.

    Proto datasets are highlighted in red.
    """
    storage_broker_lookup = dtoolcore._generate_storage_broker_lookup()
    StorageBroker = storage_broker_lookup[storage]
    info = []
    for uri in StorageBroker.list_dataset_uris(prefix, CONFIG_PATH):
        admin_metadata = dtoolcore._admin_metadata_from_uri(uri, CONFIG_PATH)
        fg = None
        if admin_metadata["type"] == "protodataset":
            fg = "red"
        info.append(dict(
            name=admin_metadata["name"],
            uuid=admin_metadata["uuid"],
            uri=uri,
            fg=fg)
        )

    if len(info) == 0:
        sys.exit(0)

    name_max_len = max([len(i["name"]) for i in info])

    for i in info:
        i["width"] = name_max_len
        line = "{uuid} - {name:{width}s} - {uri}".format(**i)
        click.secho(line, fg=i["fg"])


@click.command()
@dataset_uri_argument
def identifiers(dataset_uri):
    """List the item identifiers in the dataset."""
    dataset = validate_and_get_dataset(
        dataset_uri,
        "Cannot list identifiers in a proto dataset"
    )
    for i in dataset.identifiers:
        click.secho(i)


@click.command()
@dataset_uri_argument
def summary(dataset_uri):
    """Report summary information about a dataset."""
    dataset = validate_and_get_dataset(
        dataset_uri,
        "Cannot report summary information on a proto dataset"
    )

    creator_username = dataset._admin_metadata["creator_username"]
    num_items = len(dataset.identifiers)
    tot_size = sum([dataset.item_properties(i)["size_in_bytes"]
                    for i in dataset.identifiers])

    json_lines = [
        '{',
        '  "name": "{}",'.format(dataset.name),
        '  "uuid": "{}",'.format(dataset.uuid),
        '  "creator_username": "{}",'.format(creator_username),
        '  "number_of_items": {},'.format(num_items),
        '  "size_in_bytes": {}'.format(tot_size),
        '}',
    ]
    formatted_json = "\n".join(json_lines)
    colorful_json = pygments.highlight(
        formatted_json,
        pygments.lexers.JsonLexer(),
        pygments.formatters.TerminalFormatter())
    click.secho(colorful_json, nl=False)


@click.group()
def item():
    """
    Get information about an item in the dataset.
    """


@item.command()
@dataset_uri_argument
@item_identifier_argument
def properties(dataset_uri, item_identifier):
    """Report item properties."""
    dataset = validate_and_get_dataset(
        dataset_uri,
        "Cannot report item properties on a proto dataset"
    )

    props = dataset.item_properties(item_identifier)

    json_lines = [
        '{',
        '  "relpath": "{}",'.format(props["relpath"]),
        '  "size_in_bytes": {},'.format(props["size_in_bytes"]),
        '  "utc_timestamp": {},'.format(props["utc_timestamp"]),
        '  "hash": "{}"'.format(props["hash"]),
        '}',
    ]
    formatted_json = "\n".join(json_lines)
    colorful_json = pygments.highlight(
        formatted_json,
        pygments.lexers.JsonLexer(),
        pygments.formatters.TerminalFormatter())
    click.secho(colorful_json, nl=False)


@item.command()
@dataset_uri_argument
@item_identifier_argument
def fetch(dataset_uri, item_identifier):
    """Return abspath to file with item content.

    Fetches the file from remote storage if required.
    """
    dataset = validate_and_get_dataset(
        dataset_uri,
        "Cannot report item properties on a proto dataset"
    )

    click.secho(dataset.item_content_abspath(item_identifier))


@click.command()
@dataset_uri_argument
def verify(dataset_uri):
    """Return abspath to file with item content.

    Fetches the file from remote storage if required.
    """
    dataset = validate_and_get_dataset(
        dataset_uri,
        "Cannot verify a proto dataset"
    )
    all_okay = True

    generated_manifest = dataset.generate_manifest()
    generated_identifiers = set(generated_manifest["items"].keys())
    manifest_identifiers = set(dataset.identifiers)

    for i in generated_identifiers.difference(manifest_identifiers):
        message = "Unknown item: {} {}".format(
            i,
            generated_manifest["items"][i]["relpath"]
        )
        click.secho(message, fg="red")
        all_okay = False

    for i in manifest_identifiers.difference(generated_identifiers):
        message = "Missing item: {} {}".format(
            i,
            dataset.item_properties(i)["relpath"]
        )
        click.secho(message, fg="red")
        all_okay = False

    for i in manifest_identifiers.intersection(generated_identifiers):
        generated_hash = generated_manifest["items"][i]["hash"]
        manifest_hash = dataset.item_properties(i)["hash"]
        if generated_hash != manifest_hash:
            message = "Altered item: {} {}".format(
                i,
                dataset.item_properties(i)["relpath"]
            )
            click.secho(message, fg="red")
            all_okay = False

    if not all_okay:
        sys.exit(1)
    else:
        click.secho("All good :)", fg="green")
