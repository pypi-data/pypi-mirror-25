

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
      "%(count)s taal voldoet aan uw query.", 
      "%(count)s talen voldoen aan uw query."
    ], 
    "%(count)s project matches your query.": [
      "%(count)s project voldoet aan uw query.", 
      "%(count)s projecten voldoen aan uw query."
    ], 
    "%(count)s user matches your query.": [
      "%(count)s gebruiker voldoet aan uw query.", 
      "%(count)s gebruikers voldoen aan uw query."
    ], 
    "%(timeSince)s via file upload": "%(timeSince)s via bestandsupload", 
    "%s word": [
      "%s woord", 
      "%s woorden"
    ], 
    "%s's accepted suggestions": "Geaccepteerde suggesties van %s", 
    "%s's overwritten submissions": "Overschreven bijdragen van %s", 
    "%s's pending suggestions": "Openstaande suggesties van %s", 
    "%s's rejected suggestions": "Afgewezen suggesties van %s", 
    "%s's submissions": "Bijdragen van %s", 
    "Accept": "Accepteren", 
    "Account Activation": "Accountactivering", 
    "Account Inactive": "Account inactief", 
    "Active": "Actief", 
    "Add Language": "Taal toevoegen", 
    "Add Project": "Project toevoegen", 
    "Add User": "Gebruiker toevoegen", 
    "Administrator": "Beheerder", 
    "After changing your password you will sign in automatically.": "Nadat uw wachtwoord is gewijzigd, wordt u automatisch aangemeld.", 
    "All Languages": "Alle talen", 
    "All Projects": "Alle projecten", 
    "An error occurred while attempting to sign in via %s.": "Er is een fout opgetreden tijdens het aanmelden via %s.", 
    "An error occurred while attempting to sign in via your social account.": "Er is een fout opgetreden tijdens het aanmelden via uw sociale account.", 
    "Avatar": "Avatar", 
    "Cancel": "Annuleren", 
    "Clear all": "Alles wissen", 
    "Clear value": "Waarde wissen", 
    "Close": "Sluiten", 
    "Code": "Code", 
    "Collapse details": "Details samenvouwen", 
    "Congratulations! You have completed this task!": "Gefeliciteerd! U hebt deze taak voltooid!", 
    "Contact Us": "Contact opnemen", 
    "Contributors, 30 Days": "Medewerkers, 30 dagen", 
    "Creating new user accounts is prohibited.": "Aanmaken van nieuwe gebruikersaccounts is niet toegestaan.", 
    "Delete": "Verwijderen", 
    "Deleted successfully.": "Verwijderd.", 
    "Didn't receive an email? Check if it was accidentally filtered out as spam, or try requesting another copy of the email.": "Geen e-mailbericht ontvangen? Controleer of het per ongeluk is uitgefilterd als spam, of probeer een ander exemplaar van het e-mailbericht op te vragen.", 
    "Disabled": "Uitgeschakeld", 
    "Discard changes.": "Wijzigingen verwerpen", 
    "Edit Language": "Taal bewerken", 
    "Edit My Public Profile": "Mijn openbare profiel bewerken", 
    "Edit Project": "Project bewerken", 
    "Edit User": "Gebruiker bewerken", 
    "Edit the suggestion before accepting, if necessary": "Bewerk zo nodig de suggestie voor het accepteren", 
    "Email": "E-mailadres", 
    "Email Address": "E-mailadres", 
    "Email Confirmation": "E-mailbevestiging", 
    "Enter your email address, and we will send you a message with the special link to reset your password.": "Voer uw e-mailadres in, en we sturen u een bericht met de speciale koppeling om uw wachtwoord opnieuw in te stellen.", 
    "Error while connecting to the server": "Fout tijdens verbinden met de server", 
    "Expand details": "Details uitvouwen", 
    "File types": "Bestandstypen", 
    "Filesystems": "Bestandssystemen", 
    "Find language by name, code": "Taal zoeken op naam, code", 
    "Find project by name, code": "Project zoeken op naam, code", 
    "Find user by name, email, properties": "Gebruiker zoeken op naam, e-mailadres, eigenschappen", 
    "Full Name": "Volledige naam", 
    "Go back to browsing": "Terug naar bladeren", 
    "Go to the next string (Ctrl+.)<br/><br/>Also:<br/>Next page: Ctrl+Shift+.<br/>Last page: Ctrl+Shift+End": "Naar de volgende tekenreeks (Ctrl+.)<br/><br/>Ook:<br/>Volgende pagina: Ctrl+Shift+.<br/>Vorige pagina: Ctrl+Shift+End", 
    "Go to the previous string (Ctrl+,)<br/><br/>Also:<br/>Previous page: Ctrl+Shift+,<br/>First page: Ctrl+Shift+Home": "Naar de vorige tekenreeks (Ctrl+,)<br/><br/>Ook:<br/>Vorige pagina: Ctrl+Shift+,<br/>Eerste pagina: Ctrl+Shift+Home", 
    "Hide": "Verbergen", 
    "Hide disabled": "Verbergen uitgeschakeld", 
    "I forgot my password": "Ik ben mijn wachtwoord vergeten", 
    "Ignore Files": "Bestanden negeren", 
    "Languages": "Talen", 
    "Less": "Minder", 
    "LinkedIn": "LinkedIn", 
    "LinkedIn profile URL": "URL van LinkedIn-profiel", 
    "Load More": "Meer laden", 
    "Loading...": "Laden...", 
    "Login / Password": "Aanmelding / Wachtwoord", 
    "More": "Meer", 
    "More...": "Meer...", 
    "My Public Profile": "Mijn openbare profiel", 
    "No": "Nee", 
    "No activity recorded in a given period": "Geen activiteit geregistreerd in een gegeven periode", 
    "No results found": "Geen resultaten gevonden", 
    "No results.": "Geen resultaten.", 
    "No, thanks": "Nee, bedankt", 
    "Not found": "Niet gevonden", 
    "Note: when deleting a user their contributions to the site, e.g. comments, suggestions and translations, are attributed to the anonymous user (nobody).": "Opmerking: bij het verwijderen van gebruikers worden hun bijdragen aan de website, zoals opmerkingen, suggesties en vertalingen, aan de anonieme gebruiker (nobody) toegekend.", 
    "Number of Plurals": "Aantal meervouden", 
    "Oops...": "Oeps...", 
    "Overview": "Overzicht", 
    "Password": "Wachtwoord", 
    "Password changed, signing in...": "Wachtwoord gewijzigd, aanmelden...", 
    "Permissions": "Rechten", 
    "Personal description": "Persoonlijke beschrijving", 
    "Personal website URL": "URL van persoonlijke website", 
    "Please follow that link to continue the account creation.": "Klik op die koppeling om het aanmaken van uw account te vervolgen.", 
    "Please follow that link to continue the password reset procedure.": "Klik op die koppeling om de procedure voor het opnieuw instellen van uw wachtwoord te vervolgen.", 
    "Please select a valid user.": "Selecteer een geldige gebruiker.", 
    "Plural Equation": "Meervoudsvergelijking", 
    "Plural form %(index)s": "Meervoudsvorm %(index)s", 
    "Preview will be displayed here.": "Hier wordt een voorbeeld weergegeven.", 
    "Project / Language": "Project / Taal", 
    "Project Tree Style": "Stijl van projectstructuur", 
    "Provide optional comment (will be publicly visible)": "Voeg eventueel een opmerking toe (wordt publiekelijk zichtbaar)", 
    "Public Profile": "Openbaar profiel", 
    "Quality Checks": "Kwaliteitscontroles", 
    "Reject": "Afwijzen", 
    "Reload page": "Pagina herladen", 
    "Repeat Password": "Herhaal wachtwoord", 
    "Resend Email": "E-mailbericht opnieuw verzenden", 
    "Reset Password": "Wachtwoord opnieuw instellen", 
    "Reset Your Password": "Uw wachtwoord opnieuw instellen", 
    "Reviewed": "Gecontroleerd", 
    "Save": "Opslaan", 
    "Saved successfully.": "Opgeslagen.", 
    "Score Change": "Scorewijziging", 
    "Screenshot Search Prefix": "Zoekprefix voor schermafbeeldingen", 
    "Search Languages": "Talen zoeken", 
    "Search Projects": "Projecten zoeken", 
    "Search Users": "Gebruikers zoeken", 
    "Select...": "Selecteren...", 
    "Send Email": "E-mailbericht verzenden", 
    "Sending email to %s...": "E-mailbericht verzenden naar %s...", 
    "Server error": "Serverfout", 
    "Set New Password": "Nieuw wachtwoord: instellen", 
    "Set a new password": "Nieuw wachtwoord: instellen", 
    "Settings": "Instellingen", 
    "Short Bio": "Korte biografie", 
    "Show": "Tonen", 
    "Show disabled": "Tonen uitgeschakeld", 
    "Sign In": "Aanmelden", 
    "Sign In With %s": "Aanmelden met %s", 
    "Sign In With...": "Aanmelden met...", 
    "Sign Up": "Registreren", 
    "Sign in as an existing user": "Aanmelden als bestaande gebruiker", 
    "Sign up as a new user": "Registreren als nieuwe gebruiker", 
    "Signed in. Redirecting...": "Aangemeld. Omleiden...", 
    "Signing in with an external service for the first time will automatically create an account for you.": "Het voor de eerste keer aanmelden met een externe service zal automatisch een account voor u aanmaken.", 
    "Similar translations": "Soortgelijke vertalingen", 
    "Social Services": "Sociale services", 
    "Social Verification": "Sociale verificatie", 
    "Source Language": "Brontaal", 
    "Special Characters": "Speciale tekens", 
    "String Errors Contact": "Contact bij tekenreeksfouten", 
    "Suggested": "Voorgesteld", 
    "Team": "Team", 
    "The password reset link was invalid, possibly because it has already been used. Please request a new password reset.": "De koppeling voor het opnieuw instellen van uw wachtwoord was ongeldig, mogelijk omdat deze al is gebruikt. Dien opnieuw een aanvraag voor het instellen van een nieuw wachtwoord in.", 
    "The server seems down. Try again later.": "De server lijkt niet beschikbaar. Probeer het later nog eens.", 
    "There are unsaved changes. Do you want to discard them?": "Er zijn niet-opgeslagen wijzigingen. Wilt u deze verwerpen?", 
    "There is %(count)s language.": [
      "Er is %(count)s taal.", 
      "Er zijn %(count)s talen. De meest recent toegevoegde staan hieronder."
    ], 
    "There is %(count)s project.": [
      "Er is %(count)s project.", 
      "Er zijn %(count)s projecten. De meest recent toegevoegde staan hieronder."
    ], 
    "There is %(count)s user.": [
      "Er is %(count)s gebruiker.", 
      "Er zijn %(count)s gebruikers. De meest recent toegevoegde staan hieronder."
    ], 
    "This email confirmation link expired or is invalid.": "Deze koppeling voor e-mailbevestiging is ongeldig.", 
    "This string no longer exists.": "Deze tekenreeks bestaat niet meer.", 
    "To set or change your avatar for your email address (%(email)s), please go to gravatar.com.": "Ga voor het instellen of wijzigen van de avatar voor uw e-mailadres (%(email)s) naar gravatar.com.", 
    "Translated": "Vertaald", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project": "Vertaald door %(fullname)s in project '<span title=\"%(path)s\">%(project)s</span>'", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project %(time_ago)s": "Vertaald door %(fullname)s in project '<span title=\"%(path)s\">%(project)s</span>', %(time_ago)s", 
    "Try again": "Opnieuw proberen", 
    "Twitter": "Twitter", 
    "Twitter username": "Twitter-gebruikersnaam", 
    "Type to search": "Typ om te zoeken", 
    "Updating data": "Gegevens bijwerken", 
    "Use the search form to find the language, then click on a language to edit.": "Gebruik het zoekformulier om de taal te vinden en klik daarna op een taal om deze te bewerken.", 
    "Use the search form to find the project, then click on a project to edit.": "Gebruik het zoekformulier om het project te vinden en klik daarna op een project om dit te bewerken.", 
    "Use the search form to find the user, then click on a user to edit.": "Gebruik het zoekformulier om de gebruiker te vinden en klik daarna op een gebruiker om deze te bewerken.", 
    "Username": "Gebruikersnaam", 
    "We found a user with <span>%(email)s</span> email in our system. Please provide the password to finish the sign in procedure. This is a one-off procedure, which will establish a link between your Pootle and %(provider)s accounts.": "Er is een gebruiker met het e-mailadres <span>%(email)s</span> in ons systeem gevonden. Geef het wachtwoord op om de aanmeldingsprocedure te voltooien. Dit is een eenmalige procedure, die een koppeling tussen uw Pootle- en %(provider)s-accounts tot stand brengt.", 
    "We have sent an email containing the special link to <span>%s</span>": "We hebben een e-mailbericht met de speciale koppeling verzonden naar <span>%s</span>.", 
    "We have sent an email containing the special link to <span>%s</span>. Please check your spam folder if you do not see the email.": "We hebben een e-mailbericht met de speciale koppeling verzonden naar <span>%s</span>. Controleer uw spammap als u het e-mailbericht niet ziet.", 
    "We have sent an email containing the special link to the address used to register this account. Please check your spam folder if you do not see the email.": "We hebben een e-mailbericht met de speciale koppeling verzonden naar het adres dat voor registratie van deze account is gebruikt. Controleer uw spammap als u het e-mailbericht niet ziet.", 
    "Website": "Website", 
    "Why are you part of our translation project? Describe yourself, inspire others!": "Waarom bent u onderdeel van ons vertaalproject? Beschrijf uzelf, inspireer anderen!", 
    "Yes": "Ja", 
    "You have unsaved changes in this string. Navigating away will discard those changes.": "Er zijn niet-opgeslagen wijzigingen in deze tekenreeks. Verder browsen zal deze wijzigingen verwerpen.", 
    "Your Full Name": "Uw volledige naam", 
    "Your LinkedIn profile URL": "URL van uw LinkedIn-profiel", 
    "Your Personal website/blog URL": "URL van uw persoonlijke website/blog", 
    "Your Twitter username": "Uw Twitter-gebruikersnaam", 
    "Your account is inactive because an administrator deactivated it.": "Uw account is inactief, omdat een beheerder deze heeft gedeactiveerd.", 
    "Your account needs activation.": "Uw account heeft activering nodig.", 
    "disabled": "uitgeschakeld", 
    "some anonymous user": "een anonieme server", 
    "someone": "iemand"
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

