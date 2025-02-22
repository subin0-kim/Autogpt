import asyncio
import logging
import sys
from pathlib import Path

from autogpt.agent_manager.agent_manager import AgentManager
from autogpt.agents.agent import Agent, AgentConfiguration, AgentSettings
from autogpt.app.main import _configure_openai_provider, run_interaction_loop
from autogpt.commands import COMMAND_CATEGORIES
from autogpt.config import AIProfile, ConfigBuilder
from autogpt.file_storage import FileStorageBackendName, get_storage
from autogpt.logs.config import configure_logging
from autogpt.models.command_registry import CommandRegistry

LOG_DIR = Path(__file__).parent / "logs"


def run_specific_agent(task: str, continuous_mode: bool = False) -> None:
    agent = bootstrap_agent(task, continuous_mode)
    asyncio.run(run_interaction_loop(agent))


def bootstrap_agent(task: str, continuous_mode: bool) -> Agent:
    configure_logging(
        level=logging.DEBUG,
        log_dir=LOG_DIR,
        plain_console_output=True,
    )

    config = ConfigBuilder.build_config_from_env()
    config.continuous_mode = continuous_mode
    config.continuous_limit = 20
    config.noninteractive_mode = True
    config.memory_backend = "no_memory"

    command_registry = CommandRegistry.with_command_modules(COMMAND_CATEGORIES, config)

    ai_profile = AIProfile(
        ai_name="AutoGPT",
        ai_role="a multi-purpose AI assistant.",
        ai_goals=[task],
    )

    agent_prompt_config = Agent.default_settings.prompt_config.copy(deep=True)
    agent_prompt_config.use_functions_api = config.openai_functions
    agent_settings = AgentSettings(
        name=Agent.default_settings.name,
        agent_id=AgentManager.generate_id("AutoGPT-benchmark"),
        description=Agent.default_settings.description,
        ai_profile=ai_profile,
        config=AgentConfiguration(
            fast_llm=config.fast_llm,
            smart_llm=config.smart_llm,
            allow_fs_access=not config.restrict_to_workspace,
            use_functions_api=config.openai_functions,
            plugins=config.plugins,
        ),
        prompt_config=agent_prompt_config,
        history=Agent.default_settings.history.copy(deep=True),
    )

    local = config.file_storage_backend == FileStorageBackendName.LOCAL
    restrict_to_root = not local or config.restrict_to_workspace
    file_storage = get_storage(
        config.file_storage_backend, root_path="data", restrict_to_root=restrict_to_root
    )
    file_storage.initialize()

    agent = Agent(
        settings=agent_settings,
        llm_provider=_configure_openai_provider(config),
        command_registry=command_registry,
        file_storage=file_storage,
        legacy_config=config,
    )
    return agent


if __name__ == "__main__":
    # The first argument is the script name itself, second is the task
    if len(sys.argv) != 2:
        print("Usage: python script.py <task>")
        sys.exit(1)
    task = sys.argv[1]
    run_specific_agent(task, continuous_mode=True)
