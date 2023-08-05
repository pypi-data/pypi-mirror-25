

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
      "%(count)s spr\u00e5k matchar din s\u00f6kning.", 
      "%(count)s spr\u00e5k matchar din s\u00f6kning."
    ], 
    "%(count)s project matches your query.": [
      "%(count)s projekt matchar din s\u00f6kning.", 
      "%(count)s projekt matchar din s\u00f6kning."
    ], 
    "%(count)s user matches your query.": [
      "%(count)s anv\u00e4ndare matchar din s\u00f6kning.", 
      "%(count)s anv\u00e4ndare matchar din s\u00f6kning."
    ], 
    "%(timeSince)s via file upload": "%(timeSince)s via fil\u00f6verf\u00f6ring", 
    "%s word": [
      "%s ord", 
      "%s ord"
    ], 
    "%s's accepted suggestions": "%s godk\u00e4nda f\u00f6rslag", 
    "%s's overwritten submissions": "%s \u00f6verskrivna bidrag", 
    "%s's pending suggestions": "%s v\u00e4ntande f\u00f6rslag", 
    "%s's rejected suggestions": "%s avvisade f\u00f6rslag", 
    "%s's submissions": "%s bidrag", 
    "Accept": "Godk\u00e4nn", 
    "Account Activation": "Kontoaktivering", 
    "Account Inactive": "Konto inaktivt", 
    "Active": "Aktiv", 
    "Add Language": "L\u00e4gg till spr\u00e5k", 
    "Add Project": "L\u00e4gg till projekt", 
    "Add User": "L\u00e4gg till anv\u00e4ndare", 
    "Administrator": "Administrat\u00f6r", 
    "After changing your password you will sign in automatically.": "N\u00e4r du har \u00e4ndrat ditt l\u00f6senord kommer du att logga in automatiskt.", 
    "All Languages": "Alla spr\u00e5k", 
    "All Projects": "Alla projekt", 
    "An error occurred while attempting to sign in via %s.": "Ett fel uppstod vid f\u00f6rs\u00f6k att logga in via %s.", 
    "An error occurred while attempting to sign in via your social account.": "Ett fel uppstod vid f\u00f6rs\u00f6k att logga in via ditt sociala konto.", 
    "Avatar": "Avatar", 
    "Cancel": "Avbryt", 
    "Clear all": "Rensa alla", 
    "Clear value": "Rensa v\u00e4rde", 
    "Close": "St\u00e4ng", 
    "Code": "Kod", 
    "Collapse details": "D\u00f6lj detaljer", 
    "Congratulations! You have completed this task!": "Grattis! Du har slutf\u00f6rt denna uppgift!", 
    "Contact Us": "Kontakta oss", 
    "Contributors, 30 Days": "Bidragsgivare, 30 dagar", 
    "Creating new user accounts is prohibited.": "Skapa nya anv\u00e4ndarkonton \u00e4r f\u00f6rbjudet.", 
    "Delete": "Ta bort", 
    "Deleted successfully.": "Borttagen.", 
    "Didn't receive an email? Check if it was accidentally filtered out as spam, or try requesting another copy of the email.": "Fick du ingen e-post? Kontrollera om det inte av misstag har filtrerats bort som spam eller prova att beg\u00e4ra en kopia av e-postmeddelandet.", 
    "Disabled": "Inaktiverad", 
    "Discard changes.": "Bortse fr\u00e5n \u00e4ndringar.", 
    "Edit Language": "Redigera spr\u00e5k", 
    "Edit My Public Profile": "Redigera min publika profil", 
    "Edit Project": "Redigera projekt", 
    "Edit User": "Redigera anv\u00e4ndare", 
    "Edit the suggestion before accepting, if necessary": "Redigera f\u00f6rslaget innan du godk\u00e4nner, om n\u00f6dv\u00e4ndigt", 
    "Email": "E-post", 
    "Email Address": "E-postadress", 
    "Email Confirmation": "E-postbekr\u00e4ftelse", 
    "Enter your email address, and we will send you a message with the special link to reset your password.": "Ange din e-postadress och vi kommer att skicka ett meddelande med en s\u00e4rskild l\u00e4nk f\u00f6r att \u00e5terst\u00e4lla ditt l\u00f6senord.", 
    "Error while connecting to the server": "Fel i anslutningen till servern", 
    "Expand details": "Visa detaljer", 
    "File types": "Filtyper", 
    "Filesystems": "Filsystem", 
    "Find language by name, code": "Hitta spr\u00e5k genom namn, kod", 
    "Find project by name, code": "Hitta projekt genom namn, kod", 
    "Find user by name, email, properties": "Hitta anv\u00e4ndare genom namn, e-post, egenskaper", 
    "Full Name": "Fullst\u00e4ndigt namn", 
    "Go back to browsing": "G\u00e5 tillbaks f\u00f6r att bl\u00e4ddra", 
    "Go to the next string (Ctrl+.)<br/><br/>Also:<br/>Next page: Ctrl+Shift+.<br/>Last page: Ctrl+Shift+End": "G\u00e5 till n\u00e4sta str\u00e4ng (Ctrl+.)<br/><br/>Ocks\u00e5:<br/>N\u00e4sta sida: Ctrl+Shift+.<br/>Sista sidan: Ctrl+Shift+End", 
    "Go to the previous string (Ctrl+,)<br/><br/>Also:<br/>Previous page: Ctrl+Shift+,<br/>First page: Ctrl+Shift+Home": "G\u00e5 till f\u00f6reg\u00e5ende str\u00e4ng (Ctrl+,)<br/><br/>Ocks\u00e5:<br/>F\u00f6reg\u00e5ende sida: Ctrl+Shift+,<br/>F\u00f6rsta sidan: Ctrl+Shift+Home", 
    "Hide": "D\u00f6lj", 
    "Hide disabled": "D\u00f6lj inaktiverad", 
    "I forgot my password": "Jag har gl\u00f6mt mitt l\u00f6senord", 
    "Ignore Files": "Ignorera filer", 
    "Languages": "Spr\u00e5k", 
    "Less": "Mindre", 
    "LinkedIn": "LinkedIn", 
    "LinkedIn profile URL": "LinkedIn profil-URL", 
    "Load More": "Ladda mer", 
    "Loading...": "Laddar...", 
    "Login / Password": "Inloggning / L\u00f6senord", 
    "More": "Mer", 
    "More...": "Mer...", 
    "My Public Profile": "Min publika profil", 
    "No": "Nej", 
    "No activity recorded in a given period": "Ingen aktivitet registrerad under en viss period", 
    "No results found": "Inga resultat hittades", 
    "No results.": "Inga resultat.", 
    "No, thanks": "Nej, tack", 
    "Not found": "Hittades inte", 
    "Note: when deleting a user their contributions to the site, e.g. comments, suggestions and translations, are attributed to the anonymous user (nobody).": "Obs: n\u00e4r du tar bort en anv\u00e4ndare kommer deras bidrag till webbplatsen, t.ex. kommentarer, f\u00f6rslag och \u00f6vers\u00e4ttningar, tillskrivas till den anonyma anv\u00e4ndaren (ingen).", 
    "Number of Plurals": "Antal plural", 
    "Oops...": "Oj d\u00e5...", 
    "Overview": "\u00d6versikt", 
    "Password": "L\u00f6senord", 
    "Password changed, signing in...": "L\u00f6senord \u00e4ndrat, loggar in...", 
    "Permissions": "R\u00e4ttigheter", 
    "Personal description": "Personlig beskrivning", 
    "Personal website URL": "Personlig webbplats-URL", 
    "Please follow that link to continue the account creation.": "F\u00f6lj l\u00e4nken f\u00f6r att forts\u00e4tta skapa ett konto.", 
    "Please follow that link to continue the password reset procedure.": "F\u00f6lj l\u00e4nken f\u00f6r att forts\u00e4tta \u00e5terst\u00e4llning av l\u00f6senord.", 
    "Please select a valid user.": "V\u00e4lj en giltig anv\u00e4ndare.", 
    "Plural Equation": "Pluralsekvation", 
    "Plural form %(index)s": "Pluralform %(index)s", 
    "Preview will be displayed here.": "F\u00f6rhandsgranskning visas h\u00e4r.", 
    "Project / Language": "Projekt / Spr\u00e5k", 
    "Project Tree Style": "Projekt tr\u00e4dstil", 
    "Provide optional comment (will be publicly visible)": "Ge valfri kommentar (visas offentligt)", 
    "Public Profile": "Publik profil", 
    "Quality Checks": "Kvalitetskontroller", 
    "Reject": "Neka", 
    "Reload page": "Ladda om sida", 
    "Repeat Password": "Upprepa l\u00f6senord", 
    "Resend Email": "Skicka e-post igen", 
    "Reset Password": "\u00c5terst\u00e4ll l\u00f6senord", 
    "Reset Your Password": "\u00c5terst\u00e4ll ditt l\u00f6senord", 
    "Reviewed": "Granskat", 
    "Save": "Spara", 
    "Saved successfully.": "Sparad.", 
    "Score Change": "Po\u00e4ngf\u00f6r\u00e4ndring", 
    "Screenshot Search Prefix": "S\u00f6kprefix sk\u00e4rmbild", 
    "Search Languages": "S\u00f6k spr\u00e5k", 
    "Search Projects": "S\u00f6k projekt", 
    "Search Users": "S\u00f6k anv\u00e4ndare", 
    "Select...": "V\u00e4lj...", 
    "Send Email": "Skicka e-post", 
    "Sending email to %s...": "Skickar e-post till %s...", 
    "Server error": "Ett fel intr\u00e4ffade p\u00e5 servern", 
    "Set New Password": "Ange nytt l\u00f6senord", 
    "Set a new password": "Ange ett nytt l\u00f6senord", 
    "Settings": "Inst\u00e4llningar", 
    "Short Bio": "Kort biografi", 
    "Show": "Visa", 
    "Show disabled": "Visa inaktiverad", 
    "Sign In": "Logga in", 
    "Sign In With %s": "Logga in med %s", 
    "Sign In With...": "Logga in med...", 
    "Sign Up": "Registrera dig", 
    "Sign in as an existing user": "Logga in som en befintlig anv\u00e4ndare", 
    "Sign up as a new user": "Registrera dig som ny anv\u00e4ndare", 
    "Signed in. Redirecting...": "Inloggad. Omdirigerar...", 
    "Signing in with an external service for the first time will automatically create an account for you.": "Logga in med en extern tj\u00e4nsteleverant\u00f6r f\u00f6r f\u00f6rsta g\u00e5ngen kommer att automatiskt skapa ett konto f\u00f6r dig.", 
    "Similar translations": "Liknande \u00f6vers\u00e4ttningar", 
    "Social Services": "Sociala tj\u00e4nster", 
    "Social Verification": "Social verifikation", 
    "Source Language": "K\u00e4llspr\u00e5k", 
    "Special Characters": "Specialtecken", 
    "String Errors Contact": "Kontakt str\u00e4ngfel", 
    "Suggested": "F\u00f6reslagit", 
    "Team": "Grupp", 
    "The password reset link was invalid, possibly because it has already been used. Please request a new password reset.": "L\u00e4nken f\u00f6r l\u00f6senords\u00e5terst\u00e4llning var ogiltig, m\u00f6jligen eftersom det redan har anv\u00e4nts. Beg\u00e4r en ny l\u00f6senords\u00e5terst\u00e4llning.", 
    "The server seems down. Try again later.": "Servern tycks vara nere. F\u00f6rs\u00f6k igen senare.", 
    "There are unsaved changes. Do you want to discard them?": "Det finns \u00e4ndringar som inte sparats. Vill du kasta dem?", 
    "There is %(count)s language.": [
      "Det finns %(count)s spr\u00e5k.", 
      "Det finns %(count)s spr\u00e5k. Nedan finns de som lades till senast."
    ], 
    "There is %(count)s project.": [
      "Det finns %(count)s projekt.", 
      "Det finns %(count)s projekt. Nedan finns de som lades till senast."
    ], 
    "There is %(count)s user.": [
      "Det finns %(count)s anv\u00e4ndare.", 
      "Det finns %(count)s anv\u00e4ndare. Nedan finns de som lades till senast."
    ], 
    "This email confirmation link expired or is invalid.": "Denna e-postbekr\u00e4ftelsel\u00e4nk har upph\u00f6rt att g\u00e4lla eller \u00e4r ogiltig.", 
    "This string no longer exists.": "Str\u00e4ngen finns inte l\u00e4ngre.", 
    "To set or change your avatar for your email address (%(email)s), please go to gravatar.com.": "F\u00f6r att st\u00e4lla in eller \u00e4ndra din avatar f\u00f6r din e-postadress (%(email)s), g\u00e5 till gravatar.com.", 
    "Translated": "\u00d6versatt", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project": "\u00d6versatt av %(fullname)s i projekt \u201c<span title=\"%(path)s\">%(project)s</span>\u201d", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project %(time_ago)s": "\u00d6versatt av %(fullname)s i projekt \u201c<span title=\"%(path)s\">%(project)s</span>\u201d %(time_ago)s", 
    "Try again": "F\u00f6rs\u00f6k igen", 
    "Twitter": "Twitter", 
    "Twitter username": "Anv\u00e4ndarnamn Twitter", 
    "Type to search": "Skriv f\u00f6r att s\u00f6ka", 
    "Updating data": "Uppdaterar data", 
    "Use the search form to find the language, then click on a language to edit.": "Anv\u00e4nd s\u00f6kfunktionen f\u00f6r att hitta spr\u00e5ket, klicka p\u00e5 ett spr\u00e5k att redigera.", 
    "Use the search form to find the project, then click on a project to edit.": "Anv\u00e4nd s\u00f6kfunktionen f\u00f6r att hitta projektet, klicka sedan p\u00e5 ett projekt f\u00f6r att redigera.", 
    "Use the search form to find the user, then click on a user to edit.": "Anv\u00e4nd s\u00f6kfunktionen f\u00f6r att hitta anv\u00e4ndaren, klicka sedan p\u00e5 en anv\u00e4ndare f\u00f6r att redigera.", 
    "Username": "Anv\u00e4ndarnamn", 
    "We found a user with <span>%(email)s</span> email in our system. Please provide the password to finish the sign in procedure. This is a one-off procedure, which will establish a link between your Pootle and %(provider)s accounts.": "Vi hittade en anv\u00e4ndare med e-post <span>%s</span> i v\u00e5rt system. Ange l\u00f6senordet f\u00f6r att slutf\u00f6ra inloggningen. Detta \u00e4r en eng\u00e5ngsf\u00f6reteelse, vilket kommer att skapa en l\u00e4nk mellan Pootle och %(provider)s konton.", 
    "We have sent an email containing the special link to <span>%s</span>": "Vi har skickat ett e-postmeddelande som inneh\u00e5ller en s\u00e4rskild l\u00e4nk till <span>%s</span>", 
    "We have sent an email containing the special link to <span>%s</span>. Please check your spam folder if you do not see the email.": "Vi har skickat ett e-postmeddelande som inneh\u00e5ller en s\u00e4rskild l\u00e4nk till <span>%s</span>. Kontrollera din skr\u00e4ppostmapp om du inte ser e-postmeddelandet.", 
    "We have sent an email containing the special link to the address used to register this account. Please check your spam folder if you do not see the email.": "Vi har skickat ett e-postmeddelande som inneh\u00e5ller en s\u00e4rskild l\u00e4nk till den adress som anv\u00e4nts f\u00f6r att registrera kontot. Kontrollera din skr\u00e4ppostmapp om du inte ser e-postmeddelandet.", 
    "Website": "Webbplats", 
    "Why are you part of our translation project? Describe yourself, inspire others!": "Varf\u00f6r \u00e4r du en del av v\u00e5r \u00f6vers\u00e4ttningsprojekt? Beskriv dig sj\u00e4lv, inspirera andra!", 
    "Yes": "Ja", 
    "You have unsaved changes in this string. Navigating away will discard those changes.": "Du har \u00e4ndringar som inte sparats i str\u00e4ngen. Genom att navigera bort kastas dessa f\u00f6r\u00e4ndringar.", 
    "Your Full Name": "Ditt fullst\u00e4ndiga namn", 
    "Your LinkedIn profile URL": "Din LinkedIn profil-URL", 
    "Your Personal website/blog URL": "Din personliga hemsida/blogg-URL", 
    "Your Twitter username": "Ditt Twitter-anv\u00e4ndarnamn", 
    "Your account is inactive because an administrator deactivated it.": "Ditt konto \u00e4r inaktivt eftersom en administrat\u00f6r har inaktiverat det.", 
    "Your account needs activation.": "Ditt konto beh\u00f6ver aktiveras.", 
    "disabled": "inaktiverad", 
    "some anonymous user": "n\u00e5gon anonym anv\u00e4ndare", 
    "someone": "n\u00e5gon"
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

