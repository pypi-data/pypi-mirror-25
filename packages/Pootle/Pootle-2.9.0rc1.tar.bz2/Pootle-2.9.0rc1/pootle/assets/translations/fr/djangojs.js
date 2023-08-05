

(function(globals) {

  var django = globals.django || (globals.django = {});

  
  django.pluralidx = function(n) {
    var v=(n > 1);
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
      "%(count)s langue correspond \u00e0 votre requ\u00eate.", 
      "%(count)s langues correspondent \u00e0 votre requ\u00eate."
    ], 
    "%(count)s project matches your query.": [
      "%(count)s projet correspond \u00e0 votre requ\u00eate.", 
      "%(count)s projets correspondent \u00e0 votre requ\u00eate."
    ], 
    "%(count)s user matches your query.": [
      "%(count)s utilisateur correspond \u00e0 votre requ\u00eate.", 
      "%(count)s utilisateurs correspondent \u00e0 votre requ\u00eate."
    ], 
    "%(timeSince)s via file upload": "%(timeSince)s par envoi de fichier", 
    "%s word": [
      "%s mot", 
      "%s mots"
    ], 
    "%s's accepted suggestions": "Suggestions de %s accept\u00e9es", 
    "%s's overwritten submissions": "Contributions de %s \u00e9cras\u00e9es", 
    "%s's pending suggestions": "Suggestions de %s en attente", 
    "%s's rejected suggestions": "Suggestions de %s rejet\u00e9es", 
    "%s's submissions": "Contributions de %s", 
    "Accept": "Accepter", 
    "Account Activation": "Activation de compte", 
    "Account Inactive": "Le compte est inactif", 
    "Active": "Actif", 
    "Add Language": "Ajouter une langue", 
    "Add Project": "Ajouter projet", 
    "Add User": "Ajouter un utilisateur", 
    "Administrator": "Administrateur", 
    "After changing your password you will sign in automatically.": "Apr\u00e8s avoir chang\u00e9 le mot de passe, vous serez automatiquement reconnect\u00e9.", 
    "All Languages": "Toutes les langues", 
    "All Projects": "Tous les projets", 
    "An error occurred while attempting to sign in via %s.": "Une erreur est survenue lors de la connexion depuis %s.", 
    "An error occurred while attempting to sign in via your social account.": "Une erreur est survenue lors de la connexion depuis votre compte social.", 
    "Avatar": "Avatar", 
    "Cancel": "Annuler", 
    "Clear all": "Tout effacer", 
    "Clear value": "Effacer la valeur", 
    "Close": "Fermer", 
    "Code": "Code", 
    "Collapse details": "Masquer les d\u00e9tails", 
    "Congratulations! You have completed this task!": "F\u00e9licitations! Vous avez compl\u00e9t\u00e9 cette t\u00e2che !", 
    "Contact Us": "Contactez-nous", 
    "Contributors, 30 Days": "Contributeurs, 30 jours", 
    "Creating new user accounts is prohibited.": "La cr\u00e9ation de nouveaux comptes utilisateurs est interdite.", 
    "Delete": "Supprimer", 
    "Deleted successfully.": "Supprim\u00e9e avec succ\u00e8s.", 
    "Didn't receive an email? Check if it was accidentally filtered out as spam, or try requesting another copy of the email.": "Vous n'avez pas re\u00e7u de courriel\u00a0? V\u00e9rifiez qu'il n'a pas \u00e9t\u00e9 envoy\u00e9 dans votre dossier de spam ou essayez de demander un nouvel envoi du courriel.", 
    "Disabled": "D\u00e9sactiv\u00e9", 
    "Discard changes.": "Abandonner les modifications.", 
    "Edit Language": "\u00c9diter la langue", 
    "Edit My Public Profile": "\u00c9diter mon profil public", 
    "Edit Project": "\u00c9diter le projet", 
    "Edit User": "Modifier l'utilisateur", 
    "Edit the suggestion before accepting, if necessary": "Modifiez la suggestion avant de l'accepter, si n\u00e9cessaire", 
    "Email": "Courriel", 
    "Email Address": "Adresse \u00e9lectronique", 
    "Email Confirmation": "Confirmation par courriel", 
    "Enter your email address, and we will send you a message with the special link to reset your password.": "Saisissez votre adresse \u00e9lectronique et nous vous enverrons un message contenant un lien sp\u00e9cial pour r\u00e9initialiser votre mot de passe.", 
    "Error while connecting to the server": "Erreur lors de la connexion au serveur", 
    "Expand details": "Montrer les d\u00e9tails", 
    "File types": "Types de fichier", 
    "Filesystems": "Syst\u00e8mes de fichiers", 
    "Find language by name, code": "Trouver langue par nom, code", 
    "Find project by name, code": "Trouver projets par nom, code", 
    "Find user by name, email, properties": "Trouver par nom, email, propri\u00e9t\u00e9s", 
    "Full Name": "Nom complet", 
    "Go back to browsing": "Revenir \u00e0 la navigation", 
    "Go to the next string (Ctrl+.)<br/><br/>Also:<br/>Next page: Ctrl+Shift+.<br/>Last page: Ctrl+Shift+End": "Aller \u00e0 la cha\u00eene suivante (Ctrl+.)<br/><br/>Et aussi :<br/>Page suivante : Ctrl+Shift+.<br/>Derni\u00e8re page: Ctrl+Shift+Fin", 
    "Go to the previous string (Ctrl+,)<br/><br/>Also:<br/>Previous page: Ctrl+Shift+,<br/>First page: Ctrl+Shift+Home": "Aller \u00e0 la page pr\u00e9c\u00e9dente (Ctrl+,)<br/><br/>Et aussi :<br/>Page pr\u00e9c\u00e9dente : Ctrl+Shift+,<br/>Premi\u00e8re page : Ctrl+Shift+Home", 
    "Hide": "Cacher", 
    "Hide disabled": "Cacher d\u00e9sactiv\u00e9s", 
    "I forgot my password": "J'ai oubli\u00e9 mon mot de passe", 
    "Ignore Files": "Ignorer fichiers", 
    "Languages": "Langues", 
    "Less": "Moins", 
    "LinkedIn": "LinkedIn", 
    "LinkedIn profile URL": "URL de profil LinkedIn", 
    "Load More": "En charger d'autres", 
    "Loading...": "Chargement...", 
    "Login / Password": "Identifiant / Mot de passe", 
    "More": "Plus", 
    "More...": "Plus...", 
    "My Public Profile": "Mon profil public", 
    "No": "Non", 
    "No activity recorded in a given period": "Aucune activit\u00e9 enregistr\u00e9e dans une p\u00e9riode donn\u00e9e", 
    "No results found": "Aucun r\u00e9sultat trouv\u00e9", 
    "No results.": "Aucun r\u00e9sultat.", 
    "No, thanks": "Non merci", 
    "Not found": "Pas trouv\u00e9", 
    "Note: when deleting a user their contributions to the site, e.g. comments, suggestions and translations, are attributed to the anonymous user (nobody).": "Note : La suppression d'un utilisateur attribue l'ensemble de ses contributions (commentaires, suggestions et traductions) \u00e0 l'utilisateur anonyme.", 
    "Number of Plurals": "Nombre de pluriels", 
    "Oops...": "Oups...", 
    "Overview": "Vue d'ensemble", 
    "Password": "Mot de passe", 
    "Password changed, signing in...": "Le mot de passe a \u00e9t\u00e9 chang\u00e9, connexion\u2026", 
    "Permissions": "Permissions", 
    "Personal description": "Description personnelle", 
    "Personal website URL": "URL de site web personnel", 
    "Please follow that link to continue the account creation.": "Merci de suivre ce lien pour poursuivre la cr\u00e9ation du compte.", 
    "Please follow that link to continue the password reset procedure.": "Veuillez suivre ce lien pour continuer la proc\u00e9dure de r\u00e9initialisation du mot de passe.", 
    "Please select a valid user.": "Veuillez choisir un utilisateur valable.", 
    "Plural Equation": "\u00c9quation du pluriel", 
    "Plural form %(index)s": "Forme plurielle %(index)s", 
    "Preview will be displayed here.": "L'aper\u00e7u s'affichera ici.", 
    "Project / Language": "Projet / Langue", 
    "Project Tree Style": "Style d'arborescence du projet", 
    "Provide optional comment (will be publicly visible)": "Ajoutez un commentaire optionnel (sera publiquement visible)", 
    "Public Profile": "Profil public", 
    "Quality Checks": "V\u00e9rifications de la qualit\u00e9", 
    "Reject": "Rejeter", 
    "Reload page": "Recharger la page", 
    "Repeat Password": "R\u00e9p\u00e9tition du mot de passe", 
    "Resend Email": "R\u00e9-envoyer le courriel", 
    "Reset Password": "R\u00e9initialiser le mot de passe", 
    "Reset Your Password": "R\u00e9initialiser le mot de passe", 
    "Reviewed": "Relus", 
    "Save": "Sauvegarder", 
    "Saved successfully.": "Enregistr\u00e9e avec succ\u00e8s.", 
    "Score Change": "Score de changements", 
    "Screenshot Search Prefix": "Pr\u00e9fixe de recherche des copies d'\u00e9cran", 
    "Search Languages": "Chercher des langues", 
    "Search Projects": "Chercher des projets", 
    "Search Users": "Chercher utilisateurs", 
    "Select...": "S\u00e9lectionner...", 
    "Send Email": "Envoyer le message", 
    "Sending email to %s...": "Envoi d'un courriel \u00e0 %s\u2026", 
    "Server error": "Erreur de serveur", 
    "Set New Password": "D\u00e9finir le nouveau mot de passe", 
    "Set a new password": "D\u00e9finissez un nouveau mot de passe", 
    "Settings": "Param\u00e8tres", 
    "Short Bio": "Br\u00e8ve bio", 
    "Show": "Montrer", 
    "Show disabled": "Voir d\u00e9sactiv\u00e9s", 
    "Sign In": "Se connecter", 
    "Sign In With %s": "Se connecter avec %s", 
    "Sign In With...": "Se connecter avec\u2026", 
    "Sign Up": "S\u2019inscrire", 
    "Sign in as an existing user": "S'identifier en tant qu'utilisateur existant", 
    "Sign up as a new user": "Se connecter sous un nouvel utilisateur", 
    "Signed in. Redirecting...": "Connect\u00e9. Redirection\u2026", 
    "Signing in with an external service for the first time will automatically create an account for you.": "Se connecter depuis un service ext\u00e9rieur pour la premi\u00e8re fois vous cr\u00e9era automatiquement un compte.", 
    "Similar translations": "Traductions similaires", 
    "Social Services": "R\u00e9seaux sociaux", 
    "Social Verification": "V\u00e9rification sociale", 
    "Source Language": "Langue source", 
    "Special Characters": "Caract\u00e8res sp\u00e9ciaux", 
    "String Errors Contact": "Contact pour les erreurs dans les cha\u00eenes de caract\u00e8res", 
    "Suggested": "Sugg\u00e9r\u00e9", 
    "Team": "\u00c9quipe", 
    "The password reset link was invalid, possibly because it has already been used. Please request a new password reset.": "Le lien de r\u00e9initialisation du mot de passe n'\u00e9tait pas correct, peut-\u00eatre a-t-il d\u00e9j\u00e0 \u00e9t\u00e9 utilis\u00e9\u00a0? Veuillez demander une nouvelle r\u00e9initialisation de votre mot de passe.", 
    "The server seems down. Try again later.": "Le serveur semble hors service. Essayez plus tard.", 
    "There are unsaved changes. Do you want to discard them?": "Il y a changements qui ne sont pas sauvegard\u00e9s. Voulez-vous les annuler ?", 
    "There is %(count)s language.": [
      "Il y a %(count)s langue.", 
      "Il y a %(count)s langues. Ci-dessous se trouvent celles ajout\u00e9es le plus r\u00e9cemment."
    ], 
    "There is %(count)s project.": [
      "Il y a %(count)s projet.", 
      "Il y a %(count)s projets. Ci-dessous se trouvent ceux ajout\u00e9s le plus r\u00e9cemment."
    ], 
    "There is %(count)s user.": [
      "Il y a %(count)s utilisateur.", 
      "Il y a %(count)s utilisateurs. Ci-dessous se trouvent ceux ajout\u00e9s le plus r\u00e9cemment."
    ], 
    "This email confirmation link expired or is invalid.": "Ce lien de confirmation d'email a expir\u00e9 ou n'est pas valide.", 
    "This string no longer exists.": "Cette cha\u00eene n'existe plus.", 
    "To set or change your avatar for your email address (%(email)s), please go to gravatar.com.": "Pour mettre ou modifier votre avatar pour votre adresse email (%(email)s), veuillez aller \u00e0 gravatar.com.", 
    "Translated": "Traduit", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project": "Traduit par %(fullname)s dans le projet \u00ab\u00a0<span title=\"%(path)s\">%(project)s</span>\u00a0\u00bb", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project %(time_ago)s": "Traduit par %(fullname)s dans le projet \u00ab\u00a0<span title=\"%(path)s\">%(project)s</span>\u00a0\u00bb %(time_ago)s", 
    "Try again": "Essayez \u00e0 nouveau", 
    "Twitter": "Twitter", 
    "Twitter username": "Nom d'utilisateur Twitter", 
    "Type to search": "Saisir pour rechercher", 
    "Updating data": "Mis \u00e0 jour des donn\u00e9es", 
    "Use the search form to find the language, then click on a language to edit.": "Utilisez le formulaire de recherche pour trouver la langue, puis cliquez sur une langue pour l'\u00e9diter.", 
    "Use the search form to find the project, then click on a project to edit.": "Utilisez le formulaire de recherche pour trouver le projet, puis cliquez sur un projet pour l'\u00e9diter.", 
    "Use the search form to find the user, then click on a user to edit.": "Utilisez le formulaire de recherche pour trouver l'utilisateur, puis cliquez sur un utilisateur afin de l'\u00e9diter.", 
    "Username": "Nom d'utilisateur", 
    "We found a user with <span>%(email)s</span> email in our system. Please provide the password to finish the sign in procedure. This is a one-off procedure, which will establish a link between your Pootle and %(provider)s accounts.": "Nous avons trouv\u00e9 un utilisateur avec <span>%s</span> adresse mail dans nos syst\u00e8mes. Veuillez nous fournir le mot de passe pour finir l'inscription \u00e0 la proc\u00e9dure. C'est une proc\u00e9dure unique qui va \u00e9tablir un lien entre votre Pootle et %s comptes.", 
    "We have sent an email containing the special link to <span>%s</span>": "Nous avons envoy\u00e9 un courrier \u00e9lectronique contenant le lien sp\u00e9cial \u00e0 <span>%s</span>", 
    "We have sent an email containing the special link to <span>%s</span>. Please check your spam folder if you do not see the email.": "Nous avons envoy\u00e9 un courrier \u00e9lectronique contenant le lien d'activation \u00e0 <span>%s</span>. Veuillez v\u00e9rifier votre boite de spam si vous ne le recevez pas.", 
    "We have sent an email containing the special link to the address used to register this account. Please check your spam folder if you do not see the email.": "Nous avons envoy\u00e9 un courrier \u00e9lectronique contenant le lien sp\u00e9cial \u00e0 l'adresse email utilis\u00e9e pour enregistrer ce compte. Veuillez v\u00e9rifier votre boite de spam si vous ne le recevez pas.", 
    "Website": "Site Web", 
    "Why are you part of our translation project? Describe yourself, inspire others!": "Pourquoi faites-vous partie de notre projet de traduction ? D\u00e9crivez vous, inspirez les autres !", 
    "Yes": "Oui", 
    "You have unsaved changes in this string. Navigating away will discard those changes.": "Vous avez des changements non sauvegard\u00e9s dans ce string. Naviguer ailleurs supprimera vos changements.", 
    "Your Full Name": "Votre nom complet", 
    "Your LinkedIn profile URL": "Votre URL de profil LinkedIn", 
    "Your Personal website/blog URL": "Votre URL de blog/site web personnel", 
    "Your Twitter username": "Votre nom d'utilisateur Twitter", 
    "Your account is inactive because an administrator deactivated it.": "Votre compte est inactif car un administrateur a d\u00e9sactiv\u00e9 celui-ci.", 
    "Your account needs activation.": "Votre compte doit \u00eatre activ\u00e9.", 
    "disabled": "d\u00e9sactiv\u00e9", 
    "some anonymous user": "un certain utilisateur anonyme", 
    "someone": "quelqu'un"
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

