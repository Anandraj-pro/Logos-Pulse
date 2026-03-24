import streamlit.components.v1 as components


def copy_button(text: str, button_label: str = "Copy to Clipboard"):
    escaped_text = (
        text
        .replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("$", "\\$")
        .replace("'", "\\'")
        .replace('"', '\\"')
        .replace("\n", "\\n")
    )

    html_code = f"""
    <div style="text-align: center;">
        <button id="copyBtn" style="
            background-color: #7B68EE;
            color: white;
            border: none;
            padding: 14px 32px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            width: 100%;
            max-width: 400px;
            transition: background-color 0.3s;
        " onclick="copyToClipboard()">
            {button_label}
        </button>
        <p id="copyStatus" style="
            color: #28a745;
            font-weight: bold;
            margin-top: 8px;
            display: none;
        ">Copied! Now paste in WhatsApp</p>
    </div>

    <script>
    function copyToClipboard() {{
        const text = `{escaped_text}`;

        if (navigator.clipboard && navigator.clipboard.writeText) {{
            navigator.clipboard.writeText(text).then(function() {{
                showCopied();
            }}).catch(function() {{
                fallbackCopy(text);
            }});
        }} else {{
            fallbackCopy(text);
        }}
    }}

    function fallbackCopy(text) {{
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.left = '-9999px';
        document.body.appendChild(textarea);
        textarea.select();
        try {{
            document.execCommand('copy');
            showCopied();
        }} catch (err) {{
            alert('Copy failed. Please manually select and copy the text above.');
        }}
        document.body.removeChild(textarea);
    }}

    function showCopied() {{
        const btn = document.getElementById('copyBtn');
        const status = document.getElementById('copyStatus');
        btn.style.backgroundColor = '#28a745';
        btn.textContent = 'Copied!';
        status.style.display = 'block';
        setTimeout(function() {{
            btn.style.backgroundColor = '#7B68EE';
            btn.textContent = '{button_label}';
        }}, 3000);
    }}
    </script>
    """
    components.html(html_code, height=100)
