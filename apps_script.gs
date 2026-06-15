/**
 * The Current Regime — sign-up backend (Google Apps Script).
 *
 * Stores newsletter sign-ups in a Google Sheet. The site form POSTs an email
 * here (doPost appends it); the local sync_subscribers.py reads them back
 * (doGet returns the list).
 *
 * SETUP (once):
 *   1. Create a Google Sheet. Put "timestamp" in A1 and "email" in B1.
 *   2. Extensions -> Apps Script. Replace the default code with this file.
 *   3. Deploy -> New deployment -> type "Web app".
 *        - Execute as: Me
 *        - Who has access: Anyone
 *      Authorize, then copy the Web app URL (ends in /exec).
 *   4. Paste that URL into apps_script_url.txt in the repo, then run build_site.py.
 *   5. Set SECRET below to the value in apps_script_key.txt (it protects the
 *      read endpoint, since the URL is public). After editing, redeploy:
 *      Deploy -> Manage deployments -> (edit) -> Version: New version -> Deploy.
 */

// Must match apps_script_key.txt. Anyone can POST (subscribe), but reading the
// list back (doGet) requires this key, so the URL in the page can't dump emails.
var SECRET = 'PASTE_THE_KEY_FROM_apps_script_key.txt';

function _sheet() {
  return SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
}

function _isEmail(s) {
  return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(s);
}

// Add a sign-up. Called by the site form (POST email=...).
function doPost(e) {
  var email = ((e && e.parameter && e.parameter.email) || '').trim().toLowerCase();
  if (_isEmail(email)) {
    var sh = _sheet();
    var existing = [];
    if (sh.getLastRow() > 0) {
      existing = sh.getRange(1, 2, sh.getLastRow(), 1).getValues()
        .map(function (r) { return (r[0] || '').toString().trim().toLowerCase(); });
    }
    if (existing.indexOf(email) === -1) {
      sh.appendRow([new Date(), email]);
    }
  }
  return ContentService.createTextOutput('ok');
}

// Return the current list, one email per line. Read by sync_subscribers.py.
// Requires the key so the public URL cannot be used to dump subscriber emails.
function doGet(e) {
  if (!e || !e.parameter || e.parameter.key !== SECRET) {
    return ContentService.createTextOutput('');
  }
  var sh = _sheet();
  if (sh.getLastRow() < 1) return ContentService.createTextOutput('');
  var col = sh.getRange(1, 2, sh.getLastRow(), 1).getValues();
  var seen = {}, out = [];
  col.forEach(function (r) {
    var s = (r[0] || '').toString().trim().toLowerCase();
    if (_isEmail(s) && !seen[s]) { seen[s] = 1; out.push(s); }
  });
  return ContentService.createTextOutput(out.join('\n'));
}
