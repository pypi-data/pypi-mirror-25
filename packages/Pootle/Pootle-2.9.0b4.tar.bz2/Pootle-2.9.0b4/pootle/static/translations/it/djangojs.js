

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
      "%(count)s lingua corrisponde alla tua richiesta.", 
      "%(count)s lingue corrispondono alla tua richiesta."
    ], 
    "%(count)s project matches your query.": [
      "%(count)s progetto corrisponde alla tua richiesta.", 
      "%(count)s progetti corrispondono alla tua richiesta."
    ], 
    "%(count)s user matches your query.": [
      "%(count)s utente corrisponde alla tua richiesta.", 
      "%(count)s utenti corrispondono alla tua richiesta."
    ], 
    "%(timeSince)s via file upload": "%(timeSince)s per il caricamento del file", 
    "%s word": [
      "%s parola", 
      "%s parole"
    ], 
    "%s's accepted suggestions": "%s suggerimenti accettati", 
    "%s's overwritten submissions": "%s inserimenti sovrascritti", 
    "%s's pending suggestions": "%s suggerimenti indicati", 
    "%s's rejected suggestions": "%s suggerimenti rifiutati", 
    "%s's submissions": "%s inserimenti", 
    "Accept": "Accetta", 
    "Account Activation": "Attivazione dell'account", 
    "Account Inactive": "Account non attivo", 
    "Active": "Attivo", 
    "Add Language": "Aggiungi lingua", 
    "Add Project": "Aggiungi progetto", 
    "Add User": "Aggiungi utenti", 
    "Administrator": "Amministratore", 
    "After changing your password you will sign in automatically.": "Dopo aver cambiato la password sarai loggato automaticamente.", 
    "All Languages": "Tutte le lingue", 
    "All Projects": "Tutti i progetti", 
    "An error occurred while attempting to sign in via %s.": "Si \u00e8 verificato un errore nel tentativo di autenticazione tramite %s.", 
    "An error occurred while attempting to sign in via your social account.": "Si \u00e8 verificato un errore durante l'autenticazione tramite il tuo account su social network.", 
    "Avatar": "Avatar", 
    "Cancel": "Annulla", 
    "Clear all": "Cancella tutto", 
    "Clear value": "Cancella il valore", 
    "Close": "Chiudi", 
    "Code": "Codice", 
    "Collapse details": "Riduci dettagli", 
    "Congratulations! You have completed this task!": "Complimenti! Hai completato questo task!", 
    "Contact Us": "Contattaci", 
    "Contributors, 30 Days": "Collaboratori, 30 giorni", 
    "Creating new user accounts is prohibited.": "Non \u00e8 possibile creare nuovi account utente.", 
    "Delete": "Cancella", 
    "Deleted successfully.": "Cancellato con successo.", 
    "Didn't receive an email? Check if it was accidentally filtered out as spam, or try requesting another copy of the email.": "Non hai ricevuto l'email? Controlla che non sia stata filtrata per errore dall'antispam, oppure chiedine un'altra.", 
    "Disabled": "Disabilitato", 
    "Discard changes.": "Non salvare le modifiche", 
    "Edit Language": "Modifica lingua", 
    "Edit My Public Profile": "Modifica il mio profilo pubblico", 
    "Edit Project": "Modifica progetto", 
    "Edit User": "Modifica utente", 
    "Edit the suggestion before accepting, if necessary": "Puoi modificare il suggerimento prima di accettarlo, se lo ritieni necessario", 
    "Email": "Email", 
    "Email Address": "Indirizzo email", 
    "Email Confirmation": "Conferma dell'email", 
    "Enter your email address, and we will send you a message with the special link to reset your password.": "Inserisci il tuo indirizzo email, ti invieremo un messaggio per resettare la tua password.", 
    "Error while connecting to the server": "Errore durante la connessione al server", 
    "Expand details": "Espandi dettagli", 
    "File types": "Tipo file", 
    "Filesystems": "Filesystem", 
    "Find language by name, code": "Trova lingue per Nome, Codice linguistico", 
    "Find project by name, code": "Trova progetta per Nome, Codice progetto", 
    "Find user by name, email, properties": "Trova utente per Nome, Email, Propriet\u00e0", 
    "Full Name": "Nome completo", 
    "Go back to browsing": "Torna alla navigazione", 
    "Go to the next string (Ctrl+.)<br/><br/>Also:<br/>Next page: Ctrl+Shift+.<br/>Last page: Ctrl+Shift+End": "Vai alla prossima stringa (Ctrl+.)<br/><br/>Inoltre:<br/>Pagina seguente: Ctrl+Maiusc+.<br/>Ultima pagina: Ctrl+Maiusc+Fine", 
    "Go to the previous string (Ctrl+,)<br/><br/>Also:<br/>Previous page: Ctrl+Shift+,<br/>First page: Ctrl+Shift+Home": "Vai alla stringa precedente (Ctrl+,)<br/><br/>Inoltre:<br/>Pagina precedente: Ctrl+Maiusc+,<br/>Prima pagina: Ctrl+Maiusc+Inizio", 
    "Hide": "Nascondi", 
    "Hide disabled": "Nascondi disabilitati", 
    "I forgot my password": "Ho scordato la mia password", 
    "Ignore Files": "Ignora file", 
    "Languages": "Lingue", 
    "Less": "Di meno", 
    "LinkedIn": "LinkedIn", 
    "LinkedIn profile URL": "URL su LinkedIn", 
    "Load More": "Carica altri", 
    "Loading...": "Caricamento in corso...", 
    "Login / Password": "Login / Password", 
    "More": "Ancora", 
    "More...": "Altre...", 
    "My Public Profile": "Profilo pubblico", 
    "No": "No", 
    "No activity recorded in a given period": "Nessuna attivit\u00e0 memorizzata nel periodo specificato", 
    "No results found": "Nessun risultato restituito", 
    "No results.": "Nessun risultato.", 
    "No, thanks": "No, grazie", 
    "Not found": "Non trovato", 
    "Note: when deleting a user their contributions to the site, e.g. comments, suggestions and translations, are attributed to the anonymous user (nobody).": "Nota: quando si elimina un utente il suoi contributi al sito, ad esempio i commenti, i suggerimenti e le traduzioni, vengono attribuiti all'utente anonimo (nobody).", 
    "Number of Plurals": "Numero di Plurali", 
    "Oops...": "Oops...", 
    "Overview": "Sommario", 
    "Password": "Password", 
    "Password changed, signing in...": "Password modificata: autenticazione in corso...", 
    "Permissions": "Autorizzazioni", 
    "Personal description": "Descrizione", 
    "Personal website URL": "URL del sito personale", 
    "Please follow that link to continue the account creation.": "Puoi fare click su questo collegamento per completare la creazione dell'account.", 
    "Please follow that link to continue the password reset procedure.": "Puoi fare click su questo collegamento per continuare la procedura di reset della password.", 
    "Please select a valid user.": "Seleziona un utente valido.", 
    "Plural Equation": "Equazione plurale", 
    "Plural form %(index)s": "Forma plurale %(index)s", 
    "Preview will be displayed here.": "L'anteprima verr\u00e0 mostrata qui.", 
    "Project / Language": "Progetto / Lingue", 
    "Project Tree Style": "Progetto con Struttura ad albero", 
    "Provide optional comment (will be publicly visible)": "Fornisci un commento opzionale (sar\u00e0 visibile pubblicamente)", 
    "Public Profile": "Profilo pubblico", 
    "Quality Checks": "Controlli di qualit\u00e0", 
    "Reject": "Rifiuta", 
    "Reload page": "Ricarica pagina", 
    "Repeat Password": "Ripeti la password", 
    "Resend Email": "Reinvia l'email", 
    "Reset Password": "Reimposta la password", 
    "Reset Your Password": "Reimposta password", 
    "Reviewed": "Revisionate", 
    "Save": "Salva", 
    "Saved successfully.": "Salvato con successo.", 
    "Score Change": "Variazione di Punteggio", 
    "Screenshot Search Prefix": "Prefisso di Ricerca della Schermata", 
    "Search Languages": "Cerca lingue", 
    "Search Projects": "Cerca progetti", 
    "Search Users": "Ricerca utenti", 
    "Select...": "Seleziona...", 
    "Send Email": "Invia email", 
    "Sending email to %s...": "Invio dell'email a %s...", 
    "Server error": "Errore del server", 
    "Set New Password": "Imposta nuova password", 
    "Set a new password": "Inserire una nuova password", 
    "Settings": "Impostazioni", 
    "Short Bio": "Breve biografia", 
    "Show": "Mostra", 
    "Show disabled": "Mostra disabilitati", 
    "Sign In": "Autenticati", 
    "Sign In With %s": "Accedi con %s", 
    "Sign In With...": "Accedi con...", 
    "Sign Up": "Registrati", 
    "Sign in as an existing user": "Autenticati come utente gi\u00e0 esistente", 
    "Sign up as a new user": "Registrati come nuovo utente", 
    "Signed in. Redirecting...": "Autenticazione corretta. Redirezione in corso...", 
    "Signing in with an external service for the first time will automatically create an account for you.": "Entrando per la prima volta con un servizio esterno verr\u00e0 creato automaticamente un account per te.", 
    "Similar translations": "Traduzioni simili", 
    "Social Services": "Servizi Social", 
    "Social Verification": "Verifica Social", 
    "Source Language": "Lingua originale", 
    "Special Characters": "Caratteri speciali", 
    "String Errors Contact": "Contatti per Errori sulle Stringhe", 
    "Suggested": "Proposto", 
    "Team": "Team", 
    "The password reset link was invalid, possibly because it has already been used. Please request a new password reset.": "Il link per il reset della password non \u00e8 valido, probabilmente perch\u00e8 \u00e8 gi\u00e0 stato usato. Puoi richiedere un nuovo reset.", 
    "The server seems down. Try again later.": "Il server sembra non rispondere. Riprova pi\u00f9 tardi.", 
    "There are unsaved changes. Do you want to discard them?": "Ci sono dei cambiamenti non salvati. Vuoi uscire SENZA salvarli?", 
    "There is %(count)s language.": [
      "C'\u00e8 %(count)s lingua.", 
      "Ci sono %(count)s lingue. Qui sotto ci sono quelle aggiunte pi\u00f9 di recente."
    ], 
    "There is %(count)s project.": [
      "C'\u00e8 %(count)s progetto.", 
      "Ci sono %(count)s Progetti. Qui sotto ci sono quelli aggiunti pi\u00f9 di recente."
    ], 
    "There is %(count)s user.": [
      "C'\u00e8 %(count)s utente.", 
      "Ci sono %(count)s utenti. Qui sotto ci sono quelli aggiunti pi\u00f9 di recente."
    ], 
    "This email confirmation link expired or is invalid.": "Questo link per la conferma \u00e8 errato oppure troppo vecchio.", 
    "This string no longer exists.": "Questa stringa non esiste pi\u00f9.", 
    "To set or change your avatar for your email address (%(email)s), please go to gravatar.com.": "Per impostare o modificare l'immagine associata al tuo indirizzo email (%(email)s), vai su gravatar.com.", 
    "Translated": "Tradotto", 
    "Try again": "Riprova", 
    "Twitter": "Twitter", 
    "Twitter username": "Nome su Twitter", 
    "Type to search": "Scrivi per fare una ricerca", 
    "Updating data": "Aggiornamento dei dati", 
    "Use the search form to find the language, then click on a language to edit.": "Utilizza il modulo di ricerca per trovare la lingua, quindi clicca su una lingua per modificarla.", 
    "Use the search form to find the project, then click on a project to edit.": "Utilizza il modulo di ricerca per trovare il progetto, quindi clicca su un progetto per modificarlo.", 
    "Use the search form to find the user, then click on a user to edit.": "Usa il form di ricerca per trovare l'utente, quindi clicca sul nome dell'utente per editarlo.", 
    "Username": "Nome utente", 
    "We found a user with <span>%(email)s</span> email in our system. Please provide the password to finish the sign in procedure. This is a one-off procedure, which will establish a link between your Pootle and %(provider)s accounts.": "Abbiamo trovato un utente con l'email <span>%(email)s</span> nel nostro sistema. Ora \u00e8 necessario inserire la password per completare il processo di registrazione. Questa \u00e8 una procedura una tantum, che stabilir\u00e0 un collegamento tra i tuoi account di Pootle e quelli del tuo %(provider)s.", 
    "We have sent an email containing the special link to <span>%s</span>": "Abbiamo inviato un'email contenente il link speciale a <span>%s</span>", 
    "We have sent an email containing the special link to <span>%s</span>. Please check your spam folder if you do not see the email.": "Abbiamo inviato un'email contenente il link a <span>%s</span>. Se non la trovi nella Posta in ingresso prova a cercarla nella cartella dello Spam.", 
    "We have sent an email containing the special link to the address used to register this account. Please check your spam folder if you do not see the email.": "Abbiamo inviato un'email contenente il link speciale all'indirizzo utilizzato per registrare questo account. Se non la trovi nella Posta in ingresso prova a cercarla nella cartella dello Spam.", 
    "Website": "Sito web", 
    "Why are you part of our translation project? Describe yourself, inspire others!": "Perch\u00e9 fai parte del nostro progetto di traduzione? Descriviti, ispira gli altri!", 
    "Yes": "S\u00ec", 
    "You have unsaved changes in this string. Navigating away will discard those changes.": "Ci sono modifiche non salvate in questa stringa. Uscendo da questa pagina perderai questi cambiamenti.", 
    "Your Full Name": "Nome e cognome", 
    "Your LinkedIn profile URL": "L'URL del tuo profilo su LinkedIn", 
    "Your Personal website/blog URL": "L'URL del tuo sito/blog personale", 
    "Your Twitter username": "Il tuo nome su Twitter", 
    "Your account is inactive because an administrator deactivated it.": "Il tuo account non \u00e8 pi\u00f9 attivo, \u00e8 stato disattivato da un amministratore.", 
    "Your account needs activation.": "Il tuo account deve essere attivato.", 
    "disabled": "disabilitato", 
    "some anonymous user": "qualche utente anonimo", 
    "someone": "qualcuno"
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

