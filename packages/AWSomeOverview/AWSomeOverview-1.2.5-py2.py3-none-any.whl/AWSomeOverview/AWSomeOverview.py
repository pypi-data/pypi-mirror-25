#!/usr/bin/env python

"""
Main executable file for the AWSomeOverview project.
"""
from optparse import OptionParser
import os
import sys
import pkgutil
import inspect
import boto3

from AWSomeOverview.deplugins.base import AWSFact
from AWSomeOverview.outputformat.base import BaseOutput

from . import deplugins
from . import outputformat

# Consts used to find the modules that contain Data Extraction Plugin classes
PLUGINS_PREFIX = deplugins.__path__
PluginBaseClass = AWSFact

# Consts used to find the modules that contain Output classes
OUTPUT_PREFIX = outputformat.__path__
OutputBaseClass = BaseOutput

DEFAULT_OUTPUT = "console"


def get_modules(mod_path, base_class):
    """
    Go through all of the importable modules starting with mod_prefix
    and create a dictionary with the class names and the classes inside that
    contain descendants of base_class
    """
    classdict = {}
    impnames = [(imp, name) for imp, name, is_pkg in pkgutil.walk_packages(mod_path)]
    for imp, name in impnames:
        loader = imp.find_module(name)
        mod = loader.load_module(name)
        for item in dir(mod):
            obj = getattr(mod, item, None)
            if inspect.isclass(obj) and issubclass(obj, base_class) and \
                    obj is not base_class:
                if item in classdict:
                    raise ValueError("We already have a resource named %s coming from %s (we are now at %s)" % (item, classdict[item], obj))
                # Populate the dict. Allow classes to pick their own name via
                # the OPTION class-level var
                classdict[getattr(obj, 'OPTION', item)] = obj
    return classdict


def main():
    """
    No parameters required for main function.
    """
    # Generate the plugin list
    plugin_dict = get_modules(PLUGINS_PREFIX, PluginBaseClass)
    plugins_str = ', '.join(plugin_dict.keys())
    # Generate the output list
    output_dict = get_modules(OUTPUT_PREFIX, OutputBaseClass)
    outputs_str = ', '.join(output_dict.keys())

    # Generate the valid profiles list from your configs as described in:
    # http://boto3.readthedocs.io/en/latest/guide/configuration.html#configuring-credentials
    session = boto3.Session()
    profilelist = session.available_profiles

    # print "To dynamically generate a valid region list we do need valid credentials."
    # Regions
    default_regions = [
        r for r in AWSFact.get_all_regions() if r not in AWSFact.SKIP_REGIONS]

    # Use DEFAULT_OUTPUT if there is such a module, otherwise get the first
    # present one
    actual_default_output = DEFAULT_OUTPUT if DEFAULT_OUTPUT in output_dict \
        else sorted(output_dict.keys())[0]

    # Construct the command-line options
    usage = "Usage: %prog [-P <profile>,<profile>,..]" + \
            "[-o <output_format>] [-r <region>,<region>,..] [-p <plugin>,<plugin>,... ]\n"
    parser = OptionParser(usage=usage)

    parser.add_option(
        "-P", "--profile", action="store", dest="profile",
        help="List of profiles separated by comma.Accepted values are: %s "
        % profilelist,
        default=[]
    )
    parser.add_option(
        "-o", "--output", action="store", dest="output",
        help="Output format. ONE of: %s" % outputs_str,
        default=actual_default_output
    )
    parser.add_option(
        "-p", "--plugins", action="store", dest="plugins",
        help="List of plugins separated by comma.Accepted values are: %s "
        % plugins_str,
        default=plugins_str
    )
    parser.add_option(
        "-r", "--regions", action="store", dest="regions",
        help="List of regions separated by comma.Known good values are: %s "
        % ','.join(default_regions),
        default=[]
    )
    parser.add_option(
        "-a", "--all", action="store_true", dest="all",
        help="Runs all plugins in all regions. You're sure to handle the output?"
    )

    # Parse the given command-line options into the constructed objects
    (options, args) = parser.parse_args()

    # Make sure if no option is passed help will be returned
    if len(sys.argv) == 1 and not options.all:
        parser.print_help()
        quit()

    # If -a|--all is selected, we check for non-default plugin list and
    # for empty region list. That means the -r , -p must have been passed.
    if options.all:
        if options.plugins != plugins_str or options.regions:
            parser.error(
                "option '-a|--all' is mutually exclusive with -p and -r")
        else:
            options.plugins = plugins_str
            print("Running with '-a|--all' - this will take a while .....")

    # Validate profiles
    if options.profile:
        selected_profiles = []
        for prof in options.profile.split(','):
            if prof not in profilelist:
                print('Skipping unknown profile: %s' % prof)
            else:
                selected_profiles.append(prof.strip())
    else:
        selected_profiles = [None]
        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID', None)
        print('No profile passed, thus using AWS_ACCESS_KEY_ID from SHELL env: ', aws_access_key_id)

    # Get the plugin objects from the command-line options and show adequate
    # errors
    selected_plugins = []
    for plug in options.plugins.split(','):
        plugs = plug.strip()
        if not plugs:
            continue
        if plugs not in plugin_dict:
            parser.error('Unknown Plugin: %s' % plugs)
        selected_plugins.append(plugin_dict[plugs])

    if options.output not in output_dict:
        parser.error('Unknown Output: %s' % options.output)
    # Instantiate the desired output class
    output = output_dict[options.output]()

    # Get the desired regions
    selected_regions = [
        reg.strip() for reg in options.regions.split(',')] if options.regions \
        else []
    for profile in selected_profiles:
        for plugin_class in selected_plugins:
            print('Retrieving %s data for profile %s' % (plugin_class.NAME, profile))
            try:
                plugin = plugin_class(profile=profile, regions=selected_regions)

                plugin.retrieve_loop()
                if not plugin.data or not any(plugin.data.values()):
                    print("Plugin %s retrieved no data" % plugin_class.NAME)
                # We still add output of plugins with no data
                output.read_fact(plugin)
            except Exception as err:
                print("Plugin %s skipped due to erroring out: %s" % (plugin_class.NAME, err))

    print(output.all_output())


if __name__ == '__main__':
    main()
