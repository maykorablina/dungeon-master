from g4f.client import Client

class DungeonMaster:
    def __init__(self, user_id, prompt_file='src/text/game_rules.txt'):
        self.user_id = user_id
        self.chat_history = {}
        self.prompt_file = prompt_file
        self.client = Client()
        self.initialize_prompt()

    def initialize_prompt(self):
        prompt = open(self.prompt_file, encoding='utf-8').read().strip()
        self.set_prompt(self.user_id, prompt)

    def remember_user_message(self, role, content):
        if self.user_id not in self.chat_history:
            self.chat_history[self.user_id] = []
        self.chat_history[self.user_id].append({"role": role, "content": content})

    def set_prompt(self, user_id, prompt):
        self.chat_history[user_id] = [{"role": "system", "content": prompt}]

    def chat(self, user_message):
        if self.user_id not in self.chat_history or len(self.chat_history[self.user_id]) == 0:
            self.initialize_prompt()

        self.remember_user_message("user", user_message)

        messages = self.chat_history[self.user_id]

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )

        model_response = response.choices[0].message.content

        self.remember_user_message("assistant", model_response)

        return model_response