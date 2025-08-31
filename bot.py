# don'/t. ski please'

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    JobQueue,
    ApplicationBuilder,
    MessageHandler,
    filters,
    CallbackQueryHandler
)
import pytz
from datetime import datetime
import logging
import json
import os
import random
import string

TOKEN = "hhhhhhhhhhh"
ADMIN_IDS = [8427760533]
DATA_FILE = "bot_data.json"

REFERRAL_POINTS = 5
CHANNEL_POINTS = 10

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    user_channels = data.get('user_channels', {})
    active_jobs = {}
    banned_users = set(data.get('banned_users', []))
    user_points = data.get('user_points', {})
    referral_codes = data.get('referral_codes', {})
    used_referrals = data.get('used_referrals', {})
    channel_points = data.get('channel_points', CHANNEL_POINTS)
else:
    user_channels = {}
    active_jobs = {}
    banned_users = set()
    user_points = {}
    referral_codes = {}
    used_referrals = {}
    channel_points = CHANNEL_POINTS

FONT_STYLES = {
    1: "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗",
    2: "𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡",
    3: "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵",
    4: "𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿",
    5: "0123456789",
}

def save_data():
    data = {
        'user_channels': user_channels,
        'banned_users': list(banned_users),
        'user_points': user_points,
        'referral_codes': referral_codes,
        'used_referrals': used_referrals,
        'channel_points': channel_points
    }
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

def generate_referral_code(user_id: int) -> str:
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    referral_codes[code] = user_id
    save_data()
    return code

def convert_to_font(time_str: str, font_style: int) -> str:
    if font_style not in FONT_STYLES:
        return time_str
    
    font_digits = FONT_STYLES[font_style]
    normal_digits = "0123456789"
    translation_table = str.maketrans(normal_digits, font_digits)
    return time_str.translate(translation_table)

async def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args
    
    if user.id in banned_users:
        await update.message.reply_text("⛔ شما از استفاده از این ربات محروم شده‌اید.")
        return
    
    if args and args[0] in referral_codes:
        referral_code = args[0]
        referrer_id = referral_codes[referral_code]
        
        if user.id == referrer_id:
            await update.message.reply_text("❌ نمی‌توانید از کد رفرال خودتان استفاده کنید!")
            return
            
        if user.id in used_referrals:
            await update.message.reply_text("❌ شما قبلاً از یک کد رفرال استفاده کرده‌اید!")
            return
            
        used_referrals[user.id] = referrer_id
        user_points[referrer_id] = user_points.get(referrer_id, 0) + REFERRAL_POINTS
        user_points[user.id] = user_points.get(user.id, 0) + REFERRAL_POINTS
        save_data()
        
        await update.message.reply_text(f"✅ کد رفرال با موفقیت اعمال شد! شما و معرف شما هر کدام {REFERRAL_POINTS} امتیاز دریافت کردید.")
    
    if user.id not in referral_codes.values():
        generate_referral_code(user.id)
    
    if await is_admin(user.id):
        keyboard = [
            [
                InlineKeyboardButton("➕ ثبت کانال/گروه جدید", callback_data="add_channel"),
                InlineKeyboardButton("🗑 حذف کانال/گروه", callback_data="remove_channel")
            ],
            [
                InlineKeyboardButton("🖋 تغییر فونت", callback_data="set_font"),
                InlineKeyboardButton("🛠 پنل مدیریت", callback_data="admin_panel")
            ],
            [
                InlineKeyboardButton("🎁 سیستم امتیاز", callback_data="points_system"),
                InlineKeyboardButton("📊 لینک رفرال من", callback_data="my_referral")
            ]
        ]
    else:
        keyboard = [
            [
                InlineKeyboardButton("➕ ثبت کانال/گروه جدید", callback_data="add_channel"),
                InlineKeyboardButton("🗑 حذف کانال/گروه", callback_data="remove_channel")
            ],
            [
                InlineKeyboardButton("🖋 تغییر فونت", callback_data="set_font")
            ],
            [
                InlineKeyboardButton("🎁 سیستم امتیاز", callback_data="points_system"),
                InlineKeyboardButton("📊 لینک رفرال من", callback_data="my_referral")
            ]
        ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    points = user_points.get(user.id, 0)
    await update.message.reply_text(
        f"سلام {user.first_name}!\n\n"
        f"🤖 ربات مدیریت زمان کانال/گروه\n\n"
        f"🏆 امتیاز شما: {points}\n\n"
        "از دکمه‌های زیر برای مدیریت کانال‌ها/گروه‌ها استفاده کنید:",
        reply_markup=reply_markup
    )

async def points_system(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    points = user_points.get(user_id, 0)
    
    await query.edit_message_text(
        f"🎁 سیستم امتیازدهی\n\n"
        f"🏆 امتیاز شما: {points}\n\n"
        f"🔹 هر رفرال موفق: {REFERRAL_POINTS} امتیاز\n"
        f"🔹 ثبت هر کانال/گروه: {channel_points} امتیاز (کسر می‌شود)\n\n"
        "برای دریافت لینک رفرال خود روی دکمه زیر کلیک کنید:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📊 لینک رفرال من", callback_data="my_referral")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back")]
        ])
    )

