# 📞 CALL UP Bot

بوت ديسكورد للاستدعاءات مع صفحة ويب تعمل على Railway.

---

## 🗂️ الملفات

| الملف | الوظيفة |
|-------|---------|
| `bot.py` | البوت الرئيسي |
| `web.py` | سيرفر الويب (صفحة الفورم) |
| `requirements.txt` | المكتبات المطلوبة |
| `Procfile` | تشغيل Railway |
| `railway.toml` | إعدادات Railway |
| `.env.example` | مثال متغيرات البيئة |

---

## ⚙️ خطوات الرفع على Railway

### 1. جهّز المتغيرات
في Railway → Variables، أضف:
```
DISCORD_TOKEN   = توكن البوت
GUILD_ID        = ID السيرفر
WEB_URL         = https://اسمك.railway.app
```

### 2. ارفع الملفات
- اعمل repo على GitHub وارفع الملفات فيه
- في Railway اختر "Deploy from GitHub"

### 3. بعد الرفع
- انسخ رابط الموقع من Railway
- حطه في متغير `WEB_URL`
- أعد deploy

---

## 🤖 إعداد البوت (Discord Developer Portal)

1. روح على https://discord.com/developers/applications
2. افتح تطبيقك → **Bot**
3. فعّل:
   - ✅ Server Members Intent
   - ✅ Message Content Intent
4. من **OAuth2 → URL Generator**:
   - Scopes: `bot` + `applications.commands`
   - Permissions: `Manage Roles` + `Send Messages`
5. افتح الرابط وأضف البوت للسيرفر

---

## 📋 الأوامر

| الأمر | الوظيفة | الصلاحية |
|-------|---------|---------|
| `/send_callup` | يرسل Embed مع زر CALL UP في الروم | Administrator |

---

## 🔄 آلية العمل

```
المستخدم يضغط زر CALL UP
        ↓
يفتح صفحة الويب على Railway
        ↓
يملأ: ID الشخص + السبب + الدليل
        ↓
يضغط إرسال
        ↓
السيرفر يشيل رول WHITELIST
ويعطي رول CALL UP
        ↓
يُرسل لوق بالمعلومات للويب هوك
```

---

## 🎭 الأدوار

| الدور | ID |
|------|-----|
| WHITELIST (يُشال) | 1443294946089242727 |
| CALL UP (يُعطى) | 1502830142496575569 |
