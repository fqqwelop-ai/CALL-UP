from flask import Flask, request, jsonify, render_template_string
import requests
import os

app = Flask(__name__)

BOT_API_URL = os.getenv("BOT_API_URL", "http://localhost:8080")
WHITELIST_ROLE_ID = "1443294946089242727"
CALLUP_ROLE_ID    = "1502830142496575569"
BOT_TOKEN         = os.getenv("DISCORD_TOKEN")
GUILD_ID          = os.getenv("GUILD_ID")

LOG_WEBHOOK = "https://discord.com/api/webhooks/1502831258189955285/t9uZgbrzcjFhqy9AWjZ58_K_OLHgU7Q7gBfDLLc9kWL1G2elP7ZzIR1QT964BMwwkIZ6"

# ============================
# صفحة الفورم
# ============================
HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CALL UP</title>
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Noto+Kufi+Arabic:wght@400;700&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #0a0b0f;
    --surface: #12141a;
    --border: #1e2130;
    --accent: #e63946;
    --accent2: #ff6b6b;
    --text: #e8eaf0;
    --muted: #6b7280;
    --success: #22c55e;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Noto Kufi Arabic', 'Rajdhani', sans-serif;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    position: relative;
  }

  /* خلفية متحركة */
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
      radial-gradient(ellipse 60% 40% at 20% 20%, rgba(230,57,70,0.08) 0%, transparent 60%),
      radial-gradient(ellipse 50% 50% at 80% 80%, rgba(230,57,70,0.05) 0%, transparent 60%);
    pointer-events: none;
  }

  /* خطوط شبكية */
  body::after {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
      linear-gradient(rgba(230,57,70,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(230,57,70,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
  }

  .container {
    width: 100%;
    max-width: 520px;
    padding: 20px;
    position: relative;
    z-index: 1;
  }

  /* هيدر */
  .header {
    text-align: center;
    margin-bottom: 32px;
    animation: fadeDown 0.6s ease;
  }

  .badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(230,57,70,0.1);
    border: 1px solid rgba(230,57,70,0.3);
    color: var(--accent2);
    padding: 6px 16px;
    border-radius: 100px;
    font-size: 12px;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 16px;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 600;
  }

  .badge::before {
    content: '';
    width: 6px;
    height: 6px;
    background: var(--accent);
    border-radius: 50%;
    animation: pulse 1.5s infinite;
  }

  h1 {
    font-family: 'Rajdhani', sans-serif;
    font-size: 42px;
    font-weight: 700;
    letter-spacing: -1px;
    color: #fff;
    line-height: 1;
  }

  h1 span { color: var(--accent); }

  .subtitle {
    color: var(--muted);
    font-size: 14px;
    margin-top: 8px;
  }

  /* الكارد */
  .card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 32px;
    position: relative;
    overflow: hidden;
    animation: fadeUp 0.6s ease 0.1s both;
  }

  .card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent), transparent);
  }

  /* حقول الإدخال */
  .field {
    margin-bottom: 20px;
  }

  label {
    display: block;
    font-size: 12px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 8px;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 600;
  }

  .input-wrap {
    position: relative;
  }

  .input-icon {
    position: absolute;
    right: 14px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 16px;
    pointer-events: none;
  }

  input, textarea {
    width: 100%;
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    border-radius: 10px;
    color: var(--text);
    font-family: 'Noto Kufi Arabic', sans-serif;
    font-size: 14px;
    transition: all 0.2s;
    outline: none;
  }

  input { padding: 12px 40px 12px 14px; }
  textarea { padding: 12px 14px; resize: vertical; min-height: 90px; }

  input:focus, textarea:focus {
    border-color: var(--accent);
    background: rgba(230,57,70,0.05);
    box-shadow: 0 0 0 3px rgba(230,57,70,0.1);
  }

  input::placeholder, textarea::placeholder { color: var(--muted); }

  /* زر النسخ */
  .copy-btn {
    position: absolute;
    left: 10px;
    top: 50%;
    transform: translateY(-50%);
    background: rgba(230,57,70,0.15);
    border: 1px solid rgba(230,57,70,0.3);
    color: var(--accent2);
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 11px;
    cursor: pointer;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 600;
    letter-spacing: 1px;
    transition: all 0.2s;
  }

  .copy-btn:hover { background: rgba(230,57,70,0.3); }

  /* فاصل */
  .divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 24px 0;
  }

  /* زر الإرسال */
  .submit-btn {
    width: 100%;
    background: var(--accent);
    color: #fff;
    border: none;
    border-radius: 10px;
    padding: 14px;
    font-size: 15px;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    cursor: pointer;
    transition: all 0.2s;
    position: relative;
    overflow: hidden;
  }

  .submit-btn:hover {
    background: var(--accent2);
    transform: translateY(-1px);
    box-shadow: 0 8px 24px rgba(230,57,70,0.35);
  }

  .submit-btn:active { transform: translateY(0); }

  .submit-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
  }

  /* رسالة النجاح */
  .success-msg {
    display: none;
    text-align: center;
    padding: 20px;
    animation: fadeUp 0.4s ease;
  }

  .success-icon {
    font-size: 48px;
    margin-bottom: 12px;
    display: block;
  }

  .success-msg h3 {
    font-family: 'Rajdhani', sans-serif;
    font-size: 24px;
    color: var(--success);
    margin-bottom: 8px;
  }

  .success-msg p { color: var(--muted); font-size: 14px; }

  /* رسالة خطأ */
  .error-msg {
    display: none;
    background: rgba(230,57,70,0.1);
    border: 1px solid rgba(230,57,70,0.3);
    color: var(--accent2);
    border-radius: 8px;
    padding: 12px;
    font-size: 13px;
    margin-top: 12px;
    text-align: center;
  }

  /* أنيميشن */
  @keyframes fadeDown {
    from { opacity: 0; transform: translateY(-20px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.3; }
  }
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div class="badge">نظام الاستدعاء</div>
    <h1>CALL <span>UP</span></h1>
    <p class="subtitle">أكمل البيانات أدناه لتقديم طلب الاستدعاء</p>
  </div>

  <div class="card">
    <div id="form-content">
      <!-- ID الشخص -->
      <div class="field">
        <label>🎯 ID الشخص المُبلَّغ عنه</label>
        <div class="input-wrap">
          <span class="input-icon">🆔</span>
          <input type="text" id="target-id" placeholder="أدخل الـ ID هنا..." maxlength="20" />
          <button class="copy-btn" onclick="copyId()">نسخ</button>
        </div>
      </div>

      <!-- السبب -->
      <div class="field">
        <label>📋 السبب</label>
        <div class="input-wrap">
          <textarea id="reason" placeholder="اكتب سبب الاستدعاء بالتفصيل..."></textarea>
        </div>
      </div>

      <!-- الدليل -->
      <div class="field">
        <label>🔗 الدليل</label>
        <div class="input-wrap">
          <span class="input-icon">📎</span>
          <input type="text" id="evidence" placeholder="رابط الصورة أو الفيديو أو السكرين شوت..." />
        </div>
      </div>

      <hr class="divider">

      <button class="submit-btn" onclick="submitForm()">
        📞 إرسال طلب CALL UP
      </button>

      <div class="error-msg" id="error-msg"></div>
    </div>

    <!-- رسالة النجاح -->
    <div class="success-msg" id="success-msg">
      <span class="success-icon">✅</span>
      <h3>تم الإرسال!</h3>
      <p>تم تقديم طلب CALL UP بنجاح.<br>سيتم مراجعة الطلب من قِبل الإدارة.</p>
    </div>
  </div>
</div>

<script>
  function copyId() {
    const val = document.getElementById('target-id').value;
    if (!val) { alert('أدخل الـ ID أولاً!'); return; }
    navigator.clipboard.writeText(val).then(() => {
      const btn = document.querySelector('.copy-btn');
      btn.textContent = '✓ تم';
      setTimeout(() => btn.textContent = 'نسخ', 2000);
    });
  }

  async function submitForm() {
    const targetId = document.getElementById('target-id').value.trim();
    const reason   = document.getElementById('reason').value.trim();
    const evidence = document.getElementById('evidence').value.trim();
    const errEl    = document.getElementById('error-msg');

    errEl.style.display = 'none';

    if (!targetId || !reason || !evidence) {
      errEl.textContent = '❌ يرجى ملء جميع الحقول!';
      errEl.style.display = 'block';
      return;
    }

    if (!/^\\d{17,20}$/.test(targetId)) {
      errEl.textContent = '❌ الـ ID غير صحيح! يجب أن يكون أرقاماً فقط.';
      errEl.style.display = 'block';
      return;
    }

    const btn = document.querySelector('.submit-btn');
    btn.disabled = true;
    btn.textContent = '⏳ جاري الإرسال...';

    try {
      const res = await fetch('/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target_id: targetId, reason, evidence })
      });

      const data = await res.json();

      if (data.success) {
        document.getElementById('form-content').style.display = 'none';
        document.getElementById('success-msg').style.display  = 'block';
      } else {
        errEl.textContent = '❌ ' + (data.error || 'حدث خطأ، حاول مجدداً.');
        errEl.style.display = 'block';
        btn.disabled = false;
        btn.textContent = '📞 إرسال طلب CALL UP';
      }
    } catch (e) {
      errEl.textContent = '❌ تعذر الاتصال بالخادم.';
      errEl.style.display = 'block';
      btn.disabled = false;
      btn.textContent = '📞 إرسال طلب CALL UP';
    }
  }