async def my_referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    code = next((k for k, v in referral_codes.items() if v == user_id), None)
    
    if not code:
        code = generate_referral_code(user_id)
    
    referral_link = f"https://t.me/{context.bot.username}?start={code}"
    points = user_points.get(user_id, 0)
    
    await query.edit_message_text(
        f"📊 لینک رفرال شما\n\n"
        f"🔗 لینک اختصاصی:\n{referral_link}\n\n"
        f"💰 با هر رفرال موفق:\n"
        f"• شما {REFERRAL_POINTS} امتیاز دریافت می‌کنید\n"
        f"• دوست شما هم {REFERRAL_POINTS} امتیاز می‌گیرد\n\n"
        f"🏆 امتیاز کل شما: {points}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 بازگشت", callback_data="points_system")]
        ])
    )

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if not await is_admin(query.from_user.id):
        await query.edit_message_text("❌ شما دسترسی ادمین ندارید!")
        return
    
    keyboard = [
        [
            InlineKeyboardButton("📊 آمار ربات", callback_data="stats"),
            InlineKeyboardButton("🚫 بن کاربر", callback_data="ban_user")
        ],
        [
            InlineKeyboardButton("✅ آنبن کاربر", callback_data="unban_user"),
            InlineKeyboardButton("📋 لیست کانال‌ها/گروه‌ها", callback_data="channel_list")
        ],
        [
            InlineKeyboardButton("🎯 مدیریت امتیازها", callback_data="manage_points"),
            InlineKeyboardButton("⚙️ تنظیم امتیاز کانال/گروه", callback_data="set_channel_points")
        ],
        [
            InlineKeyboardButton("🔙 بازگشت", callback_data="back")
        ]
    ]
    
    await query.edit_message_text(
        "🛠 پنل مدیریت\n\n"
        "لطفاً یکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if not await is_admin(query.from_user.id):
        await query.edit_message_text("❌ شما دسترسی ادمین ندارید!")
        return
    
    total_users = len(user_channels)
    total_channels = sum(len(channels) for channels in user_channels.values())
    total_banned = len(banned_users)
    total_points = sum(user_points.values()) if user_points else 0
    
    total_used_referrals = len(used_referrals)
    
    total_referral_codes = len(referral_codes)
    
    await query.edit_message_text(
        f"📊 آمار کامل ربات:\n\n"
        f"👤 کاربران فعال: {total_users}\n"
        f"📌 کانال‌ها/گروه‌های ثبت شده: {total_channels}\n"
        f"🚫 کاربران بن شده: {total_banned}\n"
        f"🏆 مجموع امتیازهای کاربران: {total_points}\n"
        f"⭐ امتیاز مورد نیاز برای هر کانال/گروه: {channel_points}\n"
        f"🔗 کدهای رفرال تولید شده: {total_referral_codes}\n"
        f"📩 کدهای رفرال استفاده شده: {total_used_referrals}\n"
        f"💰 امتیاز هر رفرال موفق: {REFERRAL_POINTS}",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="admin_panel")]])
    )

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if not await is_admin(query.from_user.id):
        await query.edit_message_text("❌ شما دسترسی ادمین ندارید!")
        return
    
    await query.edit_message_text(
        "لطفاً آیدی عددی کاربر را برای بن کردن ارسال کنید:",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="admin_panel")]])
    )
    context.user_data["awaiting_ban"] = True

