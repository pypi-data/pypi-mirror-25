

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
      "%(count)s llengua coincideix amb la consulta.", 
      "%(count)s lleng\u00fces coincideixen amb la consulta."
    ], 
    "%(count)s project matches your query.": [
      "%(count)s projecte coincideix amb la consulta.", 
      "%(count)s projectes coincideixen amb la consulta."
    ], 
    "%(count)s user matches your query.": [
      "%(count)s usuari coincideix amb la consulta.", 
      "%(count)s usuaris coincideixen amb la consulta."
    ], 
    "%(timeSince)s via file upload": "%(timeSince)s via pujada de fitxer", 
    "%s word": [
      "%s paraula", 
      "%s paraules"
    ], 
    "%s's accepted suggestions": "Suggeriments acceptats de %s", 
    "%s's overwritten submissions": "Enviaments sobreescrits de %s", 
    "%s's pending suggestions": "Suggeriments pendents de %s", 
    "%s's rejected suggestions": "Suggeriments rebutjats de %s", 
    "%s's submissions": "Enviaments de %s", 
    "Accept": "Accepta", 
    "Account Activation": "Activaci\u00f3 del compte", 
    "Account Inactive": "El compte \u00e9s inactiu", 
    "Active": "Actiu", 
    "Add Language": "Afegeix una llengua", 
    "Add Project": "Afegeix un projecte", 
    "Add User": "Afegeix un usuari", 
    "Administrator": "Administrador", 
    "After changing your password you will sign in automatically.": "Despr\u00e9s de canviar la contrasenya iniciareu sessi\u00f3 autom\u00e0ticament.", 
    "All Languages": "Totes les lleng\u00fces", 
    "All Projects": "Tots els projectes", 
    "An error occurred while attempting to sign in via %s.": "S'ha produ\u00eft un error en intentar iniciar sessi\u00f3 via %s.", 
    "An error occurred while attempting to sign in via your social account.": "S'ha produ\u00eft un error en intentar iniciar sessi\u00f3 via el compte de xarxa social.", 
    "Avatar": "Avatar", 
    "Cancel": "Cancel\u00b7la", 
    "Clear all": "Neteja-ho tot", 
    "Clear value": "Neteja el valor", 
    "Close": "Tanca", 
    "Code": "Codi", 
    "Collapse details": "Redueix els detalls", 
    "Congratulations! You have completed this task!": "Enhorabona! Heu finalitzat aquesta tasca!", 
    "Contact Us": "Contacteu amb nosaltres", 
    "Contributors, 30 Days": "Col\u00b7laboradors, 30 dies", 
    "Creating new user accounts is prohibited.": "S'ha prohibit la creaci\u00f3 de comptes d'usuari.", 
    "Delete": "Suprimeix", 
    "Deleted successfully.": "S'ha suprimit correctament.", 
    "Didn't receive an email? Check if it was accidentally filtered out as spam, or try requesting another copy of the email.": "No heu rebut cap correu? Comproveu que no s'hagi classificat com a correu brossa, o proveu a sol\u00b7licitar una altra c\u00f2pia del correu.", 
    "Disabled": "Inhabilitat", 
    "Discard changes.": "Descarta els canvis.", 
    "Edit Language": "Edita la llengua", 
    "Edit My Public Profile": "Edita el meu perfil p\u00fablic", 
    "Edit Project": "Edita el projecte", 
    "Edit User": "Edita l'usuari", 
    "Edit the suggestion before accepting, if necessary": "Si cal, editeu el suggeriment abans d'acceptar-lo", 
    "Email": "Correu electr\u00f2nic", 
    "Email Address": "Adre\u00e7a electr\u00f2nica", 
    "Email Confirmation": "Confirmaci\u00f3 de l'adre\u00e7a electr\u00f2nica", 
    "Enter your email address, and we will send you a message with the special link to reset your password.": "Introdu\u00efu la vostra adre\u00e7a electr\u00f2nica de correu i us enviarem un missatge amb l'enlla\u00e7 especial que us permetr\u00e0 canviar la contrasenya.", 
    "Error while connecting to the server": "S'ha produ\u00eft un error en connectar amb el servidor", 
    "Expand details": "Augmenta els detalls", 
    "File types": "Tipus de fitxer", 
    "Filesystems": "Sistemes de fitxers", 
    "Find language by name, code": "Cerca una llengua per nom o codi", 
    "Find project by name, code": "Cerca un projecte per nom o codi", 
    "Find user by name, email, properties": "Cerca un usuari per nom, adre\u00e7a electr\u00f2nica o propietats", 
    "Full Name": "Nom complet", 
    "Go back to browsing": "Torna enrere a la navegaci\u00f3", 
    "Go to the next string (Ctrl+.)<br/><br/>Also:<br/>Next page: Ctrl+Shift+.<br/>Last page: Ctrl+Shift+End": "Va a la cadena seg\u00fcent (Ctrl+.)<br/><br/>Tamb\u00e9:<br/>P\u00e0gina seg\u00fcent: Ctrl+Maj+.<br/>\u00daltima p\u00e0gina: Ctrl+Maj+Final", 
    "Go to the previous string (Ctrl+,)<br/><br/>Also:<br/>Previous page: Ctrl+Shift+,<br/>First page: Ctrl+Shift+Home": "Va la cadena anterior (Ctrl+,)<br/><br/>Tamb\u00e9:<br/>P\u00e0gina anterior: Ctrl+Maj+,<br/>Primera p\u00e0gina: Ctrl+Maj+Inici", 
    "Hide": "Amaga", 
    "Hide disabled": "Amaga els inhabilitats", 
    "I forgot my password": "He oblidat la contrasenya", 
    "Ignore Files": "Ignora els fitxers", 
    "Languages": "Lleng\u00fces", 
    "Less": "Menys", 
    "LinkedIn": "LinkedIn", 
    "LinkedIn profile URL": "URL del perfil del LinkedIn", 
    "Load More": "Carrega'n m\u00e9s", 
    "Loading...": "S'est\u00e0 carregant...", 
    "Login / Password": "Usuari i contrasenya", 
    "More": "M\u00e9s", 
    "More...": "M\u00e9s...", 
    "My Public Profile": "Perfil p\u00fablic", 
    "No": "No", 
    "No activity recorded in a given period": "No s'ha enregistrat cap activitat en el per\u00edode determinat", 
    "No results found": "No s'ha trobat cap resultat", 
    "No results.": "No s'ha trobat cap resultat.", 
    "No, thanks": "No, gr\u00e0cies", 
    "Not found": "No s'ha trobat", 
    "Note: when deleting a user their contributions to the site, e.g. comments, suggestions and translations, are attributed to the anonymous user (nobody).": "Nota: si suprimiu un usuari, les seves aportacions al lloc, p. e. comentaris, suggeriments i traduccions, s'atribueixen a l'usuari an\u00f2nim (\u00abnobody\u00bb).", 
    "Number of Plurals": "Nombre de plurals", 
    "Oops...": "Ep...", 
    "Overview": "Vista general", 
    "Password": "Contrasenya", 
    "Password changed, signing in...": "La contrasenya ha canviat, s'est\u00e0 iniciant sessi\u00f3...", 
    "Permissions": "Permisos", 
    "Personal description": "Descripci\u00f3 personal", 
    "Personal website URL": "URL del lloc web personal", 
    "Please follow that link to continue the account creation.": "Visiteu l'enlla\u00e7 per a continuar la creaci\u00f3 del compte.", 
    "Please follow that link to continue the password reset procedure.": "Visiteu aquest enlla\u00e7 per a continuar amb el proc\u00e9s de canvi de contrasenya.", 
    "Please select a valid user.": "Seleccioneu un usuari v\u00e0lid.", 
    "Plural Equation": "F\u00f3rmula dels plurals", 
    "Plural form %(index)s": "Forma plural %(index)s", 
    "Preview will be displayed here.": "La vista preliminar es mostrar\u00e0 aqu\u00ed.", 
    "Project / Language": "Projecte / Llengua", 
    "Project Tree Style": "Estil d'arbre del projecte", 
    "Provide optional comment (will be publicly visible)": "Proporcioneu un comentari opcional (ser\u00e0 visible p\u00fablicament)", 
    "Public Profile": "Perfil p\u00fablic", 
    "Quality Checks": "Comprovacions de qualitat", 
    "Reject": "Rebutja", 
    "Reload page": "Torna a carregar la p\u00e0gina", 
    "Repeat Password": "Repetiu la contrasenya", 
    "Resend Email": "Torna a enviar el correu", 
    "Reset Password": "Reinicia la contrasenya", 
    "Reset Your Password": "Reinicia la contrasenya", 
    "Reviewed": "Revisat", 
    "Save": "Desa", 
    "Saved successfully.": "S'ha desat correctament.", 
    "Score Change": "Canvi de puntuaci\u00f3", 
    "Screenshot Search Prefix": "Prefix de cerca de captures de pantalla", 
    "Search Languages": "Cerca les lleng\u00fces", 
    "Search Projects": "Cerca projectes", 
    "Search Users": "Cerca usuaris", 
    "Select...": "Seleccioneu...", 
    "Send Email": "Envia el correu", 
    "Sending email to %s...": "S'est\u00e0 enviant un correu electr\u00f2nic a %s...", 
    "Server error": "Error del servidor", 
    "Set New Password": "Estableix una contrasenya nova", 
    "Set a new password": "Introdu\u00efu la contrasenya nova", 
    "Settings": "Configuraci\u00f3", 
    "Short Bio": "Biografia resumida", 
    "Show": "Mostra", 
    "Show disabled": "Mostra els inhabilitats", 
    "Sign In": "Inicia la sessi\u00f3", 
    "Sign In With %s": "Inicia sessi\u00f3 amb %s", 
    "Sign In With...": "Inicia sessi\u00f3 amb...", 
    "Sign Up": "Registre", 
    "Sign in as an existing user": "Inici de sessi\u00f3 com a un usuari existent", 
    "Sign up as a new user": "Enregistra'm com a un usuari nou", 
    "Signed in. Redirecting...": "S'ha iniciat la sessi\u00f3. S'est\u00e0 redirigint...", 
    "Signing in with an external service for the first time will automatically create an account for you.": "En iniciar sessi\u00f3 per primera vegada amb un servei extern se us crear\u00e0 un compte autom\u00e0ticament.", 
    "Similar translations": "Traduccions semblants", 
    "Social Services": "Serveis socials", 
    "Social Verification": "Verificaci\u00f3 social", 
    "Source Language": "Llengua d'origen", 
    "Special Characters": "Car\u00e0cters especials", 
    "String Errors Contact": "Contacte per als errors de les cadenes", 
    "Suggested": "Suggerit", 
    "Team": "Equip", 
    "The password reset link was invalid, possibly because it has already been used. Please request a new password reset.": "L'enlla\u00e7 de reinicialitzaci\u00f3 de la contrasenya no \u00e9s v\u00e0lid. Probablement s'ha utilitzat anteriorment. Haur\u00edeu de sol\u00b7licitar una altra reinicialitzaci\u00f3 de la contrasenya.", 
    "The server seems down. Try again later.": "Sembla que el servidor no funciona. Proveu-ho m\u00e9s tard.", 
    "There are unsaved changes. Do you want to discard them?": "Hi ha canvis sense desar. Voleu descartar-los?", 
    "There is %(count)s language.": [
      "Hi ha %(count)s llengua.", 
      "hi ha %(count)s lleng\u00fces. A sota es mostren les afegides recentment."
    ], 
    "There is %(count)s project.": [
      "Hi ha %(count)s projecte.", 
      "Hi ha %(count)s projectes. A sota es mostre els afegits recentment."
    ], 
    "There is %(count)s user.": [
      "Hi ha %(count)s usuari.", 
      "Hi ha %(count)s usuaris. A sota es mostra les afegits recentment."
    ], 
    "This email confirmation link expired or is invalid.": "Aquest enlla\u00e7 de confirmaci\u00f3 d'adre\u00e7a electr\u00f2nica ha caducat o no \u00e9s v\u00e0lid.", 
    "This string no longer exists.": "Aquesta cadena ja no existeix.", 
    "To set or change your avatar for your email address (%(email)s), please go to gravatar.com.": "Per a definir o canviar el vostre avatar per l'adre\u00e7a de correu (%(email)s), aneu a gravatar.com.", 
    "Translated": "Tradu\u00eft", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project": "Tradu\u00eft per %(fullname)s en el projecte \u00ab<span title=\"%(path)s\">%(project)s</span>\u00bb", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project %(time_ago)s": "Tradu\u00eft per %(fullname)s en el projecte \u00ab<span title=\"%(path)s\">%(project)s</span>\u00bb fa %(time_ago)s", 
    "Try again": "Torneu-hi", 
    "Twitter": "Twitter", 
    "Twitter username": "Nom d'usuari del Twitter", 
    "Type to search": "Escriviu per a cercar", 
    "Updating data": "S'estan actualitzant les dades", 
    "Use the search form to find the language, then click on a language to edit.": "Useu el formulari de cerca per a troba la llengua, aleshores feu clic a la llegua per a editar-la.", 
    "Use the search form to find the project, then click on a project to edit.": "Usa el formulari de cerca per a trobar el projectes, aleshores feu clic al projecte per a editar-lo.", 
    "Use the search form to find the user, then click on a user to edit.": "Usue el formulari de cerca per a trobar l'usuari, aleshores feu clic a l'usuari per a editar-lo.", 
    "Username": "Nom d'usuari", 
    "We found a user with <span>%(email)s</span> email in our system. Please provide the password to finish the sign in procedure. This is a one-off procedure, which will establish a link between your Pootle and %(provider)s accounts.": "Hem trobat un usuari al nostre sistema amb l'adre\u00e7a de correu <span>%(email)s</span>. Indiqueu la contrasenya per a finalitzar el proc\u00e8s d'inici de sessi\u00f3. Aquest procediment nom\u00e9s es realitza un cop, i enlla\u00e7ar\u00e0 els vostres comptes de Pootle i %(provider)s.", 
    "We have sent an email containing the special link to <span>%s</span>": "Us hem enviat un correu electr\u00f2nic amb l'enlla\u00e7 especial a <span>%s</span>", 
    "We have sent an email containing the special link to <span>%s</span>. Please check your spam folder if you do not see the email.": "Us hem enviat un correu electr\u00f2nic amb l'enlla\u00e7 especial a <span>%s</span>. Reviseu la carpeta de correu brossa si no veieu el correu.", 
    "We have sent an email containing the special link to the address used to register this account. Please check your spam folder if you do not see the email.": "Us hem enviat un correu electr\u00f2nic amb l'enlla\u00e7 a l'adre\u00e7a usada en enregistrar aquest compte. Reviseu la carpeta de correu brossa si no veieu el correu.", 
    "Website": "Lloc web", 
    "Why are you part of our translation project? Describe yourself, inspire others!": "Per qu\u00e8 sou part del nostre projecte de traducci\u00f3? Descriviu-vos i inspireu a altres usuaris!", 
    "Yes": "S\u00ed", 
    "You have unsaved changes in this string. Navigating away will discard those changes.": "Teniu canvis sense desar en aquesta cadena Si abandoneu la navegaci\u00f3 es descartaran tots els canvis.", 
    "Your Full Name": "Nom complet", 
    "Your LinkedIn profile URL": "L'URL del vostre perfil del LinkedIn", 
    "Your Personal website/blog URL": "L'URL al vostre bloc o lloc web personal", 
    "Your Twitter username": "El vostre nom d'usuari del Twitter", 
    "Your account is inactive because an administrator deactivated it.": "El vostre compte est\u00e0 desactivat perqu\u00e8 un administrador l'ha desactivat.", 
    "Your account needs activation.": "Cal que activeu el compte.", 
    "disabled": "inhabilitat", 
    "some anonymous user": "un usuari an\u00f2nim", 
    "someone": "alg\u00fa"
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

