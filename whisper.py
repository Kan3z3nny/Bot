# Copyright (C) @TheSmartBisnu
# Channel: https://t.me/itsSmartDev

import html
import uuid

from pyrogram import Client, filters
from pyrogram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message
)
from pyrogram.enums import ButtonStyle, ParseMode

from motor.motor_asyncio import AsyncIOMotorClient

from config import (
    API_ID,
    API_HASH,
    BOT_TOKEN,
    BOT_USERNAME,
    MONGO_URI
)

app = Client(
    "bot_session",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

bot_username = BOT_USERNAME

mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client["whisper_bot"]
messages_col = db["messages_col"]
history_col = db["history_col"]

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    full_name = message.from_user.first_name
    if message.from_user.last_name:
        full_name += f" {message.from_user.last_name}"
    
    welcome_text = (
        f"Welcome: {full_name}!\n"
        "🌐 I'm the Whisper Bot.\n\n"
        "💬 You can use me to send secret whispers in groups.\n\n"
        "🔮 I work in the Inline mode that means you can use me even if I'm not in the group.\n\n"
        "💌 It is very easy to use me, simply forward a message from a user to which you want to send a whisper and I'll do the rest for you.\n\n"
        "There are other ways to use me too. If you are interested to learn more about me, click on the Help button."
    )
    help_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("Help", callback_data="help", style=ButtonStyle.PRIMARY)]
    ])
    
    await message.reply_text(welcome_text, reply_markup=help_button)

@app.on_callback_query(filters.regex("help"))
async def help_callback(client, callback_query):
    help_text = (
        "The other way to use me is to write the inline query by yourself.\n\n"
        "The format should be in this arrangement:\n\n"
        "`@LockTextBot your whisper @username`\n\n"
        "1. `@LockTextBot`:\n"
        "   This is my username; it should be at the beginning of the inline query so I'll know that you are using me and not another bot.\n\n"
        "2. `whisper message`:\n"
        "   This is the whisper that will be sent to the target user. Replace `your whisper` with your actual message.\n\n"
        "3. `@username`:\n"
        "   You should replace this with the target's username so the bot will know which user should receive your whisper message.\n\n"
        "Example:\n"
        "`@LockTextBot hello this is a test @BisnuRay`\n\n"
        "📎 The bot works in groups and the target user should be in the same group as you.\n\n"
        "What are you waiting for?! Try me now 😉"
    )
    back_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("Back", callback_data="back")]
    ])
    
    await callback_query.message.edit_text(help_text, reply_markup=back_button)

@app.on_callback_query(filters.regex("back"))
async def back_callback(client, callback_query):
    full_name = callback_query.from_user.first_name
    if callback_query.from_user.last_name:
        full_name += f" {callback_query.from_user.last_name}"

    welcome_text = (
        f"Welcome: {full_name}!\n"
        "🌐 I'm the Whisper Bot.\n\n"
        "💬 You can use me to send secret whispers in groups.\n\n"
        "🔮 I work in the Inline mode that means you can use me even if I'm not in the group.\n\n"
        "💌 It is very easy to use me, simply forward a message from a user to which you want to send a whisper and I'll do the rest for you.\n\n"
        "There are other ways to use me too. If you are interested to learn more about me, click on the Help button."
    )
    help_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("Help", callback_data="help", style=ButtonStyle.PRIMARY)]
    ])
    
    await callback_query.message.edit_text(welcome_text, reply_markup=help_button)

async def add_to_history(sender_id, rec_id, rec_name, rec_username):
    user_record = await history_col.find_one({"sender_id": sender_id})
    new_contact = {"id": rec_id, "name": rec_name, "username": rec_username}
    
    if user_record:
        history = user_record.get("recent", [])
        history = [contact for contact in history if contact["id"] != rec_id]
        history.insert(0, new_contact)
        
        if len(history) > 5:
            history = history[:5]
            
        await history_col.update_one(
            {"sender_id": sender_id},
            {"$set": {"recent": history}}
        )
    else:
        await history_col.insert_one({
            "sender_id": sender_id,
            "recent": [new_contact]
        })

