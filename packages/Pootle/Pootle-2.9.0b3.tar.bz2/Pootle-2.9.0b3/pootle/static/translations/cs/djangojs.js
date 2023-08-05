

(function(globals) {

  var django = globals.django || (globals.django = {});

  
  django.pluralidx = function(n) {
    var v=(n==1) ? 0 : (n>=2 && n<=4) ? 1 : 2;
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
      "Dotazu odpov\u00edd\u00e1 %(count)s jazyk.", 
      "Dotazu odpov\u00eddaj\u00ed %(count)s jazyky.", 
      "Dotazu odpov\u00edd\u00e1 %(count)s jazyk\u016f."
    ], 
    "%(count)s project matches your query.": [
      "Dotazu odpov\u00edd\u00e1 %(count)s projekt.", 
      "Dotazu odpov\u00eddaj\u00ed %(count)s projekty.", 
      "Dotazu odpov\u00edd\u00e1 %(count)s projekt\u016f."
    ], 
    "%(count)s user matches your query.": [
      "Dotazu odpov\u00edd\u00e1 %(count)s u\u017eivatel.", 
      "Dotazu odpov\u00eddaj\u00ed %(count)s u\u017eivatel\u00e9.", 
      "Dotazu odpov\u00edd\u00e1 %(count)s u\u017eivatel\u016f."
    ], 
    "%(timeSince)s via file upload": "%(timeSince)s nahr\u00e1n\u00edm souboru", 
    "%s word": [
      "%s slovo", 
      "%s slova", 
      "%s slov"
    ], 
    "%s's accepted suggestions": "P\u0159ijat\u00e9 n\u00e1vrhy u\u017eivatele %s", 
    "%s's overwritten submissions": "P\u0159epsan\u00e9 p\u0159eklady u\u017eivatele %s", 
    "%s's pending suggestions": "Nevy\u0159\u00edzen\u00e9 n\u00e1vrhy u\u017eivatele %s", 
    "%s's rejected suggestions": "Odm\u00edtnut\u00e9 n\u00e1vrhy u\u017eivatele %s", 
    "%s's submissions": "P\u0159eklady u\u017eivatele %s", 
    "Accept": "P\u0159ijmout", 
    "Account Activation": "Aktivace \u00fa\u010dtu", 
    "Account Inactive": "\u00da\u010det neaktivn\u00ed", 
    "Active": "Aktivn\u00ed", 
    "Add Language": "P\u0159idat jazyk", 
    "Add Project": "P\u0159idat projekt", 
    "Add User": "P\u0159idat u\u017eivatele", 
    "Administrator": "Spr\u00e1vce", 
    "After changing your password you will sign in automatically.": "Po zm\u011bn\u011b hesla budete automaticky p\u0159ihl\u00e1\u0161eni.", 
    "All Languages": "V\u0161echny jazyky", 
    "All Projects": "V\u0161echny projekty", 
    "An error occurred while attempting to sign in via %s.": "P\u0159i pokusu o p\u0159ihl\u00e1\u0161en\u00ed prost\u0159ednictv\u00edm %s do\u0161lo k chyb\u011b.", 
    "An error occurred while attempting to sign in via your social account.": "P\u0159i pokusu o p\u0159ihl\u00e1\u0161en\u00ed prost\u0159ednictv\u00edm va\u0161eho soci\u00e1ln\u00edho \u00fa\u010dtu do\u0161lo k chyb\u011b.", 
    "Avatar": "Avatar", 
    "Cancel": "Zru\u0161it", 
    "Clear all": "Smazat v\u0161e", 
    "Clear value": "Smazat hodnotu", 
    "Close": "Zav\u0159\u00edt", 
    "Code": "K\u00f3d", 
    "Collapse details": "Sbalit podrobnosti", 
    "Congratulations! You have completed this task!": "Gratulujeme! Dokon\u010dili jste tuto \u00falohu!", 
    "Contact Us": "Kontaktujte n\u00e1s", 
    "Contributors, 30 Days": "P\u0159isp\u011bvatel\u00e9, 30 dn\u00ed", 
    "Creating new user accounts is prohibited.": "Vytv\u00e1\u0159en\u00ed nov\u00fdch u\u017eivatelsk\u00fdch \u00fa\u010dt\u016f je zak\u00e1z\u00e1no.", 
    "Delete": "Odstranit", 
    "Deleted successfully.": "\u00dasp\u011b\u0161n\u011b odstran\u011bno.", 
    "Didn't receive an email? Check if it was accidentally filtered out as spam, or try requesting another copy of the email.": "Neobdr\u017eeli jste \u017e\u00e1dn\u00fd e-mail? Zkontrolujte, zda nebyl omylem ozna\u010den jako spam, nebo zkuste po\u017e\u00e1dat o op\u011btovn\u00e9 zasl\u00e1n\u00ed e-mailu.", 
    "Disabled": "Zak\u00e1z\u00e1no", 
    "Discard changes.": "Zahodit zm\u011bny.", 
    "Edit Language": "Upravit jazyk", 
    "Edit My Public Profile": "Upravit m\u016fj ve\u0159ejn\u00fd profil", 
    "Edit Project": "Upravit projekt", 
    "Edit User": "Upravit u\u017eivatele", 
    "Edit the suggestion before accepting, if necessary": "Pokud je to t\u0159eba, n\u00e1vrh p\u0159ed jeho p\u0159ijet\u00edm upravte", 
    "Email": "E-mail", 
    "Email Address": "E-mailov\u00e1 adresa", 
    "Email Confirmation": "Potvrzovac\u00ed e-mail", 
    "Enter your email address, and we will send you a message with the special link to reset your password.": "Zadejte svou e-mailovou adresu a my v\u00e1m za\u0161leme speci\u00e1ln\u00ed odkaz pro resetov\u00e1n\u00ed hesla.", 
    "Error while connecting to the server": "P\u0159i p\u0159ipojov\u00e1n\u00ed k serveru do\u0161lo k chyb\u011b", 
    "Expand details": "Rozbalit podrobnosti", 
    "File types": "Typy soubor\u016f", 
    "Filesystems": "Syst\u00e9my soubor\u016f", 
    "Find language by name, code": "Naj\u00edt jazyk podle n\u00e1zvu nebo k\u00f3du", 
    "Find project by name, code": "Naj\u00edt projekt podle n\u00e1zvu nebo k\u00f3du", 
    "Find user by name, email, properties": "Naj\u00edt u\u017eivatele podle jm\u00e9na, emailu nebo vlastnost\u00ed", 
    "Full Name": "Cel\u00fd n\u00e1zev", 
    "Go back to browsing": "Zp\u011bt na proch\u00e1zen\u00ed", 
    "Go to the next string (Ctrl+.)<br/><br/>Also:<br/>Next page: Ctrl+Shift+.<br/>Last page: Ctrl+Shift+End": "P\u0159ej\u00edt na dal\u0161\u00ed \u0159et\u011bzec (Ctrl+.)<br/><br/>Tak\u00e9:<br/>Dal\u0161\u00ed str\u00e1nka: Ctrl+Shift+.<br/>Posledn\u00ed str\u00e1nka: Ctrl+Shift+End", 
    "Go to the previous string (Ctrl+,)<br/><br/>Also:<br/>Previous page: Ctrl+Shift+,<br/>First page: Ctrl+Shift+Home": "P\u0159ej\u00edt na p\u0159edchoz\u00ed \u0159et\u011bzec (Ctrl+,)<br/><br/>Tak\u00e9:<br/>P\u0159edchoz\u00ed str\u00e1nka: Ctrl+Shift+,<br/>Prvn\u00ed str\u00e1nka: Ctrl+Shift+Home", 
    "Hide": "Skr\u00fdt", 
    "Hide disabled": "Skr\u00fdt vypnut\u00e9", 
    "I forgot my password": "Zapomn\u011bl jsem heslo", 
    "Ignore Files": "Ignorovat soubory", 
    "Languages": "Jazyky", 
    "Less": "M\u00e9n\u011b", 
    "LinkedIn": "LinkedIn", 
    "LinkedIn profile URL": "Adresa profilu LinkedIn", 
    "Load More": "Na\u010d\u00edst dal\u0161\u00ed", 
    "Loading...": "Na\u010d\u00edt\u00e1n\u00ed...", 
    "Login / Password": "U\u017eivatelsk\u00e9 jm\u00e9no / Heslo", 
    "More": "V\u00edce", 
    "More...": "Podrobnosti...", 
    "My Public Profile": "M\u016fj ve\u0159ejn\u00fd profil", 
    "No": "Ne", 
    "No activity recorded in a given period": "Ve vybran\u00e9m obdob\u00ed nebyla zaznamen\u00e1na \u017e\u00e1dn\u00e1 aktivita", 
    "No results found": "Nebyly nalezeny \u017e\u00e1dn\u00e9 v\u00fdsledky", 
    "No results.": "\u017d\u00e1dn\u00e9 v\u00fdsledky.", 
    "No, thanks": "Ne, d\u011bkuji", 
    "Not found": "Nenalezeno", 
    "Note: when deleting a user their contributions to the site, e.g. comments, suggestions and translations, are attributed to the anonymous user (nobody).": "Pozn\u00e1mka: po smaz\u00e1n\u00ed u\u017eivatele budou jeho p\u0159\u00edsp\u011bvky, tedy pozn\u00e1mky, n\u00e1vrhy a p\u0159eklady p\u0159i\u0159azeny anonymn\u00edmu u\u017eivateli (nobody).", 
    "Number of Plurals": "Po\u010det forem plur\u00e1lu", 
    "Oops...": "Jejda...", 
    "Overview": "P\u0159ehled", 
    "Password": "Heslo", 
    "Password changed, signing in...": "Heslo bylo zm\u011bn\u011bno, pros\u00edm p\u0159ihlaste se...", 
    "Permissions": "Opr\u00e1vn\u011bn\u00ed", 
    "Personal description": "Osobn\u00ed popis", 
    "Personal website URL": "Adresa osobn\u00ed webov\u00e9 str\u00e1nky", 
    "Please follow that link to continue the account creation.": "Pro pokra\u010dov\u00e1n\u00ed v procesu zalo\u017een\u00ed \u00fa\u010dtu klikn\u011bte na zadan\u00fd odkaz.", 
    "Please follow that link to continue the password reset procedure.": "Pro pokra\u010dov\u00e1n\u00ed v procesu resetov\u00e1n\u00ed hesla klikn\u011bte na dan\u00fd odkaz.", 
    "Please select a valid user.": "Vyberte existuj\u00edc\u00edho u\u017eivatele.", 
    "Plural Equation": "Podm\u00ednky pou\u017eit\u00ed forem plur\u00e1lu", 
    "Plural form %(index)s": "Forma plur\u00e1lu %(index)s", 
    "Preview will be displayed here.": "Zde bude zobrazen n\u00e1hled.", 
    "Project / Language": "Projekt / Jazyk", 
    "Project Tree Style": "Adres\u00e1\u0159ov\u00e1 struktura projektu", 
    "Provide optional comment (will be publicly visible)": "Zadejte nepovinn\u00fd koment\u00e1\u0159 (bude ve\u0159ejn\u011b viditeln\u00fd)", 
    "Public Profile": "Ve\u0159ejn\u00fd profil", 
    "Quality Checks": "Kontroly kvality", 
    "Reject": "Zam\u00edtnout", 
    "Reload page": "Znovu na\u010d\u00edst str\u00e1nku", 
    "Repeat Password": "Zopakujte heslo", 
    "Resend Email": "Znovu odeslat e-mail", 
    "Reset Password": "Resetovat heslo", 
    "Reset Your Password": "Resetovat heslo", 
    "Reviewed": "Zkontrolov\u00e1no", 
    "Save": "Ulo\u017eit", 
    "Saved successfully.": "\u00dasp\u011b\u0161n\u011b ulo\u017eeno.", 
    "Score Change": "Zm\u011bna hodnoty", 
    "Screenshot Search Prefix": "P\u0159edpona pro hled\u00e1n\u00ed sn\u00edmk\u016f obrazovky", 
    "Search Languages": "Vyhledat jazyky", 
    "Search Projects": "Vyhledat projekty", 
    "Search Users": "Vyhledat u\u017eivatele", 
    "Select...": "Vybrat...", 
    "Send Email": "Odeslat e-mail", 
    "Sending email to %s...": "Odes\u00edl\u00e1n\u00ed e-mailu na adresu %s...", 
    "Server error": "Chyba na stran\u011b serveru", 
    "Set New Password": "Nastavit nov\u00e9 heslo", 
    "Set a new password": "Nastavit nov\u00e9 heslo", 
    "Settings": "Nastaven\u00ed", 
    "Short Bio": "Stru\u010dn\u00fd \u017eivotopis", 
    "Show": "Zobrazit", 
    "Show disabled": "Zobrazit vypnut\u00e9", 
    "Sign In": "P\u0159ihl\u00e1sit se", 
    "Sign In With %s": "P\u0159ihl\u00e1sit se prost\u0159ednictv\u00edm %s", 
    "Sign In With...": "P\u0159ihlaste se prost\u0159ednictv\u00edm...", 
    "Sign Up": "Zaregistrovat se", 
    "Sign in as an existing user": "P\u0159ihl\u00e1sit se jako existuj\u00edc\u00ed u\u017eivatel", 
    "Sign up as a new user": "Zaregistrovat se jako nov\u00fd u\u017eivatel", 
    "Signed in. Redirecting...": "Jste p\u0159ihl\u00e1\u0161eni. Prob\u00edh\u00e1 p\u0159esm\u011brov\u00e1n\u00ed...", 
    "Signing in with an external service for the first time will automatically create an account for you.": "Prvn\u00ed p\u0159ihl\u00e1\u0161en\u00ed prost\u0159ednictv\u00edm extern\u00ed slu\u017eby automaticky vytvo\u0159\u00ed u\u017eivatelsk\u00fd \u00fa\u010det.", 
    "Similar translations": "Obdobn\u00e9 p\u0159eklady", 
    "Social Services": "Soci\u00e1ln\u00ed slu\u017eby", 
    "Social Verification": "Soci\u00e1ln\u00ed ov\u011b\u0159en\u00ed", 
    "Source Language": "Zdrojov\u00fd jazyk", 
    "Special Characters": "Speci\u00e1ln\u00ed znaky", 
    "String Errors Contact": "Kontakt pro nahl\u00e1\u0161en\u00ed chyb v \u0159et\u011bzc\u00edch", 
    "Suggested": "Navrhnul", 
    "Team": "T\u00fdm", 
    "The password reset link was invalid, possibly because it has already been used. Please request a new password reset.": "Odkaz na resetov\u00e1n\u00ed hesla byl neplatn\u00fd, patrn\u011b kv\u016fli tomu, \u017ee u\u017e byl jednou pou\u017eit. Po\u017e\u00e1dejte pros\u00edm o resetov\u00e1n\u00ed hesla znovu.", 
    "The server seems down. Try again later.": "Zd\u00e1 se, \u017ee server nen\u00ed funk\u010dn\u00ed. Zkuste se p\u0159ipojit pozd\u011bji.", 
    "There are unsaved changes. Do you want to discard them?": "Zm\u011bny nebyly ulo\u017eeny. Chcete je zahodit?", 
    "There is %(count)s language.": [
      "Existuje %(count)s jazyk.", 
      "Existuj\u00ed %(count)s jazyky. N\u00ed\u017ee jsou uvedeny ty ned\u00e1vno p\u0159idan\u00e9.", 
      "Existuje %(count)s jazyk\u016f. N\u00ed\u017ee jsou uvedeny ty ned\u00e1vno p\u0159idan\u00e9."
    ], 
    "There is %(count)s project.": [
      "Existuje %(count)s projekt.", 
      "Existuj\u00ed %(count)s projekty. N\u00ed\u017ee jsou uvedeny ty ned\u00e1vno p\u0159idan\u00e9.", 
      "Existuje %(count)s projekt\u016f. N\u00ed\u017ee jsou uvedeny ty ned\u00e1vno p\u0159idan\u00e9."
    ], 
    "There is %(count)s user.": [
      "Existuje %(count)s u\u017eivatel.", 
      "Existuj\u00ed %(count)s u\u017eivatel\u00e9. N\u00ed\u017ee jsou uvedeni ti ned\u00e1vno p\u0159idan\u00ed.", 
      "Existuje %(count)s u\u017eivatel\u016f. N\u00ed\u017ee jsou uvedeni ti ned\u00e1vno p\u0159idan\u00ed."
    ], 
    "This email confirmation link expired or is invalid.": "Platnost potvrzovac\u00edho odkazu vypr\u0161ela, nebo je odkaz neplatn\u00fd.", 
    "This string no longer exists.": "Tento \u0159et\u011bzec ji\u017e neexistuje.", 
    "To set or change your avatar for your email address (%(email)s), please go to gravatar.com.": "Pro nastaven\u00ed avataru pro va\u0161i e-mailovou adresu (%(email)s) pros\u00edm p\u0159ejd\u011bte na str\u00e1nky gravatar.com.", 
    "Translated": "P\u0159elo\u017eeno", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project": "P\u0159elo\u017eil %(fullname)s v projektu \u201e<span title=\"%(path)s\">%(project)s</span>\u201c", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project %(time_ago)s": "P\u0159elo\u017eil %(fullname)s v projektu \u201e<span title=\"%(path)s\">%(project)s</span>\u201c %(time_ago)s", 
    "Try again": "Zkusit znovu", 
    "Twitter": "Twitter", 
    "Twitter username": "U\u017eivatelsk\u00e9 jm\u00e9no pro Twitter", 
    "Type to search": "Zadejte text pro vyhled\u00e1v\u00e1n\u00ed", 
    "Updating data": "Prob\u00edh\u00e1 aktualizace dat", 
    "Use the search form to find the language, then click on a language to edit.": "Pou\u017eijte formul\u00e1\u0159 pro vyhled\u00e1n\u00ed jazyku a pot\u00e9 klikn\u011bte na jeho n\u00e1zev pro proveden\u00ed \u00faprav.", 
    "Use the search form to find the project, then click on a project to edit.": "Pou\u017eijte formul\u00e1\u0159 pro vyhled\u00e1n\u00ed projektu a pot\u00e9 klikn\u011bte na jeho n\u00e1zev pro proveden\u00ed \u00faprav.", 
    "Use the search form to find the user, then click on a user to edit.": "Pou\u017eijte formul\u00e1\u0159 pro vyhled\u00e1n\u00ed u\u017eivatele a pot\u00e9 klikn\u011bte na jeho jm\u00e9no pro proveden\u00ed \u00faprav.", 
    "Username": "U\u017eivatelsk\u00e9 jm\u00e9no", 
    "We found a user with <span>%(email)s</span> email in our system. Please provide the password to finish the sign in procedure. This is a one-off procedure, which will establish a link between your Pootle and %(provider)s accounts.": "Nalezli jsme v na\u0161em syst\u00e9mu u\u017eivatele s e-mailem <span>%(email)s</span>. Pro dokon\u010den\u00ed procesu p\u0159ihl\u00e1\u0161en\u00ed zadejte jeho heslo. Toto je jednor\u00e1zov\u00fd po\u017eadavek, kter\u00fd vytvo\u0159\u00ed propojen\u00ed mezi va\u0161\u00edm \u00fa\u010dtem na Pootle serveru a %(provider)s \u00fa\u010dtem.", 
    "We have sent an email containing the special link to <span>%s</span>": "Odeslali jsme e-mail obsahuj\u00edc\u00ed tento speci\u00e1ln\u00ed odkaz na adresu <span>%s</span>", 
    "We have sent an email containing the special link to <span>%s</span>. Please check your spam folder if you do not see the email.": "Odeslali jsme e-mail obsahuj\u00edc\u00ed tento speci\u00e1ln\u00ed odkaz na adresu <span>%s</span>. Pokud tento e-mail nevid\u00edte, zkontrolujte slo\u017eku s nevy\u017e\u00e1danou po\u0161tou.", 
    "We have sent an email containing the special link to the address used to register this account. Please check your spam folder if you do not see the email.": "Odeslali jsme e-mail obsahuj\u00edc\u00ed tento speci\u00e1ln\u00ed odkaz na adresu pou\u017eitou p\u0159i registraci va\u0161eho \u00fa\u010dtu. Pokud tento e-mail nevid\u00edte, zkontrolujte slo\u017eku s nevy\u017e\u00e1danou po\u0161tou.", 
    "Website": "Webov\u00e1 str\u00e1nka", 
    "Why are you part of our translation project? Describe yourself, inspire others!": "Pro\u010d jste se stali \u00fa\u010dastn\u00edky na\u0161eho p\u0159ekladov\u00e9ho projektu? \u0158ekn\u011bte n\u00e1m n\u011bco o sob\u011b a inspirujte ostatn\u00ed u\u017eivatele!", 
    "Yes": "Ano", 
    "You have unsaved changes in this string. Navigating away will discard those changes.": "Pro tento \u0159et\u011bzec existuj\u00ed neulo\u017een\u00e9 zm\u011bny. P\u0159i p\u0159echodu na jin\u00fd \u0159et\u011bzec budou tyto zm\u011bny zahozeny.", 
    "Your Full Name": "Va\u0161e cel\u00e9 jm\u00e9no", 
    "Your LinkedIn profile URL": "Adresa va\u0161eho profilu LinkedIn", 
    "Your Personal website/blog URL": "Adresa va\u0161\u00ed osobn\u00ed webov\u00e9 str\u00e1nky nebo blogu", 
    "Your Twitter username": "Va\u0161e u\u017eivatelsk\u00e9 jm\u00e9no pro Twitter", 
    "Your account is inactive because an administrator deactivated it.": "V\u00e1\u0161 \u00fa\u010det je neaktivn\u00ed, proto\u017ee byl deaktivov\u00e1n administr\u00e1torem.", 
    "Your account needs activation.": "V\u00e1\u0161 \u00fa\u010det vy\u017eaduje aktivaci.", 
    "disabled": "zak\u00e1z\u00e1no", 
    "some anonymous user": "anonymn\u00ed u\u017eivatel", 
    "someone": "u\u017eivatel"
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

