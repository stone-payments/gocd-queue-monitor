import pytest
from src.app.models.Pipeline import Pipeline



def test_should_extract_pipeline_name_from_full_pipeline_name():
    pipeline_name = 'PipelineName-Staging'
    full_pipeline_name = 'PipelineName-Staging/9/Deploy/1/InstallPackageAndRegisterService'
    assert Pipeline.extract_pipeline_name(full_pipeline_name) == pipeline_name
        