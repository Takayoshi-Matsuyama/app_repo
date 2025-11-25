from tkmotion.motion_profile import MotionProfile


class MotionProfileLoader:
    def __init__(self):
        pass

    def load(self, filepath="tkmotion/default_motion_prof.json"):
        import json

        try:
            with open(filepath, "r") as f:
                profile = json.load(f)
                return MotionProfile(profile)
        except Exception as e:
            print(f"Error loading motion profile: {e}")
        return None
