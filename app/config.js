/* Site settings. Leave the values empty and the app works on each device only, exactly as now.
   Fill them in after following SETUP.md. The Supabase "anon" key is safe to publish here:
   the database rules (supabase/schema.sql) decide what it can do. Never put the service key here. */
window.MTG_CONFIG = {
  supabaseUrl: "",      // e.g. "https://abcdefgh.supabase.co"
  supabaseKey: "",      // Supabase → Project settings → API → anon public key
  payMonthly: "",       // Stripe payment link for £6 a month
  payOneoff: "",        // Stripe payment link for £39 until the test
  paywall: false        // true = free plan limits apply to anyone who has not paid
};
