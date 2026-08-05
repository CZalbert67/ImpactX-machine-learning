from impactx_ml.dataset import generate_synthetic_dataset
from impactx_ml.domain import FEATURE_NAMES, Severity


def test_dataset_contains_expected_schema_and_classes():
    dataset = generate_synthetic_dataset(n_samples=800, random_state=7)
    assert len(dataset) == 800
    assert set(FEATURE_NAMES).issubset(dataset.columns)
    assert set(dataset["severity"].unique()) == {severity.value for severity in Severity}
