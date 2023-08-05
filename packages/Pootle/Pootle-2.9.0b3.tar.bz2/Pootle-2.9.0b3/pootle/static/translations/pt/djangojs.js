

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
      "%(count)s idioma coincidente com a sua consulta.", 
      "%(count)s idiomas coincidentes com a sua consulta."
    ], 
    "%(count)s project matches your query.": [
      "%(count)s projeto corresponde com a sua consulta.", 
      "%(count)s projetos correspondem com a sua consulta."
    ], 
    "%(count)s user matches your query.": [
      "%(count)s utilizador coincidente com a sua consulta.", 
      "%(count)s utilizadores coincidentes com a sua consulta."
    ], 
    "%(timeSince)s via file upload": "%(timeSince)s atrav\u00e9s de envio de ficheiro", 
    "%s word": [
      "%s palavra", 
      "%s palavras"
    ], 
    "%s's accepted suggestions": "Sugest\u00f5es aceites para %s", 
    "%s's overwritten submissions": "Submiss\u00f5es substitu\u00eddas para %s", 
    "%s's pending suggestions": "Sugest\u00f5es pendentes para %s", 
    "%s's rejected suggestions": "Sugest\u00f5es rejeitadas para %s", 
    "%s's submissions": "Submiss\u00f5es de %s", 
    "Accept": "Aceitar", 
    "Account Activation": "Ativa\u00e7\u00e3o de conta", 
    "Account Inactive": "Conta inativa", 
    "Active": "Ativo", 
    "Add Language": "Adicionar idioma", 
    "Add Project": "Adicionar projeto", 
    "Add User": "Adicionar utilizador", 
    "Administrator": "Administrador", 
    "After changing your password you will sign in automatically.": "Depois de alterar a sua palavra-passe, a sua sess\u00e3o ser\u00e1 iniciada automaticamente.", 
    "All Languages": "Todos os idiomas", 
    "All Projects": "Todos os projetos", 
    "An error occurred while attempting to sign in via %s.": "Ocorreu um erro ao tentar iniciar sess\u00e3o via %s.", 
    "An error occurred while attempting to sign in via your social account.": "Ocorreu um erro ao tentar iniciar a sess\u00e3o atrav\u00e9s da sua conta social.", 
    "Avatar": "Avatar", 
    "Cancel": "Cancelar", 
    "Clear all": "Limpar tudo", 
    "Clear value": "Limpar valor", 
    "Close": "Fechar", 
    "Code": "C\u00f3digo", 
    "Collapse details": "Ocultar detalhes", 
    "Congratulations! You have completed this task!": "Parab\u00e9ns! Concluiu esta tarefa!", 
    "Contact Us": "Contacte-nos", 
    "Contributors, 30 Days": "Colaboradores, 30 dias", 
    "Creating new user accounts is prohibited.": "\u00c9 proibido criar novas contas de utilizador.", 
    "Delete": "Apagar", 
    "Deleted successfully.": "Apagada com sucesso.", 
    "Didn't receive an email? Check if it was accidentally filtered out as spam, or try requesting another copy of the email.": "N\u00e3o recebeu o e-mail? Verifique se esta est\u00e1 na pasta de spam ou tente solicitar uma outra c\u00f3pia do e-mail.", 
    "Disabled": "Desativado", 
    "Discard changes.": "Rejeitar altera\u00e7\u00f5es.", 
    "Edit Language": "Editar idioma", 
    "Edit My Public Profile": "Editar o meu perfil p\u00fablico", 
    "Edit Project": "Editar projeto", 
    "Edit User": "Editar utilizador", 
    "Edit the suggestion before accepting, if necessary": "Se necess\u00e1rio, editar sugest\u00e3o antes de aceitar", 
    "Email": "E-mail", 
    "Email Address": "Endere\u00e7o de e-mail", 
    "Email Confirmation": "Mensagem de confirma\u00e7\u00e3o", 
    "Enter your email address, and we will send you a message with the special link to reset your password.": "Insira o seu endere\u00e7o de e-mail, e n\u00f3s iremos enviar-lhe uma mensagem com uma liga\u00e7\u00e3o especial para redefinir a sua palavra-passe.", 
    "Error while connecting to the server": "Ocorreu um erro ao ligar ao servidor.", 
    "Expand details": "Expandir detalhes", 
    "File types": "Tipos de ficheiro", 
    "Filesystems": "Sistema de ficheiros", 
    "Find language by name, code": "Encontrar idiomas por nome, c\u00f3digo", 
    "Find project by name, code": "Encontrar projeto pelo nome, c\u00f3digo", 
    "Find user by name, email, properties": "Encontrar utilizador por nome, e-mail, propriedades", 
    "Full Name": "Nome completo", 
    "Go back to browsing": "Voltar para a navega\u00e7\u00e3o", 
    "Go to the next string (Ctrl+.)<br/><br/>Also:<br/>Next page: Ctrl+Shift+.<br/>Last page: Ctrl+Shift+End": "Ir para a linha seguinte (Ctrl+.)<br/><br/>Tamb\u00e9m:<br/>P\u00e1gina seguinte: Ctrl+Shift+.<br/>\u00daltima p\u00e1gina: Ctrl+Shift+End", 
    "Go to the previous string (Ctrl+,)<br/><br/>Also:<br/>Previous page: Ctrl+Shift+,<br/>First page: Ctrl+Shift+Home": "Ir para a linha anterior (Ctrl+,)<br/><br/>Tamb\u00e9m:<br/>P\u00e1gina anterior: Ctrl+Shift+,<br/>Primeira p\u00e1gina: Ctrl+Shift+Home", 
    "Hide": "Ocultar", 
    "Hide disabled": "Ocultar desativados", 
    "I forgot my password": "Eu esqueci-me da minha palavra-passe", 
    "Ignore Files": "Ignorar ficheiros", 
    "Languages": "Idiomas", 
    "Less": "Menos", 
    "LinkedIn": "LinkedIn", 
    "LinkedIn profile URL": "URL do perfil LinkedIn", 
    "Load More": "Carregar mais", 
    "Loading...": "A carregar...", 
    "Login / Password": "Sess\u00e3o/Palavra-passe", 
    "More": "Mais", 
    "More...": "Mais...", 
    "My Public Profile": "O meu perfil p\u00fablico", 
    "No": "N\u00e3o", 
    "No activity recorded in a given period": "N\u00e3o existe atividade no per\u00edodo indicado.", 
    "No results found": "N\u00e3o foram encontrados resultados", 
    "No results.": "Nenhum resultado.", 
    "No, thanks": "N\u00e3o, obrigado", 
    "Not found": "N\u00e3o encontrado", 
    "Note: when deleting a user their contributions to the site, e.g. comments, suggestions and translations, are attributed to the anonymous user (nobody).": "Nota: se eliminar um utilizador, todos os contributos desse utilizador, por exemplo coment\u00e1rios, sugest\u00f5es e tradu\u00e7\u00f5es ser\u00e3o atribu\u00eddos ao utilizador an\u00f3nimo (ningu\u00e9m).", 
    "Number of Plurals": "N\u00famero de plurais", 
    "Oops...": "Ups...", 
    "Overview": "Sinopse", 
    "Password": "Palavra-passe", 
    "Password changed, signing in...": "Palavra-passe alterada, a iniciar sess\u00e3o...", 
    "Permissions": "Permiss\u00f5es", 
    "Personal description": "Descri\u00e7\u00e3o pessoal", 
    "Personal website URL": "URL do site pessoal", 
    "Please follow that link to continue the account creation.": "Por favor, siga esta liga\u00e7\u00e3o para continuar com a cria\u00e7\u00e3o da conta.", 
    "Please follow that link to continue the password reset procedure.": "Por favor, siga essa liga\u00e7\u00e3o para continuar com a reposi\u00e7\u00e3o da palavra-passe.", 
    "Please select a valid user.": "Por favor, selecione um utilizador v\u00e1lido.", 
    "Plural Equation": "Equa\u00e7\u00e3o plural", 
    "Plural form %(index)s": "Forma plural %(index)s", 
    "Preview will be displayed here.": "A pr\u00e9-visualiza\u00e7\u00e3o ser\u00e1 mostrada aqui.", 
    "Project / Language": "Projeto/Idioma", 
    "Project Tree Style": "Estilo de \u00e1rvore do projeto", 
    "Provide optional comment (will be publicly visible)": "Disponibilizar coment\u00e1rio opcional (vis\u00edvel ao p\u00fablico)", 
    "Public Profile": "Perfil p\u00fablico", 
    "Quality Checks": "Verifica\u00e7\u00f5es de qualidade", 
    "Reject": "Rejeitar", 
    "Reload page": "Recarregar p\u00e1gina", 
    "Repeat Password": "Repetir palavra-passe", 
    "Resend Email": "Reenviar mensagem", 
    "Reset Password": "Repor palavra-passe", 
    "Reset Your Password": "Repor a sua palavra-passe", 
    "Reviewed": "Revista", 
    "Save": "Guardar", 
    "Saved successfully.": "Guardada com sucesso.", 
    "Score Change": "Altera\u00e7\u00e3o de pontua\u00e7\u00e3o", 
    "Screenshot Search Prefix": "Prefixo para a captura de ecr\u00e3 da procura", 
    "Search Languages": "Procurar idiomas", 
    "Search Projects": "Procurar projetos", 
    "Search Users": "Procurar utilizadores", 
    "Select...": "Selecionar...", 
    "Send Email": "Enviar e-mail", 
    "Sending email to %s...": "A enviar e-mail para %s...", 
    "Server error": "Erro de servidor", 
    "Set New Password": "Definir nova palavra-passe", 
    "Set a new password": "Defina uma nova palavra-passe", 
    "Settings": "Defini\u00e7\u00f5es", 
    "Short Bio": "Biografia", 
    "Show": "Mostrar", 
    "Show disabled": "Mostrar desativados", 
    "Sign In": "Iniciar sess\u00e3o", 
    "Sign In With %s": "Iniciar sess\u00e3o com %s", 
    "Sign In With...": "Iniciar sess\u00e3o com...", 
    "Sign Up": "Registar", 
    "Sign in as an existing user": "Iniciar sess\u00e3o como utilizador existente", 
    "Sign up as a new user": "Registar como um novo utilizador", 
    "Signed in. Redirecting...": "Sess\u00e3o iniciada. A redirecionar...", 
    "Signing in with an external service for the first time will automatically create an account for you.": "Ao iniciar a sess\u00e3o com um servi\u00e7o externo pela primeira vez, ir\u00e1 criar automaticamente uma nova conta.", 
    "Similar translations": "Tradu\u00e7\u00f5es similares", 
    "Social Services": "Servi\u00e7os sociais", 
    "Social Verification": "Verifica\u00e7\u00e3o social", 
    "Source Language": "Idioma original", 
    "Special Characters": "Carateres especiais", 
    "String Errors Contact": "Contacto para erros nas cadeias", 
    "Suggested": "Sugerida", 
    "Team": "Equipa", 
    "The password reset link was invalid, possibly because it has already been used. Please request a new password reset.": "A liga\u00e7\u00e3o de reposi\u00e7\u00e3o de palavra-passe era inv\u00e1lida, possivelmente porque j\u00e1 foi utilizada. Por favor, solicite uma nova reposi\u00e7\u00e3o de palavra-passe.", 
    "The server seems down. Try again later.": "Parece que o servidor est\u00e1 desligado. Tente mais tarde.", 
    "There are unsaved changes. Do you want to discard them?": "Existem altera\u00e7\u00f5es n\u00e3o guardadas. Pretende rejeit\u00e1-las?", 
    "There is %(count)s language.": [
      "Existe %(count)s idioma.", 
      "Existem %(count)s idiomas. Em baixo est\u00e3o as adi\u00e7\u00f5es mais recentes."
    ], 
    "There is %(count)s project.": [
      "Existe %(count)s projeto.", 
      "Existem %(count)s projetos. Em baixo est\u00e3o as adi\u00e7\u00f5es mais recentes."
    ], 
    "There is %(count)s user.": [
      "Existe %(count)s utilizador.", 
      "Existem %(count)s utilizadores. Em baixo est\u00e3o os adicionados mais recentemente."
    ], 
    "This email confirmation link expired or is invalid.": "Esta liga\u00e7\u00e3o de confirma\u00e7\u00e3o de e-mail expirou ou \u00e9 inv\u00e1lida.", 
    "This string no longer exists.": "Esta linha j\u00e1 n\u00e3o existe.", 
    "To set or change your avatar for your email address (%(email)s), please go to gravatar.com.": "Para definir ou alterar o seu avatar do seu endere\u00e7o de e-mail (%(email)s), por favor, v\u00e1 para gravatar.com.", 
    "Translated": "Traduzida", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project": "Traduzido por %(fullname)s no projeto \u201c<span title=\"%(path)s\">%(project)s</span>\u201d", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project %(time_ago)s": "Traduzido por %(fullname)s no projeto \u201c<span title=\"%(path)s\">%(project)s</span>\u201d a %(time_ago)s", 
    "Try again": "Tentar novamente", 
    "Twitter": "Twitter", 
    "Twitter username": "Nome de utilizador do Twitter", 
    "Type to search": "Digite para procurar", 
    "Updating data": "A atualizar dados", 
    "Use the search form to find the language, then click on a language to edit.": "Utilize o campo de procura para encontrar o idioma e clique no idioma para o editar.", 
    "Use the search form to find the project, then click on a project to edit.": "Utilize o campo de procura para encontrar o projeto e clique no projeto para o editar.", 
    "Use the search form to find the user, then click on a user to edit.": "Utilize o campo de procura para encontrar o utilizador e clique no utilizador para o editar.", 
    "Username": "Nome de utilizador", 
    "We found a user with <span>%(email)s</span> email in our system. Please provide the password to finish the sign in procedure. This is a one-off procedure, which will establish a link between your Pootle and %(provider)s accounts.": "Encontr\u00e1mos, no nosso sistema, um utilizador com o e-mail <span>%(email)s</span>. Por favor, introduza a palavra-passe para terminar o in\u00edcio da sess\u00e3o. Este \u00e9 um procedimento \u00fanico, que ir\u00e1 estabelecer uma associa\u00e7\u00e3o entre o seu Pootle e as contas %(provider)s.", 
    "We have sent an email containing the special link to <span>%s</span>": "Envi\u00e1mos um e-mail com uma liga\u00e7\u00e3o especial para <span>%s</span>", 
    "We have sent an email containing the special link to <span>%s</span>. Please check your spam folder if you do not see the email.": "Envi\u00e1mos uma mensagem com uma hiperliga\u00e7\u00e3o especial para <span>%s</span>. Verifique a sua pasta de Spam caso n\u00e3o veja a mensagem.", 
    "We have sent an email containing the special link to the address used to register this account. Please check your spam folder if you do not see the email.": "Envi\u00e1mos uma mensagem com uma hiperliga\u00e7\u00e3o especial para o endere\u00e7o utilizado no registo desta conta. Verifique a sua pasta de Spam caso n\u00e3o veja a mensagem. ", 
    "Website": "Site", 
    "Why are you part of our translation project? Describe yourself, inspire others!": "Porque \u00e9 que faz parte do nosso projeto de tradu\u00e7\u00e3o? Descreva-se, e inspire as outras pessoas!", 
    "Yes": "Sim", 
    "You have unsaved changes in this string. Navigating away will discard those changes.": "Tem altera\u00e7\u00f5es n\u00e3o guardadas nesta linha. Se sair da mesma, estas ser\u00e3o ignoradas.", 
    "Your Full Name": "O seu nome completo", 
    "Your LinkedIn profile URL": "O URL do seu perfil LinkedIn", 
    "Your Personal website/blog URL": "O URL do seu site da Web/blogue Pessoal", 
    "Your Twitter username": "O seu nome de utilizador do Twitter", 
    "Your account is inactive because an administrator deactivated it.": "A sua conta est\u00e1 inativa porque foi desativada por um administrador.", 
    "Your account needs activation.": "A sua conta precisa de ser ativada.", 
    "disabled": "desativado", 
    "some anonymous user": "algum utilizador an\u00f3nimo", 
    "someone": "algu\u00e9m"
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

