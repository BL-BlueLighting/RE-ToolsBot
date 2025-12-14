from toolsbot.configs import DATA_PATH


async def init():
    cfg_path = DATA_PATH / "configuration.toml"
    if not cfg_path.exists():
        # Create a default configuration file if it doesn't exist
        with open(DATA_PATH / "configuration_template.toml", "r", encoding="utf-8") as f:
            default_config = f.read()
        with open(cfg_path, "w", encoding="utf-8") as f:
            f.write(default_config)

async def shutdown():
    pass