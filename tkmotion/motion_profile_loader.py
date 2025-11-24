class MotionProfileLoader:
    def __init__(self, filepath="tkmotion/default_motion_prof.json"):
        self.filepath = filepath
        self.profile = []

    def load(self):
        import json

        try:
            with open(self.filepath, "r") as f:
                self.profile = json.load(f)
        except Exception as e:
            print(f"Error loading motion profile: {e}")
        return self.profile
