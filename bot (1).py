import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import os
import traceback

TOKEN             = os.getenv("DISCORD_TOKEN")
GUILD_ID          = int(os.getenv("GUILD_ID", "0"))
WHITELIST_ROLE_ID = 1443294946089242727
CALLUP_ROLE_ID    = 1502830142496575569
LOG_WEBHOOK       = "https://discord.com/api/webhooks/1502831258189955285/t9uZgbrzcjFhqy9AWjZ58_K_OLHgU7Q7gBfDLLc9kWL1G2elP7ZzIR1QT964BMwwkIZ6"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)


class CallUpModal(discord.ui.Modal, title="📞 CALL UP"):
    target_id = discord.ui.TextInput(label="ID الشخص", placeholder="أدخل الـ ID...", max_length=20)
    reason    = discord.ui.TextInput(label="السبب", style=discord.TextStyle.paragraph, placeholder="السبب...")
    evidence  = discord.ui.TextInput(label="الدليل", placeholder="رابط الدليل...")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        tid = self.target_id.value.strip()

        if not tid.isdigit():
            await interaction.followup.send("❌ الـ ID غير صحيح!", ephemeral=True)
            return

        guild = interaction.guild
        try:
            member = guild.get_member(int(tid)) or await guild.fetch_member(int(tid))
        except Exception:
            await interaction.followup.send("❌ العضو مو موجود!", ephemeral=True)
            return

        wl_role  = guild.get_role(WHITELIST_ROLE_ID)
        cup_role = guild.get_role(CALLUP_ROLE_ID)
        actions  = []

        if wl_role and wl_role in member.roles:
            await member.remove_roles(wl_role)
            actions.append("✅ شُيل رول WHITELIST")
        else:
            actions.append("⚠️ لم يكن يملك WHITELIST")

        if cup_role and cup_role not in member.roles:
            await member.add_roles(cup_role)
            actions.append("✅ أُعطي رول CALL UP")
        else:
            actions.append("⚠️ كان يملك CALL UP مسبقاً")

        async with aiohttp.ClientSession() as s:
            await s.post(LOG_WEBHOOK, json={"embeds": [{
                "title": "📞 طلب CALL UP جديد",
                "color": 0xe63946,
                "fields": [
                    {"name": "👤 مقدم الطلب",      "value": f"{interaction.user.mention} (`{interaction.user.id}`)", "inline": False},
                    {"name": "🎯 ID المُبلَّغ عنه", "value": f"{member.mention} (`{tid}`)",                          "inline": False},
                    {"name": "📋 السبب",            "value": self.reason.value,                                       "inline": False},
                    {"name": "🔗 الدليل",           "value": self.evidence.value,                                     "inline": False},
                    {"name": "⚙️ الإجراءات",        "value": "\n".join(actions),                                     "inline": False},
                ],
                "footer": {"text": "CALL UP System"}
            }]})

        await interaction.followup.send("✅ تم!\n" + "\n".join(actions), ephemeral=True)


class CallUpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📞 CALL UP", style=discord.ButtonStyle.danger, custom_id="callup_v4")
    async def callup_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(CallUpModal())


@bot.event
async def on_ready():
    try:
        print(f"[READY] {bot.user}")
        bot.add_view(CallUpView())
        await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print("[READY] Synced")
    except Exception as e:
        print(f"[ERROR] {e}")
        traceback.print_exc()


@bot.tree.command(name="send_callup", description="أرسل embed CALL UP", guild=discord.Object(id=GUILD_ID))
@app_commands.checks.has_permissions(administrator=True)
async def send_callup(interaction: discord.Interaction):
    # نرسل الرسالة عبر REST API مباشرة
    embed = discord.Embed(
        title="📞 CALL UP",
        description=(
            "اضغط على الزر أدناه لتقديم طلب **CALL UP**\n\n"
            "🎯 **ID** الشخص المُبلَّغ عنه\n"
            "📋 **السبب**\n"
            "🔗 **الدليل**"
        ),
        color=0xe63946
    )
    embed.set_footer(text="CALL UP System")

    view = CallUpView()

    # نرسل عبر channel مباشرة
    msg = await interaction.channel.send(embed=embed, view=view)
    print(f"[SENT] Message ID: {msg.id} | Components: {msg.components}")

    await interaction.response.send_message("✅ تم إرسال الـ Embed!", ephemeral=True)


# استقبال أي interaction يدوياً كـ backup
@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:
        cid = interaction.data.get("custom_id", "")
        print(f"[INTERACTION] custom_id={cid}")
        if cid == "callup_v4":
            await interaction.response.send_modal(CallUpModal())


bot.run(TOKEN)
