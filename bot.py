from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from datetime import datetime
import jdatetime
import logging
import signal
import sys

# تنظیمات logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# توکن ربات
BOT_TOKEN = "7959686586:AAHFT-aOJB0xzm5pf4P36z28A2b9w3-CvHU"

# مدیریت graceful shutdown
def signal_handler(sig, frame):
    logger.info("دریافت سیگنال خاموشی، ربات به صورت graceful خاموش می‌شود...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# تابع برای تبدیل تاریخ به شمسی
def get_persian_date():
    try:
        now = datetime.now()
        jalili_date = jdatetime.date.fromgregorian(
            day=now.day, 
            month=now.month, 
            year=now.year
        )
        return jalili_date.strftime("%Y/%m/%d")
    except Exception as e:
        logger.error(f"خطا در تبدیل تاریخ: {e}")
        return "1403/01/01"  # تاریخ پیش‌فرض در صورت خطا

# ایجاد کیبورد اصلی سوالات پرتکرار
def main_faq_keyboard():
    keyboard = [
        [InlineKeyboardButton("⏰ زمان آزمون کتبی کی هست؟", callback_data="exam_time")],
        [InlineKeyboardButton("📊 مشاهده نتیجه آزمون کتبی", callback_data="exam_result")],
        [InlineKeyboardButton("🔧 آزمون عملی کی هست؟", callback_data="practical_exam")],
        [InlineKeyboardButton("🕘 ساعت و محل آزمون عملی", callback_data="exam_location")],
        [InlineKeyboardButton("📮 چه مدارکی باید ارسال کنم؟ و به کی تحویل بدم؟", callback_data="send_documents")],
        [InlineKeyboardButton("💰 تعرفه خدمات آموزشی چیه؟", callback_data="service_tariff")],
        [InlineKeyboardButton("🏫 سوالات مربوط به آموزشگاه", callback_data="institute_questions")],
        [InlineKeyboardButton("📞 شماره تماس پرسنل آموزشگاه", callback_data="contact_staff")],
        [InlineKeyboardButton("👨‍💼 شماره تماس مسئول فنی و حرفه ای", callback_data="contact_technical")],
        [InlineKeyboardButton("📜 مدرک مو چجوری دریافت کنم", callback_data="certificate")],
        [InlineKeyboardButton("🎫 کارت ورود به جلسه آزمون کتبی", callback_data="exam_card")],
        [InlineKeyboardButton("❌ کارت ورود به جلسه دانلود نمیشه", callback_data="card_problem")],
        [InlineKeyboardButton("📝 نمونه سوالات از کجا دریافت کنم", callback_data="sample_questions")],
    ]
    return InlineKeyboardMarkup(keyboard)

# ایجاد کیبورد بازگشت
def back_to_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

# دستور استارت
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        welcome_text = """
        🌟 به ربات آموزشگاه فنی و حرفه ای ایده پاژ خوش آمدید! 🌟

        برای دریافت پاسخ سوالات پرتکرار، یکی از گزینه‌های زیر را انتخاب کنید:
        """
        await update.message.reply_text(welcome_text, reply_markup=main_faq_keyboard())
    except Exception as e:
        logger.error(f"خطا در دستور start: {e}")

# هندلر کلیک روی دکمه‌های اینلاین
async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()
        
        callback_data = query.data
        
        if callback_data == "exam_time":
            response = """
            ⏰ زمان آزمون من کی هست؟
            
            زمان آزمون شما توسط سازمان فنی و حرفه ای تعیین می‌گردد و معمولا بعد از پرداخت حق تعرفه ۱ الی ۲ ماه زمان خواهد برد.
            """
            await query.edit_message_text(response, reply_markup=back_to_main_keyboard())
        
        elif callback_data == "exam_result":
            keyboard = [
                [InlineKeyboardButton("🌐 مشاهده نتیجه آزمون", url="https://azmoon.portaltvto.com/result/result/index/1/80")],
                [InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")]
            ]
            response = """
            📊 نتیجه آزمون کتبی و شرایط قبولی به چه صورت است؟
            
            میتوانید از طریق سایت فنی و حرفه ای نتیجه آزمون خود را ببینید.
            شرایط قبولی در آزمون کتبی گرفتن حداقل نمره ۵۰ می‌باشد.
            
            در صورت مردودی به بخش شماره تماس مسئول فنی و حرفه مراجعه کنید و هزینه آزمون را پرداخت کنید.
            """
            await query.edit_message_text(response, reply_markup=InlineKeyboardMarkup(keyboard))
        
        elif callback_data == "practical_exam":
            response = """
            🔧 آزمون عملی من کی هست؟
            
            آزمون عملی در هر ماه توسط سازمان فنی و حرفه ای تعیین می‌گردد و اطلاع‌رسانی از طریق مسئول فنی و حرفه ای انجام می‌گیرد تاریخ آزمون عملی شهریورماه به این صورت میباشد
             اگر آزمون کتبی شما در بازه زمانی 
            1404/05/16 تا 1404/06/15 بوده است
            آزمون عملی شما در تاریخ 1404/06/26  میباشد
            توجه داشته باشید.
            شرط حضور در آزمون عملی، قبولی در آزمون کتبی است.
            """
            await query.edit_message_text(response, reply_markup=back_to_main_keyboard())
        
        elif callback_data == "exam_location":
            response = """
            🕘 ساعت آزمون و محل آزمون عملی 
            
            ساعت ۹ صبح و در محل آموزشگاه ایده پاژ برگزار می‌گردد.
            نیازی به دریافت کارت ورود به جلسه نمی‌باشد.
            """
            await query.edit_message_text(response, reply_markup=back_to_main_keyboard())
        
        elif callback_data == "send_documents":
            response = """
            📮 مدارکمو کجا ارسال کنم؟
            
            مدارک خود را به آیدی مسئول فنی و حرفه ای ایده پاژ ارسال کنید:
            
            👤 آیدی: https://t.me/idepazhs
            
        🔹 کارت ملی ( یا صفحه اول شناسنامه )
        🔹 برای اتباع  ( عکس از مدرک حاوی شناسه یکتا )
        🔹  عکس پرسنلی  4*3  ( مانند نمونه بالا )

 ⭕️  نکات مهم:
( عکس حداکثر باید مربوط به 6 ماه گذشته باشد)
( روی مدرک درج میشه حتما با پس زمینه سفید و با کیفیت)
بدون مهر ، منگنه و پارگی و ... باشد.

در غیر این صورت عکس شما توسط سازمان فنی و حرفه ای رد خواهد شد و اجازه شرکت در آزمون نخواهید داشت
            """
            await query.edit_message_text(response, reply_markup=back_to_main_keyboard())
        
        elif callback_data == "service_tariff":
            keyboard = [
                [InlineKeyboardButton("🌐 استعلام دهک یارانه‌ای", url="https://sso.mcls.gov.ir/auth/realms/sso/protocol/openid-connect/auth?response_type=code&client_id=hemayat&scope=openid%20profile%20email&state=132&redirect_uri=https://hemayat.mcls.gov.ir/api/sso/auth?provider=REFAH")],
                [InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")]
            ]
            response = """
            💰 تعرفه خدمات آموزشی دولت چیه و چرا باید پرداخت کنم؟
            
            تعرفه خدمات دولت بر اساس دهک بندی یارانه‌ای شما می‌باشد. این مصوبه در سال ۱۴۰۴ توسط سازمان فنی و حرفه‌ای به آموزشگاه‌های فنی و حرفه‌ای ابلاغ گردید.
            هزینه تعرفه خدمات آموزشی بستگی به دوره انتخابی شما دارد
            📊 دهک‌بندی یارانه‌ای:
            • دهک ۱ تا ۵: نیازی به پرداخت تعرفه خدمات آموزشی ندارند
            • دهک ۶ به بالا: موظف به پرداخت تعرفه می‌باشند
            برای استعلام دهک یارانه‌ای خود می‌توانید با اطلاعات سرپرست خانوار به لینک زیر مراجعه کنید.
            """
            await query.edit_message_text(response, reply_markup=InlineKeyboardMarkup(keyboard))
        
        elif callback_data == "institute_questions":
            response = """
            🏫 سوالات مربوط به موسسه ایده پاژ
            
            لطفا با شماره موسسه تماس بگیرید:
            ساعت اداری ۹ الی ۲۰
            
            📞 05138452386
            📞 05138401556
            """
            await query.edit_message_text(response, reply_markup=back_to_main_keyboard())
        
        elif callback_data == "contact_staff":
            response = """
            📞 شماره تماس پرسنل ایده پاژ
            
            آقای سهیلی: [09359202990](tel:+989359202990)
________________________
            آقای عمرانی:     [09355251039](tel:+989355251039)
________________________
            آقای سلطانی:     [09371500714](tel:+989371500714)
________________________
            آقای چهارمحالی:     [09152093244](tel:+989152093244)
________________________
            آقای ریاضی:     [09330761741](tel:+989330761741)
________________________
            آقای صالح آبادی:     [09389791122](tel:+989389791122)
________________________
            آقای اژدری:     [09155465113](tel:+989155465113)
________________________
            خانم سیار:     [09010702940](tel:+989010702940)
________________________
            آقای شبرنگی:     [09051092940](tel:+989051092940)
            """
            await query.edit_message_text(response, parse_mode='Markdown', reply_markup=back_to_main_keyboard())
        
        elif callback_data == "contact_technical":
            response = """
            👨‍💼 شماره تماس مسئول فنی و حرفه‌ای
            
            دینکو: [09301024593](tel:+989301024593)
            
            لطفا در ساعت ۹ الی ۱۴ تماس بگیرید.
            """
            await query.edit_message_text(response, parse_mode='Markdown', reply_markup=back_to_main_keyboard())
        
        elif callback_data == "certificate":
            keyboard = [
                [InlineKeyboardButton("🌐 آموزش نحوه دریافت مدرک", url="https://idepazh.ir/blog/certificate-inquiry")],
                [InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")]
            ]
            response = """
            📜 مدرکم رو چجوری دریافت کنم؟
            
            مدرک شما بعد از قبولی در آزمون کتبی با حداقل نمره ۵۰ و آزمون عملی با حداقل نمره ۷۸ به مدت حداکثر ۴۵ روز زمان خواهد برد.
            
            مدرک شما ۴۵ روز بعد از قبولی در آزمون عملی صادر می‌شود.
            """
            await query.edit_message_text(response, reply_markup=InlineKeyboardMarkup(keyboard))
        
        elif callback_data == "exam_card":
            keyboard = [
                [InlineKeyboardButton("🌐 دریافت کارت ورود به جلسه", url="https://azmoon.portaltvto.com/card/card/index/1/80")],
                [InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")]
            ]
            response = """
            🎫 کارت ورود به جلسه آزمون چجوری دریافت کنم؟
            اطلاعات محل برگزاری آزمون کتبی (ساعت و آدرس) در کارت ورود به جلسه درج شده است
            لطفا ۱ روز قبل از آزمون اقدام به دانلود کارت کنید.
            """
            await query.edit_message_text(response, reply_markup=InlineKeyboardMarkup(keyboard))
        
        elif callback_data == "card_problem":
            today = get_persian_date()
            response = f"""
            ❌ کارت ورود به جلسه دانلود نمیشه؟
            
            به این نکات خوب دقت کنید:
            
            امروز {today}
            
            • اگر تاریخ آزمون شما یک روز قبل از تاریخ امروز می‌باشد لطفا از ساعت ۱۲ به بعد امتحان کنید.

            • در صورتی که باز هم با دریافت کارت مشکل مواجه شدید در روز آزمون ساعت ۷ به آدرس مشهد- میدان نمایشگاه بزرگراه آیت الله هاشمی رفسنجانی میدان خلیج فارس مجیدیه ۳۷- نبش صادقیه ۱۰ مجتمع ثامن(سازمان سنجش) مراجعه کنید.
            
            • حتما قبل از هر اقدام مطمئن شوید آزمون کتبی دارید.
            """
            await query.edit_message_text(response, reply_markup=back_to_main_keyboard())
        
        elif callback_data == "sample_questions":
            keyboard = [
                [InlineKeyboardButton("🌐 دریافت نمونه سوالات", url="https://idepazh.ir/sample-professional-technical-questions/")],
                [InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")]
            ]
            response = """
            📝 نمونه سوالات از کجا باید دریافت کنم؟
            
            از طریق لینک زیر دوره خود را انتخاب کنید و نمونه سوالات را بخوانید.

            اطلاعات نمونه سوالات از سازمان سنجش دریافت شده است و مورد تائید سازمان فنی و حرفه ای میباشد.

            لطفا توجه داشته باشید نمونه سوالات به صورت کمکی میباشد
            """
            await query.edit_message_text(response, reply_markup=InlineKeyboardMarkup(keyboard))
        
        elif callback_data == "main_menu":
            welcome_text = """
            🌟 سلام من پاسخگوی هوشمند آموزشگاه ایده پاژ هستم! 🌟

            برای دریافت پاسخ سوالات خود، یکی از گزینه‌های زیر را انتخاب کنید:
            """
            await query.edit_message_text(welcome_text, reply_markup=main_faq_keyboard())
    
    except Exception as e:
        logger.error(f"خطا در هندلر دکمه: {e}")

# هندلر خطا
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"خطا: {context.error}")

def main():
    try:
        # ایجاد اپلیکیشن
        application = Application.builder().token(BOT_TOKEN).build()
        
        # اضافه کردن هندلرها
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CallbackQueryHandler(handle_button_click))
        
        # اضافه کردن هندلر خطا
        application.add_error_handler(error_handler)
        
        # شروع ربات
        logger.info("✅ ربات آموزشگاه ایده پاژ در حال اجراست...")
        application.run_polling(
            drop_pending_updates=True,
            allowed_updates=Update.ALL_TYPES
        )
    
    except Exception as e:
        logger.error(f"خطای جدی در اجرای ربات: {e}")

if __name__ == "__main__":
    # اجرای ربات با قابلیت restart خودکار
    while True:
        try:
            main()
        except KeyboardInterrupt:
            logger.info("ربات توسط کاربر متوقف شد")
            break
        except Exception as e:
            logger.error(f"ربات crashed شده و restart می‌شود: {e}")
            # کمی صبر قبل از restart
            import time
            time.sleep(10)
