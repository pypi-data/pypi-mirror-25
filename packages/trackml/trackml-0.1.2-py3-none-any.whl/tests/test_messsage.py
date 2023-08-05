# Sample Test passing with nose and pytest
import json

from trackml import trackml

def test_pass():
    assert True, "dummy sample test"

def test_json_serialization():
    message = trackml.Message("api_key","experiment_key","run_id")
    message.set_param("num_layers",10)
    message.set_metric("f1",0.8)
    as_json = message.to_json()

    new_obj = json.loads(as_json)
    assert new_obj["metric"]['metricName'] =='f1'
    assert new_obj["metric"]['metricValue'] == '0.8'
