

(function(globals) {

  var django = globals.django || (globals.django = {});

  
  django.pluralidx = function(n) {
    var v=(n%100==1 ? 0 : n%100==2 ? 1 : n%100==3 || n%100==4 ? 2 : 3);
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
      "%(count)s r\u011b\u010d wa\u0161emu napra\u0161owanju wotpow\u011bduje.", 
      "%(count)s r\u011b\u010di wa\u0161emu napra\u0161owanju wotpow\u011bdujetej.", 
      "%(count)s r\u011b\u010de wa\u0161emu napra\u0161owanju wotpow\u011bduja.", 
      "%(count)s r\u011b\u010dow wa\u0161emu napra\u0161owanju wotpow\u011bduje."
    ], 
    "%(count)s project matches your query.": [
      "%(count)s projekt twojemu napra\u0161owanju wotpow\u011bduje.", 
      "%(count)s projektaj twojemu napra\u0161owanju wotpow\u011bdujetej.", 
      "%(count)s projekty twojemu napra\u0161owanju wotpow\u011bduja.", 
      "%(count)s projektow twojemu napra\u0161owanju wotpow\u011bduje."
    ], 
    "%(count)s user matches your query.": [
      "%(count)s wu\u017eiwar twojemu napra\u0161owanju wotpow\u011bduje.", 
      "%(count)s wu\u017eiwarjej twojemu napra\u0161owanju wotpow\u011bdujetej.", 
      "%(count)s wu\u017eiwarjo twojemu napra\u0161owanju wotpow\u011bduja.", 
      "%(count)s wu\u017eiwarjow twojemu napra\u0161owanju wotpow\u011bduje."
    ], 
    "%(timeSince)s via file upload": "%(timeSince)s p\u0159ez datajowe nahra\u0107e", 
    "%s word": [
      "%s s\u0142owo", 
      "%s s\u0142owje", 
      "%s s\u0142owa", 
      "%s s\u0142owow"
    ], 
    "%s's accepted suggestions": "akceptowane namjety wu\u017eiwarja %s", 
    "%s's overwritten submissions": "zm\u011bnjene zapoda\u0107a wu\u017eiwarja %s", 
    "%s's pending suggestions": "\u010dakace namjety wu\u017eiwarja %s", 
    "%s's rejected suggestions": "wotpokazane namjety wu\u017eiwarja %s", 
    "%s's submissions": "zapoda\u0107a wu\u017eiwarja %s", 
    "Accept": "Akceptowa\u0107", 
    "Account Activation": "Aktiwizowanje konta", 
    "Account Inactive": "Konto je inaktiwne", 
    "Active": "Aktiwny", 
    "Add Language": "R\u011b\u010d p\u0159ida\u0107", 
    "Add Project": "Projekt p\u0159ida\u0107", 
    "Add User": "Wu\u017eiwarja p\u0159ida\u0107", 
    "Administrator": "Administrator", 
    "After changing your password you will sign in automatically.": "Po tym zo sy swoje hes\u0142o zm\u011bni\u0142, so awtomatisce p\u0159izjewi\u0161.", 
    "All Languages": "W\u0161\u011b r\u011b\u010de", 
    "All Projects": "W\u0161\u011b projekty", 
    "An error occurred while attempting to sign in via %s.": "P\u0159i pospy\u0107e so p\u0159ez %s p\u0159izjewi\u0107, je zmylk wustupi\u0142.", 
    "An error occurred while attempting to sign in via your social account.": "P\u0159i pospy\u0107e p\u0159ez swoje konto p\u0159izjewi\u0107, je zmylk wustupi\u0142.", 
    "Avatar": "Awatar", 
    "Cancel": "P\u0159etorhny\u0107", 
    "Clear all": "W\u0161\u011b zha\u0161e\u0107", 
    "Clear value": "H\u00f3dnotu zha\u0161e\u0107", 
    "Close": "Za\u010dini\u0107", 
    "Code": "Kod", 
    "Collapse details": "Podrobnos\u0107e schowa\u0107", 
    "Congratulations! You have completed this task!": "Zbo\u017eop\u0159e\u0107e! Sy tut\u00f3n nadawk s\u010dini\u0142!", 
    "Contact Us": "Staj so z nami do zwiska", 
    "Contributors, 30 Days": "P\u0159ino\u0161owarjo, 30 dnjow", 
    "Creating new user accounts is prohibited.": "Za\u0142o\u017eenje nowych wu\u017eiwarskich kontow je zakazane.", 
    "Delete": "Zha\u0161e\u0107", 
    "Deleted successfully.": "Wusp\u011b\u0161nje zha\u0161any.", 
    "Didn't receive an email? Check if it was accidentally filtered out as spam, or try requesting another copy of the email.": "Njesy e-mejlku d\u00f3sta\u0142? P\u0159epruwuj\u0107e, ha\u010d je so zmylnje jako spam wufiltrowa\u0142a abo po\u017eadaj dal\u0161u kopiju e-mejlki.", 
    "Disabled": "Znjem\u00f3\u017enjeny", 
    "Discard changes.": "Zm\u011bny za\u0107isny\u0107.", 
    "Edit Language": "R\u011b\u010d wobd\u017a\u011b\u0142a\u0107", 
    "Edit My Public Profile": "M\u00f3j zjawny profil wobd\u017a\u011b\u0142a\u0107", 
    "Edit Project": "Projekt wobd\u017a\u011b\u0142a\u0107", 
    "Edit User": "Wu\u017eiwarja wobd\u017a\u011b\u0142a\u0107", 
    "Edit the suggestion before accepting, if necessary": "Wobd\u017a\u011b\u0142aj namjet, prjedy ha\u010d j\u00f3n akceptuje\u0161, jeli trjeba", 
    "Email": "E-mejl", 
    "Email Address": "E-mejlowa adresa", 
    "Email Confirmation": "E-mejlowe wobkru\u0107enje", 
    "Enter your email address, and we will send you a message with the special link to reset your password.": "Zapodaj swoju e-mejlowu adresu a my p\u00f3s\u0107elemy wam pow\u011bs\u0107 ze specialnym wotkazom za wr\u00f3\u0107ostajenje twojeho hes\u0142a.", 
    "Error while connecting to the server": "Zmylk p\u0159i zwjazowanju ze serwerom", 
    "Expand details": "Podrobnos\u0107e pokaza\u0107", 
    "File types": "Datajowe typy", 
    "Filesystems": "Datajowe systemy", 
    "Find language by name, code": "R\u011b\u010d po mjenje abo kod\u017ae pyta\u0107", 
    "Find project by name, code": "Projekt po mjenje abo kod\u017ae pyta\u0107", 
    "Find user by name, email, properties": "Wu\u017eiwarja po mjenje, e-mejli abo kajkos\u0107ach pyta\u0107", 
    "Full Name": "Dospo\u0142ne mjeno", 
    "Go back to browsing": "Rozhladuj\u0107e so dale", 
    "Go to the next string (Ctrl+.)<br/><br/>Also:<br/>Next page: Ctrl+Shift+.<br/>Last page: Ctrl+Shift+End": "D\u017ai k p\u0159ichodnemu znamje\u0161kowemu rje\u0107azkej (Str+.)<br/><br/>Te\u017e:<br/>P\u0159ichodna strona: Strg+Umsch+.<br/>Poslednja strona: Strg+Umsch+Ende", 
    "Go to the previous string (Ctrl+,)<br/><br/>Also:<br/>Previous page: Ctrl+Shift+,<br/>First page: Ctrl+Shift+Home": "D\u017ai k p\u0159edchadnemu znamje\u0161kowemu rje\u0107azkej (Str+,)<br/><br/>Te\u017e:<br/>P\u0159edchadna strona: Strg+Umsch+,<br/>Pr\u011bnja strona: Strg+Umsch+Pos1", 
    "Hide": "Schowa\u0107", 
    "Hide disabled": "Znjem\u00f3\u017enjene schowa\u0107", 
    "I forgot my password": "Sym swoje hes\u0142o zaby\u0142", 
    "Ignore Files": "Dataje ignorowa\u0107", 
    "Languages": "R\u011b\u010de", 
    "Less": "Mjenje", 
    "LinkedIn": "LinkedIn", 
    "LinkedIn profile URL": "Profilowy URL LinkedIn", 
    "Load More": "Dal\u0161e za\u010dita\u0107", 
    "Loading...": "Za\u010dituje so...", 
    "Login / Password": "P\u0159izjewjenje / Hes\u0142o", 
    "More": "Wjace", 
    "More...": "Wjace...", 
    "My Public Profile": "M\u00f3j zjawny profil", 
    "No": "N\u011b", 
    "No activity recorded in a given period": "\u017dana aktiwita njeje so w datej dobje zw\u011bs\u0107i\u0142a", 
    "No results found": "\u017dane wusl\u011bdki namakane", 
    "No results.": "\u017dane wusl\u011bdki.", 
    "No, thanks": "N\u011b, d\u017aakuju so", 
    "Not found": "Njenamakany", 
    "Note: when deleting a user their contributions to the site, e.g. comments, suggestions and translations, are attributed to the anonymous user (nobody).": "Ked\u017abu: hdy\u017e so wu\u017eiwar zha\u0161a, so jeho p\u0159ino\u0161ki za syd\u0142o, na p\u0159. komentary, namjety a p\u0159e\u0142o\u017eki, anonymnemu wu\u017eiwarjej (nikomu) p\u0159opokazaja.", 
    "Number of Plurals": "Li\u010dba pluralow", 
    "Oops...": "Hopla...", 
    "Overview": "P\u0159ehlad", 
    "Password": "Hes\u0142o", 
    "Password changed, signing in...": "Hes\u0142o je so zm\u011bni\u0142o, p\u0159izjewjenje b\u011b\u017ei...", 
    "Permissions": "Prawa", 
    "Personal description": "Wosobinske wopisanje", 
    "Personal website URL": "URL wosobinskeho websyd\u0142a", 
    "Please follow that link to continue the account creation.": "Pro\u0161u sl\u011bduj tutomu wotkazej, zo by ze za\u0142o\u017eenjom konta pokro\u010dowa\u0142.", 
    "Please follow that link to continue the password reset procedure.": "Pro\u0161u sl\u011bduj wotkazej, zo by z proceduru wr\u00f3\u0107ostajenja hes\u0142a pokro\u010dowa\u0142.", 
    "Please select a valid user.": "Pro\u0161u wubjer p\u0142a\u0107iweho wu\u017eiwarja.", 
    "Plural Equation": "Pluralowa formla", 
    "Plural form %(index)s": "Pluralowa forma %(index)s", 
    "Preview will be displayed here.": "P\u0159ehlad so tu pokaza.", 
    "Project / Language": "Projekt / R\u011b\u010d", 
    "Project Tree Style": "Stil projektoweho \u0161toma", 
    "Provide optional comment (will be publicly visible)": "Pisaj\u0107e komentar (bud\u017ae zjawnje wid\u017aomny)", 
    "Public Profile": "Zjawny profil", 
    "Quality Checks": "Kwalitne kontrole", 
    "Reject": "Wotpokaza\u0107", 
    "Reload page": "Stronu znowa za\u010dita\u0107", 
    "Repeat Password": "Hes\u0142o wospjetowa\u0107", 
    "Resend Email": "E-mejlku hi\u0161\u0107e raz p\u00f3s\u0142a\u0107", 
    "Reset Password": "Hes\u0142o wr\u00f3\u0107o staji\u0107", 
    "Reset Your Password": "Wa\u0161e hes\u0142o wr\u00f3\u0107o staji\u0107", 
    "Reviewed": "Poh\u00f3dno\u0107eny", 
    "Save": "Sk\u0142adowa\u0107", 
    "Saved successfully.": "Wusp\u011b\u0161nje sk\u0142adowany.", 
    "Score Change": "Zm\u011bna stawa", 
    "Screenshot Search Prefix": "Prefiks za pytanje za fotami wobrazowki", 
    "Search Languages": "R\u011b\u010de p\u0159epytowa\u0107", 
    "Search Projects": "Projekty p\u0159epytowa\u0107", 
    "Search Users": "Wu\u017eiwarjow p\u0159epytowa\u0107", 
    "Select...": "Wubra\u0107...", 
    "Send Email": "E-mejlku p\u00f3s\u0142a\u0107", 
    "Sending email to %s...": "E-mejlka so na %s s\u0107ele...", 
    "Server error": "Serwerowy zmylk", 
    "Set New Password": "Nowe hes\u0142o postaji\u0107", 
    "Set a new password": "Nowe hes\u0142o postaji\u0107", 
    "Settings": "Nastajenja", 
    "Short Bio": "Kr\u00f3tki \u017eiwjenjob\u011bh", 
    "Show": "Pokaza\u0107", 
    "Show disabled": "Znjem\u00f3\u017enjene pokaza\u0107", 
    "Sign In": "P\u0159izjewi\u0107", 
    "Sign In With %s": "P\u0159izjewjenje z %s", 
    "Sign In With...": "P\u0159izjewi\u0107 z...", 
    "Sign Up": "Registrowa\u0107", 
    "Sign in as an existing user": "P\u0159izjew so jako eksistowacy wu\u017eiwar", 
    "Sign up as a new user": "Registruj so jako nowy wu\u017eiwar", 
    "Signed in. Redirecting...": "P\u0159izjewjeny. Sposr\u011bdkuje so dale...", 
    "Signing in with an external service for the first time will automatically create an account for you.": "Hdy\u017e so pr\u011bni raz z eksternej s\u0142u\u017ebu p\u0159izjewje\u0107e, so awtomatisce konto za was za\u0142o\u017ei.", 
    "Similar translations": "Podobne p\u0159e\u0142o\u017eki", 
    "Social Services": "Socialne s\u0142u\u017eby", 
    "Social Verification": "Socialne p\u0159epruwowanje", 
    "Source Language": "\u017d\u00f3r\u0142owa r\u011b\u010d", 
    "Special Characters": "Wosebite znamje\u0161ka", 
    "String Errors Contact": "Kontakt za zmylki w znamje\u0161kowych rje\u0107azkach", 
    "Suggested": "Namjetowany", 
    "Team": "Team", 
    "The password reset link was invalid, possibly because it has already been used. Please request a new password reset.": "Wotkaz za wr\u00f3\u0107ostajenje hes\u0142a b\u011b njep\u0142a\u0107iwy, snano dokel\u017e je so hi\u017eo wu\u017ei\u0142. Pro\u0161u pro\u0161 wo nowe wr\u00f3\u0107ostajenje hes\u0142a.", 
    "The server seems down. Try again later.": "Zda so, zo serwer je spadnjeny. Spytaj\u0107e pozd\u017ai\u0161o hi\u0161\u0107e raz.", 
    "There are unsaved changes. Do you want to discard them?": "Su njesk\u0142adowane zm\u011bny. Chce\u0161 je za\u0107isny\u0107?", 
    "There is %(count)s language.": [
      "Je %(count)s r\u011b\u010d.", 
      "Stej %(count)s r\u011b\u010di. Deleka su te, kotre\u017e su so njedawno p\u0159idali.", 
      "Su %(count)s r\u011b\u010de. Deleka su te, kotre\u017e su so njedawno p\u0159idali.", 
      "Je %(count)s r\u011b\u010dow. Deleka su te, kotre\u017e su so njedawno p\u0159idali."
    ], 
    "There is %(count)s project.": [
      "Je %(count)s projekt.", 
      "Stej %(count)s projektaj. Deleka su te, kotre\u017e su njedawno p\u0159idali.", 
      "Su %(count)s projekty. Deleka su te, kotre\u017e su njedawno p\u0159idali.", 
      "Je %(count)s projektow. Deleka su te, kotre\u017e su njedawno p\u0159idali."
    ], 
    "There is %(count)s user.": [
      "Je %(count)s wu\u017eiwar.", 
      "Stej %(count)s wu\u017eiwarjej. Deleka su njedawno p\u0159ida\u0107i.", 
      "Su %(count)s wu\u017eiwarjo. Deleka su njedawno p\u0159ida\u0107i.", 
      "Je %(count)s wu\u017eiwarjow. Deleka su njedawno p\u0159ida\u0107i."
    ], 
    "This email confirmation link expired or is invalid.": "Tut\u00f3n e-mejlowy wobkru\u0107enski wotkaz je spadnjeny abo njep\u0142a\u0107iwy.", 
    "This string no longer exists.": "Tut\u00f3n znamje\u0161kowy rje\u0107azk hi\u017eo njeeksistuje.", 
    "To set or change your avatar for your email address (%(email)s), please go to gravatar.com.": "Zo by sw\u00f3j awatar za swoju e-mejlowu adresu (%(email)s) nastaji\u0142 abo zm\u011bni\u0142, d\u017ai na gravatar.com.", 
    "Translated": "P\u0159e\u0142o\u017eeny", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project": "P\u0159e\u0142o\u017eeny wot %(fullname)s w projek\u0107e \u201c<span title=\"%(path)s\">%(project)s</span>\u201d", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project %(time_ago)s": "P\u0159e\u0142o\u017eeny wot %(fullname)s w projek\u0107e \u201c<span title=\"%(path)s\">%(project)s</span>\u201d %(time_ago)s", 
    "Try again": "Hi\u0161\u0107e raz spyta\u0107", 
    "Twitter": "Twitter", 
    "Twitter username": "Wu\u017eiwarske mjeno Twitter", 
    "Type to search": "Pisaj, zo by pyta\u0142", 
    "Updating data": "Aktualizowanje datow", 
    "Use the search form to find the language, then click on a language to edit.": "Wu\u017eiwaj pytanski formular, zo by r\u011b\u010d namaka\u0142 a klik\u0144 potom na r\u011b\u010d, kotru\u017e chce\u0161 wobd\u017a\u011b\u0142a\u0107.", 
    "Use the search form to find the project, then click on a project to edit.": "Wu\u017eiwaj pytanski formular, zo by projekt namaka\u0142 a klik\u0144 potom na projekt, kotry\u017e chce\u0161 wobd\u017a\u011b\u0142a\u0107.", 
    "Use the search form to find the user, then click on a user to edit.": "Wu\u017eiwaj pytanski formular, zo by wu\u017eiwarja namaka\u0142 a klik\u0144 potom na wu\u017eiwarja, kotreho\u017e chce\u0161 wobd\u017a\u011b\u0142a\u0107.", 
    "Username": "Wu\u017eiwarske mjeno", 
    "We found a user with <span>%(email)s</span> email in our system. Please provide the password to finish the sign in procedure. This is a one-off procedure, which will establish a link between your Pootle and %(provider)s accounts.": "Smy wu\u017eiwarja z e-mejlowej adresu <span>%(email)s</span> w swojim systemje namakali. Pro\u0161u podaj hes\u0142o, zo by p\u0159izjewjensku proceduru dok\u00f3n\u010di\u0142. To je j\u00f3nkr\u00f3\u0107na procedura, kotra\u017e wotkaz mjez wa\u0161imaj kontomaj Pootle a %(provider)s wutwori.", 
    "We have sent an email containing the special link to <span>%s</span>": "Smy e-mejlku p\u00f3s\u0142ali, kotra\u017e specialny wotkaz k <span>%s</span> wobsahuje", 
    "We have sent an email containing the special link to <span>%s</span>. Please check your spam folder if you do not see the email.": "Smy e-mejlku p\u00f3s\u0142ali, kotra\u017e wosebity wotkaz na <span>%s</span> wobsahuje. Pro\u0161u hladaj do swojeho spamoweho rjadowaka, jeli e-mejlku njewid\u017ai\u0161.", 
    "We have sent an email containing the special link to the address used to register this account. Please check your spam folder if you do not see the email.": "Smy e-mejlku p\u00f3s\u0142ali, kotra\u017e wotkaz na adresu wobsahuje, kotra\u017e so za registrowanje tutoho konta wu\u017eiwa. Pro\u0161u hladaj do swojeho spamoweho rjadowaka, jeli e-mejlku njewid\u017ai\u0161.", 
    "Website": "Websyd\u0142o", 
    "Why are you part of our translation project? Describe yourself, inspire others!": "\u010cehodla sy d\u017a\u011bl na\u0161eho p\u0159e\u0142o\u017eowanskeho projekta? Wopisaj so, inspiruj druhich!", 
    "Yes": "Haj", 
    "You have unsaved changes in this string. Navigating away will discard those changes.": "Sy njesk\u0142adowane zm\u011bny w tutym znamje\u0161kowym rje\u0107azku. Hdy\u017e pre\u010d nawiguje\u0161, so tute zm\u011bny zhubja.", 
    "Your Full Name": "Twoje dopo\u0142ne mjeno", 
    "Your LinkedIn profile URL": "URL twojeho profila LinkedIn", 
    "Your Personal website/blog URL": "URL twojeho wosobinskeho websyd\u0142a/bloga", 
    "Your Twitter username": "Twoje wu\u017eiwarske mjeno Twitter", 
    "Your account is inactive because an administrator deactivated it.": "Wa\u0161e konto je inaktiwne, dokel\u017e administrator je jo deaktiwizowa\u0142.", 
    "Your account needs activation.": "Twoje konto sej aktiwizowanje wu\u017eaduje.", 
    "disabled": "znjem\u00f3\u017enjeny", 
    "some anonymous user": "anonymny wu\u017eiwar", 
    "someone": "n\u011bcht\u00f3"
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