@app.on_inline_query()
async def answer(client, inline_query):
    text = inline_query.query.strip()
    sender_id = inline_query.from_user.id

    if not text:
        await inline_query.answer(
            results=[
                InlineQueryResultArticle(
                    id=str(uuid.uuid4()),
                    title="How to Send Secret Message",
                    description="Include the recipient's @username or user ID at the end of your message.",
                    input_message_content=InputTextMessageContent(
                        "How to Send Secret Message\n\n"
                        "Include the recipient's @username or user ID at the end of your message.\n\n"
                        "Example: @LockTextBot Hello there! @username"
                    ),
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("Start Bot", url=f"https://t.me/{bot_username}?start=inline_help", style=ButtonStyle.PRIMARY)]]
                    )
                )
            ],
            cache_time=1
        )
        return

    parts = text.split()
    recipient_identifier = parts[-1]
    
    if not (recipient_identifier.startswith("@") or recipient_identifier.isdigit()):
        results = []
        user_record = await history_col.find_one({"sender_id": sender_id})
        
        if user_record and user_record.get("recent"):
            user_history = user_record["recent"]
            
            for contact in user_history:
                message_content = text 
                message_id = str(uuid.uuid4())
                
                safe_name = html.escape(contact["name"])
                mention_link = f'<a href="tg://user?id={contact["id"]}">{safe_name}</a>'
                
                await messages_col.insert_one({
                    "_id": message_id,
                    "content": message_content,
                    "sender_id": sender_id,
                    "recipient_id": contact["id"],
                    "recipient_name": contact["name"],
                    "mention_link": mention_link,
                    "read": False
                })
                
                whisper_text = f"🔒 Whisper to {mention_link}, only viewable by you and them."
                
                results.append(
                    InlineQueryResultArticle(
                        id=message_id,
                        title=f"A whisper message to {contact['name']}",
                        description=f"Only {contact['name']} can open this whisper.",
                        input_message_content=InputTextMessageContent(
                            whisper_text,
                            parse_mode=ParseMode.HTML
                        ),
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton("💌 Open Whisper", callback_data=message_id, style=ButtonStyle.PRIMARY)]
                        ])
                    )
                )
            
            await inline_query.answer(results, cache_time=1)
            return
        else:
            await inline_query.answer(
                results=[
                    InlineQueryResultArticle(
                        id=str(uuid.uuid4()),
                        title="Keep typing...",
                        description="End your message with @username or User ID to send.",
                        input_message_content=InputTextMessageContent(
                            "Please specify a user to send the whisper to by adding their @username or User ID at the end."
                        ),
                        reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton("Start Bot", url=f"https://t.me/{bot_username}?start=inline_help", style=ButtonStyle.PRIMARY)]]
                        )
                    )
                ],
                cache_time=1
            )
            return

    message_content = " ".join(parts[:-1])
    
    if not message_content:
        return
        
    message_id = str(uuid.uuid4())
    recipient_id = None
    recipient_username = None
    full_name = "the recipient"

    if recipient_identifier.startswith("@"):
        recipient_username = recipient_identifier[1:]
        try:
            recipient_user = await client.get_users(recipient_username)
            recipient_id = recipient_user.id
            full_name = recipient_user.first_name
            if recipient_user.last_name:
                full_name += f" {recipient_user.last_name}"
        except Exception as e:
            await inline_query.answer(
                results=[
                    InlineQueryResultArticle(
                        id=str(uuid.uuid4()),
                        title="Recipient Not Found",
                        description="Recipient not found. Please try again with a valid username.",
                        input_message_content=InputTextMessageContent("Recipient not found. Please try again with a valid username."),
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Learn More", url=f"https://t.me/{bot_username}?start=inline_help", style=ButtonStyle.PRIMARY)]])
                    )
                ],
                cache_time=1
            )
            return
    elif recipient_identifier.isdigit():
        try:
            recipient_id = int(recipient_identifier)
            recipient_user = await client.get_users(recipient_id)
            full_name = recipient_user.first_name
            if recipient_user.last_name:
                full_name += f" {recipient_user.last_name}"
        except Exception as e:
            await inline_query.answer(
                results=[
                    InlineQueryResultArticle(
                        id=str(uuid.uuid4()),
                        title="Ask Recipient to Start the Bot",
                        description="Recipient not found. Ask the recipient to start the bot first.",
                        input_message_content=InputTextMessageContent("The recipient is not found. Please ask the recipient to start the bot first, and then you can send secret messages."),
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Start Bot", url=f"https://t.me/{bot_username}?start=inline_help", style=ButtonStyle.PRIMARY)]])
                    )
                ],
                cache_time=1
            )
            return

    await add_to_history(sender_id, recipient_id, full_name, recipient_username)

    safe_name = html.escape(full_name)
    mention_link = f'<a href="tg://user?id={recipient_id}">{safe_name}</a>'

    await messages_col.insert_one({
        "_id": message_id,
        "content": message_content,
        "sender_id": sender_id,
        "recipient_id": recipient_id,
        "recipient_name": full_name,
        "mention_link": mention_link,
        "read": False
    })

    whisper_message = f"🔒 Whisper to {mention_link}, only viewable by you and them."
    
    results = [
        InlineQueryResultArticle(
            id=message_id,
            title=f"A whisper message to {full_name}",
            description=f"Only {full_name} can open this whisper.",
            input_message_content=InputTextMessageContent(
                whisper_message,
                parse_mode=ParseMode.HTML
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💌 Open Whisper", callback_data=message_id, style=ButtonStyle.PRIMARY)]
            ])
        )
    ]

    await inline_query.answer(results, cache_time=1)

@app.on_callback_query(filters.regex(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"))
async def whisper_callback(client, callback_query):
    message_id = callback_query.data
    user_id = callback_query.from_user.id
    
    message_data = await messages_col.find_one({"_id": message_id})

    if not message_data:
        await callback_query.answer("Message not found or expired.", show_alert=True)
        return

    sender_id = message_data["sender_id"]
    recipient_id = message_data["recipient_id"]

    if user_id == sender_id or user_id == recipient_id:
        message_content = message_data["content"]
        try:
            await callback_query.answer(f"{message_content}", show_alert=True)
            
            if user_id == recipient_id and not message_data.get("read"):
                await messages_col.update_one({"_id": message_id}, {"$set": {"read": True}})
                
                mention_link = message_data.get("mention_link")
                
                updated_text = f"🔓 Whisper to {mention_link} (Read ✅)"
                updated_markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton("💌 Open Whisper", callback_data=message_id, style=ButtonStyle.SUCCESS)]
                ])
                
                await callback_query.edit_message_text(
                    text=updated_text,
                    reply_markup=updated_markup,
                    parse_mode=ParseMode.HTML
                )

        except Exception as e:
            pass
    else:
        await callback_query.answer("Hey Dear! This Message is Not For You", show_alert=True)

app.run()
