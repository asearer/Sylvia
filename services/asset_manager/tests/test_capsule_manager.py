from capsule_manager import CapsuleManager

def test_create_get_capsule():
    cm = CapsuleManager()
    capsule_id = cm.create(["dataset_1"])
    assert cm.get_capsule(capsule_id) == ["dataset_1"]
