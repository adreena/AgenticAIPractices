from helper import print_in_box, do_chat_completion
from textwrap import dedent

class ChatAgent:
    system_prompt = "You are a helpful assistant."
    messages = []

    def __init__(self, name, system_prompt, client, model):
        self.name = name or self.__class__.__name__
        
        self.system_prompt = system_prompt
        self.client = client
        self.model = model
        self.reset()

    def add_message(self, role, content):
        
        self.messages.append({"role": role, "content": content})
        if role == "system":
            print_in_box(
                content,
                f"{self.name} - System Prompt",
            )
        elif role == "user":
            print_in_box(
                content,
                f"{self.name} - User Prompt",
            )
        elif role == "assistant":
            print_in_box(
                content,
                f"{self.name} - Assistant Response",
            )

    def reset(self):
        system_prompt = dedent(self.system_prompt).strip()

        # Clear previous messages and add the system prompt
        self.messages = []
        self.add_message(
            "system",
            system_prompt,
        )

    def get_response(self, add_to_messages=True, model=None, client=None, **kwargs):
        response = do_chat_completion(
            messages=self.messages,
            model=model or self.model,
            client=client or self.client,
            **kwargs
        )
        if add_to_messages:
            self.add_message("assistant", response)
        return response

    def chat(self, user_message, add_to_messages=True, model=None, **kwargs):
        self.add_message("user", user_message)
        return self.get_response(add_to_messages=add_to_messages, model=model, **kwargs)