async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if not await is_admin(query.from_user.id):
        await query.edit_message_text("❌ شما دسترسی ادمین ندارید!")
        return
    
    await query.edit_message_text(
        "لطفاً آیدی عددی کاربر را برای آنبن کردن ارسال کنید:",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="admin_panel")]])
    )
    context.user_data["awaiting_unban"] = True

async def channel_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if not await is_admin(query.from_user.id):
        await query.edit_message_text("❌ شما دسترسی ادمین ندارید!")
        return
    
    if not user_channels:
        await query.edit_message_text(
            "هنوز هیچ کانال/گروهی ثبت نشده است.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="admin_panel")]])
        )
        return
    
    message = "📋 لیست کانال‌ها/گروه‌های ثبت شده:\n\n"
    for user_id, channels in user_channels.items():
        message += f"👤 کاربر {user_id} (امتیاز: {user_points.get(user_id, 0)}):\n"
        for channel_id, data in channels.items():
            message += f"  - {data['base_name']} (ID: {channel_id})\n"
    
    max_length = 4096
    for i in range(0, len(message), max_length):
        part = message[i:i+max_length]
        if i == 0:
            await query.edit_message_text(
                part,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="admin_panel")]])
            )
        else:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=part
            )

async def manage_points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if not await is_admin(query.from_user.id):
        await query.edit_message_text("❌ شما دسترسی ادمین ندارید!")
        return
    
    await query.edit_message_text(
        "لطفاً آیدی کاربر و مقدار امتیاز را به صورت زیر ارسال کنید:\n\n"
        "مثال:\n"
        "123456789 +10 (برای اضافه کردن امتیاز)\n"
        "123456789 -5 (برای کم کردن امتیاز)",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_panel")]
        ])
    )
    context.user_data["awaiting_points"] = True

async def set_channel_points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if not await is_admin(query.from_user.id):
        await query.edit_message_text("❌ شما دسترسی ادمین ندارید!")
        return
    
    await query.edit_message_text(
        f"امتیاز فعلی برای هر کانال/گروه: {channel_points} (کسر می‌شود)\n\n"
        "لطفاً مقدار جدید امتیاز برای هر کانال/گروه را ارسال کنید:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_panel")]
        ])
    )
    context.user_data["awaiting_channel_points"] = True

async def add_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    if user_id in banned_users:
        await query.edit_message_text("⛔ شما از استفاده از این ربات محروم شده‌اید.")
        return
    
    current_points = user_points.get(user_id, 0)
    if current_points < channel_points:
        await query.edit_message_text(
            f"❌ امتیاز کافی ندارید!\n\n"
            f"برای ثبت کانال/گروه به {channel_points} امتیاز نیاز دارید.\n"
            f"امتیاز فعلی شما: {current_points}\n\n"
            "می‌توانید با معرفی دوستان از طریق سیستم رفرال امتیاز کسب کنید.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="back")]])
        )
        return
    
    await query.edit_message_text(
        "لطفاً آیدی کانال/گروه را به صورت عددی ارسال کنید (مثال: -1001234567890)\n\n"
        "📌 برای دریافت آیدی کانال/گروه:\n"
        "یک پیام از کانال/گروه به @RawDataBot فوروارد کنید",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="back")]])
    )
    context.user_data["awaiting_channel_id"] = True

