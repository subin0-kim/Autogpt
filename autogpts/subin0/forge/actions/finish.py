from forge.sdk.forge_log import ForgeLogger

from .registry import action

logger = ForgeLogger(__name__)


@action(
    name="finish",
    description="Use this to shut down once you have accomplished all of your goals,"
    " or when there are insurmountable problems that make it impossible"
    " for you to finish your task.",
    parameters=[
        {
            "name": "reason",
            "description": "A summary to the user of how the goals were accomplished",
            "type": "string",
            "required": True,
        }
    ],
    output_type="None",
)
async def finish(
    agent,
    task_id: str,
    reason: str,
) -> str:
    """
    A function that takes in a string and exits the program

    Parameters:
        reason (str): A summary to the user of how the goals were accomplished.
    Returns:
        A result string from create chat completion. A list of suggestions to
            improve the code.
    """
    logger.info(reason, extra={"title": "Shutting down...\n"})
    return reason


@action(
    name="create_vm",
    description ="This function creates a virtual machine (VM). If vm_name not provided, use ask_user to know about virtual machine name.",
    parameters= [
    {
        "name" : "vm_name",
        "description" : "The name of the virtual machine to be created.",
        "type" : "string",
        "required" : True,
    }
    ],
    output_type="None"
)
async def create_vm(agent,
                   task_id: str,
                   vm_name: str,) -> str:
    print(f"\n########### : {vm_name}")
    
    return vm_name

@action(
    name="ask_user",
    description ="If you need more details or information regarding the given goals,"
        " you can ask the user for input",
    parameters= [
    {
        "name" : "question",
        "description" : "The question or prompt to the user",
        "type" : "string",
        "required" : True,
    }
    ],
    output_type="None"
)
async def ask_user(agent,
                   task_id: str,
                   question: str,) -> str:
    print(f"\nQ: {question}")
    return "str"