# Switching on accounts and payments

The site works without any of this: progress is kept on each device. Do these steps when you are ready to charge.

## 1. Database (Supabase, free plan)
1. Create a project at supabase.com. Choose the London (eu-west-2) region.
2. SQL Editor → New query → paste all of `supabase/schema.sql` → Run.
3. Authentication → URL Configuration: Site URL `https://mind-the-gap-11plus.netlify.app/app/`, and add the same address under Redirect URLs.
4. Authentication → Providers → Email: keep it on (sign-in links, no passwords).
5. Project settings → API: copy the **Project URL** and the **anon public** key.

## 2. Payments (Stripe)
1. Create two products: "Monthly" £6 recurring monthly, and "Until the test" £39 one-off.
2. Make a Payment Link for each. In each link's settings, after payment redirect to `https://mind-the-gap-11plus.netlify.app/app/`.
3. Developers → Webhooks → Add endpoint `https://mind-the-gap-11plus.netlify.app/.netlify/functions/stripe-webhook`, events: `checkout.session.completed`, `invoice.paid`, `customer.subscription.deleted`. Copy the signing secret (`whsec_…`).

## 3. Netlify
Site configuration → Environment variables:
- `STRIPE_WEBHOOK_SECRET` = the whsec_ secret
- `SUPABASE_URL` = the Project URL
- `SUPABASE_SERVICE_KEY` = Supabase → API → **service_role** key (secret: only here, never in the site files)
- `TEST_DATE` = the day the £39 plan should end, e.g. `2027-09-30`

## 4. Switch on in the app
Edit `app/config.js`: fill in `supabaseUrl`, `supabaseKey` (anon key), `payMonthly`, `payOneoff`. Set `paywall: true` when you want the free limits to apply. Upload the file to GitHub; Netlify redeploys.

## 5. Before launch
- Fill in the [brackets] in `privacy.html` (your name, address, email, date).
- Register with the ICO (data protection fee, usually £52 a year): ico.org.uk/for-organisations/data-protection-fee.
- Test with Stripe test mode first: pay, check the `access` table gets a row, check the app shows "Full access".

## Seeing which questions children miss
Supabase → Table editor → `hardest_questions` (or `qstats`). Reported questions come first, then the most missed. Each id (e.g. `PT12-07a`, `SK-frac-Y03b`) matches the review sheet.

## When you upload a new app version
Change `VERSION` at the top of `app/sw.js` (any new text) so installed phones pick up the update.
