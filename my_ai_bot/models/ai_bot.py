from odoo import models, fields, api
import requests

class AiBot(models.Model):
    _name = 'ai.bot'
    _description = 'AI Chatbot for Odoo'

    name = fields.Char(string="Name")
    message = fields.Text(string="User Message")
    response = fields.Text(string="AI Response")

    @api.model
    def get_ai_response(self, message):
        """
        Одоо байгаа AI сервис руу хэрэглэгчийн асуултыг илгээж, хариуг авах.
        """
        api_url = "http://127.0.0.1:11434/api/generate"
        payload = {"model": "llama3.1", "prompt": message}
        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            return response.json().get('response', 'AI response not found.')
        else:
            return "Error: Unable to connect to AI."

    @api.model
    def send_message(self):
        """
        Хэрэглэгчийн мессежийг AI руу илгээж, хариуг хадгалах.
        """
        if self.message:
            ai_response = self.get_ai_response(self.message)
            self.response = ai_response
        else:
            self.response = "Please enter a message."
