import json
from tkmotion.motion_profile import MotionProfile
from tkmotion.motion_profile import TrapezoidalMotionProfile


class MotionProfileLoader:
    """Loader for MotionProfile from a JSON file."""

    def __init__(self):
        """Initialize the MotionProfileLoader."""
        pass

    def load(self, filepath="tkmotion/default_motion_prof.json"):
        """Load motion profile from a JSON file."""

        try:
            with open(filepath, "r") as f:
                profile = json.load(f)
                # リスト先頭のディクショナリを渡す
                if profile[0]["motion_profile"][0]["type"] == "trapezoid":
                    return TrapezoidalMotionProfile(profile[0])
                else:
                    return MotionProfile(profile[0])
        except Exception as e:
            print(f"Error loading motion profile: {e}")
        return None
