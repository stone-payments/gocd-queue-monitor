from src.app.parsers.PipelineParser import PipelineParser


def test_should_extract_pipeline_name_from_full_pipeline_name():
    pipeline_name = 'PipelineName-Staging'
    full_pipeline_name = 'PipelineName-Staging/9/Deploy/1/InstallPackageAndRegisterService'
    pipeline_parser = PipelineParser()
    assert pipeline_parser.extract_pipeline_name(full_pipeline_name) == pipeline_name
