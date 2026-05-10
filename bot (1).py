import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import os

# ============================
# إعدادات
# ============================
TOKEN             = os.getenv("DISCORD_TOKEN")
GUILD_ID          = int(os.getenv("GUILD_ID", "0"))
WHITELIST_ROLE_ID = 1443294946089242727
CALLUP_ROLE_ID    = 1502830142496575569
LOG_WEBHOOK       = "https://discord.com/api/webhooks/1502831258189955285/t9uZgbrzcjFhqy9AWjZ58_K_OLHgU7Q7gBfDLLc9kWL1G2elP7ZzIR1QT964BMwwkIZ6"

# ============================
# إعداد البوت
# ============================
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


# ============================
# Modal (النموذج)
# ============================
class CallUpModal(discord.ui.Modal, title="📞 CALL UP Request"):
    target_id = discord.ui.TextInput(
        label="ID الشخص المُبلَّغ عنه",
        placeholder="أدخل الـ ID هنا...",
        max_length=20,
        required=True
    )
    reason = discord.ui.TextInput(
        label="السبب",
        placeholder="اكتب سبب الاستدعاء بالتفصيل...",
        style=discord.TextStyle.paragraph,
        required=True
    )
    evidence = discord.ui.TextInput(
        label="الدليل",
        placeholder="رابط الصورة أو الفيديو أو السكرين شوت...",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        guild     = interaction.guild
        target_id = self.target_id.value.strip()
        reason    = self.reason.value.strip()
        evidence  = self.evidence.value.strip()

        if not target_id.isdigit():
            await interaction.followup.send("❌ الـ ID غير صحيح!", ephemeral=True)
            return

        try:
            member = guild.get_member(int(target_id)) or await guild.fetch_member(int(target_id))
        except Exception:
            await interaction.followup.send("❌ ما قدرت أجد هذا العضو في السيرفر!", ephemeral=True)
            return

        whitelist_role = guild.get_role(WHITELIST_ROLE_ID)
        callup_role    = guild.get_role(CALLUP_ROLE_ID)
        actions        = []

        if whitelist_role and whitelist_role in member.roles:
            await member.remove_roles(whitelist_role, reason="CALL UP submitted")
            actions.append("✅ شُيل منه رول WHITELIST")
        else:
            actions.append("⚠️ لم يكن يملك رول WHITELIST")

        if callup_role and callup_role not in member.roles:
            await member.add_roles(callup_role, reason="CALL UP submitted")
            actions.append("✅ أُعطي رول CALL UP")
        else:
            actions.append("⚠️ كان يملك رول CALL UP مسبقاً")

        async with aiohttp.ClientSession() as session:
            log_embed = {
                "embeds": [{
                    "title": "📞 طلب CALL UP جديد",
                    "color": 0xe63946,
                    "fields": [
                        {"name": "👤 مقدم الطلب",       "value": f"{interaction.user.mention} (`{interaction.user.id}`)", "inline": False},
                        {"name": "🎯 ID المُبلَّغ عنه",  "value": f"{member.mention} (`{target_id}`)",                   "inline": False},
                        {"name": "📋 السبب",             "value": reason,                                                 "inline": False},
                        {"name": "🔗 الدليل",            "value": evidence,                                               "inline": False},
                        {"name": "⚙️ الإجراءات",         "value": "\n".join(actions),                                    "inline": False},
                    ],
                    "footer": {"text": "CALL UP System"}
                }]
            }
            await session.post(LOG_WEBHOOK, json=log_embed)

        await interaction.followup.send(
            "✅ تم تقديم طلب CALL UP بنجاح!\n" + "\n".join(actions),
            ephemeral=True
        )


# ============================
# View مع الزر
# ============================
class CallUpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📞 CALL UP", style=discord.ButtonStyle.danger, custom_id="callup_button")
    async def callup_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(CallUpModal())


# ============================
# on_ready
# ============================
@bot.event
async def on_ready():
    print(f"✅ البوت شغال كـ {bot.user}")
    bot.add_view(CallUpView())
    guild = discord.Object(id=GUILD_ID)
    bot.tree.copy_global_to(guild=guild)
    synced = await bot.tree.sync(guild=guild)
    print(f"🔄 تمت مزامنة {len(synced)} أمر للسيرفر")


# ============================
# أمر: إرسال Embed مع زر CALL UP
# ============================
@bot.tree.command(name="send_callup", description="ترسل embed زر CALL UP في الروم")
@app_commands.checks.has_permissions(administrator=True)
async def send_callup(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📞 CALL UP",
        description=(
            "اضغط على الزر أدناه لتقديم طلب **CALL UP**\n\n"
            "سيتم فتح نموذج تملأ فيه:\n"
            "🎯 **ID** الشخص المُبلَّغ عنه\n"
            "📋 **السبب**\n"
            "🔗 **الدليل**"
        ),
        color=0xe63946
    )
    embed.set_footer(text="CALL UP System")

    await interaction.response.send_message(embed=embed, view=CallUpView())


# ============================
# تشغيل
# ============================
bot.run(TOKEN)
