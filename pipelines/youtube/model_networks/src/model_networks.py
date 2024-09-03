import icsspy

logger = icsspy.initialize_logger()

icsspy.run_in_conda(script="one_mode_networks.py", conda_env_name="gt")
icsspy.run_in_conda(script="two_mode_networks.py", conda_env_name="gt")
