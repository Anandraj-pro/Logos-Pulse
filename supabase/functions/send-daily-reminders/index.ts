import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const SMTP_HOST = Deno.env.get("SMTP_HOST") ?? "smtp.gmail.com";
const SMTP_PORT = parseInt(Deno.env.get("SMTP_PORT") ?? "587");
const SMTP_USER = Deno.env.get("SMTP_USER")!;
const SMTP_PASSWORD = Deno.env.get("SMTP_PASSWORD")!;
const FROM_NAME = Deno.env.get("FROM_NAME") ?? "Logos Pulse";
const APP_URL = Deno.env.get("APP_URL") ?? "https://logos-pulse.streamlit.app";

const DAILY_VERSES = [
  "\"This is the day the LORD has made; we will rejoice and be glad in it.\" — Psalm 118:24",
  "\"But seek first the kingdom of God and His righteousness.\" — Matthew 6:33",
  "\"The prayer of a righteous person is powerful and effective.\" — James 5:16",
  "\"Your word is a lamp to my feet and a light to my path.\" — Psalm 119:105",
  "\"I can do all things through Christ who strengthens me.\" — Philippians 4:13",
  "\"Be still, and know that I am God.\" — Psalm 46:10",
  "\"Draw near to God and He will draw near to you.\" — James 4:8",
];

async function sendSmtpEmail(to: string, subject: string, body: string): Promise<boolean> {
  // Use Deno's TCP to connect to SMTP
  try {
    const conn = await Deno.connect({ hostname: SMTP_HOST, port: SMTP_PORT });
    const encoder = new TextEncoder();
    const decoder = new TextDecoder();

    const readLine = async (): Promise<string> => {
      const buf = new Uint8Array(1024);
      const n = await conn.read(buf);
      return decoder.decode(buf.subarray(0, n ?? 0));
    };

    const send = async (cmd: string) => {
      await conn.write(encoder.encode(cmd + "\r\n"));
    };

    await readLine(); // 220 greeting
    await send(`EHLO logos-pulse`);
    const ehloResp = await readLine();
    if (!ehloResp.includes("250")) throw new Error("EHLO failed");

    await send("STARTTLS");
    await readLine(); // 220 ready

    // Upgrade to TLS
    const tlsConn = await Deno.startTls(conn, { hostname: SMTP_HOST });

    const tlsRead = async (): Promise<string> => {
      const buf = new Uint8Array(4096);
      const n = await tlsConn.read(buf);
      return decoder.decode(buf.subarray(0, n ?? 0));
    };
    const tlsSend = async (cmd: string) => {
      await tlsConn.write(encoder.encode(cmd + "\r\n"));
    };

    await tlsSend(`EHLO logos-pulse`);
    await tlsRead();

    await tlsSend("AUTH LOGIN");
    await tlsRead();
    await tlsSend(btoa(SMTP_USER));
    await tlsRead();
    await tlsSend(btoa(SMTP_PASSWORD));
    const authResp = await tlsRead();
    if (!authResp.includes("235")) throw new Error("Auth failed");

    await tlsSend(`MAIL FROM:<${SMTP_USER}>`);
    await tlsRead();
    await tlsSend(`RCPT TO:<${to}>`);
    await tlsRead();
    await tlsSend("DATA");
    await tlsRead();

    const message = [
      `From: ${FROM_NAME} <${SMTP_USER}>`,
      `To: ${to}`,
      `Subject: ${subject}`,
      `Content-Type: text/plain; charset=utf-8`,
      ``,
      body,
      `.`,
    ].join("\r\n");

    await tlsSend(message);
    await tlsRead();
    await tlsSend("QUIT");
    tlsConn.close();
    return true;
  } catch (e) {
    console.error("SMTP error:", e);
    return false;
  }
}

Deno.serve(async (req: Request) => {
  // Only accept requests from pg_cron or authorized callers
  const authHeader = req.headers.get("Authorization") ?? "";
  if (!authHeader.startsWith("Bearer ") || authHeader.slice(7) !== SERVICE_ROLE_KEY) {
    return new Response(JSON.stringify({ error: "Unauthorized" }), { status: 401 });
  }

  const supabase = createClient(SUPABASE_URL, SERVICE_ROLE_KEY);
  const today = new Date().toISOString().slice(0, 10);
  const dayOfWeek = new Date().getDay(); // 0=Sun … 6=Sat
  const verse = DAILY_VERSES[dayOfWeek];

  // Check global toggle
  const { data: setting } = await supabase
    .from("system_settings")
    .select("value")
    .eq("key", "reminders_enabled")
    .single();

  if (!setting || setting.value !== "true") {
    return new Response(JSON.stringify({ skipped: "reminders_disabled" }), { status: 200 });
  }

  // Get Prayer Warriors with reminders enabled who haven't logged today
  const { data: warriors } = await supabase
    .from("user_profiles")
    .select("user_id")
    .eq("role", "prayer_warrior")
    .eq("reminder_enabled", true);

  if (!warriors?.length) {
    return new Response(JSON.stringify({ sent: 0, failed: 0 }), { status: 200 });
  }

  // Exclude those who already logged today
  const { data: loggedToday } = await supabase
    .from("daily_entries")
    .select("user_id")
    .eq("date", today)
    .in("user_id", warriors.map((w: { user_id: string }) => w.user_id));

  const loggedSet = new Set((loggedToday ?? []).map((r: { user_id: string }) => r.user_id));
  const unlogged = warriors.filter((w: { user_id: string }) => !loggedSet.has(w.user_id));

  let sent = 0;
  let failed = 0;

  for (const warrior of unlogged) {
    try {
      // Get auth user for email + preferred name
      const { data: authUser } = await supabase.auth.admin.getUserById(warrior.user_id);
      if (!authUser?.user?.email) continue;

      const email = authUser.user.email;
      const name =
        authUser.user.user_metadata?.preferred_name ||
        authUser.user.user_metadata?.first_name ||
        "Warrior";

      const subject = `Logos Pulse — Don't forget your spiritual disciplines today`;
      const body = [
        `Hi ${name},`,
        ``,
        `It looks like you haven't logged your spiritual disciplines for today (${today}).`,
        ``,
        `Take a few minutes to pray, read, and record your activity:`,
        `${APP_URL}`,
        ``,
        `Today's verse:`,
        verse,
        ``,
        `Keep pressing forward — your consistency matters!`,
        ``,
        `— The Logos Pulse Team`,
        ``,
        `To stop receiving these reminders, visit Settings in the app.`,
      ].join("\n");

      const ok = await sendSmtpEmail(email, subject, body);

      if (ok) {
        sent++;
        await supabase.from("audit_log").insert({
          actor_id: warrior.user_id,
          action: "reminder_email_sent",
          target_type: "user",
          target_id: warrior.user_id,
          details: { date: today },
        });
      } else {
        failed++;
        await supabase.from("audit_log").insert({
          actor_id: warrior.user_id,
          action: "reminder_email_failed",
          target_type: "user",
          target_id: warrior.user_id,
          details: { date: today, error: "SMTP delivery failed" },
        });
      }
    } catch (err) {
      failed++;
      console.error("Error processing warrior:", warrior.user_id, err);
    }
  }

  // Log overall run summary (actor_id = first warrior or a placeholder)
  const summaryActorId = unlogged[0]?.user_id ?? warriors[0]?.user_id;
  if (summaryActorId) {
    await supabase.from("audit_log").insert({
      actor_id: summaryActorId,
      action: "reminder_email_sent",
      target_type: "digest",
      details: { sent, failed, date: today },
    });
  }

  return new Response(JSON.stringify({ sent, failed }), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
});