async def remove_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    if user_id not in user_channels or not user_channels[user_id]:
        await query.edit_message_text(
            "شما هیچ کانال/گروهی ثبت نکرده‌اید.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="back")]])
        )
        return
        
    keyboard = []
    for channel_id in user_channels[user_id]:
        base_name = user_channels[user_id][channel_id]["base_name"]
        keyboard.append([InlineKeyboardButton(f"حذف {base_name}", callback_data=f"remove_{channel_id}")])
    
    keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data="back")])
    
    await query.edit_message_text(
        "لطفاً کانال/گروه مورد نظر برای حذف را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def set_font(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟡 (پررنگ)", callback_data="font_1")],
        [InlineKeyboardButton("𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡 (دوبل)", callback_data="font_2")],
        [InlineKeyboardButton("𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵 (ساده)", callback_data="font_3")],
        [InlineKeyboardButton("𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿 (تک‌فاصله)", callback_data="font_4")],
        [InlineKeyboardButton("0123456789 (پیش‌فرض)", callback_data="font_5")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="back")]
    ]
    
    await query.edit_message_text(
        "لطفاً فونت مورد نظر را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "admin_panel":
        await admin_panel(update, context)
    elif query.data == "stats":
        await show_stats(update, context)
    elif query.data == "ban_user":
        await ban_user(update, context)
    elif query.data == "unban_user":
        await unban_user(update, context)
    elif query.data == "channel_list":
        await channel_list(update, context)
    elif query.data == "manage_points":
        await manage_points(update, context)
    elif query.data == "set_channel_points":
        await set_channel_points(update, context)
    elif query.data == "points_system":
        await points_system(update, context)
    elif query.data == "my_referral":
        await my_referral(update, context)
    elif query.data == "add_channel":
        await add_channel(update, context)
    elif query.data == "remove_channel":
        await remove_channel(update, context)
    elif query.data.startswith("remove_"):
        channel_id = query.data.split("_")[1]
        user_id = query.from_user.id
        
        if channel_id in active_jobs:
            active_jobs[channel_id].schedule_removal()
            del active_jobs[channel_id]
        
        if user_id in user_channels and channel_id in user_channels[user_id]:
            del user_channels[user_id][channel_id]
            save_data()
        
        await query.edit_message_text(
            f"کانال/گروه با موفقیت حذف شد.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="back")]])
        )
    elif query.data == "set_font":
        await set_font(update, context)
    elif query.data.startswith("font_"):
        font_style = int(query.data.split("_")[1])
        user_id = query.from_user.id
        
        if user_id in user_channels:
            for channel_id in user_channels[user_id]:
                user_channels[user_id][channel_id]["font_style"] = font_style
            save_data()
        
        sample_time = convert_to_font("12:34", font_style)
        
        await query.edit_message_text(
            f"✅ فونت اعداد با موفقیت تغییر کرد\n\n"
            f"نمونه زمان با فونت جدید:\n"
            f"{sample_time}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت", callback_data="back")]])
        )
    elif query.data == "back":
        user = query.from_user
        
        if await is_admin(user.id):
            keyboard = [
                [
                    InlineKeyboardButton("➕ ثبت کانال/گروه جدید", callback_data="add_channel"),
                    InlineKeyboardButton("🗑 حذف کانال/گروه", callback_data="remove_channel")
                ],
                [
                    InlineKeyboardButton("🖋 تغییر فونت", callback_data="set_font"),
                    InlineKeyboardButton("🛠 پنل مدیریت", callback_data="admin_panel")
                ],
                [
                    InlineKeyboardButton("🎁 سیستم امتیاز", callback_data="points_system"),
                    InlineKeyboardButton("📊 لینک رفرال من", callback_data="my_referral")
                ]
            ]
        else:
            keyboard = [
                [
                    InlineKeyboardButton("➕ ثبت کانال/گروه جدید", callback_data="add_channel"),
                    InlineKeyboardButton("🗑 حذف کانال/گروه", callback_data="remove_channel")
                ],
                [
                    InlineKeyboardButton("🖋 تغییر فونت", callback_data="set_font")
                ],
                [
                    InlineKeyboardButton("🎁 سیستم امتیاز", callback_data="points_system"),
                    InlineKeyboardButton("📊 لینک رفرال من", callback_data="my_referral")
                ]
            ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        points = user_points.get(user.id, 0)
        await query.edit_message_text(
            f"سلام {user.first_name}!\n\n"
            f"🤖 ربات مدیریت زمان کانال/گروه\n\n"
            f"🏆 امتیاز شما: {points}\n\n"
            "از دکمه‌های زیر برای مدیریت کانال‌ها/گروه‌ها استفاده کنید:",
            reply_markup=reply_markup
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message_text = update.message.text.strip()
    
    if user.id in banned_users:
        await update.message.reply_text("⛔ شما از استفاده از این ربات محروم شده‌اید.")
        return
    
    if "awaiting_points" in context.user_data and context.user_data["awaiting_points"]:
        if not await is_admin(user.id):
            await update.message.reply_text("❌ شما دسترسی ادمین ندارید!")
            return
            
        try:
            parts = message_text.split()
            user_id = int(parts[0])
            points_change = int(parts[1])
            
            current_points = user_points.get(user_id, 0)
            new_points = current_points + points_change
            user_points[user_id] = new_points
            save_data()
            
            await update.message.reply_text(
                f"✅ امتیاز کاربر {user_id} با موفقیت تغییر کرد.\n"
                f"امتیاز جدید: {new_points}"
            )
        except (ValueError, IndexError):
            await update.message.reply_text("❌ فرمت پیام نادرست است!")
        finally:
            del context.user_data["awaiting_points"]

    elif "awaiting_channel_points" in context.user_data and context.user_data["awaiting_channel_points"]:
        if not await is_admin(user.id):
            await update.message.reply_text("❌ شما دسترسی ادمین ندارید!")
            return
            
        try:
            global channel_points
            channel_points = int(message_text)
            save_data()
            
            await update.message.reply_text(
                f"✅ امتیاز هر کانال/گروه با موفقیت به {channel_points} تغییر کرد."
            )
        except ValueError:
            await update.message.reply_text("❌ لطفاً یک عدد معتبر وارد کنید!")
        finally:
            del context.user_data["awaiting_channel_points"]
    
    elif "awaiting_ban" in context.user_data and context.user_data["awaiting_ban"]:
        if not await is_admin(user.id):
            await update.message.reply_text("❌ شما دسترسی ادمین ندارید!")
            return
            
        try:
            user_id = int(message_text.strip())
            banned_users.add(user_id)
            save_data()
            await update.message.reply_text(f"✅ کاربر {user_id} با موفقیت بن شد.")
        except ValueError:
            await update.message.reply_text("❌ لطفاً یک آیدی عددی معتبر وارد کنید.")
        finally:
            del context.user_data["awaiting_ban"]
    
    elif "awaiting_unban" in context.user_data and context.user_data["awaiting_unban"]:
        if not await is_admin(user.id):
            await update.message.reply_text("❌ شما دسترسی ادمین ندارید!")
            return
            
        try:
            user_id = int(message_text.strip())
            if user_id in banned_users:
                banned_users.remove(user_id)
                save_data()
                await update.message.reply_text(f"✅ کاربر {user_id} با موفقیت آنبن شد.")
            else:
                await update.message.reply_text("ℹ️ این کاربر بن نشده بود.")
        except ValueError:
            await update.message.reply_text("❌ لطفاً یک آیدی عددی معتبر وارد کنید.")
        finally:
            del context.user_data["awaiting_unban"]
    
    elif "awaiting_channel_id" in context.user_data and context.user_data["awaiting_channel_id"]:
        chat_id = message_text.strip()
        user_id = update.message.from_user.id
        
        try:
            chat = await context.bot.get_chat(chat_id=chat_id)
            chat_member = await context.bot.get_chat_member(chat_id=chat_id, user_id=user_id)
            
            if chat.type not in ['channel', 'group', 'supergroup']:
                await update.message.reply_text("❌ فقط کانال‌ها و گروه‌ها پشتیبانی می‌شوند!")
                return
                
            if chat_member.status not in ['administrator', 'creator']:
                await update.message.reply_text(
                    "❌ شما مدیر این کانال/گروه نیستید!\n\n"
                    "برای استفاده از این ربات باید:\n"
                    "1. مدیر کانال/گروه باشید\n"
                    "2. ربات را به عنوان مدیر اضافه کرده باشید"
                )
                return
                
            await update.message.reply_text(
                "✅ کانال/گروه با موفقیت تأیید شد.\n\n"
                "لطفاً نام پایه را ارسال کنید (بدون زمان):\n"
                "مثال: نام کانال من"
            )
            
            context.user_data["temp_channel_id"] = chat_id
            context.user_data["awaiting_channel_id"] = False
            context.user_data["awaiting_base_name"] = True
            
        except Exception as e:
            await update.message.reply_text(
                "❌ خطا در دسترسی به کانال/گروه!\n\n"
                "لطفاً موارد زیر را بررسی کنید:\n"
                "1. ربات را به کانال/گروه اضافه کرده‌اید\n"
                "2. ربات را به عنوان مدیر تنظیم کرده‌اید\n"
                "3. از آیدی عددی استفاده کنید\n\n"
                f"🔧 خطای فنی: {str(e)}"
            )
            
    elif "awaiting_base_name" in context.user_data and context.user_data["awaiting_base_name"]:
        base_name = message_text.strip()
        channel_id = context.user_data["temp_channel_id"]
        user_id = update.message.from_user.id
        
        current_points = user_points.get(user_id, 0)
        if current_points < channel_points:
            await update.message.reply_text(
                f"❌ امتیاز کافی ندارید!\n\n"
                f"برای ثبت کانال/گروه به {channel_points} امتیاز نیاز دارید.\n"
                f"امتیاز فعلی شما: {current_points}\n\n"
                "می‌توانید با معرفی دوستان از طریق سیستم رفرال امتیاز کسب کنید."
            )
            return
        
        user_points[user_id] = current_points - channel_points
        
        if user_id not in user_channels:
            user_channels[user_id] = {}
            
        user_channels[user_id][channel_id] = {
            "base_name": base_name,
            "font_style": 5
        }
        
        save_data()
        
        if context.job_queue:
            if channel_id in active_jobs:
                active_jobs[channel_id].schedule_removal()
                
            job = context.job_queue.run_repeating(
                update_channel,
                interval=10,
                first=0,
                data=(channel_id, user_id),
                name=channel_id
            )
            
            active_jobs[channel_id] = job
        
        await update.message.reply_text(
            f"✅ کانال/گروه با موفقیت ثبت شد!\n\n"
            f"📌 کانال/گروه: {channel_id}\n"
            f"📝 نام پایه: {base_name}\n"
            f"⭐ امتیاز کسر شده: -{channel_points}\n"
            f"🏆 امتیاز باقیمانده شما: {user_points.get(user_id, 0)}\n"
            f"⏰ زمان هر ۱۰ ثانیه آپدیت می‌شود\n\n"
            f"برای تغییر تنظیمات از منوی اصلی استفاده کنید."
        )
        
        del context.user_data["temp_channel_id"]
        del context.user_data["awaiting_base_name"]

async def update_channel(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    channel_id, user_id = job.data
    
    if user_id not in user_channels or channel_id not in user_channels[user_id]:
        job.schedule_removal()
        if channel_id in active_jobs:
            del active_jobs[channel_id]
        return
    
    tehran_time = datetime.now(pytz.timezone('Asia/Tehran'))
    current_time = tehran_time.strftime("%H:%M")
    
    channel_data = user_channels[user_id][channel_id]
    base_name = channel_data["base_name"]
    font_style = channel_data["font_style"]
    
    current_time = convert_to_font(current_time, font_style)
    
    try:
        new_name = f"{base_name} | {current_time}"
        await context.bot.set_chat_title(chat_id=channel_id, title=new_name)
        logger.info(f"زمان کانال/گروه {channel_id} آپدیت شد: {current_time}")
    except Exception as e:
        logger.error(f"خطا در آپدیت کانال/گروه {channel_id}: {e}")

async def delete_service_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message or update.channel_post
    if not message:
        return
    
    # فقط پیام‌های سرویسی را مدیریت کن
    service_messages = [
        message.new_chat_title,
        message.new_chat_photo,
        message.delete_chat_photo,
        getattr(message, 'left_chat_member', None),
        getattr(message, 'new_chat_members', None),
        getattr(message, 'pinned_message', None)
    ]
    
    if any(service_messages):
        try:
            await message.delete()
            logger.info(f"پیام سرویسی در چت {message.chat.id} حذف شد")
        except Exception as e:
            logger.error(f"خطا در حذف پیام سرویسی: {e}")
    else:
        return

def main():
    application = (
        ApplicationBuilder()
        .token(TOKEN)
        .build()
    )
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    application.add_handler(MessageHandler(
        filters.TEXT & 
        ~filters.COMMAND & 
        (filters.ChatType.PRIVATE | 
         filters.Regex(f'@{application.bot.username}') |
         filters.REPLY),
        handle_message
    ))
    
    
    application.add_handler(
        MessageHandler(
            (filters.ChatType.CHANNEL | 
             filters.ChatType.GROUP | 
             filters.ChatType.SUPERGROUP) &
            (filters.UpdateType.MESSAGE | 
             filters.UpdateType.CHANNEL_POST),
            delete_service_messages
        )
    )
    
    application.run_polling()

if __name__ == "__main__":
    main()