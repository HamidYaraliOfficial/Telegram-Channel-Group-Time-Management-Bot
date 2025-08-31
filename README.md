# Telegram Channel/Group Time Management Bot

## Overview
This is a Telegram bot designed to manage and update the time displayed in the titles of Telegram channels or groups. The bot supports features such as referral systems, point-based channel registration, font style customization for time display, and admin functionalities like banning users and managing points.

## Features
- **Time Updates**: Automatically updates the channel/group title with the current time in Tehran timezone every 10 seconds.
- **Referral System**: Users can earn points by referring others using a unique referral link.
- **Point System**: Points are required to register a channel or group, with configurable point costs.
- **Font Customization**: Users can choose from multiple font styles for the time display.
- **Admin Panel**: Admins can manage users, ban/unban, view statistics, and adjust point settings.
- **Service Message Deletion**: Automatically deletes Telegram service messages in channels and groups.

## Requirements
- Python 3.7+
- `python-telegram-bot` library (v20.0+)
- `pytz` for timezone handling
- A valid Telegram Bot Token

## Installation
1. Install the required Python libraries:
   ```bash
   pip install python-telegram-bot pytz
   ```
2. Replace `TOKEN` in the code with your Telegram Bot Token.
3. Optionally, configure `ADMIN_IDS` with the Telegram user IDs of administrators.
4. Run the bot:
   ```bash
   python bot.py
   ```

## Usage
- **Start the Bot**: Use the `/start` command to access the main menu.
- **Register a Channel/Group**: Requires sufficient points; users must be admins of the channel/group.
- **Referral Link**: Share your referral link to earn points for you and the referred user.
- **Font Styles**: Choose from five different font styles for time display.
- **Admin Commands**: Admins can access the admin panel to manage users, points, and bot statistics.

## File Structure
- `bot.py`: Main bot script containing all the logic.
- `bot_data.json`: Stores user data, channel info, points, and referral codes.

## Notes
- The bot requires the bot to be an admin in the target channel/group.
- Ensure a stable internet connection for continuous time updates.
- Data is persistently stored in `bot_data.json`.

## License
This project is licensed under the MIT License.

---

# ربات مدیریت زمان کانال/گروه تلگرام

## بررسی اجمالی
این یک ربات تلگرامی است که برای مدیریت و به‌روزرسانی زمان نمایش داده شده در عنوان کانال‌ها یا گروه‌های تلگرامی طراحی شده است. این ربات از قابلیت‌هایی مانند سیستم رفرال، ثبت کانال مبتنی بر امتیاز، شخصی‌سازی سبک فونت برای نمایش زمان و امکانات مدیریتی مانند بن کردن کاربران و مدیریت امتیازها پشتیبانی می‌کند.

## قابلیت‌ها
- **به‌روزرسانی زمان**: به‌صورت خودکار هر ۱۰ ثانیه عنوان کانال/گروه را با زمان فعلی در منطقه زمانی تهران به‌روزرسانی می‌کند.
- **سیستم رفرال**: کاربران می‌توانند با دعوت از دیگران از طریق لینک رفرال اختصاصی امتیاز کسب کنند.
- **سیستم امتیازدهی**: برای ثبت کانال یا گروه به امتیاز نیاز است و هزینه امتیاز قابل تنظیم است.
- **شخصی‌سازی فونت**: کاربران می‌توانند از چندین سبک فونت برای نمایش زمان انتخاب کنند.
- **پنل مدیریت**: مدیران می‌توانند کاربران را مدیریت کنند، بن/آنبن کنند، آمار را مشاهده کنند و تنظیمات امتیاز را تغییر دهند.
- **حذف پیام‌های سرویسی**: پیام‌های سرویسی تلگرام در کانال‌ها و گروه‌ها به‌صورت خودکار حذف می‌شوند.

## پیش‌نیازها
- پایتون نسخه ۳.۷ یا بالاتر
- کتابخانه `python-telegram-bot` (نسخه ۲۰.۰ یا بالاتر)
- کتابخانه `pytz` برای مدیریت منطقه زمانی
- یک توکن معتبر ربات تلگرام

