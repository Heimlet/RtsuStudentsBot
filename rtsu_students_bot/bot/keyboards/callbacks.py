from aiogram.utils.callback_data import CallbackData

AUTH_CALLBACK = CallbackData("auth")
CANCELLATION_CALLBACK = CallbackData("cancel")
CONFIRMATION_CALLBACK = CallbackData("cnfrm", "ok")
SUBJECT_CALLBACK = CallbackData("sbj", "id")
