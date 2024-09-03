import icsspy

logger = icsspy.initialize_logger()

icsspy.run_in_conda(script="topic_entity_networks.py", conda_env_name="gt")
icsspy.run_in_conda(script="entity_entity_networks.py", conda_env_name="gt")
