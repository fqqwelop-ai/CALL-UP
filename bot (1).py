import discord
from discord.ext import commands
from discord import app_commands
import os

# ============================
# إعدادات
# ============================
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID", "0"))
WEB_URL = os.getenv("WEB_URL", "https://your-app.railway.app")  # رابط Railway

WHITELIST_ROLE_ID = 1443294946089242727
CALLUP_ROLE_ID    = 1502830142496575569

WEBHOOK_URL = "https://discord.com/api/webhooks/1502831258189955285/t9uZgbrzcjFhqy9AWjZ58_K_OLHgU7Q7gBfDLLc9kWL1G2elP7ZzIR1QT964BMwwkIZ6"

# ============================
# البوت
# ============================
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ البوت شغال كـ {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🔄 تمت مزامنة {len(synced)} أمر")
    except Exception as e:
        print(f"❌ خطأ: {e}")


# ============================
# أمر إرسال الـ Embed عبر Webhook
# ============================
@bot.tree.command(name="send_callup", description="ترسل embed زر CALL UP في الروم")
@app_commands.checks.has_permissions(administrator=True)
async def send_callup(interaction: discord.Interaction):
    import aiohttp

    embed_data = {
        "embeds": [{
            "title": "📞 CALL UP",
            "description": (
                "اضغط على الزر أدناه لتقديم طلب **CALL UP**\n\n"
                "سيتم فتح صفحة تملأ فيها:\n"
                "• **ID** الشخص المُبلَّغ عنه\n"
                "• **السبب**\n"
                "• **الدليل**\n\n"
                "بعد الإرسال سيتم مراجعة طلبك."
            ),
            "color": 0x5865F2,
            "footer": {"text": "CALL UP System"}
        }],
        "components": [{
            "type": 1,
            "components": [{
                "type": 2,
                "label": "📞 CALL UP",
                "style": 5,  # Link button
                "url": f"{WEB_URL}/callup"
            }]
        }]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(WEBHOOK_URL, json=embed_data) as resp:
            if resp.status in (200, 204):
                await interaction.response.send_message("✅ تم إرسال الـ Embed!", ephemeral=True)
            else:
                text = await resp.text()
                await interaction.response.send_message(f"❌ خطأ: {resp.status} - {text}", ephemeral=True)


# ============================
# Endpoint داخلي: تنفيذ CALL UP
# (يُستدعى من صفحة الويب بعد الإرسال)
# ============================
@bot.tree.command(name="execute_callup", description="تنفيذ CALL UP على عضو (للأدمن فقط)")
@app_commands.describe(member="العضو اللي تبي تطبق عليه CALL UP")
@app_commands.checks.has_permissions(administrator=True)
async def execute_callup(interaction: discord.Interaction, member: discord.Member):
    guild = interaction.guild

    whitelist_role = guild.get_role(WHITELIST_ROLE_ID)
    callup_role    = guild.get_role(CALLUP_ROLE_ID)

    removed = False
    added   = False

    if whitelist_role and whitelist_role in member.roles:
        await member.remove_roles(whitelist_role, reason="CALL UP submitted")
        removed = True

    if callup_role and callup_role not in member.roles:
        await member.add_roles(callup_role, reason="CALL UP submitted")
        added = True

    await interaction.response.send_message(
        f"✅ تم تطبيق CALL UP على {member.mention}\n"
        f"{'❌ شُيل منه WHITELIST' if removed else '⚠️ لم يكن يملك WHITELIST'}\n"
        f"{'✅ أُعطي رتبة CALL UP' if added else '⚠️ كان يملك CALL UP مسبقاً'}",
        ephemeral=True
    )


bot.run(TOKEN)
