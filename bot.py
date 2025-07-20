import time
import logging
from database import Database
from telegram_api import TelegramAPI
from config import Config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ForwardBot:
    def __init__(self):
        self.api = TelegramAPI(Config.BOT_TOKEN)
        self.db = Database()
        self.last_update_id = 0
        
    def is_admin(self, user_id):
        return user_id in Config.ADMIN_IDS
        
    def process_message(self, message):
        try:
            if "text" in message:
                text = message["text"]
                chat_id = message["chat"]["id"]
                user_id = message["from"]["id"]
                
                if text.startswith("/start"):
                    self.handle_start(chat_id, user_id)
                elif text.startswith("/setchat"):
                    self.handle_setchat(chat_id, user_id, text)
                elif text.startswith("/delchat"):
                    self.handle_delchat(chat_id, user_id, text)
                elif text.startswith("/listchats"):
                    self.handle_listchats(chat_id, user_id)
                    
            elif "forward_from_chat" in message:
                self.handle_channel_post(message)
                
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            
    def handle_start(self, chat_id, user_id):
        help_text = (
            "🤖 Auto-Forward Bot\n\n"
            "Admin Commands:\n"
            "/setchat [source] [target1,target2] - Configure forwarding\n"
            "/delchat [source] - Remove forwarding\n"
            "/listchats - List current rules"
        )
        self.api.send_message(chat_id, help_text)
        
    def handle_setchat(self, chat_id, user_id, text):
        if not self.is_admin(user_id):
            self.api.send_message(chat_id, "❌ Unauthorized")
            return
            
        try:
            parts = text.split()
            if len(parts) < 3:
                self.api.send_message(chat_id, "Usage: /setchat [source] [target1,target2]")
                return
                
            source = int(parts[1])
            targets = [int(t) for t in parts[2].split(",")]
            
            self.db.add_forward_rule(source, targets)
            self.api.send_message(chat_id, f"✅ Rule added: {source} → {targets}")
            
        except Exception as e:
            self.api.send_message(chat_id, f"❌ Error: {str(e)}")
            
    def handle_delchat(self, chat_id, user_id, text):
        if not self.is_admin(user_id):
            self.api.send_message(chat_id, "❌ Unauthorized")
            return
            
        try:
            parts = text.split()
            if len(parts) < 2:
                self.api.send_message(chat_id, "Usage: /delchat [source]")
                return
                
            source = int(parts[1])
            self.db.remove_forward_rule(source)
            self.api.send_message(chat_id, f"✅ Rule removed for {source}")
            
        except Exception as e:
            self.api.send_message(chat_id, f"❌ Error: {str(e)}")
            
    def handle_listchats(self, chat_id, user_id):
        if not self.is_admin(user_id):
            self.api.send_message(chat_id, "❌ Unauthorized")
            return
            
        rules = self.db.get_forward_rules()
        if not rules:
            self.api.send_message(chat_id, "No forwarding rules configured")
            return
            
        response = "📋 Forwarding Rules:\n\n"
        for source, targets in rules.items():
            response += f"🔹 {source} → {', '.join(map(str, targets))}\n"
            
        self.api.send_message(chat_id, response)
        
    def handle_channel_post(self, message):
        try:
            source_chat = message["forward_from_chat"]["id"]
            message_id = message["message_id"]
            
            rules = self.db.get_forward_rules()
            if source_chat in rules:
                for target in rules[source_chat]:
                    self.api.forward_message(target, source_chat, message_id)
                    logger.info(f"Forwarded {message_id} from {source_chat} to {target}")
                    
        except Exception as e:
            logger.error(f"Error forwarding message: {e}")
            
    def run(self):
        logger.info("Starting bot...")
        try:
            while True:
                updates = self.api.get_updates(self.last_update_id + 1)
                
                if updates.get("ok"):
                    for update in updates["result"]:
                        self.last_update_id = update["update_id"]
                        
                        if "message" in update:
                            self.process_message(update["message"])
                        elif "channel_post" in update:
                            self.process_message(update["channel_post"])
                            
                time.sleep(Config.POLL_INTERVAL)
                
        except KeyboardInterrupt:
            logger.info("Stopping bot...")
        finally:
            self.db.close()

if __name__ == "__main__":
    bot = ForwardBot()
    bot.run()
