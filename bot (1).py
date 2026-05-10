import discord
import aiohttp
import os
import traceback

TOKEN             = os.getenv("DISCORD_TOKEN")
GUILD_ID          = int(os.getenv("GUILD_ID", "0"))
WHITELIST_ROLE_ID = 1443294946089242727
CALLUP_ROLE_ID    = 1502830142496575569
LOG_WEBHOOK       = "https://discord.com/api/webhooks/1502831258189955285/t9uZgbrzcjFhqy9AWjZ58_K_OLHgU7Q7gBfDLLc9kWL1G2elP7ZzIR1QT964BMwwkIZ6"

print(f"[START] TOKEN={'SET' if TOKEN else 'MISSING'} | GUILD_ID={GUILD_ID}")

intents = discord.Intents.all()
client  = discord.Client(intents=intents)
tree    = discord.app_commands.CommandTree(client)


class CallUpModal(discord.ui.Modal, title="📞 CALL UP"):
    target_id = discord.ui.TextInput(label="ID الشخص المُبلَّغ عنه", placeholder="أدخل الـ ID...", max_length=20)
    reason    = discord.ui.TextInput(label="السبب", style=discord.TextStyle.paragraph, placeholder="اكتب السبب...")
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
            await interaction.followup.send("❌ العضو مو موجود في السيرفر!", ephemeral=True)
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

        await interaction.followup.send("✅ تم تقديم الطلب!\n" + "\n".join(actions), ephemeral=True)


class CallUpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📞 CALL UP", style=discord.ButtonStyle.danger, custom_id="callup_btn")
    async def btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(CallUpModal())


@client.event
async def on_ready():
    try:
        print(f"[READY] Logged in as {client.user} (ID: {client.user.id})")
        client.add_view(CallUpView())
        print("[READY] View registered")
        guild_obj = discord.Object(id=GUILD_ID)
        tree.copy_global_to(guild=guild_obj)
        synced = await tree.sync(guild=guild_obj)
        print(f"[READY] Synced {len(synced)} commands to guild {GUILD_ID}")
    except Exception as e:
        print(f"[ERROR] on_ready failed: {e}")
        traceback.print_exc()


@tree.command(name="send_callup", description="أرسل embed CALL UP")
@discord.app_commands.checks.has_permissions(administrator=True)
async def send_callup(interaction: discord.Interaction):
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
    await interaction.response.send_message(embed=embed, view=CallUpView())


print("[START] Running bot...")
client.run(TOKEN)
