# Copyright (C) 2015 by Per Unneberg
from blaze import DataFrame, odo
from snakemakelib.odo import picard
import pytest
import re

@pytest.fixture(scope="module")
def insert_metrics(tmpdir_factory):
    fn = tmpdir_factory.mktemp('data').join('test.insert_metrics')
    fn.write("""## htsjdk.samtools.metrics.StringHeader
# picard.analysis.CollectInsertSizeMetrics HISTOGRAM_FILE=P001_101/P001_101.sort.merge.rg.dup.hist INPUT=P001_101/P001_101.sort.merge.rg.dup.bam OUTPUT=P001_101/P001_101.sort.merge.rg.dup.insert_metrics REFERENCE_SEQUENCE=chr11.fa VALIDATION_STRINGENCY=SILENT    DEVIATIONS=10.0 MINIMUM_PCT=0.05 METRIC_ACCUMULATION_LEVEL=[ALL_READS] ASSUME_SORTED=true STOP_AFTER=0 VERBOSITY=INFO QUIET=false COMPRESSION_LEVEL=5 MAX_RECORDS_IN_RAM=500000 CREATE_INDEX=false CREATE_MD5_FILE=false
## htsjdk.samtools.metrics.StringHeader
# Started on: Sat May 30 22:22:35 CEST 2015

## METRICS CLASS	picard.analysis.InsertSizeMetrics
MEDIAN_INSERT_SIZE	MEDIAN_ABSOLUTE_DEVIATION	MIN_INSERT_SIZE	MAX_INSERT_SIZE	MEAN_INSERT_SIZE	STANDARD_DEVIATION	READ_PAIRS	PAIR_ORIENTATION	WIDTH_OF_10_PERCENT	WIDTH_OF_20_PERCENT	WIDTH_OF_30_PERCENT	WIDTH_OF_40_PERCENT	WIDTH_OF_50_PERCENT	WIDTH_OF_60_PERCENT	WIDTH_OF_70_PERCENT	WIDTH_OF_80_PERCENT	WIDTH_OF_90_PERCENT	WIDTH_OF_99_PERCENT	SAMPLE	LIBRARY	READ_GROUP
156	39	70	485	167.819235	61.548998	1726	FR	15	29	43	61	79	93	111	133	195	443			

## HISTOGRAM	java.lang.Integer
insert_size	All_Reads.fr_count
70	1
76	2
78	4
""")
    return fn

@pytest.fixture(scope="module")
def align_metrics(tmpdir_factory):
    fn = tmpdir_factory.mktemp('data').join('test.align_metrics')
    fn.write("""## htsjdk.samtools.metrics.StringHeader
# picard.analysis.CollectAlignmentSummaryMetrics INPUT=P001_101/P001_101.sort.merge.rg.dup.bam OUTPUT=P001_101/P001_101.sort.merge.rg.dup.align_metrics REFERENCE_SEQUENCE=chr11.fa VALIDATION_STRINGENCY=SILENT    MAX_INSERT_SIZE=100000 ADAPTER_SEQUENCE=[AATGATACGGCGACCACCGAGATCTACACTCTTTCCCTACACGACGCTCTTCCGATCT, AGATCGGAAGAGCTCGTATGCCGTCTTCTGCTTG, AATGATACGGCGACCACCGAGATCTACACTCTTTCCCTACACGACGCTCTTCCGATCT, AGATCGGAAGAGCGGTTCAGCAGGAATGCCGAGACCGATCTCGTATGCCGTCTTCTGCTTG, AATGATACGGCGACCACCGAGATCTACACTCTTTCCCTACACGACGCTCTTCCGATCT, AGATCGGAAGAGCACACGTCTGAACTCCAGTCACNNNNNNNNATCTCGTATGCCGTCTTCTGCTTG] METRIC_ACCUMULATION_LEVEL=[ALL_READS] IS_BISULFITE_SEQUENCED=false ASSUME_SORTED=true STOP_AFTER=0 VERBOSITY=INFO QUIET=false COMPRESSION_LEVEL=5 MAX_RECORDS_IN_RAM=500000 CREATE_INDEX=false CREATE_MD5_FILE=false
## htsjdk.samtools.metrics.StringHeader
# Started on: Sat May 30 22:22:34 CEST 2015

## METRICS CLASS	picard.analysis.AlignmentSummaryMetrics
CATEGORY	TOTAL_READS	PF_READS	PCT_PF_READS	PF_NOISE_READS	PF_READS_ALIGNED	PCT_PF_READS_ALIGNED	PF_ALIGNED_BASES	PF_HQ_ALIGNED_READS	PF_HQ_ALIGNED_BASES	PF_HQ_ALIGNED_Q20_BASES	PF_HQ_MEDIAN_MISMATCHES	PF_MISMATCH_RATE	PF_HQ_ERROR_RATE	PF_INDEL_RATE	MEAN_READ_LENGTH	READS_ALIGNED_IN_PAIRS	PCT_READS_ALIGNED_IN_PAIRS	BAD_CYCLES	STRAND_BALANCE	PCT_CHIMERAS	PCT_ADAPTER	SAMPLE	LIBRARY	READ_GROUP
FIRST_OF_PAIR	2002	2002	1	0	1992	0.995005	150742	1991	150698	139715	0	0.006223	0.006211	0.00004	76	1945	0.976406	0	0.49498	0	0			
SECOND_OF_PAIR	2002	2002	1	0	1952	0.975025	147881	1952	147881	138323	0	0.006397	0.006397	0.00002	76	1945	0.996414	0	0.504611	0	0			
PAIR	4004	4004	1	0	3944	0.985015	298623	3943	298579	278038	0	0.006309	0.006303	0.00003	76	3890	0.986308	0	0.499746	0	0			


""")
    return fn

def test_hist_metrics(insert_metrics):
    (metrics, hist) = odo(str(insert_metrics), list)
    assert all(metrics["MEDIAN_INSERT_SIZE"] == [156])
    assert all(hist["insert_size"] == [70,76,78])
    

def test_metrics(align_metrics):
    metrics = odo(str(align_metrics), DataFrame)
    assert metrics.loc["FIRST_OF_PAIR"]["MEAN_READ_LENGTH"] == 76


