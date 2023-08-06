import logging

import click

from covimerage import MergedProfiles, Profile

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


logger = logging.getLogger('covimerage')


@click.group()
@click.version_option()
@click.option('-v', '--verbose', count=True, help='Increase verbosity.')
@click.option('-q', '--quiet', count=True, help='Decrease verbosity.')
def main(verbose, quiet):
    if verbose - quiet:
        logger.setLevel(logger.level - (verbose - quiet) * 10)


@main.command()
@click.argument('filename', required=True, nargs=-1)
@click.option('-o', '--output', required=False, default='.coverage')
def write_coverage(filename, output):
    """Parse FILENAME (output from Vim's :profile)."""
    profiles = []
    for f in filename:
        p = Profile(f)
        try:
            p.parse()
        except FileNotFoundError as exc:
            raise click.FileError(f, exc.strerror)
        profiles.append(p)

    m = MergedProfiles(profiles)
    m.write_coveragepy_data()


@main.command()
@click.argument('cmd', required=False)
@click.option('--vim', required=False, default='nvim')
# @click.option('--vimrc', required=False)
@click.option('--profile_file', required=False,
              default='/tmp/covimerage.profile')
@click.option('--data-file', required=False, type=click.File('w'))
@click.option('--report/--no-report', is_flag=True, default=True)
def run(cmd, vim, profile_file, data_file, report):
    """Run VIM wrapped with :profile instructions."""
    import subprocess

    # args = [vim, '--noplugin', '-N',
    #         '-u', vimrc,
    #         '--cmd', 'profile start /tmp/covimerage.profile',
    #         '--cmd', 'profile! file ./**',
    #         '-c', 'call test_plugin#integration#func1()',
    #         '-cq']
    # if True or not vimrc:
    #     vimrc = 'tests/test_plugin/vimrc'

    cmd = [vim,
           '--cmd', 'profile start %s' % profile_file,
           '--cmd', 'profile! file *']

    logger.info('Running %r.', cmd)
    subprocess.run(cmd)

    p = Profile(profile_file)
    p.parse()
    m = MergedProfiles([p])
    if data_file:
        m.write_coveragepy_data(data_file)

    # if report:

@main.command()
def report():
    """A wrapper around `coverage report`."""
    import coverage

    cov_data = coverage.data.CoverageData()
    cov_data_file = '.coverage.covimerage-run'
    cov_data.read_file(cov_data_file)

    cov_config = coverage.config.CoverageConfig()
    cov_config.data_file = cov_data_file
    cov_config.plugins = ['covimerage']

    cov_coverage = coverage.Coverage(data_file=cov_data_file, config_file=False)
    cov_coverage.config = cov_config
    cov_coverage._init()
    cov_coverage.data = cov_data
    cov_coverage.report()
    return

    reporter = coverage.summary.SummaryReporter(cov_coverage, cov_config)
    reporter.report(morfs=None)
    return
    import pdb
    pdb.set_trace()



    # from coverage import Coverage
    # from coverage.config import CoverageConfig
    #
    # from covimerage.plugin import CoveragePlugin
    # from coverage import CoverageData
    # plugin = CoveragePlugin()
    #
    # cov_config = CoverageConfig()
    # cov_config.data_file = cov_data_file
    # cov_config.plugins = ['covimerage']
    #
    # from coverage.summary import SummaryReporter
    #
    # cov_data = coverage.data.CoverageData()
    # cov_data.write_file(cov_data_file)
    #
    # reporter = SummaryReporter(cov_coverage, cov_config)
    # import pdb
    # pdb.set_trace()
    # return reporter.report(morfs, outfile=file)
    #
    # cov_coverage.set_option('run:plugins', ['covimerage'])
    # # cov_coverage.plugins.add_file_tracer(plugin)
    # cov_coverage.report()
    #
    #
    # # run(['coverage', 'report', '-m'], env={'COVERAGE_FILE': cov_data_file})
