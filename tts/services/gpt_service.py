from openai import OpenAI
from dotenv import load_dotenv
import uuid
import os
from fastapi.responses import FileResponse

class GPTService:
    def __init__(self, tts_service):
        load_dotenv()
        self.tts_service = tts_service
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.sessions = {}

    def get_session_history(self, session_id):
        if session_id not in self.sessions:
            self.sessions[session_id] = [
                {"role": "system", "content": "You are a helpful and emotional AI who remembers and speaks like a close friend. Be natural and conversational."}
            ]
        return self.sessions[session_id]
    
    def chat_and_speak(self, user_text, conversation_id):
        try:
            # 🔮 Call OpenAI
            history = self.get_session_history(conversation_id)
            history.append({"role": "user", "content": user_text})

            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=history,
                max_tokens=300,
                temperature=0.7
            )

            ai_response = completion.choices[0].message.content.strip()
            history.append({"role": "assistant", "content": ai_response})
            print(f"🧠 AI replied: {ai_response}")

            # 🎙️ Convert AI response to speech
            output_file = f"outputs/{uuid.uuid4()}.wav"
            self.tts_service.generate_speech(ai_response, output_path=output_file)

            # 📤 Return the audio file as a streamable response
            return FileResponse(output_file, media_type="audio/wav")

        except Exception as e:
            print(f"Error in GPTService: {e}")
            raise e