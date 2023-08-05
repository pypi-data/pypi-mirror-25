

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
    "#%(position)s": "n.\u00ba %(position)s", 
    "%(count)s language matches your query.": [
      "Hay %(count)s idioma que coincide con la consulta.", 
      "Hay %(count)s idiomas que coinciden con la consulta."
    ], 
    "%(count)s project matches your query.": [
      "La b\u00fasqueda encontr\u00f3 %(count)s proyecto.", 
      "La b\u00fasqueda encontr\u00f3 %(count)s proyectos."
    ], 
    "%(count)s user matches your query.": [
      "Hay %(count)s cuenta de usuario que coincide con la consulta.", 
      "Hay %(count)s cuentas de usuario que coinciden con la consulta."
    ], 
    "%(timeSince)s via file upload": "%(timeSince)s por carga de archivo", 
    "%s word": [
      "%s palabra", 
      "%s palabras"
    ], 
    "%s's accepted suggestions": "Sugerencias aceptadas de %s", 
    "%s's overwritten submissions": "Env\u00edos sobrescritos de %s", 
    "%s's pending suggestions": "Sugerencias pendientes de %s", 
    "%s's rejected suggestions": "Sugerencias rechazadas de %s", 
    "%s's submissions": "Env\u00edos de %s", 
    "Accept": "Aceptar", 
    "Account Activation": "Activaci\u00f3n de la cuenta", 
    "Account Inactive": "Cuenta inactiva", 
    "Active": "Activa", 
    "Add Language": "A\u00f1adir un idioma", 
    "Add Project": "A\u00f1adir un proyecto", 
    "Add User": "A\u00f1adir un usuario", 
    "Administrator": "Administrador", 
    "After changing your password you will sign in automatically.": "Tras modificar la contrase\u00f1a acceder\u00e1 autom\u00e1ticamente.", 
    "All Languages": "Todos los idiomas", 
    "All Projects": "Todos los proyectos", 
    "An error occurred while attempting to sign in via %s.": "Se produjo un error al intentar acceder mediante %s.", 
    "An error occurred while attempting to sign in via your social account.": "Se produjo un error al intentar acceder mediante su cuenta de red social.", 
    "Avatar": "Avatar", 
    "Cancel": "Cancelar", 
    "Clear all": "Vaciar todo", 
    "Clear value": "Vaciar el valor", 
    "Close": "Cerrar", 
    "Code": "C\u00f3digo", 
    "Collapse details": "Reducir detalles", 
    "Congratulations! You have completed this task!": "Felicidades; ha terminado esta tarea.", 
    "Contact Us": "Cont\u00e1ctenos", 
    "Contributors, 30 Days": "Colaboradores, 30 d\u00edas", 
    "Creating new user accounts is prohibited.": "Se ha prohibido la creaci\u00f3n de cuentas de usuario nuevas.", 
    "Delete": "Eliminar", 
    "Deleted successfully.": "Eliminado correctamente.", 
    "Didn't receive an email? Check if it was accidentally filtered out as spam, or try requesting another copy of the email.": "\u00bfNo ha recibido el mensaje? Revise si se ha marcado accidentalmente como \u00abcorreo no deseado\u00bb; o bien, pruebe a solicitar una copia nueva del mensaje.", 
    "Disabled": "Desactivado", 
    "Discard changes.": "Descartar los cambios.", 
    "Edit Language": "Editar el idioma", 
    "Edit My Public Profile": "Editar mi perfil p\u00fablico", 
    "Edit Project": "Editar el proyecto", 
    "Edit User": "Editar el usuario", 
    "Edit the suggestion before accepting, if necessary": "Si fuera necesario, editar sugerencia antes de aceptarla", 
    "Email": "Correo electr\u00f3nico", 
    "Email Address": "Direcci\u00f3n de correo electr\u00f3nico", 
    "Email Confirmation": "Conformaci\u00f3n del correo electr\u00f3nico", 
    "Enter your email address, and we will send you a message with the special link to reset your password.": "Escriba su direcci\u00f3n electr\u00f3nica y le enviaremos un mensaje con el enlace especial que le permitir\u00e1 restablecer su contrase\u00f1a.", 
    "Error while connecting to the server": "Error al conectar con el servidor", 
    "Expand details": "Ampliar detalles", 
    "File types": "Tipos de archivo", 
    "Filesystems": "Sistemas de archivos", 
    "Find language by name, code": "Encontrar un idioma por nombre o c\u00f3digo", 
    "Find project by name, code": "Encontrar un proyecto por nombre o c\u00f3digo", 
    "Find user by name, email, properties": "Encontrar un usuario por nombre, correo electr\u00f3nico o propiedades", 
    "Full Name": "Nombre completo", 
    "Go back to browsing": "Volver a la navegaci\u00f3n", 
    "Go to the next string (Ctrl+.)<br/><br/>Also:<br/>Next page: Ctrl+Shift+.<br/>Last page: Ctrl+Shift+End": "Ir a la pr\u00f3xima cadena (Ctrl\u202f+\u202f.)<br/><br/>Adem\u00e1s:<br/>Pr\u00f3xima p\u00e1gina: Ctrl\u202f+\u202fMay\u00fas\u202f+\u202f.<br/>\u00daltima p\u00e1gina: Ctrl\u202f+\u202fMay\u00fas\u202f+\u202fFin", 
    "Go to the previous string (Ctrl+,)<br/><br/>Also:<br/>Previous page: Ctrl+Shift+,<br/>First page: Ctrl+Shift+Home": "Ir a la cadena anterior (Ctrl\u202f+\u202f,)<br/><br/>Adem\u00e1s:<br/>P\u00e1gina anterior: Ctrl\u202f+\u202fMay\u00fas\u202f+\u202f,<br/>Primera p\u00e1gina: Ctrl\u202f+\u202fMay\u00fas\u202f+\u202fInicio", 
    "Hide": "Ocultar", 
    "Hide disabled": "Ocultar desactivados", 
    "I forgot my password": "He olvidado mi contrase\u00f1a", 
    "Ignore Files": "Ignorar archivos", 
    "Languages": "Idiomas", 
    "Less": "Menos", 
    "LinkedIn": "LinkedIn", 
    "LinkedIn profile URL": "URL del perfil de LinkedIn", 
    "Load More": "Cargar m\u00e1s", 
    "Loading...": "Cargando\u2026", 
    "Login / Password": "Usuario y contrase\u00f1a", 
    "More": "M\u00e1s", 
    "More...": "M\u00e1s\u2026", 
    "My Public Profile": "Perfil p\u00fablico", 
    "No": "No", 
    "No activity recorded in a given period": "No se registr\u00f3 actividad en un per\u00edodo determinado", 
    "No results found": "No se encontr\u00f3 ning\u00fan resultado", 
    "No results.": "No hay resultados.", 
    "No, thanks": "No, gracias", 
    "Not found": "No se ha encontrado", 
    "Note: when deleting a user their contributions to the site, e.g. comments, suggestions and translations, are attributed to the anonymous user (nobody).": "Nota: al eliminar una cuenta de usuario, las contribuciones de la persona \u2014p.\u00a0ej., comentarios, sugerencias y traducciones\u2014 se atribuir\u00e1n al usuario an\u00f3nimo (\u00abnobody\u00bb).", 
    "Number of Plurals": "N\u00famero de plurales", 
    "Oops...": "\u00a1Vaya!", 
    "Overview": "Vista general", 
    "Password": "Contrase\u00f1a", 
    "Password changed, signing in...": "La contrase\u00f1a se ha modificado; accediendo\u2026", 
    "Permissions": "Permisos", 
    "Personal description": "Descripci\u00f3n personal", 
    "Personal website URL": "URL del sitio web personal", 
    "Please follow that link to continue the account creation.": "Pulse en ese enlace para continuar con el proceso de creaci\u00f3n de la cuenta.", 
    "Please follow that link to continue the password reset procedure.": "Pulse en ese enlace para continuar con el proceso de restablecimiento de la contrase\u00f1a.", 
    "Please select a valid user.": "Seleccione una cuenta de usuario v\u00e1lida.", 
    "Plural Equation": "F\u00f3rmula de los plurales", 
    "Plural form %(index)s": "Plural %(index)s", 
    "Preview will be displayed here.": "La previsualizaci\u00f3n aparecer\u00e1 aqu\u00ed.", 
    "Project / Language": "Proyecto/idioma", 
    "Project Tree Style": "Estilo del \u00e1rbol del proyecto", 
    "Provide optional comment (will be publicly visible)": "Proporcione un comentario opcional (visible para el p\u00fablico)", 
    "Public Profile": "Perfil p\u00fablico", 
    "Quality Checks": "Comprobaciones de calidad", 
    "Reject": "Rechazar", 
    "Reload page": "Cargar la p\u00e1gina de nuevo", 
    "Repeat Password": "Repita la contrase\u00f1a", 
    "Resend Email": "Enviar el mensaje de nuevo", 
    "Reset Password": "Restablecer la contrase\u00f1a", 
    "Reset Your Password": "Restablecer la contrase\u00f1a", 
    "Reviewed": "Revis\u00f3", 
    "Save": "Guardar", 
    "Saved successfully.": "Guardado correctamente.", 
    "Score Change": "Cambio en la puntuaci\u00f3n", 
    "Screenshot Search Prefix": "Prefijo de b\u00fasqueda de capturas de pantalla", 
    "Search Languages": "Buscar idiomas", 
    "Search Projects": "Buscar proyectos", 
    "Search Users": "Buscar usuarios", 
    "Select...": "Seleccionar\u2026", 
    "Send Email": "Enviar el mensaje", 
    "Sending email to %s...": "Enviando un mensaje a %s\u2026", 
    "Server error": "Error en el servidor", 
    "Set New Password": "Establecer una contrase\u00f1a nueva", 
    "Set a new password": "Escriba una contrase\u00f1a nueva", 
    "Settings": "Configuraci\u00f3n", 
    "Short Bio": "Biograf\u00eda breve", 
    "Show": "Mostrar", 
    "Show disabled": "Mostrar desactivados", 
    "Sign In": "Acceder", 
    "Sign In With %s": "Acceder mediante %s", 
    "Sign In With...": "Acceder mediante\u2026", 
    "Sign Up": "Registrarse", 
    "Sign in as an existing user": "Acceder como un usuario existente", 
    "Sign up as a new user": "Registrarse como un usuario nuevo", 
    "Signed in. Redirecting...": "Se ha accedido. Redirigiendo\u2026", 
    "Signing in with an external service for the first time will automatically create an account for you.": "Al acceder por primera vez mediante un servicio externo se crear\u00e1 una cuenta autom\u00e1ticamente.", 
    "Similar translations": "Traducciones similares", 
    "Social Services": "Servicios de redes sociales", 
    "Social Verification": "Verificaci\u00f3n social", 
    "Source Language": "Idioma de origen", 
    "Special Characters": "Caracteres especiales", 
    "String Errors Contact": "Contacto de errores en cadenas", 
    "Suggested": "Sugiri\u00f3", 
    "Team": "Equipo", 
    "The password reset link was invalid, possibly because it has already been used. Please request a new password reset.": "El enlace de restablecimiento de la contrase\u00f1a no es v\u00e1lido; quiz\u00e1s se ha utilizado con anterioridad. Solicite un restablecimiento de contrase\u00f1a otra vez.", 
    "The server seems down. Try again later.": "Parece que el servidor est\u00e1 desconectado. Int\u00e9ntelo de nuevo m\u00e1s tarde.", 
    "There are unsaved changes. Do you want to discard them?": "Hay cambios no guardados. \u00bfQuiere descartarlos?", 
    "There is %(count)s language.": [
      "Hay %(count)s idioma registrado.", 
      "Hay %(count)s idiomas registrados. Debajo se muestran los a\u00f1adidos m\u00e1s recientemente."
    ], 
    "There is %(count)s project.": [
      "Hay %(count)s proyecto.", 
      "Hay %(count)s proyectos. Debajo se muestran los a\u00f1adidos m\u00e1s recientemente."
    ], 
    "There is %(count)s user.": [
      "Hay %(count)s cuentas de usuario.", 
      "Hay %(count)s cuentas de usuario. Debajo se muestran las a\u00f1adidas m\u00e1s recientemente."
    ], 
    "This email confirmation link expired or is invalid.": "Este enlace de confirmaci\u00f3n de correo electr\u00f3nico ha caducado o no es v\u00e1lido.", 
    "This string no longer exists.": "Esta cadena ya no existe.", 
    "To set or change your avatar for your email address (%(email)s), please go to gravatar.com.": "Para establecer o modificar un avatar para su direcci\u00f3n de correo (%(email)s), dir\u00edjase a gravatar.com.", 
    "Translated": "Tradujo", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project": "Traducido por %(fullname)s en el proyecto \u00ab<span title=\"%(path)s\">%(project)s</span>\u00bb", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project %(time_ago)s": "Traducido por %(fullname)s en el proyecto \u00ab<span title=\"%(path)s\">%(project)s</span>\u00bb %(time_ago)s", 
    "Try again": "Intentar de nuevo", 
    "Twitter": "Twitter", 
    "Twitter username": "Nombre de usuario de Twitter", 
    "Type to search": "Escriba para buscar", 
    "Updating data": "Actualizando datos", 
    "Use the search form to find the language, then click on a language to edit.": "Utilice el buscador para encontrar el idioma y, a continuaci\u00f3n, pulse en este para editarlo.", 
    "Use the search form to find the project, then click on a project to edit.": "Utilice el buscador para encontrar el proyecto y, a continuaci\u00f3n, pulse en este para editarlo.", 
    "Use the search form to find the user, then click on a user to edit.": "Utilice el buscador para encontrar la cuenta de usuario y, a continuaci\u00f3n, pulse en esta para editarla.", 
    "Username": "Nombre de usuario", 
    "We found a user with <span>%(email)s</span> email in our system. Please provide the password to finish the sign in procedure. This is a one-off procedure, which will establish a link between your Pootle and %(provider)s accounts.": "Encontramos un usuario con la direcci\u00f3n <span>%(email)s</span> en nuestro sistema. Proporcione la contrase\u00f1a para completar el proceso de acceso. Este proceso, que se realiza solo una vez, enlazar\u00e1 sus cuentas de Pootle y %(provider)s.", 
    "We have sent an email containing the special link to <span>%s</span>": "Le hemos enviado un mensaje que contiene el enlace especial a <span>%s</span>", 
    "We have sent an email containing the special link to <span>%s</span>. Please check your spam folder if you do not see the email.": "Le hemos enviado un mensaje que contiene el enlace especial a <span>%s</span>. Revise la carpeta de correo basura si no ve el mensaje.", 
    "We have sent an email containing the special link to the address used to register this account. Please check your spam folder if you do not see the email.": "Le hemos enviado un mensaje que contiene el enlace especial a la direcci\u00f3n usada para registrar esta cuenta. Revise la carpeta de correo basura si no ve el mensaje.", 
    "Website": "Sitio web", 
    "Why are you part of our translation project? Describe yourself, inspire others!": "\u00bfPor qu\u00e9 se ha unido a nuestro proyecto de traducci\u00f3n? \u00a1Descr\u00edbase e inspire a los dem\u00e1s!", 
    "Yes": "S\u00ed", 
    "You have unsaved changes in this string. Navigating away will discard those changes.": "Hay cambios sin guardar en esta cadena. Si contin\u00faa la navegaci\u00f3n se perder\u00e1n esos cambios.", 
    "Your Full Name": "Su nombre completo", 
    "Your LinkedIn profile URL": "El URL de su perfil de LinkedIn", 
    "Your Personal website/blog URL": "El URL de su sitio web o blog personal", 
    "Your Twitter username": "Su nombre de usuario de Twitter", 
    "Your account is inactive because an administrator deactivated it.": "Un administrador ha desactivado su cuenta.", 
    "Your account needs activation.": "La cuenta necesita activaci\u00f3n.", 
    "disabled": "desactivado", 
    "some anonymous user": "un usuario an\u00f3nimo", 
    "someone": "alguien"
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

