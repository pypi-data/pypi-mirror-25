

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
      "%(count)s idioma corresponde \u00e0 sua consulta.", 
      "%(count)s idiomas correspondem \u00e0 sua consulta."
    ], 
    "%(count)s project matches your query.": [
      "%(count)s projeto corresponde \u00e0 sua consulta.", 
      "%(count)s projetos correspondem \u00e0 sua consulta."
    ], 
    "%(count)s user matches your query.": [
      "%(count)s usu\u00e1rio corresponde \u00e0 sua consulta.", 
      "%(count)s usu\u00e1rios correspondem \u00e0 sua consulta."
    ], 
    "%(timeSince)s via file upload": "%(timeSince)s via envio de arquivo", 
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
    "Add User": "Adicionar usu\u00e1rio", 
    "Administrator": "Administrador", 
    "After changing your password you will sign in automatically.": "Depois de alterar sua senha, voc\u00ea vai entrar automaticamente.", 
    "All Languages": "Todos os idiomas", 
    "All Projects": "Todos os projetos", 
    "An error occurred while attempting to sign in via %s.": "Ocorreu um erro ao tentar entrar via %s.", 
    "An error occurred while attempting to sign in via your social account.": "Ocorreu um erro ao tentar entrar atrav\u00e9s da sua conta social.", 
    "Avatar": "Avatar", 
    "Cancel": "Cancelar", 
    "Clear all": "Limpar tudo", 
    "Clear value": "Limpar valor", 
    "Close": "Fechar", 
    "Code": "C\u00f3digo", 
    "Collapse details": "Ocultar detalhes", 
    "Congratulations! You have completed this task!": "Parab\u00e9ns! Voc\u00ea concluiu esta tarefa!", 
    "Contact Us": "Contate-nos", 
    "Contributors, 30 Days": "Colaboradores, 30 dias", 
    "Creating new user accounts is prohibited.": "Criar novas contas de usu\u00e1rio \u00e9 proibido.", 
    "Delete": "Excluir", 
    "Deleted successfully.": "Exclu\u00eddo com sucesso.", 
    "Didn't receive an email? Check if it was accidentally filtered out as spam, or try requesting another copy of the email.": "N\u00e3o recebeu um e-mail? Verifique se ele foi filtrado acidentalmente como spam, ou tente pedir outra c\u00f3pia do e-mail.", 
    "Disabled": "Desativado", 
    "Discard changes.": "Descartar altera\u00e7\u00f5es.", 
    "Edit Language": "Editar Idioma", 
    "Edit My Public Profile": "Editar meu perfil p\u00fablico", 
    "Edit Project": "Editar projeto", 
    "Edit User": "Editar usu\u00e1rio", 
    "Edit the suggestion before accepting, if necessary": "Editar a sugest\u00e3o antes de aceitar, se necess\u00e1rio", 
    "Email": "E-mail", 
    "Email Address": "Endere\u00e7o de e-mail", 
    "Email Confirmation": "Confirma\u00e7\u00e3o de e-mail", 
    "Enter your email address, and we will send you a message with the special link to reset your password.": "Digite seu endere\u00e7o de e-mail, e vamos enviar uma mensagem para voc\u00ea com o link especial para redefinir sua senha.", 
    "Error while connecting to the server": "Ocorreu um erro ao ligar ao servidor", 
    "Expand details": "Mostrar detalhes", 
    "File types": "Tipos de arquivo", 
    "Filesystems": "Sistemas de arquivo", 
    "Find language by name, code": "Encontrar idioma por nome, c\u00f3digo", 
    "Find project by name, code": "Encontrar projeto por nome, c\u00f3digo", 
    "Find user by name, email, properties": "Encontrar usu\u00e1rio por nome, e-mail, propriedades", 
    "Full Name": "Nome completo", 
    "Go back to browsing": "Voltar para a navega\u00e7\u00e3o", 
    "Go to the next string (Ctrl+.)<br/><br/>Also:<br/>Next page: Ctrl+Shift+.<br/>Last page: Ctrl+Shift+End": "Ir para a pr\u00f3xima string (Ctrl+.)<br/><br/>Tamb\u00e9m:<br/>Pr\u00f3xima p\u00e1gina: Ctrl+Shift+.<br/>\u00daltima p\u00e1gina: Ctrl+Shift+End", 
    "Go to the previous string (Ctrl+,)<br/><br/>Also:<br/>Previous page: Ctrl+Shift+,<br/>First page: Ctrl+Shift+Home": "Ir para a string anterior (Ctrl+,)<br/><br/>Tamb\u00e9m:<br/>P\u00e1gina anterior: Ctrl+Shift+,<br/>Primeira p\u00e1gina: Ctrl+Shift+Home", 
    "Hide": "Ocultar", 
    "Hide disabled": "Ocultar desativados", 
    "I forgot my password": "Esqueci minha senha", 
    "Ignore Files": "Ignorar arquivos", 
    "Languages": "Idiomas", 
    "Less": "Menos", 
    "LinkedIn": "LinkedIn", 
    "LinkedIn profile URL": "URL do perfil do LinkedIn", 
    "Load More": "Carregar mais", 
    "Loading...": "Carregando...", 
    "Login / Password": "Login/senha", 
    "More": "Mais", 
    "More...": "Mais...", 
    "My Public Profile": "Meu perfil p\u00fablico", 
    "No": "N\u00e3o", 
    "No activity recorded in a given period": "Nenhuma atividade registrada em um determinado per\u00edodo", 
    "No results found": "Nenhum resultado encontrado", 
    "No results.": "Nenhum resultado.", 
    "No, thanks": "N\u00e3o, obrigado", 
    "Not found": "N\u00e3o encontrado", 
    "Note: when deleting a user their contributions to the site, e.g. comments, suggestions and translations, are attributed to the anonymous user (nobody).": "Nota: ao excluir um usu\u00e1rio, suas contribui\u00e7\u00f5es para o site, ex: coment\u00e1rios, sugest\u00f5es e tradu\u00e7\u00f5es, s\u00e3o atribu\u00eddas ao usu\u00e1rio an\u00f4nimo (ningu\u00e9m).", 
    "Number of Plurals": "N\u00famero de plurais", 
    "Oops...": "Ops...", 
    "Overview": "Vis\u00e3o geral", 
    "Password": "Senha", 
    "Password changed, signing in...": "Senha alterada, entrando...", 
    "Permissions": "Permiss\u00f5es", 
    "Personal description": "Descri\u00e7\u00e3o pessoal", 
    "Personal website URL": "URL do site pessoal", 
    "Please follow that link to continue the account creation.": "Siga o link para continuar a cria\u00e7\u00e3o da conta.", 
    "Please follow that link to continue the password reset procedure.": "Siga o link para continuar o processo de redefini\u00e7\u00e3o de senha.", 
    "Please select a valid user.": "Selecione um usu\u00e1rio v\u00e1lido.", 
    "Plural Equation": "Equa\u00e7\u00e3o plural", 
    "Plural form %(index)s": "Forma plural %(index)s", 
    "Preview will be displayed here.": "A pr\u00e9-visualiza\u00e7\u00e3o ser\u00e1 mostrada aqui.", 
    "Project / Language": "Projeto/idioma", 
    "Project Tree Style": "Estilo de \u00e1rvore do projeto", 
    "Provide optional comment (will be publicly visible)": "Fornecer coment\u00e1rio adicional (vis\u00edvel ao p\u00fablico)", 
    "Public Profile": "Perfil p\u00fablico", 
    "Quality Checks": "Verifica\u00e7\u00f5es de qualidade", 
    "Reject": "Rejeitar", 
    "Reload page": "Recarregar p\u00e1gina", 
    "Repeat Password": "Repita a senha", 
    "Resend Email": "Reenviar e-mail", 
    "Reset Password": "Redefinir senha", 
    "Reset Your Password": "Redefina sua senha", 
    "Reviewed": "Revisado", 
    "Save": "Salvar", 
    "Saved successfully.": "Salvo com sucesso.", 
    "Score Change": "Altera\u00e7\u00e3o de pontua\u00e7\u00e3o", 
    "Screenshot Search Prefix": "Prefixo de pesquisa de captura de tela", 
    "Search Languages": "Procurar idiomas", 
    "Search Projects": "Procurar projetos", 
    "Search Users": "Procurar usu\u00e1rios", 
    "Select...": "Selecionar...", 
    "Send Email": "Enviar e-mail", 
    "Sending email to %s...": "Enviando e-mail para %s...", 
    "Server error": "Erro no servidor", 
    "Set New Password": "Defina uma nova senha", 
    "Set a new password": "Defina uma nova senha", 
    "Settings": "Configura\u00e7\u00f5es", 
    "Short Bio": "Biografia curta", 
    "Show": "Mostrar", 
    "Show disabled": "Mostrar desativados", 
    "Sign In": "Entrar", 
    "Sign In With %s": "Entrar com %s", 
    "Sign In With...": "Entrar com...", 
    "Sign Up": "Registrar", 
    "Sign in as an existing user": "Entrar como um usu\u00e1rio existente", 
    "Sign up as a new user": "Registrar como um novo usu\u00e1rio", 
    "Signed in. Redirecting...": "Logado. Redirecionando...", 
    "Signing in with an external service for the first time will automatically create an account for you.": "Entrar com um servi\u00e7o externo pela primeira vez ir\u00e1 criar automaticamente uma conta para voc\u00ea.", 
    "Similar translations": "Tradu\u00e7\u00f5es similares", 
    "Social Services": "Servi\u00e7os sociais", 
    "Social Verification": "Verifica\u00e7\u00e3o social", 
    "Source Language": "Idioma fonte", 
    "Special Characters": "Caracteres especiais", 
    "String Errors Contact": "Contato para erros nas strings", 
    "Suggested": "Sugerido", 
    "Team": "Equipe", 
    "The password reset link was invalid, possibly because it has already been used. Please request a new password reset.": "O link de redefini\u00e7\u00e3o de senha era inv\u00e1lido, possivelmente porque ele j\u00e1 foi usado. Solicite uma nova redefini\u00e7\u00e3o de senha.", 
    "The server seems down. Try again later.": "Parece que o servidor est\u00e1 desligado. Tente mais tarde.", 
    "There are unsaved changes. Do you want to discard them?": "H\u00e1 altera\u00e7\u00f5es n\u00e3o salvas. Voc\u00ea deseja descart\u00e1-las?", 
    "There is %(count)s language.": [
      "H\u00e1 %(count)s idioma.", 
      "H\u00e1 %(count)s idiomas. Abaixo est\u00e3o os mais recentemente adicionados."
    ], 
    "There is %(count)s project.": [
      "H\u00e1 %(count)s projeto.", 
      "H\u00e1 %(count)s projetos. Abaixo est\u00e3o os mais recentemente adicionados."
    ], 
    "There is %(count)s user.": [
      "H\u00e1 %(count)s usu\u00e1rio.", 
      "H\u00e1 %(count)s usu\u00e1rios. Abaixo est\u00e3o os mais recentemente adicionados."
    ], 
    "This email confirmation link expired or is invalid.": "Este link de confirma\u00e7\u00e3o de e-mail expirou ou \u00e9 inv\u00e1lido.", 
    "This string no longer exists.": "Esta string n\u00e3o existe mais.", 
    "To set or change your avatar for your email address (%(email)s), please go to gravatar.com.": "Para definir ou alterar o seu avatar para seu endere\u00e7o de e-mail (%(email)s), v\u00e1 para gravatar.com.", 
    "Translated": "Traduzido", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project": "Traduzido por %(fullname)s no projeto \u201c<span title=\"%(path)s\">%(project)s</span>\u201d", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project %(time_ago)s": "Traduzido por %(fullname)s no projeto \u201c<span title=\"%(path)s\">%(project)s</span>\u201d a %(time_ago)s", 
    "Try again": "Tentar novamente", 
    "Twitter": "Twitter", 
    "Twitter username": "Nome de usu\u00e1rio do Twitter", 
    "Type to search": "Digite para pesquisar", 
    "Updating data": "Enviando dados", 
    "Use the search form to find the language, then click on a language to edit.": "Use o formul\u00e1rio de pesquisa para encontrar o idioma, em seguida, clique em um idioma para editar.", 
    "Use the search form to find the project, then click on a project to edit.": "Use o formul\u00e1rio de pesquisa para encontrar o projeto, em seguida, clique em um projeto para editar.", 
    "Use the search form to find the user, then click on a user to edit.": "Use o formul\u00e1rio de pesquisa para encontrar o usu\u00e1rio, em seguida, clique em um usu\u00e1rio para editar.", 
    "Username": "Nome de usu\u00e1rio", 
    "We found a user with <span>%(email)s</span> email in our system. Please provide the password to finish the sign in procedure. This is a one-off procedure, which will establish a link between your Pootle and %(provider)s accounts.": "Encontramos um usu\u00e1rio com o e-mail <span>%(email)s</span> no nosso sistema. Forne\u00e7a a senha para terminar o processo de login. Este \u00e9 um procedimento que s\u00f3 acontece uma vez, que ir\u00e1 estabelecer uma liga\u00e7\u00e3o entre as suas contas Pootle e %(provider)s.", 
    "We have sent an email containing the special link to <span>%s</span>": "Enviamos um e-mail contendo o link especial para <span>%s</span>", 
    "We have sent an email containing the special link to <span>%s</span>. Please check your spam folder if you do not see the email.": "Enviamos um e-mail contendo o link especial para <span>%s</span>. Verifique sua pasta de SPAM se voc\u00ea n\u00e3o encontrar o e-mail.", 
    "We have sent an email containing the special link to the address used to register this account. Please check your spam folder if you do not see the email.": "Enviamos um e-mail contendo o link especial para o endere\u00e7o usado para registrar esta conta. Verifique sua pasta de SPAM se voc\u00ea n\u00e3o encontrar o e-mail.", 
    "Website": "Site", 
    "Why are you part of our translation project? Describe yourself, inspire others!": "Por que voc\u00ea faz parte do nosso projeto de tradu\u00e7\u00e3o? Descreva-se, inspire outras pessoas!", 
    "Yes": "Sim", 
    "You have unsaved changes in this string. Navigating away will discard those changes.": "Voc\u00ea tem altera\u00e7\u00f5es n\u00e3o salvas nesta string. Navegar fora ir\u00e1 descartar estas altera\u00e7\u00f5es.", 
    "Your Full Name": "Seu nome completo", 
    "Your LinkedIn profile URL": "URL do seu perfil do LinkedIn", 
    "Your Personal website/blog URL": "URL do seu site/blog pessoal", 
    "Your Twitter username": "Seu nome de usu\u00e1rio do Twitter", 
    "Your account is inactive because an administrator deactivated it.": "Sua conta est\u00e1 inativa porque um administrador desativou.", 
    "Your account needs activation.": "Sua conta precisa de ativa\u00e7\u00e3o.", 
    "disabled": "desativado", 
    "some anonymous user": "algum usu\u00e1rio an\u00f4nimo", 
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

