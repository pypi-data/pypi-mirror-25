

(function(globals) {

  var django = globals.django || (globals.django = {});

  
  django.pluralidx = function(n) {
    var v=(n != 1);
    if (typeof(v) == 'boolean') {
      return v ? 1 : 0;
    } else {
      return v;
    }
  };
  

  /* gettext library */

  django.catalog = django.catalog || {};
  
  var newcatalog = {
    "#%(position)s": "#%(position)s", 
    "%(count)s language matches your query.": [
      "%(count)s spr\u00e5k samsvarer med din sp\u00f8rring.", 
      "%(count)s spr\u00e5k samsvarer med din sp\u00f8rring."
    ], 
    "%(count)s project matches your query.": [
      "%(count)s prosjekt samsvarer med din sp\u00f8rring.", 
      "%(count)s prosjekter samsvarer med din sp\u00f8rring."
    ], 
    "%(count)s user matches your query.": [
      "%(count)s bruker samsvarer med ditt s\u00f8k.", 
      "%(count)s brukere samsvarer med ditt s\u00f8k."
    ], 
    "%(timeSince)s via file upload": "%(timeSince)s via filopplasting", 
    "%s word": [
      "%s ord", 
      "%s ord"
    ], 
    "%s's accepted suggestions": "%ss godtatte forslag", 
    "%s's overwritten submissions": "%ss overskrevne innsendelser", 
    "%s's pending suggestions": "%ss ventende forslag", 
    "%s's rejected suggestions": "%ss avsl\u00e5tte forslag", 
    "%s's submissions": "%ss innsendelser", 
    "Accept": "Godta", 
    "Account Activation": "Kontoaktivering", 
    "Account Inactive": "Inaktiv konto", 
    "Active": "Aktiv", 
    "Add Language": "Legg til spr\u00e5k", 
    "Add Project": "Legg til prosjekt", 
    "Add User": "Legg til bruker", 
    "Administrator": "Administrator", 
    "After changing your password you will sign in automatically.": "Etter at du endrer ditt passord vil bli logget inn automatisk.", 
    "All Languages": "Alle spr\u00e5k", 
    "All Projects": "Alle prosjekter", 
    "An error occurred while attempting to sign in via %s.": "En feil inntraff i fors\u00f8k p\u00e5 \u00e5 logge inn via %s.", 
    "An error occurred while attempting to sign in via your social account.": "En feil inntraff under fors\u00f8k p\u00e5 \u00e5 logge inn via din sosiale konto.", 
    "Avatar": "Avatar", 
    "Cancel": "Avbryt", 
    "Clear all": "T\u00f8m alle", 
    "Clear value": "T\u00f8m verdi", 
    "Close": "Lukk", 
    "Code": "Kode", 
    "Collapse details": "Fold sammen detaljer", 
    "Congratulations! You have completed this task!": "Gratulerer, du har fullf\u00f8rt denne oppgaven!", 
    "Contact Us": "Kontakt oss", 
    "Contributors, 30 Days": "Bidrag, 30 dager", 
    "Creating new user accounts is prohibited.": "Opprettelse av nye kontoer nektes.", 
    "Delete": "Slett", 
    "Deleted successfully.": "Slettet.", 
    "Didn't receive an email? Check if it was accidentally filtered out as spam, or try requesting another copy of the email.": "Fikk du ikke e-posten? Sjekk at den ikke feilaktig ble filtrert ut som s\u00f8ppelpost, eller ved \u00e5 foresp\u00f8rre ny kopi av av den.", 
    "Disabled": "Avskrudd", 
    "Discard changes.": "Forkast endringer.", 
    "Edit Language": "Rediger spr\u00e5k", 
    "Edit My Public Profile": "Rediger min offentlige profil", 
    "Edit Project": "Rediger prosjekt", 
    "Edit User": "Rediger bruker", 
    "Edit the suggestion before accepting, if necessary": "Rediger forslaget f\u00f8r du godtar det, hvis n\u00f8dvendig", 
    "Email": "E-post", 
    "Email Address": "E-postadresse", 
    "Email Confirmation": "E-postbekreftelse", 
    "Enter your email address, and we will send you a message with the special link to reset your password.": "Skriv inn din e-postadresse, og du vil f\u00e5 tilsendt en melding med en spesiell lenke for \u00e5 tilbakestille ditt passord.", 
    "Error while connecting to the server": "Feil ved tilkopling til tjeneren", 
    "Expand details": "Utvid detaljer", 
    "File types": "Filtyper", 
    "Filesystems": "Filsystem", 
    "Find language by name, code": "Finn spr\u00e5k etter navn, kode", 
    "Find project by name, code": "Finn prosjekt etter navn, kode", 
    "Find user by name, email, properties": "Finn bruker etter navn, e-post, egenskaper", 
    "Full Name": "Fullt navn", 
    "Go back to browsing": "G\u00e5 tilbake til surfing", 
    "Go to the next string (Ctrl+.)<br/><br/>Also:<br/>Next page: Ctrl+Shift+.<br/>Last page: Ctrl+Shift+End": "G\u00e5 til neste streng (Ctrl+.)<br/><br/>Ogs\u00e5:<br/>Neste side: Ctrl+Shift+.<br/>Forrige side: Ctrl+Shift+End", 
    "Go to the previous string (Ctrl+,)<br/><br/>Also:<br/>Previous page: Ctrl+Shift+,<br/>First page: Ctrl+Shift+Home": "G\u00e5 til forrige streng (Ctrl+,)<br/><br/>Ogs\u00e5:<br/>Forrige side: Ctrl+Shift+,<br/>F\u00f8rste side: Ctrl+Shift+Home", 
    "Hide": "Skjul", 
    "Hide disabled": "Gjem avskrudde", 
    "I forgot my password": "Passordet mitt, det husker jeg ikke", 
    "Ignore Files": "Ignorer filer", 
    "Languages": "Spr\u00e5k", 
    "Less": "Mindre", 
    "LinkedIn": "LinkedIn", 
    "LinkedIn profile URL": "Nettadresse til LinkedIn-profil", 
    "Load More": "Last flere", 
    "Loading...": "Laster\u2026", 
    "Login / Password": "Innlogging / Passord", 
    "More": "Mer", 
    "More...": "Mer\u2026", 
    "My Public Profile": "Min offentlige profil", 
    "No": "Nei", 
    "No activity recorded in a given period": "Ingen aktivitet over en gitt tidsperiode", 
    "No results found": "Ingen resultater funnet", 
    "No results.": "Ingen resultater.", 
    "No, thanks": "Nei takk", 
    "Not found": "Ikke funnet", 
    "Note: when deleting a user their contributions to the site, e.g. comments, suggestions and translations, are attributed to the anonymous user (nobody).": "Merk: N\u00e5r du sletter en bruker vil deres bidrag til siden, f.eks. kommentarer, forslag og oversettelser bli kreditert den anonyme brukeren (ingen).", 
    "Number of Plurals": "Antall flertallsformer", 
    "Oops...": "Oida\u2026", 
    "Overview": "Oversikt", 
    "Password": "Passord", 
    "Password changed, signing in...": "Passord endret, logger inn\u2026", 
    "Permissions": "Tilganger", 
    "Personal description": "Biografi", 
    "Personal website URL": "Nettadresse til hjemmeside", 
    "Please follow that link to continue the account creation.": "F\u00f8lg den lenken for \u00e5 fortsette kontopprettelse.", 
    "Please follow that link to continue the password reset procedure.": "F\u00f8lg den lenken for \u00e5 fortsette prosessen med \u00e5 tilbakestille passord.", 
    "Please select a valid user.": "Velg en gyldig bruker.", 
    "Plural Equation": "Flertallsformel", 
    "Plural form %(index)s": "Flertallsform %(index)s", 
    "Preview will be displayed here.": "Forh\u00e5ndsvisning vil bli vist her.", 
    "Project Tree Style": "Stil for prosjekttre", 
    "Public Profile": "Offentlig profil", 
    "Quality Checks": "Kvalitetssjekk", 
    "Reject": "Avvis", 
    "Reload page": "Gjeninnlast side", 
    "Repeat Password": "Gjenta passord", 
    "Resend Email": "Send e-post p\u00e5 ny", 
    "Reset Password": "Tilbakestill passord", 
    "Reset Your Password": "Tilbakestill ditt passord", 
    "Reviewed": "Korrekturlest", 
    "Save": "Lagre", 
    "Saved successfully.": "Lagret.", 
    "Screenshot Search Prefix": "Prefiks for skjermbildes\u00f8k", 
    "Search Languages": "S\u00f8k i spr\u00e5k", 
    "Search Projects": "S\u00f8k i prosjekter", 
    "Search Users": "S\u00f8k i brukere", 
    "Select...": "Velg\u2026", 
    "Send Email": "Send e-post", 
    "Sending email to %s...": "Sender e-post til %s\u2026", 
    "Server error": "Tjenerfeil", 
    "Set New Password": "Sett nytt passord", 
    "Set a new password": "Sett et nytt passord", 
    "Settings": "Innstillinger", 
    "Short Bio": "Kort bio", 
    "Show": "Vis", 
    "Show disabled": "Vis avskrudde", 
    "Sign In": "Logg inn", 
    "Sign In With %s": "Logg inn med %s", 
    "Sign In With...": "Logg inn med\u2026", 
    "Sign Up": "Lag konto", 
    "Sign in as an existing user": "Logg inn som eksisterende bruker", 
    "Sign up as a new user": "Lag ny konto", 
    "Signed in. Redirecting...": "Innlogget. Omdirigerer\u2026", 
    "Signing in with an external service for the first time will automatically create an account for you.": "Innlogging med en ekstern tjeneste vil lage en konto til deg f\u00f8rste gang du logger inn.", 
    "Similar translations": "Lignende oversettelser", 
    "Social Services": "Sosiale tjenester", 
    "Social Verification": "Sosial bekreftelse", 
    "Source Language": "Kildespr\u00e5k", 
    "Special Characters": "Spesialtegn", 
    "String Errors Contact": "Kontakt for tekststrengfeil", 
    "Suggested": "Foresl\u00e5tt", 
    "Team": "Lag", 
    "The password reset link was invalid, possibly because it has already been used. Please request a new password reset.": "Tilbakestillingslenken for passordet var ikke gyldig, muligvis siden den allerede kan ha blitt brukt. Foresp\u00f8r en ny tilbakestilling.", 
    "The server seems down. Try again later.": "Tjeneren virker frakoblet. Pr\u00f8v igjen senere.", 
    "There are unsaved changes. Do you want to discard them?": "Ulagrede endringer. \u00d8nsker du \u00e5 forkaste dem?", 
    "There is %(count)s language.": [
      "Det finnes %(count)s spr\u00e5k.", 
      "Det finnes %(count)s spr\u00e5k. Nedenfor finner du de nyligst tillagte."
    ], 
    "There is %(count)s project.": [
      "Det finnes %(count)s prosjekt.", 
      "Det finnes %(count)s prosjekter. Nedenfor finner du de sist tillagte."
    ], 
    "There is %(count)s user.": [
      "Det er %(count)s bruker.", 
      "Det er %(count)s brukere. Nedenfor er de mest nylig tillagte."
    ], 
    "This email confirmation link expired or is invalid.": "Denne e-postbekreftelseslenken er utl\u00f8pt eller ugyldig.", 
    "This string no longer exists.": "Denne strengen finnes ikke lenger.", 
    "To set or change your avatar for your email address (%(email)s), please go to gravatar.com.": "For \u00e5 sette eller endre avatar for din e-postadresse (%(email)s), g\u00e5 til gravatar.com.", 
    "Translated": "Oversatt", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project": "Oversatt av %(fullname)s i \"<span title=\"%(path)s\">%(project)s</span>\"-prosjektet", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project %(time_ago)s": "Oversatt av %(fullname)s i \"<span title=\"%(path)s\">%(project)s</span>\"-prosjektet %(time_ago)s", 
    "Try again": "Pr\u00f8v igjen", 
    "Twitter": "Twitter", 
    "Twitter username": "Twitter-brukernavn", 
    "Type to search": "Skriv for \u00e5 s\u00f8ke", 
    "Updating data": "Oppdaterer data", 
    "Use the search form to find the language, then click on a language to edit.": "Bruk s\u00f8kefunksjonen til \u00e5 finne spr\u00e5ket, klikk s\u00e5 p\u00e5 spr\u00e5ket for \u00e5 redigere.", 
    "Use the search form to find the project, then click on a project to edit.": "Bruk s\u00f8kefunksjonen for \u00e5 finne prosjektet, klikk s\u00e5 p\u00e5 et prosjektet for \u00e5 redigere.", 
    "Use the search form to find the user, then click on a user to edit.": "Bruk s\u00f8kefunksjonen til \u00e5 finne brukeren, klikk s\u00e5 p\u00e5 brukeren for \u00e5 redigere.", 
    "Username": "Brukernavn", 
    "We have sent an email containing the special link to <span>%s</span>": "En e-post som inneholder den spesielle lenken har blitt sendt til <span>%s</span>", 
    "We have sent an email containing the special link to <span>%s</span>. Please check your spam folder if you do not see the email.": "En e-post som inneholder den spesielle lenken har blitt sendt til <span>%s</span>. Se gjennom s\u00f8ppelposten hvis du ikke ser e-posten.", 
    "We have sent an email containing the special link to the address used to register this account. Please check your spam folder if you do not see the email.": "En e-post som inneholder den spesielle lenken har blitt sendt til adressen brukeren oppga i registreringen av denne kontoen. Se gjennom sp\u00f8ppelposten din hvis du ikke ser e-posten.", 
    "Website": "Nettside", 
    "Yes": "Ja", 
    "You have unsaved changes in this string. Navigating away will discard those changes.": "Du har ulagrede endringer i denne tekststrengen. \u00c5 navigere bort herfra vil forkaste de endringene.", 
    "Your Full Name": "Ditt fulle navn", 
    "Your LinkedIn profile URL": "Nettadresse til din LinkedIn-profil", 
    "Your Personal website/blog URL": "Nettadresse til din hjemmeside/blogg", 
    "Your Twitter username": "Ditt Twitter-brukernavn", 
    "Your account is inactive because an administrator deactivated it.": "Din konto er inaktiv fordi en administrator deaktiverte den.", 
    "Your account needs activation.": "Din konto m\u00e5 aktiveres.", 
    "disabled": "avskrudd", 
    "some anonymous user": "en anonym bruker", 
    "someone": "noen"
  };
  for (var key in newcatalog) {
    django.catalog[key] = newcatalog[key];
  }
  

  if (!django.jsi18n_initialized) {
    django.gettext = function(msgid) {
      var value = django.catalog[msgid];
      if (typeof(value) == 'undefined') {
        return msgid;
      } else {
        return (typeof(value) == 'string') ? value : value[0];
      }
    };

    django.ngettext = function(singular, plural, count) {
      var value = django.catalog[singular];
      if (typeof(value) == 'undefined') {
        return (count == 1) ? singular : plural;
      } else {
        return value[django.pluralidx(count)];
      }
    };

    django.gettext_noop = function(msgid) { return msgid; };

    django.pgettext = function(context, msgid) {
      var value = django.gettext(context + '\x04' + msgid);
      if (value.indexOf('\x04') != -1) {
        value = msgid;
      }
      return value;
    };

    django.npgettext = function(context, singular, plural, count) {
      var value = django.ngettext(context + '\x04' + singular, context + '\x04' + plural, count);
      if (value.indexOf('\x04') != -1) {
        value = django.ngettext(singular, plural, count);
      }
      return value;
    };

    django.interpolate = function(fmt, obj, named) {
      if (named) {
        return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
      } else {
        return fmt.replace(/%s/g, function(match){return String(obj.shift())});
      }
    };


    /* formatting library */

    django.formats = {
    "DATETIME_FORMAT": "N j, Y, P", 
    "DATETIME_INPUT_FORMATS": [
      "%Y-%m-%d %H:%M:%S", 
      "%Y-%m-%d %H:%M:%S.%f", 
      "%Y-%m-%d %H:%M", 
      "%Y-%m-%d", 
      "%m/%d/%Y %H:%M:%S", 
      "%m/%d/%Y %H:%M:%S.%f", 
      "%m/%d/%Y %H:%M", 
      "%m/%d/%Y", 
      "%m/%d/%y %H:%M:%S", 
      "%m/%d/%y %H:%M:%S.%f", 
      "%m/%d/%y %H:%M", 
      "%m/%d/%y"
    ], 
    "DATE_FORMAT": "N j, Y", 
    "DATE_INPUT_FORMATS": [
      "%Y-%m-%d", 
      "%m/%d/%Y", 
      "%m/%d/%y", 
      "%b %d %Y", 
      "%b %d, %Y", 
      "%d %b %Y", 
      "%d %b, %Y", 
      "%B %d %Y", 
      "%B %d, %Y", 
      "%d %B %Y", 
      "%d %B, %Y"
    ], 
    "DECIMAL_SEPARATOR": ".", 
    "FIRST_DAY_OF_WEEK": "0", 
    "MONTH_DAY_FORMAT": "F j", 
    "NUMBER_GROUPING": "0", 
    "SHORT_DATETIME_FORMAT": "m/d/Y P", 
    "SHORT_DATE_FORMAT": "m/d/Y", 
    "THOUSAND_SEPARATOR": ",", 
    "TIME_FORMAT": "P", 
    "TIME_INPUT_FORMATS": [
      "%H:%M:%S", 
      "%H:%M:%S.%f", 
      "%H:%M"
    ], 
    "YEAR_MONTH_FORMAT": "F Y"
  };

    django.get_format = function(format_type) {
      var value = django.formats[format_type];
      if (typeof(value) == 'undefined') {
        return format_type;
      } else {
        return value;
      }
    };

    /* add to global namespace */
    globals.pluralidx = django.pluralidx;
    globals.gettext = django.gettext;
    globals.ngettext = django.ngettext;
    globals.gettext_noop = django.gettext_noop;
    globals.pgettext = django.pgettext;
    globals.npgettext = django.npgettext;
    globals.interpolate = django.interpolate;
    globals.get_format = django.get_format;

    django.jsi18n_initialized = true;
  }

}(this));