</script>
</body>
</html>
"""


@app.route("/callup")
def callup_page():
    return render_template_string(HTML_PAGE)


@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    target_id = data.get("target_id", "").strip()
    reason    = data.get("reason", "").strip()
    evidence  = data.get("evidence", "").strip()

    if not target_id or not reason or not evidence:
        return jsonify({"success": False, "error": "جميع الحقول مطلوبة"})

    if not target_id.isdigit():
        return jsonify({"success": False, "error": "ID غير صحيح"})

    # ---- تطبيق الأدوار على الديسكورد ----
    headers = {
        "Authorization": f"Bot {BOT_TOKEN}",
        "Content-Type": "application/json"
    }

    role_errors = []

    # شيل WHITELIST
    r1 = requests.delete(
        f"https://discord.com/api/v10/guilds/{GUILD_ID}/members/{target_id}/roles/{WHITELIST_ROLE_ID}",
        headers=headers
    )
    if r1.status_code not in (204, 404):
        role_errors.append(f"فشل شيل WHITELIST: {r1.status_code}")

    # أعطه CALL UP
    r2 = requests.put(
        f"https://discord.com/api/v10/guilds/{GUILD_ID}/members/{target_id}/roles/{CALLUP_ROLE_ID}",
        headers=headers
    )
    if r2.status_code not in (204, 200):
        role_errors.append(f"فشل إعطاء CALL UP: {r2.status_code}")

    # ---- إرسال لوق للويب هوك ----
    embed = {
        "embeds": [{
            "title": "📞 طلب CALL UP جديد",
            "color": 0xe63946,
            "fields": [
                {"name": "🎯 ID المُبلَّغ عنه", "value": f"`{target_id}`", "inline": True},
                {"name": "📋 السبب",            "value": reason,           "inline": False},
                {"name": "🔗 الدليل",           "value": evidence,         "inline": False},
                {"name": "⚙️ الإجراءات",        "value": "\n".join(role_errors) or "✅ تم تطبيق الأدوار بنجاح", "inline": False},
            ],
            "footer": {"text": "CALL UP System"}
        }]
    }
    requests.post(LOG_WEBHOOK, json=embed)

    return jsonify({"success": True})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
