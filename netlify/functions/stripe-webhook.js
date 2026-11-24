// Stripe tells this function when a parent pays; it records full access in Supabase.
// Netlify → Site configuration → Environment variables needs:
//   STRIPE_WEBHOOK_SECRET  (whsec_..., from Stripe → Developers → Webhooks)
//   SUPABASE_URL           (https://xxxx.supabase.co)
//   SUPABASE_SERVICE_KEY   (Supabase → Project settings → API → service_role; keep secret)
//   TEST_DATE              (optional, e.g. 2027-09-15: when the "until the test" plan ends)
const crypto = require("crypto");

function verify(body, header, secret) {
  if (!header || !secret) return false;
  const parts = Object.fromEntries(header.split(",").map(p => p.split("=")));
  const sig = crypto.createHmac("sha256", secret).update(`${parts.t}.${body}`).digest("hex");
  const age = Math.abs(Date.now() / 1000 - Number(parts.t));
  const v1 = header.split(",").filter(p => p.startsWith("v1=")).map(p => p.slice(3));
  return age < 600 && v1.some(s => s.length === sig.length && crypto.timingSafeEqual(Buffer.from(s), Buffer.from(sig)));
}

async function db(path, method, payload, extra = {}) {
  const r = await fetch(process.env.SUPABASE_URL + "/rest/v1/" + path, {
    method,
    headers: {
      apikey: process.env.SUPABASE_SERVICE_KEY,
      Authorization: "Bearer " + process.env.SUPABASE_SERVICE_KEY,
      "Content-Type": "application/json",
      ...extra,
    },
    body: payload ? JSON.stringify(payload) : undefined,
  });
  if (!r.ok) throw new Error(`Supabase ${r.status}: ${await r.text()}`);
  return r;
}

const addDays = d => new Date(Date.now() + d * 864e5).toISOString();

exports.handler = async event => {
  const body = event.isBase64Encoded ? Buffer.from(event.body, "base64").toString("utf8") : event.body;
  if (!verify(body, event.headers["stripe-signature"], process.env.STRIPE_WEBHOOK_SECRET)) return { statusCode: 400, body: "bad signature" };
  const ev = JSON.parse(body), o = ev.data.object;
  try {
    if (ev.type === "checkout.session.completed" && o.client_reference_id) {
      const monthly = o.mode === "subscription";
      const until = monthly ? addDays(35) : (process.env.TEST_DATE ? new Date(process.env.TEST_DATE + "T23:59:59Z").toISOString() : addDays(365));
      await db("access", "POST", {
        user_id: o.client_reference_id, plan: monthly ? "monthly" : "until-test", until,
        stripe_customer: o.customer || null, stripe_subscription: o.subscription || null, updated_at: new Date().toISOString(),
      }, { Prefer: "resolution=merge-duplicates" });
    }
    if (ev.type === "invoice.paid" && o.subscription) {           // each month's payment extends access
      await db(`access?stripe_subscription=eq.${encodeURIComponent(o.subscription)}`, "PATCH", { until: addDays(35), updated_at: new Date().toISOString() });
    }
    if (ev.type === "customer.subscription.deleted") {            // cancelled: access ends at the end of the paid period
      const end = o.current_period_end ? new Date(o.current_period_end * 1000).toISOString() : new Date().toISOString();
      await db(`access?stripe_subscription=eq.${encodeURIComponent(o.id)}`, "PATCH", { until: end, updated_at: new Date().toISOString() });
    }
  } catch (e) {
    console.error(e);
    return { statusCode: 500, body: "database error" };   // Stripe retries later
  }
  return { statusCode: 200, body: "ok" };
};
