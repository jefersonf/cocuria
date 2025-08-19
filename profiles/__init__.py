from pathlib import Path
import yaml

class AgentProfileLoader:
    def __init__(self):
        self.profile_dir = Path(__file__).parent / "roles"
        self.profiles = {}
        self._load_profiles()

    def _load_profiles(self):
        for yaml_file in self.profile_dir.glob("*.yaml"):
            with open(yaml_file, "r") as f:
                profile = yaml.safe_load(f)
                if "extends" in profile:
                    base = self._load_base_profile(profile["extends"])
                    profile = self._merge_profiles(base, profile)
                self.profiles[profile["role"]] = profile

    def _load_base_profile(self, base_name):
        base_path = self.profile_dir / f"{base_name}.yaml"
        if base_path.exists():
            with open(base_path, "r") as f:
                return yaml.safe_load(f)
        return {}

    def _merge_profiles(self, base, extension):
        merged = base.copy()
        for key, value in extension.items():
            if isinstance(value, dict) and key in merged:
                merged[key].update(value)
            else:
                merged[key] = value
        return merged

    def get_profile(self, role_name):
        return self.profiles.get(role_name)
