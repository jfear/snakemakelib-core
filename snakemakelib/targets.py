# Copyright (C) 2015 by Per Unneberg
import re
import os
import csv
import snakemake.workflow
from snakemakelib.sample.regexp import RegexpDict
from snakemakelib.utils import find_files
from snakemakelib.log import LoggerManager
from snakemakelib.exceptions import DeprecatedException

smllogger = LoggerManager().getLogger(__name__)

def make_targets(tgt_re, samples, target_suffix=""):
    """Make targets
    
    Create target names based on the target regular expression and a
    target suffix.

    Args:
      tgt_re (RegexpDict): RegexpDict object corresponding to the target
                           regular expression

      samples (list): list of dicts where each dict is an annotated
                      sample. The keys correspond to read group labels.
      target_suffix (str): target suffix to add to target regexp

    Returns:
      targets (list): list of target names
    """
    tgts = list(set(tgt_re.fmt.format(**unit) + target_suffix for unit in samples))
    return tgts

def generic_target_generator(**kwargs):
    raise DeprecatedException("""snakemakelib.targets.generic_target_generator has been deprecated.

    To use the old function, do from snakemakelib.targets import _generic_target_generator
    """)


def _generic_target_generator(tgt_re, src_re=None, samples=[], runs=[],
                             sample_column_map={}, sampleinfo="",
                             target_suffix="", filter_suffix="", **kwargs):
    """Generic target generator.

    Args:
      tgt_re (RegexpDict): RegexpDict object corresponding to the target
                           regular expression
      src_re (RegexpDict): RegexpDict object corresponding to the source
                           regular expression
      samples (list): sample names
      runs (list): run names
      sample_column_map (dict): mapping from sampleinfo column names to
                         regexp group names, e.g.
                         {'SampleID':'SM', 'Lane':'PU1'}
      sampleinfo (str): sample information file
      target_suffix (str): suffix of generated targets
      filter_suffix (str): suffix to use for filtering when generating target
                     names based on input files

    Returns:
      list of target names
    """
    assert isinstance(tgt_re, RegexpDict),\
        "tgt_re argument must be of type {}".format(RegexpDict)
    if src_re is None:
        src_re = tgt_re
    assert isinstance(src_re, RegexpDict),\
        "src_re argument must be of type {}".format(RegexpDict)
    # 1. Generate targets from command line options
    if samples and runs:
        logger.debug("trying to gather target information based on " +
                        "configuration keys 'samples' and 'runs'")
        if len(samples) == len(runs):
            config_list = list(zip(samples, runs))
            mlist = []
            for (s, r) in config_list:
                # Use basename searches for samples and runs
                m = re.search(src_re.basename_pattern, r).groupdict()\
                    if not re.search(src_re.basename_pattern, r) is None else {}
                if m:
                    m.update({'SM': s})
                    mlist.append(m)
            tgts = [tgt_re.fmt.format(**ml) + target_suffix for ml in mlist]
            return sorted(tgts)
        else:
            logger.warn("if samples and runs are provided, they must be of equal lengths")

    # 2. Generate targets from information in samplesheet
    if sampleinfo != "":
        logger.debug("trying to gather target information from configuration key 'sampleinfo'")
        if isinstance(sampleinfo, str) and not os.path.exists(sampleinfo):
            logger.debug("no such sample information file '{sampleinfo}'; trying to deduct targets from existing files".format(sampleinfo=sampleinfo))
        else:
            logger.debug("Reading sample information from '{sampleinfo}'".format(sampleinfo=sampleinfo))
            if isinstance(sampleinfo, str):
                with open(sampleinfo, 'r') as fh:
                    reader = csv.DictReader(fh.readlines())
            else:
                reader = sampleinfo
                assert type(reader) is csv.DictReader,\
                    "sampleinfo is not a 'csv.DictReader'; if not a file name, must be a 'csv.DictReader'"
            reader.fieldnames = [fn if fn not in sample_column_map.keys()
                                 else sample_column_map[fn]
                                 for fn in reader.fieldnames]
            if samples:
                tgts = [tgt_re.fmt.format(**row) + target_suffix
                        for row in reader if row['SM'] in samples]
            else:
                tgts = [tgt_re.fmt.format(**row) + target_suffix
                        for row in reader]
            return sorted(tgts)

    # 3. Generate targets from input files
    logger.debug("Getting sample information from input files")
    inputs = find_files(regexp=src_re.basename_pattern + filter_suffix,
                        limit={'SM': samples} if samples else {})
    if inputs:
        tgts = [tgt_re.fmt.format(**src_re.parse(f))
                + target_suffix for f in inputs]
        return sorted(tgts)
    logger.warn("No targets could be generated!")
    return []