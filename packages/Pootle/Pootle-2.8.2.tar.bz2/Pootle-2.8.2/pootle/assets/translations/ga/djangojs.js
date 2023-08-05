

(function(globals) {

  var django = globals.django || (globals.django = {});

  
  django.pluralidx = function(n) {
    var v=(n==1) ? 0 : (n==2) ? 1 : (n>2 && n<7) ? 2 :(n>6 && n<11) ? 3 : 4;
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
      "%(count)s teanga a mheaitse\u00e1lann.", 
      "%(count)s theanga a mheaitse\u00e1lann.", 
      "%(count)s theanga a mheaitse\u00e1lann.", 
      "%(count)s dteanga a mheaitse\u00e1lann.", 
      "%(count)s teanga a mheaitse\u00e1lann."
    ], 
    "%(count)s project matches your query.": [
      "%(count)s tionscadal a mheaitse\u00e1lann.", 
      "%(count)s thionscadal a mheaitse\u00e1lann.", 
      "%(count)s thionscadal a mheaitse\u00e1lann.", 
      "%(count)s dtionscadal a mheaitse\u00e1lann.", 
      "%(count)s tionscadal a mheaitse\u00e1lann."
    ], 
    "%(count)s user matches your query.": [
      "%(count)s \u00fas\u00e1ideoir a mheaitse\u00e1lann.", 
      "%(count)s \u00fas\u00e1ideoir a mheaitse\u00e1lann.", 
      "%(count)s \u00fas\u00e1ideoir a mheaitse\u00e1lann.", 
      "%(count)s \u00fas\u00e1ideoir a mheaitse\u00e1lann.", 
      "%(count)s \u00fas\u00e1ideoir a mheaitse\u00e1lann."
    ], 
    "%(timeSince)s via file upload": "Uasl\u00f3d\u00e1ilte %(timeSince)s \u00f3 shin", 
    "%s word": [
      "%s fhocal", 
      "%s fhocal", 
      "%s fhocal", 
      "%s bhfocal", 
      "%s focal"
    ], 
    "%s's accepted suggestions": "Molta\u00ed glactha \u00f3 %s", 
    "%s's overwritten submissions": "Aistri\u00fach\u00e1in fhorscr\u00edofa de chuid %s", 
    "%s's pending suggestions": "Molta\u00ed \u00f3 %s ar feitheamh", 
    "%s's rejected suggestions": "Molta\u00ed di\u00faltaithe \u00f3 %s", 
    "%s's submissions": "Aistri\u00fach\u00e1in de chuid %s", 
    "Accept": "Glac Leis", 
    "Account Activation": "Gn\u00edomhacht\u00fa Cuntais", 
    "Account Inactive": "Cuntas Neamhghn\u00edomhach", 
    "Active": "Gn\u00edomhach", 
    "Add Language": "Teanga Nua", 
    "Add Project": "Tionscadal Nua", 
    "Add User": "\u00das\u00e1ideoir Nua", 
    "Administrator": "Riarth\u00f3ir", 
    "After changing your password you will sign in automatically.": "Tar \u00e9is duit an focal faire a athr\u00fa, beidh t\u00fa log\u00e1ilte isteach go huathoibr\u00edoch.", 
    "All Languages": "Gach Teanga", 
    "All Projects": "Gach Tionscadal", 
    "An error occurred while attempting to sign in via %s.": "Tharla earr\u00e1id le linn log\u00e1la isteach tr\u00ed %s.", 
    "An error occurred while attempting to sign in via your social account.": "Tharla earr\u00e1id le linn log\u00e1la isteach tr\u00ed do chuntas s\u00f3isialta.", 
    "Avatar": "Abhat\u00e1r", 
    "Cancel": "Cealaigh", 
    "Clear all": "B\u00e1naigh uile", 
    "Clear value": "B\u00e1naigh an luach", 
    "Close": "D\u00fan", 
    "Code": "C\u00f3d", 
    "Collapse details": "Folaigh mionsonra\u00ed", 
    "Congratulations! You have completed this task!": "Comhghairdeas! Chr\u00edochnaigh t\u00fa an tasc seo!", 
    "Contact Us": "D\u00e9an Teagmh\u00e1il Linn", 
    "Contributors, 30 Days": "Rannph\u00e1irtithe, 30 L\u00e1", 
    "Creating new user accounts is prohibited.": "N\u00edl cead agat cuntais nua a chruth\u00fa.", 
    "Delete": "Scrios", 
    "Deleted successfully.": "Scriosadh.", 
    "Didn't receive an email? Check if it was accidentally filtered out as spam, or try requesting another copy of the email.": "Nach bhfuair t\u00fa an r\u00edomhphost? F\u00e9ach an bhfuil s\u00e9 i d'fhillte\u00e1n dramhphoist, n\u00f3 iarr c\u00f3ip nua den teachtaireacht.", 
    "Disabled": "D\u00edchumasaithe", 
    "Discard changes.": "N\u00e1 s\u00e1bh\u00e1il na hathruithe.", 
    "Edit Language": "Cuir Teanga in Eagar", 
    "Edit My Public Profile": "Cuir Mo Phr\u00f3if\u00edl Phoibl\u00ed in Eagar", 
    "Edit Project": "Cuir Tionscadal in Eagar", 
    "Edit User": "Cuir \u00das\u00e1ideoir in Eagar", 
    "Edit the suggestion before accepting, if necessary": "Cuir an moladh in eagar sula nglacfaidh t\u00fa leis, m\u00e1s g\u00e1", 
    "Email": "R\u00edomhphost", 
    "Email Address": "Seoladh R\u00edomhphoist", 
    "Email Confirmation": "Deimhni\u00fa R\u00edomhphoist", 
    "Enter your email address, and we will send you a message with the special link to reset your password.": "Cuir isteach do sheoladh r\u00edomhphoist agus seolfaimid teachtaireacht ina bhfuil nasc lenar f\u00e9idir d'fhocal faire a athr\u00fa.", 
    "Error while connecting to the server": "Earr\u00e1id agus ceangal \u00e1 bhun\u00fa leis an bhfreastala\u00ed", 
    "Expand details": "Taispe\u00e1in mionsonra\u00ed", 
    "File types": "Cine\u00e1lacha comhaid", 
    "Filesystems": "C\u00f3rais chomhad", 
    "Find language by name, code": "Aimsigh teanga tr\u00ed ainm n\u00f3 c\u00f3d", 
    "Find project by name, code": "Aimsigh tionscadal tr\u00ed ainm n\u00f3 c\u00f3d", 
    "Find user by name, email, properties": "Aimsigh \u00fas\u00e1ideoir tr\u00ed ainm, seoladh r\u00edomhphoist, air\u00edonna", 
    "Full Name": "Ainm Ioml\u00e1n", 
    "Go back to browsing": "Brabhs\u00e1il", 
    "Go to the next string (Ctrl+.)<br/><br/>Also:<br/>Next page: Ctrl+Shift+.<br/>Last page: Ctrl+Shift+End": "An ch\u00e9ad teaghr\u00e1n eile (Ctrl+.)<br/><br/>N\u00f3:<br/>An ch\u00e9ad leathanach eile: Ctrl+Shift+.<br/>An leathanach roimhe seo: Ctrl+Shift+End", 
    "Go to the previous string (Ctrl+,)<br/><br/>Also:<br/>Previous page: Ctrl+Shift+,<br/>First page: Ctrl+Shift+Home": "An teaghr\u00e1n roimhe seo (Ctrl+,)<br/><br/>N\u00f3:<br/>An leathanach roimhe seo: Ctrl+Shift+,<br/>An ch\u00e9ad leathanach: Ctrl+Shift+Home", 
    "Hide": "Folaigh", 
    "Hide disabled": "Folaigh d\u00edchumasaithe", 
    "I forgot my password": "N\u00ed cuimhin liom m'fhocal faire", 
    "Ignore Files": "D\u00e9an Neamhaird de Chomhaid", 
    "Languages": "Teangacha", 
    "Less": "N\u00edos L\u00fa", 
    "LinkedIn": "LinkedIn", 
    "LinkedIn profile URL": "URL pr\u00f3if\u00edl LinkedIn", 
    "Load More": "Luchtaigh Tuilleadh", 
    "Loading...": "\u00c1 Lucht\u00fa...", 
    "Login / Password": "Ainm / Focal Faire", 
    "More": "Tuilleadh", 
    "More...": "Tuilleadh...", 
    "My Public Profile": "Mo Phr\u00f3if\u00edl Phoibl\u00ed", 
    "No": "N\u00edl", 
    "No activity recorded in a given period": "N\u00edl aon ghn\u00edomha\u00edocht sa tr\u00e9imhse roghnaithe", 
    "No results found": "Gan tortha\u00ed", 
    "No results.": "Gan tortha\u00ed.", 
    "No, thanks": "N\u00edl, GRMA", 
    "Not found": "Gan aimsi\u00fa", 
    "Note: when deleting a user their contributions to the site, e.g. comments, suggestions and translations, are attributed to the anonymous user (nobody).": "N\u00f3ta: m\u00e1 scriosann t\u00fa \u00fas\u00e1ideoir, cuirfear a c(h)uid n\u00f3ta\u00ed tr\u00e1chta, molta\u00ed agus aistri\u00fach\u00e1n i leith \u00fas\u00e1ideora gan ainm (nobody).", 
    "Number of Plurals": "L\u00edon na hIolra\u00ed", 
    "Oops...": "\u00daps...", 
    "Overview": "Foramharc", 
    "Password": "Focal Faire", 
    "Password changed, signing in...": "Athra\u00edodh an focal faire, do do log\u00e1il isteach...", 
    "Permissions": "Ceadanna", 
    "Personal description": "Cur s\u00edos pearsanta", 
    "Personal website URL": "URL su\u00edmh phearsanta", 
    "Please follow that link to continue the account creation.": "Clice\u00e1il an nasc sin chun an cuntas a chruth\u00fa.", 
    "Please follow that link to continue the password reset procedure.": "Clice\u00e1il an nasc sin chun dul ar aghaidh le hathshocr\u00fa an fhocail fhaire.", 
    "Please select a valid user.": "Roghnaigh \u00fas\u00e1ideoir bail\u00ed.", 
    "Plural Equation": "Cothrom\u00f3id Iolrach", 
    "Plural form %(index)s": "Foirm iolra %(index)s", 
    "Preview will be displayed here.": "Taispe\u00e1nfar r\u00e9amhamharc anseo.", 
    "Project / Language": "Tionscadal / Teanga", 
    "Project Tree Style": "St\u00edl Chrainn an Tionscadail", 
    "Provide optional comment (will be publicly visible)": "Cuir n\u00f3ta tr\u00e1chta roghnach leis (os comhair an tsaoil)", 
    "Public Profile": "Pr\u00f3if\u00edl Phoibl\u00ed", 
    "Quality Checks": "Seice\u00e1lacha C\u00e1il\u00edochta", 
    "Reject": "Di\u00faltaigh", 
    "Reload page": "Athluchtaigh an leathanach", 
    "Repeat Password": "An focal faire ar\u00eds", 
    "Resend Email": "Seol an R\u00edomhphost Ar\u00eds", 
    "Reset Password": "Athshocraigh an Focal Faire", 
    "Reset Your Password": "Athshocraigh d'fhocal faire", 
    "Reviewed": "Athbhreithnithe", 
    "Save": "S\u00e1bh\u00e1il", 
    "Saved successfully.": "S\u00e1bh\u00e1ladh.", 
    "Score Change": "Athr\u00fa Sc\u00f3ir", 
    "Screenshot Search Prefix": "R\u00e9im\u00edr Chuardaigh do Phicti\u00fair", 
    "Search Languages": "Cuardaigh Teangacha", 
    "Search Projects": "Cuardaigh Tionscadail", 
    "Search Users": "Cuardaigh \u00das\u00e1ideoir\u00ed", 
    "Select...": "Roghnaigh...", 
    "Send Email": "Seol R\u00edomhphost", 
    "Sending email to %s...": "R\u00edomhphost \u00e1 sheoladh chuig %s...", 
    "Server error": "Earr\u00e1id fhreastala\u00ed", 
    "Set New Password": "Roghnaigh Focal Faire Nua", 
    "Set a new password": "Roghnaigh focal faire nua", 
    "Settings": "Socruithe", 
    "Short Bio": "Beathaisn\u00e9is\u00edn", 
    "Show": "Taispe\u00e1in", 
    "Show disabled": "Taispe\u00e1in d\u00edchumasaithe", 
    "Sign In": "Log\u00e1il Isteach", 
    "Sign In With %s": "Log\u00e1il Isteach Tr\u00ed %s", 
    "Sign In With...": "Log\u00e1il Isteach Tr\u00ed...", 
    "Sign Up": "Cl\u00e1raigh", 
    "Sign in as an existing user": "Log\u00e1il isteach mar \u00fas\u00e1ideoir at\u00e1 ann", 
    "Sign up as a new user": "Cl\u00e1raigh mar \u00fas\u00e1ideoir nua", 
    "Signed in. Redirecting...": "Log\u00e1ilte isteach. Do d'athdh\u00edri\u00fa...", 
    "Signing in with an external service for the first time will automatically create an account for you.": "An ch\u00e9ad uair a log\u00e1lann t\u00fa isteach tr\u00ed sheirbh\u00eds sheachtrach, cruth\u00f3far cuntas nua ar do shon.", 
    "Similar translations": "Aistri\u00fach\u00e1in cos\u00fail leis seo", 
    "Social Services": "Seirbh\u00eds\u00ed S\u00f3isialta", 
    "Social Verification": "Deimhni\u00fa S\u00f3isialta", 
    "Source Language": "Bunteanga", 
    "Special Characters": "Carachtair Speisialta", 
    "String Errors Contact": "Teagmh\u00e1la\u00ed d'Earr\u00e1id\u00ed sa Bhunteanga", 
    "Suggested": "Molta", 
    "Team": "Foireann", 
    "The password reset link was invalid, possibly because it has already been used. Please request a new password reset.": "N\u00edorbh fh\u00e9idir an focal faire a athshocr\u00fa leis an nasc; b'fh\u00e9idir gur baineadh \u00fas\u00e1id as cheana.  Ba ch\u00f3ir duit nasc nua a iarraidh.", 
    "The server seems down. Try again later.": "Dealra\u00edonn s\u00e9 go bhfuil an freastala\u00ed as feidhm. D\u00e9an iarracht eile ar ball.", 
    "There are unsaved changes. Do you want to discard them?": "Athruithe gan s\u00e1bh\u00e1il. An bhfuil fonn ort iad a sh\u00e1bh\u00e1il?", 
    "There is %(count)s language.": [
      "T\u00e1 %(count)s teanga ann.", 
      "T\u00e1 %(count)s theanga ann. Seo iad na cinn is d\u00e9ana\u00ed.", 
      "T\u00e1 %(count)s theanga ann. Seo iad na cinn is d\u00e9ana\u00ed.", 
      "T\u00e1 %(count)s dteanga ann. Seo iad na cinn is d\u00e9ana\u00ed.", 
      "T\u00e1 %(count)s teanga ann. Seo iad na cinn is d\u00e9ana\u00ed."
    ], 
    "There is %(count)s project.": [
      "T\u00e1 %(count)s tionscadal ann.", 
      "T\u00e1 %(count)s thionscadal ann. Seo iad na cinn is d\u00e9ana\u00ed.", 
      "T\u00e1 %(count)s thionscadal ann. Seo iad na cinn is d\u00e9ana\u00ed.", 
      "T\u00e1 %(count)s dtionscadal ann. Seo iad na cinn is d\u00e9ana\u00ed.", 
      "T\u00e1 %(count)s tionscadal ann. Seo iad na cinn is d\u00e9ana\u00ed."
    ], 
    "There is %(count)s user.": [
      "T\u00e1 %(count)s \u00fas\u00e1ideoir ann.", 
      "T\u00e1 %(count)s \u00fas\u00e1ideoir ann. Seo iad na cinn is d\u00e9ana\u00ed.", 
      "T\u00e1 %(count)s \u00fas\u00e1ideoir ann. Seo iad na cinn is d\u00e9ana\u00ed.", 
      "T\u00e1 %(count)s n-\u00fas\u00e1ideoir ann. Seo iad na cinn is d\u00e9ana\u00ed.", 
      "T\u00e1 %(count)s \u00fas\u00e1ideoir ann. Seo iad na cinn is d\u00e9ana\u00ed."
    ], 
    "This email confirmation link expired or is invalid.": "T\u00e1 an nasc deimhnithe imithe in \u00e9ag, n\u00f3 t\u00e1 s\u00e9 neamhbhail\u00ed.", 
    "This string no longer exists.": "N\u00edl an teaghr\u00e1n seo ann a thuilleadh.", 
    "To set or change your avatar for your email address (%(email)s), please go to gravatar.com.": "Tabhair cuairt ar gravatar.com chun grianghraf nua a cheangal le do sheoladh r\u00edomhphoist (%(email)s).", 
    "Translated": "Aistrithe", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project": "Aistrithe ag %(fullname)s sa tionscadal \u201c<span title=\"%(path)s\">%(project)s</span>\u201d", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project %(time_ago)s": "Aistrithe ag %(fullname)s sa tionscadal \u201c<span title=\"%(path)s\">%(project)s</span>\u201d %(time_ago)s", 
    "Try again": "Bain triail eile as", 
    "Twitter": "Twitter", 
    "Twitter username": "Leasainm Twitter", 
    "Type to search": "Cl\u00f3scr\u00edobh le cuardach", 
    "Updating data": "Sonra\u00ed \u00e1 nuashonr\u00fa", 
    "Use the search form to find the language, then click on a language to edit.": "\u00das\u00e1id an fhoirm le teacht ar an teanga, ansin clice\u00e1il uirthi chun cur in eagar.", 
    "Use the search form to find the project, then click on a project to edit.": "\u00das\u00e1id an fhoirm le teacht ar an tionscadal, ansin clice\u00e1il air le cur in eagar.", 
    "Use the search form to find the user, then click on a user to edit.": "\u00das\u00e1id an fhoirm le teacht ar an \u00fas\u00e1ideoir, ansin clice\u00e1il air le cur in eagar.", 
    "Username": "Ainm \u00fas\u00e1ideora", 
    "We found a user with <span>%(email)s</span> email in our system. Please provide the password to finish the sign in procedure. This is a one-off procedure, which will establish a link between your Pootle and %(provider)s accounts.": "D'aims\u00edomar \u00fas\u00e1ideoir le seoladh r\u00edomhphoist <span>%(email)s</span> in\u00e1r gc\u00f3ras. Tabhair an focal faire chun an log\u00e1il isteach a chur i gcr\u00edch. N\u00ed bheidh s\u00e9 ort \u00e9 seo a dh\u00e9anamh ar\u00eds, agus d\u00e9anfaidh s\u00e9 nasc idir do chuntas Pootle agus do chuntas %(provider)s.", 
    "We have sent an email containing the special link to <span>%s</span>": "T\u00e1imid tar \u00e9is r\u00edomhphost leis an nasc speisialta a sheoladh chuig <span>%s</span>", 
    "We have sent an email containing the special link to <span>%s</span>. Please check your spam folder if you do not see the email.": "T\u00e1imid tar \u00e9is r\u00edomhphost leis an nasc speisialta a sheoladh chuig <span>%s</span>. Mura bhfeiceann t\u00fa an teachtaireacht, breathnaigh ar d'fhillte\u00e1n turscair.", 
    "We have sent an email containing the special link to the address used to register this account. Please check your spam folder if you do not see the email.": "Sheolamar r\u00edomhphost leis an nasc speisialta chuig an seoladh r\u00edomhphoist at\u00e1 ceangailte leis an gcuntas seo. Mura bhfeiceann t\u00fa an teachtaireacht, breathnaigh ar d'fhillte\u00e1n turscair.", 
    "Website": "Su\u00edomh Gr\u00e9as\u00e1in", 
    "Why are you part of our translation project? Describe yourself, inspire others!": "C\u00e9n f\u00e1th a nglacann t\u00fa p\u00e1irt sa tionscadal seo? Abair linn, agus spreag daoine eile!", 
    "Yes": "T\u00e1", 
    "You have unsaved changes in this string. Navigating away will discard those changes.": "Athruithe gan s\u00e1bh\u00e1il sa teaghr\u00e1n seo. Caillfidh t\u00fa na hathruithe seo m\u00e1 fh\u00e1gann t\u00fa.", 
    "Your Full Name": "D'ainm ioml\u00e1n", 
    "Your LinkedIn profile URL": "URL do phr\u00f3if\u00edle LinkedIn", 
    "Your Personal website/blog URL": "URL do shu\u00edmh/bhlag phearsanta", 
    "Your Twitter username": "Do leasainm Twitter", 
    "Your account is inactive because an administrator deactivated it.": "N\u00edl do chuntas ar f\u00e1il toisc gur chuir riarth\u00f3ir \u00f3 fheidhm \u00e9.", 
    "Your account needs activation.": "N\u00ed m\u00f3r duit do chuntas a ghn\u00edomhacht\u00fa.", 
    "disabled": "d\u00edchumasaithe", 
    "some anonymous user": "\u00fas\u00e1ideoir \u00e9igin gan ainm", 
    "someone": "duine \u00e9igin"
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

