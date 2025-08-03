# start.py - ثبت همه هندلرها از فایل‌های ماژولار

from aiogram import Dispatcher

from handlers.admin import register_admin_handlers
from handlers.crush import register_crush_handlers
from handlers.gender import register_gender_handlers
from handlers.info import register_info_handlers
from handlers.middleware import register_middleware
from handlers.profile import register_profile_handlers
from handlers.relationship import register_relationship_handlers
from handlers.ship_logic import register_ship_logic_handlers
from handlers.start import register_start_handlers

def register_all_handlers(dp: Dispatcher):
    register_admin_handlers(dp)
    register_crush_handlers(dp)
    register_gender_handlers(dp)
    register_info_handlers(dp)
    register_middleware(dp)
    register_profile_handlers(dp)
    register_relationship_handlers(dp)
    register_ship_logic_handlers(dp)
    register_start_handlers(dp)
