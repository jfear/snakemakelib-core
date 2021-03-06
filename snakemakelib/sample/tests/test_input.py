# Copyright (C) 2015 by Per Unneberg
# pylint: disable=R0904, C0301, C0103
import csv
import pytest
from snakemakelib.sample.input import _parse_sampleinfo, _samples_from_input_files, initialize_input
from snakemakelib.sample.organization import config, illumina_scilife


@pytest.fixture(scope="module")
def illumina_scilife_files():
    """Input file names following naming conventions at SciLife"""
    return [
        "P001_102/120924_AC003CCCXX/2_120924_AC003CCCXX_P001_102_1.fastq.gz",
        "P001_101/121015_BB002BBBXX/1_121015_BB002BBBXX_P001_101_1.fastq.gz",
        "P001_101/120924_AC003CCCXX/1_120924_AC003CCCXX_P001_101_1.fastq.gz"
    ]




class TestParseSampleinfo:
    def test_parse_sampleinfo(self):
        samples = _parse_sampleinfo(sampleinfo=csv.DictReader(['SM\n', 'Sample1\n', 'Sample2\n']))
        assert samples == [{'SM':'Sample1'}, {'SM':'Sample2'}]

    def test_parse_sampleinfo_samplecolumn(self):
        samples = _parse_sampleinfo(sampleinfo=csv.DictReader(['Sample\n', 'Sample1\n', 'Sample2\n']),
                                   sample_column_map={'Sample': 'SM', 'Platform': 'PL'})
        assert samples == [{'SM':'Sample1'}, {'SM':'Sample2'}]

    def test_parse_sampleinfo_wrong_samplecolumn(self):
        samples = _parse_sampleinfo(sampleinfo=csv.DictReader(['Sample\n', 'Sample1\n', 'Sample2\n']),
                                   sample_column_map={'SMM': 'SM', 'Platform': 'PL'})
        assert samples == [{'Sample':'Sample1'}, {'Sample':'Sample2'}]


class TestSamplesFromInputFiles:
    def test_samples_from_input_files(self, illumina_scilife_files, mocker):
        mock_find = mocker.patch('snakemakelib.sample.input.find_files')
        mock_find.return_value = illumina_scilife_files
        samples = _samples_from_input_files(config['settings']['sample_organization'].run_id_re)
        assert samples[0] == {'SM': 'P001_102', 'DT': '120924', 'PU2': '2', 'PU': 'AC003CCCXX_2', 'PU1': 'AC003CCCXX'}



class TestInitializeInput:
    def test_initialize_input(self, mocker):
        mock_samples = mocker.patch('snakemakelib.sample.input._samples_from_input_files')
        mock_samples.return_value = [{'SM': 'P001_102', 'DT': '120924', 'PU2': '2', 'PU': 'AC003CCCXX_2', 'PU1': 'AC003CCCXX'},
                                     {'SM': 'P001_101', 'DT': '120924', 'PU2': '1', 'PU': 'AC003CCCXX_1', 'PU1': 'AC003CCCXX'},
                                     {'SM': 'P001_101', 'DT': '121015', 'PU2': '1', 'PU': 'BB002BBBXX_1', 'PU1': 'BB002BBBXX'}]
        samples = initialize_input(src_re=config['settings']['sample_organization'].run_id_re, sample_filter=["P001_101"])
        assert len(samples) == 2
        assert not 'P001_102' in [s['SM'] for s in samples]
        

    def test_initalize_input_common_prefix(self, mocker):
        mock_samples = mocker.patch('snakemakelib.sample.input._samples_from_input_files')
        mock_samples.return_value = [{'SM': 'SM_1', 'DT': '120924', 'PU2': '2', 'PU': 'AC003CCCXX_2', 'PU1': 'AC003CCCXX'},
                                     {'SM': 'SM_2', 'DT': '120924', 'PU2': '1', 'PU': 'AC003CCCXX_1', 'PU1': 'AC003CCCXX'},
                                     {'SM': 'SM_11', 'DT': '121015', 'PU2': '1', 'PU': 'BB002BBBXX_1', 'PU1': 'BB002BBBXX'}]
        samples = initialize_input(src_re=config['settings']['sample_organization'].run_id_re, sample_filter=["SM_11"])
        assert len(samples) == 1
        samples = initialize_input(src_re=config['settings']['sample_organization'].run_id_re, sample_filter=["SM_1"])
        assert len(samples) == 1


    def test_initialize_input_sample_filter(self, mocker):
        mock_samples = mocker.patch('snakemakelib.sample.input._samples_from_input_files')
        mock_samples.return_value = [{'SM': 'SM_1', 'DT': '120924', 'PU2': '2', 'PU': 'AC003CCCXX_2', 'PU1': 'AC003CCCXX'},
                                     {'SM': 'SM_2', 'DT': '120924', 'PU2': '1', 'PU': 'AC003CCCXX_1', 'PU1': 'AC003CCCXX'},
                                     {'SM': 'SM_11', 'DT': '121015', 'PU2': '1', 'PU': 'BB002BBBXX_1', 'PU1': 'BB002BBBXX'}]
        samples = initialize_input(src_re=config['settings']['sample_organization'].run_id_re, sample_filter="['SM_11']")
        assert len(samples) == 1
        samples = initialize_input(src_re=config['settings']['sample_organization'].run_id_re, sample_filter="['SM_11','SM_1']")
        assert len(samples) == 2
        samples = initialize_input(src_re=config['settings']['sample_organization'].run_id_re, sample_filter=["SM_1", "SM_11"])
        assert len(samples) == 2
        samples = initialize_input(src_re=config['settings']['sample_organization'].run_id_re, sample_filter='"SM_2" "SM_1","SM_11"')
        assert len(samples) == 1

