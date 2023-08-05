

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
      "%(count)s idioma coincide coa s\u00faa consulta.", 
      "%(count)s idiomas coinciden coa s\u00faa consulta."
    ], 
    "%(count)s project matches your query.": [
      "%(count)s proxecto coincide coa s\u00faa consulta.", 
      "%(count)s proxectos coinciden coa s\u00faa consulta."
    ], 
    "%(count)s user matches your query.": [
      "%(count)s usuario coincide coa s\u00faa consulta.", 
      "%(count)s usuarios coinciden coa s\u00faa consulta."
    ], 
    "%(timeSince)s via file upload": "%(timeSince)s mediante env\u00edo", 
    "%s word": [
      "%s palabra", 
      "%s palabras"
    ], 
    "%s's accepted suggestions": "Suxesti\u00f3ns aceptadas de %s", 
    "%s's overwritten submissions": "Env\u00edos sobrescritos de %s", 
    "%s's pending suggestions": "Suxesti\u00f3ns pendentes de %s", 
    "%s's rejected suggestions": "Suxesti\u00f3ns rexeitadas de %s", 
    "%s's submissions": "Env\u00edos de %s", 
    "Accept": "Aceptar", 
    "Account Activation": "Activaci\u00f3n de conta", 
    "Account Inactive": "Conta inactiva", 
    "Active": "Activo", 
    "Add Language": "Engadir idioma", 
    "Add Project": "Engadir proxecto", 
    "Add User": "Engadir un usuario", 
    "Administrator": "Administrador", 
    "After changing your password you will sign in automatically.": "Acceder\u00e1 automaticamente despois de cambiar o seu contrasinal.", 
    "All Languages": "Todos os idiomas", 
    "All Projects": "Todos os proxectos", 
    "An error occurred while attempting to sign in via %s.": "Produciuse un erro ao intentar acceder a trav\u00e9s de %s.", 
    "An error occurred while attempting to sign in via your social account.": "Produciuse un erro ao intentar acceder empregando a s\u00faa conta social.", 
    "Avatar": "Avatar", 
    "Cancel": "Cancelar", 
    "Clear all": "Limpar todo", 
    "Clear value": "Limpar o valor", 
    "Close": "Pechar", 
    "Code": "C\u00f3digo", 
    "Collapse details": "Ocultar os detalles", 
    "Congratulations! You have completed this task!": "Parab\u00e9ns! Completou esta tarefa!", 
    "Contact Us": "Contacte connosco", 
    "Contributors, 30 Days": "Colaboradores, 30 d\u00edas", 
    "Creating new user accounts is prohibited.": "A creaci\u00f3n de novas contas de usuario est\u00e1 prohibida.", 
    "Delete": "Eliminar", 
    "Deleted successfully.": "Eliminouse con \u00e9xito.", 
    "Didn't receive an email? Check if it was accidentally filtered out as spam, or try requesting another copy of the email.": "Non recibiu ningunha mensaxe? Comprobe se de xeito accidental se filtrou como correo lixo, ou solicite outra copia da mensaxe de correo electr\u00f3nico.", 
    "Disabled": "Desactivado", 
    "Discard changes.": "Desbotar os cambios.", 
    "Edit Language": "Editar idioma", 
    "Edit My Public Profile": "Editar o meu perfil p\u00fablico", 
    "Edit Project": "Editar o proxecto", 
    "Edit User": "Editar o usuario", 
    "Edit the suggestion before accepting, if necessary": "Editar a suxesti\u00f3n antes de aceptala, se for necesario", 
    "Email": "Correo electr\u00f3nico", 
    "Email Address": "Enderezo de correo-e", 
    "Email Confirmation": "Mensaxe de correo-e de confirmaci\u00f3n", 
    "Enter your email address, and we will send you a message with the special link to reset your password.": "Introduza o seu enderezo de correo-e e enviar\u00e1selle unha mensaxe cunha ligaz\u00f3n especial para cambiar o seu contrasinal.", 
    "Error while connecting to the server": "Produciuse un erro ao conectar co servidor", 
    "Expand details": "Mostrar os detalles", 
    "File types": "Tipos de ficheiro", 
    "Filesystems": "Sistemas de ficheiros", 
    "Find language by name, code": "Buscar idioma por nome, c\u00f3digo", 
    "Find project by name, code": "Buscar proxecto por nome ou c\u00f3digo", 
    "Find user by name, email, properties": "Buscar usuario por nome, correo-e, propiedades", 
    "Full Name": "Nome completo", 
    "Go back to browsing": "Volver \u00e1 navegaci\u00f3n", 
    "Go to the next string (Ctrl+.)<br/><br/>Also:<br/>Next page: Ctrl+Shift+.<br/>Last page: Ctrl+Shift+End": "Ir \u00e1 seguinte cadea (Ctrl+.)<br/><br/>Tam\u00e9n:<br/>Seguinte p\u00e1xina: Ctrl+Mai\u00fas+.<br/>\u00daltima p\u00e1xina: Ctrl+Mai\u00fas+Fin", 
    "Go to the previous string (Ctrl+,)<br/><br/>Also:<br/>Previous page: Ctrl+Shift+,<br/>First page: Ctrl+Shift+Home": "Ir \u00e1 cadea anterior (Ctrl+,)<br/><br/>Tam\u00e9n:<br/>P\u00e1xina anterior: Ctrl+Mai\u00fas+,<br/>Primeira p\u00e1xina: Ctrl+Mai\u00fas+Inicio", 
    "Hide": "Ocultar", 
    "Hide disabled": "Ocultar os desactivados", 
    "I forgot my password": "Esquec\u00edn o meu contrasinal", 
    "Ignore Files": "Ficheiros ignorados", 
    "Languages": "Idiomas", 
    "Less": "Menos", 
    "LinkedIn": "LinkedIn", 
    "LinkedIn profile URL": "URL do perfil de LinkedIn", 
    "Load More": "Cargar m\u00e1is", 
    "Loading...": "Cargando\u2026", 
    "Login / Password": "Nome de usuario / Contrasinal", 
    "More": "M\u00e1is", 
    "More...": "M\u00e1is\u2026", 
    "My Public Profile": "O meu perfil p\u00fablico", 
    "No": "Non", 
    "No activity recorded in a given period": "Non se rexistrou actividade no per\u00edodo especificado", 
    "No results found": "Non se atopou ning\u00fan resultado", 
    "No results.": "Sen resultados.", 
    "No, thanks": "Non, grazas", 
    "Not found": "Non atopado", 
    "Note: when deleting a user their contributions to the site, e.g. comments, suggestions and translations, are attributed to the anonymous user (nobody).": "Nota: eliminar un usuario far\u00e1 que as s\u00faas contribuci\u00f3ns (comentarios, suxesti\u00f3ns e traduci\u00f3ns) se lle atrib\u00faan ao usuario an\u00f3nimo (nobody).", 
    "Number of Plurals": "N\u00famero de plurais", 
    "Oops...": "Ups...", 
    "Overview": "Vista xeral", 
    "Password": "Contrasinal", 
    "Password changed, signing in...": "O contrasinal cambiou, accedendo...", 
    "Permissions": "Permisos", 
    "Personal description": "Descrici\u00f3n persoal", 
    "Personal website URL": "URL do sitio web persoal", 
    "Please follow that link to continue the account creation.": "Visite esa ligaz\u00f3n para continuar coa creaci\u00f3n da conta.", 
    "Please follow that link to continue the password reset procedure.": "Visite esa ligaz\u00f3n para continuar co procedemento de cambio do contrasinal.", 
    "Please select a valid user.": "Seleccione un usuario v\u00e1lido.", 
    "Plural Equation": "Ecuaci\u00f3n dos plurais", 
    "Plural form %(index)s": "Forma plural %(index)s", 
    "Preview will be displayed here.": "A vista previa mostrarase aqu\u00ed.", 
    "Project / Language": "Proxecto / Idioma", 
    "Project Tree Style": "Estilo de \u00e1rbore do proxecto", 
    "Provide optional comment (will be publicly visible)": "Prover un comentario opcional (ser\u00e1 vis\u00edbel e p\u00fablico)", 
    "Public Profile": "Perfil p\u00fablico", 
    "Quality Checks": "Comprobaci\u00f3ns de calidade", 
    "Reject": "Rexeitar", 
    "Reload page": "Recargar a p\u00e1xina", 
    "Repeat Password": "Repetir o contrasinal", 
    "Resend Email": "Volver enviar mensaxe de correo electr\u00f3nico", 
    "Reset Password": "Cambiar o contrasinal", 
    "Reset Your Password": "Cambiar o contrasinal", 
    "Reviewed": "Revisadas", 
    "Save": "Gardar", 
    "Saved successfully.": "Gardouse con \u00e9xito.", 
    "Score Change": "Cambio de puntuaci\u00f3n", 
    "Screenshot Search Prefix": "Prefixo de busca de capturas de pantalla", 
    "Search Languages": "Buscar idiomas", 
    "Search Projects": "Buscar proxectos", 
    "Search Users": "Buscar usuarios", 
    "Select...": "Seleccionar\u2026", 
    "Send Email": "Enviar mensaxe de correo electr\u00f3nico", 
    "Sending email to %s...": "Enviando mensaxe a %s...", 
    "Server error": "Erro do servidor", 
    "Set New Password": "Definir un novo contrasinal", 
    "Set a new password": "Definir un novo contrasinal", 
    "Settings": "Preferencias", 
    "Short Bio": "Breve biograf\u00eda", 
    "Show": "Mostrar", 
    "Show disabled": "Mostrar os desactivados", 
    "Sign In": "Acceder", 
    "Sign In With %s": "Acceder con %s", 
    "Sign In With...": "Acceder con...", 
    "Sign Up": "Crear conta", 
    "Sign in as an existing user": "Acceder como un usuario existente", 
    "Sign up as a new user": "Crear conta de usuario", 
    "Signed in. Redirecting...": "Accedeu. Redirix\u00edndoo...", 
    "Signing in with an external service for the first time will automatically create an account for you.": "Acceder cun servizo externo por primeira vez crear\u00e1 automaticamente unha conta para vostede.", 
    "Similar translations": "Traduci\u00f3ns semellantes", 
    "Social Services": "Servizos sociais", 
    "Social Verification": "Verificaci\u00f3n social", 
    "Source Language": "Idioma de orixe", 
    "Special Characters": "Caracteres especiais", 
    "String Errors Contact": "Contacto para informar de erros nas cadeas", 
    "Suggested": "Suxeriu", 
    "Team": "Equipo", 
    "The password reset link was invalid, possibly because it has already been used. Please request a new password reset.": "A ligaz\u00f3n para cambiar o contrasinal era incorrecta, posibelmente porque xa foi usada. Solicite un novo cambio de contrasinal.", 
    "The server seems down. Try again later.": "Parece ser que o servidor est\u00e1 ca\u00eddo. Probe de novo m\u00e1is tarde.", 
    "There are unsaved changes. Do you want to discard them?": "Hai cambios sen gardar. Desexa desbotalos?", 
    "There is %(count)s language.": [
      "Hai %(count)s idioma.", 
      "Hai %(count)s idiomas. Debaixo est\u00e1n os \u00faltimos que se engadiron."
    ], 
    "There is %(count)s project.": [
      "Hai %(count)s proxecto.", 
      "Hai %(count)s proxectos. Debaixo est\u00e1n os \u00faltimos que se engadiron."
    ], 
    "There is %(count)s user.": [
      "Hai %(count)s usuario.", 
      "Hai %(count)s usuarios. Debaixo est\u00e1n os \u00faltimos que se engadiron."
    ], 
    "This email confirmation link expired or is invalid.": "Esta ligaz\u00f3n de confirmaci\u00f3n caducou ou non \u00e9 v\u00e1lida.", 
    "This string no longer exists.": "Esta cadea xa non existe.", 
    "To set or change your avatar for your email address (%(email)s), please go to gravatar.com.": "Para definir ou cambiar o avatar do seu enderezo de correo electr\u00f3nico (%(email)s) vaia a gravatar.com.", 
    "Translated": "Traducidas", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project": "Traducido por %(fullname)s no proxecto \u00ab<span title=\"%(path)s\">%(project)s</span>\u00bb", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project %(time_ago)s": "Traducido por %(fullname)s no proxecto \u00ab<span title=\"%(path)s\">%(project)s</span>\u00bb hai %(time_ago)s", 
    "Try again": "Probar de novo", 
    "Twitter": "Twitter", 
    "Twitter username": "Nome de usuario de Twitter", 
    "Type to search": "Escriba para buscar", 
    "Updating data": "Actualizando os datos", 
    "Use the search form to find the language, then click on a language to edit.": "Use o formulario de busca para atopar o idioma e despois prema nun idioma para editalo.", 
    "Use the search form to find the project, then click on a project to edit.": "Use o formulario de busca para atopar o proxecto, despois prema nun proxecto para editalo.", 
    "Use the search form to find the user, then click on a user to edit.": "Use o formulario de busca para atopar o usuario e despois prema nun usuario para editalo.", 
    "Username": "Nome de usuario", 
    "We found a user with <span>%(email)s</span> email in our system. Please provide the password to finish the sign in procedure. This is a one-off procedure, which will establish a link between your Pootle and %(provider)s accounts.": "Atopouse un usuario neste sistema co correo-e <span>%(email)s</span>. Forneza o contrasinal para rematar o inicio de sesi\u00f3n. Este procedemento realizarase unha \u00fanica vez e asociar\u00e1 as s\u00faas contas de Pootle e %(provider)s.", 
    "We have sent an email containing the special link to <span>%s</span>": "Enviouse unha mensaxe de correo electr\u00f3nico coa ligaz\u00f3n especial a <span>%s</span>", 
    "We have sent an email containing the special link to <span>%s</span>. Please check your spam folder if you do not see the email.": "Enviouse unha mensaxe de correo electr\u00f3nico coa ligaz\u00f3n especial a <span>%s</span>. Comprobe o seu cartafol de spam se non ve a mensaxe.", 
    "We have sent an email containing the special link to the address used to register this account. Please check your spam folder if you do not see the email.": "Enviouse unha mensaxe de correo electr\u00f3nico coa ligaz\u00f3n especial ao enderezo empregado para rexistrar esta conta. Comprobe o seu cartafol de spam se non ve a mensaxe.", 
    "Website": "Sitio web", 
    "Why are you part of our translation project? Describe yourself, inspire others!": "Por que \u00e9 parte do noso proxecto de traduci\u00f3n? Descr\u00edbase, inspire a outros!", 
    "Yes": "Si", 
    "You have unsaved changes in this string. Navigating away will discard those changes.": "Ten cambios sen gardar nesta cadea. Continuar sen gardalos far\u00e1 que se desboten.", 
    "Your Full Name": "O seu nome completo", 
    "Your LinkedIn profile URL": "O URL do seu perfil en LinkedIn", 
    "Your Personal website/blog URL": "O URL do seu sitio web/blog persoal", 
    "Your Twitter username": "O seu nome de usuario en Twitter", 
    "Your account is inactive because an administrator deactivated it.": "A s\u00faa conta est\u00e1 inactiva porque un administrador a desactivou.", 
    "Your account needs activation.": "A s\u00faa conta precisa ser activada.", 
    "disabled": "desactivado", 
    "some anonymous user": "alg\u00fan usuario an\u00f3nimo", 
    "someone": "algu\u00e9n"
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

