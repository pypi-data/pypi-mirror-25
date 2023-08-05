

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
    "%(count)s language matches your query.": [
      "%(count)s Sprache passt zu Ihrer Anfrage.", 
      "%(count)s Sprachen passen zu Ihrer Anfrage."
    ], 
    "%(count)s project matches your query.": [
      "%(count)s Projekt passt zu Ihrer Anfrage.", 
      "%(count)s Projekte passen zu Ihrer Anfrage."
    ], 
    "%(count)s user matches your query.": [
      "%(count)s Benutzer passt zu Ihrer Anfrage.", 
      "%(count)s Benutzer passen zu Ihrer Anfrage."
    ], 
    "%s's accepted suggestions": "%ss akzeptierte Vorschl\u00e4ge", 
    "%s's overwritten submissions": "%ss ge\u00e4nderte Einreichungen", 
    "%s's pending suggestions": "%ss wartende Vorschl\u00e4ge", 
    "%s's rejected suggestions": "%ss abgelehnte Vorschl\u00e4ge", 
    "%s's submissions": "%ss Einreichungen", 
    "Account Activation": "Konten-Aktivierung", 
    "Account Inactive": "Konto ist inaktiv", 
    "Active": "Aktiv", 
    "Add Language": "Sprache hinzuf\u00fcgen", 
    "Add Project": "Projekt hinzuf\u00fcgen", 
    "Add User": "Benutzer hinzuf\u00fcgen", 
    "Administrator": "Administrator", 
    "After changing your password you will sign in automatically.": "Nach dem \u00c4ndern des Passwortes werden Sie automatisch angemeldet.", 
    "All Languages": "Alle Sprachen", 
    "All Projects": "Alle Projekte", 
    "An error occurred while attempting to sign in via %s.": "Beim Versuch der Anmeldung \u00fcber %s ist ein Fehler aufgetreten.", 
    "An error occurred while attempting to sign in via your social account.": "Beim Versuch der Anmeldung \u00fcber Ihren Social Account ist ein Fehler aufgetreten.", 
    "Avatar": "Avatar", 
    "Cancel": "Abbrechen", 
    "Clear all": "Alles l\u00f6schen", 
    "Clear value": "Wert l\u00f6schen", 
    "Close": "Schlie\u00dfen", 
    "Code": "Code", 
    "Collapse details": "Details verbergen", 
    "Contact Us": "Kontaktiere uns", 
    "Delete": "L\u00f6schen", 
    "Deleted successfully.": "Erfolgreich gel\u00f6scht.", 
    "Didn't receive an email? Check if it was accidentally filtered out as spam, or try requesting another copy of the email.": "Sie haben keine E-Mail erhalten? Pr\u00fcfen Sie, ob sie versehentlich als Spam ausgefiltert wurde oder fordern Sie eine weitere Kopie der E-Mail an.", 
    "Disabled": "Deaktiviert", 
    "Discard changes.": "\u00c4nderungen verwerfen.", 
    "Edit Language": "Sprache editieren", 
    "Edit My Public Profile": "Mein \u00f6ffentliches Profile editieren", 
    "Edit Project": "Projekt editieren", 
    "Edit User": "Benutzer editieren", 
    "Email": "E-Mail", 
    "Email Confirmation": "Email-Best\u00e4tigung", 
    "Error while connecting to the server": "Fehler beim Verbinden mit dem Server", 
    "Expand details": "Details erweitern", 
    "File types": "Dateitypen", 
    "Find language by name, code": "Sprache nach Namen oder Code suchen", 
    "Find project by name, code": "Projekt nach Namen oder Code suchen", 
    "Find user by name, email, properties": "Benutzer nach Namen, E-Mail oder Eigenschaften suchen", 
    "Full Name": "Vollst\u00e4ndiger Name", 
    "Go back to browsing": "Schauen Sie sich weiter um", 
    "Go to the next string (Ctrl+.)<br/><br/>Also:<br/>Next page: Ctrl+Shift+.<br/>Last page: Ctrl+Shift+End": "Zur n\u00e4chsten Zeichenkette gehen (Ctrl+.)<br/><br/>Au\u00dferdem:<br/>N\u00e4chste Seite: Ctrl+Shift+.<br/>Letzte Seite: Ctrl+Shift+End", 
    "Go to the previous string (Ctrl+,)<br/><br/>Also:<br/>Previous page: Ctrl+Shift+,<br/>First page: Ctrl+Shift+Home": "Zur vorigen Zeichenkette gehen (Ctrl+,)<br/><br/>Au\u00dferdem:<br/>Vorige Seite: Ctrl+Shift+,<br/>Erste Seite: Ctrl+Shift+Home", 
    "Hide": "Verbergen", 
    "I forgot my password": "Ich habe mein Passwort vergessen", 
    "Ignore Files": "Dateien ignorieren", 
    "Languages": "Sprachen", 
    "Less": "Weniger", 
    "LinkedIn": "LinkedIn", 
    "LinkedIn profile URL": "LinkedIn-Profile-URL", 
    "Load More": "Weitere laden", 
    "Loading...": "Lade...", 
    "Login / Password": "Login / Passwort", 
    "More": "Mehr", 
    "More...": "Mehr...", 
    "My Public Profile": "Mein \u00f6ffentliches Profile", 
    "No": "Nein", 
    "No activity recorded in a given period": "Keine Aktivit\u00e4t in einem bestimmten Zeitraum festgestellt", 
    "No results found": "Keine Ergebnisse verbunden", 
    "No results.": "Keine Ergebnisse.", 
    "Not found": "Nicht gefunden", 
    "Number of Plurals": "Anzahl der Plurals", 
    "Oops...": "Hoppla...", 
    "Overview": "\u00dcberblick", 
    "Password": "Passwort", 
    "Password changed, signing in...": "Passwort ge\u00e4ndert, Anmeldung erfolgt...", 
    "Permissions": "Berechtigungen", 
    "Personal description": "Personenbeschreibung", 
    "Personal website URL": "Pers\u00f6nliche Webseiten-URL", 
    "Please follow that link to continue the account creation.": "Bitte folge dem Link, um die Erzeugung des Kontos fortzusetzen.", 
    "Please follow that link to continue the password reset procedure.": "Bitte folgen Sie dem Link, um die Passwort-Zur\u00fccksetzungsprozedur fortzusetzen.", 
    "Please select a valid user.": "Bitte w\u00e4hle einen g\u00fcltigen Benutzer.", 
    "Plural Equation": "Pluralformel", 
    "Preview will be displayed here.": "Vorschau wird hier angezeigt werden.", 
    "Project / Language": "Projekt / Sprache", 
    "Project Tree Style": "Stil des Projektbaums", 
    "Public Profile": "\u00d6ffentliches Profil", 
    "Quality Checks": "Qualit\u00e4tskontrolle", 
    "Reload page": "Seite neu laden", 
    "Repeat Password": "Passwort wiederholen", 
    "Resend Email": "E-Mail nochmal senden", 
    "Reset Password": "Passwort zur\u00fccksetzen", 
    "Reset Your Password": "Passwort zur\u00fccksetzen", 
    "Reviewed": "Bewertet", 
    "Save": "Speichern", 
    "Saved successfully.": "Erfolgreich gespeichert.", 
    "Score Change": "\u00c4nderung des Scores", 
    "Screenshot Search Prefix": "Screenshot-Pr\u00e4fix-Suche", 
    "Search Languages": "Sprachen durchsuchen", 
    "Search Projects": "Projekte durchsuchen", 
    "Search Users": "Benutzer durchsuchen", 
    "Select...": "Ausw\u00e4hlen...", 
    "Sending email to %s...": "Sende E-Mail an %s...", 
    "Server error": "Serverfehler", 
    "Set New Password": "Neues Passwort setzen", 
    "Set a new password": "Neues Passwort setzen", 
    "Settings": "Einstellungen", 
    "Short Bio": "Kurzbiographie", 
    "Show": "Anzeigen", 
    "Sign In": "Anmelden", 
    "Sign In With %s": "Anmeldung mit %s", 
    "Sign In With...": "Anmelden mit...", 
    "Sign Up": "Registrieren", 
    "Sign in as an existing user": "Melden Sie sich als existierender Benutzer an", 
    "Sign up as a new user": "Melden Sie sich als neuer Benutzer an", 
    "Signed in. Redirecting...": "Angemeldet. Umleitung...", 
    "Signing in with an external service for the first time will automatically create an account for you.": "Wenn Sie sich mit einem externen Service zum ersten Mal anmelden, wird automatisch ein Konto f\u00fcr Sie angelegt.", 
    "Similar translations": "\u00c4hnliche \u00dcbersetzungen", 
    "Social Services": "Social Services", 
    "Source Language": "Quellsprache", 
    "Special Characters": "Sonderzeichen", 
    "String Errors Contact": "Kontakt f\u00fcr Fehler in Zeichenketten", 
    "Team": "Team", 
    "The password reset link was invalid, possibly because it has already been used. Please request a new password reset.": "Der Passwort-Zur\u00fccksetzungs-Link ist ung\u00fcltig, m\u00f6glicherweise, weil er bereits verwendet wurde. Bitte fordere eine neue Passwort-Zur\u00fccksetzung an.", 
    "The server seems down. Try again later.": "Der Server scheint nicht erreichbar zu sein. Versuchen Sie es sp\u00e4ter nochmals.", 
    "There are unsaved changes. Do you want to discard them?": "Es gibt noch nicht gespeicherte \u00c4nderungen. Wollen Sie diese verwerfen?", 
    "There is %(count)s language.": [
      "Es gibt %(count)s Sprache.", 
      "Es gibt %(count)s Sprachen. Unten stehen die k\u00fcrzlich hinzugekommenen."
    ], 
    "There is %(count)s project.": [
      "Es gibt %(count)s Projekt.", 
      "Es gibt %(count)s Projekte. Unten stehen die k\u00fcrzlich hinzu gekommenen."
    ], 
    "There is %(count)s user.": [
      "Es gibt %(count)s Benutzer.", 
      "Es gibt %(count)s Benutzer. Unten stehen die k\u00fcrzlich hinzu gekommenen."
    ], 
    "This email confirmation link expired or is invalid.": "Der E-Mail Best\u00e4tigungs-Link ist entweder abgelaufen oder ung\u00fcltig.", 
    "To set or change your avatar for your email address (%(email)s), please go to gravatar.com.": "Um den Avatar f\u00fcr Ihre E-Mail-Addresse (%(email)s) zu setzen oder zu \u00e4ndern, gehen Sie bitte zu gravatar.com.", 
    "Translated": "\u00dcbersetzt", 
    "Try again": "Noch einmal versuchen", 
    "Twitter": "Twitter", 
    "Twitter username": "Twitter-Benutzername", 
    "Type to search": "Zum Suchen tippen", 
    "Use the search form to find the language, then click on a language to edit.": "Nutze das Formular, um die Sprache zu finden, dann klicke zum Bearbeiten auf eine Sprache.", 
    "Use the search form to find the project, then click on a project to edit.": "Nutze das Formular, um das Projekt zu finden, dann klicke zum Bearbeiten auf ein Projekt.", 
    "Use the search form to find the user, then click on a user to edit.": "Nutze das Formular, um den Benutzer zu finden, dann klicke zum Bearbeiten auf einen Benutzer.", 
    "Username": "Benutzername", 
    "We have sent an email containing the special link to <span>%s</span>. Please check your spam folder if you do not see the email.": "Wir haben eine E-Mail mit dem speziellen Link an <span>%s</span> gesandt. Bitte sehen Sie im Spam Ordner nach falls Sie die E-Mail nicht bekommen haben.", 
    "We have sent an email containing the special link to the address used to register this account. Please check your spam folder if you do not see the email.": "Wir haben eine E-Mail mit dem speziellen Link an die Adresse gesandt, die Sie zur Registrierung des Kontos verwendet haben. Bitte sehen Sie im Spam Ordner nach falls Sie die E-Mail nicht bekommen haben.", 
    "Website": "Webseite", 
    "Why are you part of our translation project? Describe yourself, inspire others!": "Warum Sind Sie Teil dieses \u00dcbersetzungsprojekts? Beschreiben Sie sich selbst, inspirieren Sie andere!", 
    "Yes": "Ja", 
    "Your Full Name": "Ihr vollst\u00e4ndiger Name", 
    "Your LinkedIn profile URL": "Ihre LinkedIn-Profil-URL", 
    "Your Personal website/blog URL": "Ihre pers\u00f6nliche Webseiten-/Blog-URL", 
    "Your Twitter username": "Ihr Twitter-Benutzername", 
    "Your account is inactive because an administrator deactivated it.": "Ihr Konto ist inaktiv, weil es ein Administrator deaktiviert hat.", 
    "Your account needs activation.": "Ihr Konto wartet auf Aktivierung.", 
    "disabled": "deaktiviert", 
    "some anonymous user": "ein anonymer Benutzer", 
    "someone": "jemand"
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