## نصب
1. کتابخانه‌های مورد نیاز پایتون را نصب کنید:
   ```bash
   pip install python-telegram-bot pytz
   ```
2. مقدار `TOKEN` را در کد با توکن ربات تلگرام خود جایگزین کنید.
3. به‌صورت اختیاری، `ADMIN_IDS` را با آیدی‌های عددی کاربران مدیر در تلگرام تنظیم کنید.
4. ربات را اجرا کنید:
   ```bash
   python bot.py
   ```

## استفاده
- **شروع ربات**: از دستور `/start` برای دسترسی به منوی اصلی استفاده کنید.
- **ثبت کانال/گروه**: نیاز به امتیاز کافی دارد؛ کاربران باید مدیر کانال/گروه باشند.
- **لینک رفرال**: لینک رفرال خود را به اشتراک بگذارید تا برای شما و کاربر دعوت‌شده امتیاز کسب شود.
- **سبک‌های فونت**: از بین پنج سبک مختلف فونت برای نمایش زمان انتخاب کنید.
- **دستورات مدیریتی**: مدیران می‌توانند به پنل مدیریت دسترسی داشته باشند تا کاربران، امتیازها و آمار ربات را مدیریت کنند.

## ساختار فایل‌ها
- `bot.py`: اسکریپت اصلی ربات که شامل تمام منطق است.
- `bot_data.json`: ذخیره داده‌های کاربران، اطلاعات کانال، امتیازها و کدهای رفرال.

## نکات
- ربات باید در کانال/گروه هدف به‌عنوان مدیر تنظیم شده باشد.
- برای به‌روزرسانی مداوم زمان، اتصال پایدار به اینترنت لازم است.
- داده‌ها به‌صورت دائمی در فایل `bot_data.json` ذخیره می‌شوند.

## مجوز
این پروژه تحت مجوز MIT منتشر شده است.

---

# Telegram 频道/群组时间管理机器人

## 概述
这是一个为 Telegram 频道或群组设计的机器人，用于管理和更新显示在频道/群组标题中的时间。该机器人支持推荐系统、基于积分的频道注册、时间显示字体样式自定义以及管理员功能，如封禁用户和管理积分。

## 功能
- **时间更新**：每 10 秒自动更新频道/群组标题，显示德黑兰时区的当前时间。
- **推荐系统**：用户可通过分享独特的推荐链接获得积分。
- **积分系统**：注册频道或群组需要积分，积分成本可配置。
- **字体自定义**：用户可从多种字体样式中选择用于时间显示。
- **管理员面板**：管理员可管理用户、封禁/解封用户、查看统计信息和调整积分设置。
- **服务消息删除**：自动删除 Telegram 频道和群组中的服务消息。

## 要求
- Python 3.7 或更高版本
- `python-telegram-bot` 库（版本 20.0 或更高）
- `pytz` 用于处理时区
- 一个有效的 Telegram 机器人令牌

## 安装
1. 安装所需的 Python 库：
   ```bash
   pip install python-telegram-bot pytz
   ```
2. 在代码中将 `TOKEN` 替换为您的 Telegram 机器人令牌。
3. 可选：将 `ADMIN_IDS` 配置为管理员的 Telegram 用户 ID。
4. 运行机器人：
   ```bash
   python bot.py
   ```

## 使用方法
- **启动机器人**：使用 `/start` 命令访问主菜单。
- **注册频道/群组**：需要足够的积分；用户必须是频道/群组的管理员。
- **推荐链接**：分享您的推荐链接，为您和被邀请的用户赚取积分。
- **字体样式**：从五种不同的字体样式中选择用于时间显示。
- **管理员命令**：管理员可访问管理员面板以管理用户、积分和机器人统计信息。

## 文件结构
- `bot.py`：包含所有逻辑的主机器人脚本。
- `bot_data.json`：存储用户数据、频道信息、积分和推荐代码。

## 注意事项
- 机器人需要在目标频道/群组中设置为管理员。
- 确保稳定的互联网连接以进行持续的时间更新。
- 数据持久存储在 `bot_data.json` 文件中。

## 许可证
本项目采用 MIT 许可证。