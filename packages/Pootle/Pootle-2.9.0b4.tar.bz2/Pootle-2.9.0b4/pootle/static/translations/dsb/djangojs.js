

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
      "%(count)s r\u011bc w\u00f3tpow\u011bdujo wa\u0161omu nap\u0161a\u0161owanjeju.", 
      "%(count)s r\u011bcy w\u00f3tpow\u011bdujotej wa\u0161omu nap\u0161a\u0161owanjeju.", 
      "%(count)s r\u011bcy w\u00f3tpow\u011bduju wa\u0161omu nap\u0161a\u0161owanjeju.", 
      "%(count)s r\u011bcow w\u00f3tpow\u011bdujo wa\u0161omu nap\u0161a\u0161owanjeju."
    ], 
    "%(count)s project matches your query.": [
      "%(count)s projekt w\u00f3tpow\u011bdujo tw\u00f3jomu nap\u0161a\u0161owanjeju.", 
      "%(count)s projekta w\u00f3tpow\u011bdujotej tw\u00f3jomu nap\u0161a\u0161owanjeju.", 
      "%(count)s projekty w\u00f3tpow\u011bduju tw\u00f3jomu nap\u0161a\u0161owanjeju.", 
      "%(count)s projektow w\u00f3tpow\u011bdujo tw\u00f3jomu nap\u0161a\u0161owanjeju."
    ], 
    "%(count)s user matches your query.": [
      "%(count)s wu\u017eywa\u0155 w\u00f3tpow\u011bdujo tw\u00f3jomu nap\u0161a\u0161owanjeju.", 
      "%(count)s wu\u017eywarja w\u00f3tpow\u011bdujotej tw\u00f3jomu nap\u0161a\u0161owanjeju.", 
      "%(count)s wu\u017eywarje w\u00f3tpow\u011bduju tw\u00f3jomu nap\u0161a\u0161owanjeju.", 
      "%(count)s wu\u017eywarjow w\u00f3tpow\u011bdujo tw\u00f3jomu nap\u0161a\u0161owanjeju."
    ], 
    "%(timeSince)s via file upload": "%(timeSince)s p\u015bez datajowe nagra\u015be", 
    "%s word": [
      "%s s\u0142owo", 
      "%s s\u0142owje", 
      "%s s\u0142owa", 
      "%s s\u0142owow"
    ], 
    "%s's accepted suggestions": "akcept\u011browane nara\u017aenja wu\u017eywarja %s", 
    "%s's overwritten submissions": "zm\u011bnjone zap\u00f3da\u015ba wu\u017eywarja %s", 
    "%s's pending suggestions": "cakajuce nara\u017aenja wu\u017eywarja %s", 
    "%s's rejected suggestions": "w\u00f3tpokazane nara\u017aenja wu\u017eywarja %s", 
    "%s's submissions": "zap\u00f3da\u015ba wu\u017eywarja %s", 
    "Accept": "Akcept\u011browa\u015b", 
    "Account Activation": "Aktiw\u011browanje konta", 
    "Account Inactive": "Konto jo inaktiwne", 
    "Active": "Aktiwny", 
    "Add Language": "R\u011bc p\u015bida\u015b", 
    "Add Project": "Projekt p\u015bida\u015b", 
    "Add User": "Wu\u017eywarja p\u015bida\u015b", 
    "Administrator": "Administrator", 
    "After changing your password you will sign in automatically.": "Za tym a\u017e sy sw\u00f3jo gronid\u0142o zm\u011bni\u0142, se awtomatiski p\u015bizjawijo\u0161.", 
    "All Languages": "W\u0161e r\u011bcy", 
    "All Projects": "W\u0161e projekty", 
    "An error occurred while attempting to sign in via %s.": "P\u015bi wopy\u015be se p\u015bez %s p\u015bizjawi\u015b, jo zm\u00f3lka nasta\u0142a.", 
    "An error occurred while attempting to sign in via your social account.": "P\u015bi wopy\u015be se p\u015bez wa\u0161o socialne konto p\u015bizjawi\u015b, jo zm\u00f3lka nasta\u0142a.", 
    "Avatar": "Awatar", 
    "Cancel": "P\u015betergnu\u015b", 
    "Clear all": "Wsykno wula\u0161owa\u015b", 
    "Clear value": "G\u00f3dnotu wula\u0161owa\u015b", 
    "Close": "Zacyni\u015b", 
    "Code": "Kod", 
    "Collapse details": "Drobnostki schowa\u015b", 
    "Congratulations! You have completed this task!": "Gluku\u017eycenje! Sy to\u015b ten nadawk dok\u00f3\u0144cy\u0142!", 
    "Contact Us": "Staj se z nami do zwiska", 
    "Contributors, 30 Days": "P\u015binosowarje, 30 dnjow", 
    "Creating new user accounts is prohibited.": "Za\u0142o\u017eenje nowych wu\u017eywarskich kontow jo zakazane.", 
    "Delete": "La\u0161owa\u015b", 
    "Deleted successfully.": "Wusp\u011b\u0161nje wula\u0161owany.", 
    "Didn't receive an email? Check if it was accidentally filtered out as spam, or try requesting another copy of the email.": "Njejsy mejlku dosta\u0142? Kontrol\u011bruj, l\u011bc jo se z p\u015big\u00f3dy ako spam wufiltrowa\u0142a, abo pominaj dal\u0161nu kopiju mejlki.", 
    "Disabled": "Znjem\u00f3\u017enjony", 
    "Discard changes.": "Zm\u011bny zachy\u015bi\u015b.", 
    "Edit Language": "R\u011bc wob\u017a\u011b\u0142a\u015b", 
    "Edit My Public Profile": "M\u00f3j zjawny profil wob\u017a\u011b\u0142a\u015b", 
    "Edit Project": "Projekt wob\u017a\u011b\u0142a\u015b", 
    "Edit User": "Wu\u017eywarja wob\u017a\u011b\u0142a\u015b", 
    "Edit the suggestion before accepting, if necessary": "Wob\u017a\u011b\u0142aj nara\u017aenje, nje\u017eli a\u017e jo akcept\u011brujo\u0161, jolic trjeba", 
    "Email": "E-mail", 
    "Email Address": "E-mailowa adresa", 
    "Email Confirmation": "E-mailowe wobk\u0161u\u015benje", 
    "Enter your email address, and we will send you a message with the special link to reset your password.": "Zap\u00f3daj sw\u00f3ju e-mailowu adresu a my p\u00f3s\u0107elomy wam pow\u011bs\u0107 ze specialnym w\u00f3tkazom za sl\u011bdkstajenje tw\u00f3jogo gronid\u0142a.", 
    "Error while connecting to the server": "Zm\u00f3lka p\u015bi zw\u011bzowanju ze serwerom", 
    "Expand details": "Drobnostki pokaza\u015b", 
    "File types": "Datajowe typy", 
    "Filesystems": "Datajowe systemy", 
    "Find language by name, code": "R\u011bc p\u00f3 mjenju abo ko\u017ae pyta\u015b", 
    "Find project by name, code": "Projekt p\u00f3 mjenju abo ko\u017ae pyta\u015b", 
    "Find user by name, email, properties": "Wu\u017eywarja p\u00f3 mjenju, e-mail abo kakos\u0107ach pyta\u015b", 
    "Full Name": "Dopo\u0142ne m\u011b", 
    "Go back to browsing": "Rozgl\u011bduj se dalej", 
    "Go to the next string (Ctrl+.)<br/><br/>Also:<br/>Next page: Ctrl+Shift+.<br/>Last page: Ctrl+Shift+End": "\u0179i k p\u015biducemu znamu\u0161kowemu rje\u015bazkoju (Str+.)<br/><br/>Teke:<br/>P\u015biducy bok: Strg+Umsch+.<br/>Sl\u011bdny bok: Strg+Umsch+Ende", 
    "Go to the previous string (Ctrl+,)<br/><br/>Also:<br/>Previous page: Ctrl+Shift+,<br/>First page: Ctrl+Shift+Home": "\u0179i k pjerwjej\u0161nemu znamu\u0161kowemu rje\u015bazkoju (Str+,)<br/><br/>Teke:<br/>Pjerwjej\u0161ny bok: Strg+Umsch+,<br/>Pr\u011bdny bok: Strg+Umsch+Pos1", 
    "Hide": "Schowa\u015b", 
    "Hide disabled": "Znjem\u00f3\u017enjone schowa\u015b", 
    "I forgot my password": "Som sw\u00f3jo gronid\u0142o zaby\u0142", 
    "Ignore Files": "Dataje ignor\u011browa\u015b", 
    "Languages": "R\u011bcy", 
    "Less": "Mjenjej", 
    "LinkedIn": "LinkedIn", 
    "LinkedIn profile URL": "Profilowy URL LinkedIn", 
    "Load More": "Dal\u0161ne zacyta\u015b", 
    "Loading...": "Zacytujo se...", 
    "Login / Password": "P\u015bizjawjenje / Gronid\u0142o", 
    "More": "W\u011bcej", 
    "More...": "W\u011bcej...", 
    "My Public Profile": "M\u00f3j zjawny profil", 
    "No": "N\u011b", 
    "No activity recorded in a given period": "\u017dedna aktiwita njejo se w danej dobje zw\u011bs\u0107i\u0142a", 
    "No results found": "\u017dedne wusl\u011bdki namakane", 
    "No results.": "\u017dedne wusl\u011bdki.", 
    "No, thanks": "N\u011b, \u017a\u011bkujom se", 
    "Not found": "Njenamakany", 
    "Note: when deleting a user their contributions to the site, e.g. comments, suggestions and translations, are attributed to the anonymous user (nobody).": "Gl\u011bdaj: ga\u017e se wu\u017eywa\u0155 wula\u0161ujo, p\u015bipoka\u017eu se jogo p\u015binoski za sed\u0142o, na p\u015b. komentary, nara\u017aenja a p\u015be\u0142o\u017eki, anonymnemu wu\u017eywarjeju (nikomu).", 
    "Number of Plurals": "Licba pluralow", 
    "Oops...": "Hopla...", 
    "Overview": "P\u015begl\u011bd", 
    "Password": "Gronid\u0142o", 
    "Password changed, signing in...": "Gronid\u0142o zm\u011bnjone, p\u0159izjewja so...", 
    "Permissions": "P\u0161awa", 
    "Personal description": "W\u00f3sobinske wopisanje", 
    "Personal website URL": "URL w\u00f3sobinskego websed\u0142a", 
    "Please follow that link to continue the account creation.": "P\u0161osym sl\u011bduj to\u015b tomu w\u00f3tkazoju, aby ze za\u0142o\u017eowanim konta p\u00f3k\u0161acowa\u0142.", 
    "Please follow that link to continue the password reset procedure.": "P\u0161osym sl\u011bduj w\u00f3tkazoju, aby z proceduru sl\u011bdkstajenja gronid\u0142a.", 
    "Please select a valid user.": "P\u0161osym wubje\u0155 p\u0142a\u015biwego wu\u017eywarja.", 
    "Plural Equation": "Pluralowa formula", 
    "Plural form %(index)s": "Pluralowa forma %(index)s", 
    "Preview will be displayed here.": "P\u015begl\u011bd se how poka\u017eo.", 
    "Project / Language": "Projekt / R\u011bc", 
    "Project Tree Style": "Stil projektowego boma", 
    "Provide optional comment (will be publicly visible)": "Pi\u0161\u0107o komentar (bu\u017ao zjawnje widobny)", 
    "Public Profile": "Zjawny profil", 
    "Quality Checks": "Kwalitne kontrole", 
    "Reject": "W\u00f3tpokaza\u015b", 
    "Reload page": "Bok znowego zacyta\u015b", 
    "Repeat Password": "Gronid\u0142o w\u00f3spjetowa\u015b", 
    "Resend Email": "Mejlku hy\u0161\u0107i raz p\u00f3s\u0142a\u015b", 
    "Reset Password": "Gronid\u0142o sl\u011bdk staji\u015b", 
    "Reset Your Password": "Wa\u0161o gronid\u0142o sl\u011bdk staji\u015b", 
    "Reviewed": "P\u00f3g\u00f3dno\u015bony", 
    "Save": "Sk\u0142adowa\u015b", 
    "Saved successfully.": "Wusp\u011b\u0161nje sk\u0142a\u017aony.", 
    "Score Change": "Staw dypkow", 
    "Screenshot Search Prefix": "Prefiks za pytanje za fotami wobrazowki", 
    "Search Languages": "R\u011bcy p\u015bepyta\u015b", 
    "Search Projects": "Projekty p\u015bepytowa\u015b", 
    "Search Users": "Wu\u017eywarje p\u015bepytowa\u015b", 
    "Select...": "Wubra\u015b...", 
    "Send Email": "Mejlku p\u00f3s\u0142a\u015b", 
    "Sending email to %s...": "Mejlka se na %s s\u0107elo...", 
    "Server error": "Serwerowa zm\u00f3lka", 
    "Set New Password": "Nowe gronid\u0142o nastaji\u015b", 
    "Set a new password": "Nowe gronid\u0142o nastaji\u015b", 
    "Settings": "Nastajenja", 
    "Short Bio": "Krotki \u017eywjenjob\u011bg", 
    "Show": "Pokaza\u015b", 
    "Show disabled": "Znjem\u00f3\u017enjone pokaza\u015b", 
    "Sign In": "P\u015bizjawi\u015b", 
    "Sign In With %s": "Z %s p\u015bizjawi\u015b", 
    "Sign In With...": "P\u015bizjawi\u015b z...", 
    "Sign Up": "Registr\u011browa\u015b", 
    "Sign in as an existing user": "P\u015bizjaw se ako eksist\u011brujucy wu\u017eywa\u0155", 
    "Sign up as a new user": "Ako nowy wu\u017eywa\u0155 registr\u011browa\u015b", 
    "Signed in. Redirecting...": "P\u015bizjawjony. P\u00f3sr\u011bdnja so dalej...", 
    "Signing in with an external service for the first time will automatically create an account for you.": "Ga\u017e se pr\u011bdny raz z eksterneju s\u0142u\u017ebu p\u015bizjawijo\u015bo, se awtomatiski konto za was za\u0142o\u017eijo.", 
    "Similar translations": "P\u00f3dobne p\u015be\u0142o\u017eki", 
    "Social Services": "Socialne s\u0142u\u017eby", 
    "Social Verification": "Socialne p\u015bespytanje", 
    "Source Language": "\u017dr\u011bd\u0142owa r\u011bc", 
    "Special Characters": "W\u00f3sebne znamu\u0161ka", 
    "String Errors Contact": "Kontakt za zm\u00f3lki w znamu\u0161kowych rje\u015bazkach", 
    "Suggested": "Nara\u017aony", 
    "Team": "Team", 
    "The password reset link was invalid, possibly because it has already been used. Please request a new password reset.": "W\u00f3tkaz za sl\u011bdkstajenje gronid\u0142a jo njep\u0142a\u015biwy by\u0142, sna\u017a dokula\u017e jo se ju\u017eo wu\u017ey\u0142. P\u0161osym p\u0161os w\u00f3 nowe sl\u011bdkstajenje gronid\u0142a.", 
    "The server seems down. Try again later.": "Zda so, a\u017e serwer jo se wowali\u0142. Wopytaj p\u00f3zd\u017aej hy\u0161\u0107i raz.", 
    "There are unsaved changes. Do you want to discard them?": "Su njesk\u0142a\u017aone zm\u011bny. Co\u0161 je zachy\u015bi\u015b?", 
    "There is %(count)s language.": [
      "Jo %(count)s r\u011bc.", 
      "Stej %(count)s r\u011bcy. Do\u0142ojce su njedawno p\u015bidane.", 
      "Su %(count)s r\u011bcy. Do\u0142ojce su njedawno p\u015bidane.", 
      "Jo %(count)s r\u011bcow. Do\u0142ojce su njedawno p\u015bidane."
    ], 
    "There is %(count)s project.": [
      "Jo %(count)s projekt.", 
      "Stej %(count)s projekta. Do\u0142ojce su te, k\u00f3tare\u017e su njedawno p\u015bidali.", 
      "Su %(count)s projekty. Do\u0142ojce su te, k\u00f3tare\u017e su njedawno p\u015bidali.", 
      "Jo %(count)s projektow. Do\u0142ojce su te, k\u00f3tare\u017e su njedawno p\u015bidali."
    ], 
    "There is %(count)s user.": [
      "Jo %(count)s wu\u017eywa\u0155.", 
      "Stej %(count)s wu\u017eywarja. Do\u0142ojce su njedawno p\u015bidane.", 
      "Su %(count)s wu\u017eywarje. Do\u0142ojce su njedawno p\u015bidane.", 
      "Jo %(count)s wu\u017eywarjow. Do\u0142ojce su njedawno p\u015bidane."
    ], 
    "This email confirmation link expired or is invalid.": "To\u015b ten e-mailowy wobk\u0161u\u015be\u0144ski w\u00f3tkaz jo spadnjony abo njep\u0142a\u015biwy.", 
    "This string no longer exists.": "To\u015b ten znamu\u0161kowy rje\u015bazk w\u011bcej njeeksist\u011brujo.", 
    "To set or change your avatar for your email address (%(email)s), please go to gravatar.com.": "Aby sw\u00f3j awatar za sw\u00f3ju e-mailowu adresu (%(email)s) nastaji\u0142 abo zm\u011bni\u0142, \u017ai na gravatar.com.", 
    "Translated": "P\u015be\u0142o\u017eony", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project": "P\u015be\u0142o\u017eony w\u00f3t %(fullname)s w projek\u015be \u201c<span title=\"%(path)s\">%(project)s</span>\u201d", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project %(time_ago)s": "P\u015be\u0142o\u017eony w\u00f3t %(fullname)s w projek\u015be \u201c<span title=\"%(path)s\">%(project)s</span>\u201d %(time_ago)s", 
    "Try again": "Hy\u0161\u0107i raz wopyta\u015b", 
    "Twitter": "Twitter", 
    "Twitter username": "Wu\u017eywarske m\u011b Twitter", 
    "Type to search": "Pi\u0161\u0107o, aby pyta\u0142", 
    "Updating data": "Daty se aktualiz\u011bruju", 
    "Use the search form to find the language, then click on a language to edit.": "Wu\u017eywaj pyta\u0144ski formular, aby r\u011bc namaka\u0142 a klikni p\u00f3tom na r\u011bc, k\u00f3taru\u017e co\u0161 wob\u017a\u011b\u0142a\u015b.", 
    "Use the search form to find the project, then click on a project to edit.": "Wu\u017eywaj pyta\u0144ski formular, aby projekt namaka\u0142 a klikni p\u00f3tom na projekt, k\u00f3tary\u017e co\u0161 wob\u017a\u011b\u0142a\u015b.", 
    "Use the search form to find the user, then click on a user to edit.": "Wu\u017eywaj pyta\u0144ski formular, aby wu\u017eywarja namaka\u0142 a klikni p\u00f3tom na wu\u017eywarja, k\u00f3tarego\u017e co\u0161 wob\u017a\u011b\u0142a\u015b.", 
    "Username": "Wu\u017eywarske m\u011b", 
    "We found a user with <span>%(email)s</span> email in our system. Please provide the password to finish the sign in procedure. This is a one-off procedure, which will establish a link between your Pootle and %(provider)s accounts.": "Smy namakali wu\u017eywarja z e-mailoweju adresu <span>%(email)s</span> w sw\u00f3jom systemje. P\u0161osym p\u00f3daj gronid\u0142o, aby p\u015bizjewje\u0144sku proceduru dok\u00f3\u0144cy\u0142. To jo jadnorazowa procedura, k\u00f3tara\u017e w\u00f3tkaz mjazy wa\u0161yma kontoma Pootle a %(provider)s nap\u00f3rajo.", 
    "We have sent an email containing the special link to <span>%s</span>": "Smy mejlku p\u00f3s\u0142ali, k\u00f3tara\u017e specialny w\u00f3tkaz k <span>%s</span> wobp\u015bimujo", 
    "We have sent an email containing the special link to <span>%s</span>. Please check your spam folder if you do not see the email.": "Smy mejlku p\u00f3s\u0142ali, k\u00f3tara\u017e wop\u015bimujo w\u00f3sebny w\u00f3tkaz na <span>%s</span>. P\u0161osym gl\u011bdaj do sw\u00f3jogo spamowego zar\u011bdnika, jolic njewi\u017ai\u015b mejlku.", 
    "We have sent an email containing the special link to the address used to register this account. Please check your spam folder if you do not see the email.": "Smy mejlku p\u00f3s\u0142ali, k\u00f3tara\u017e wop\u015bimujo w\u00f3tkaz na adresu, k\u00f3tara\u017e wu\u017eywa se za registr\u011browanje to\u015b togo konta. P\u0161osym gl\u011bdaj do sw\u00f3jogo spamowego zar\u011bdnika, jolic njewi\u017ai\u0161 mejlku.", 
    "Website": "Websed\u0142o", 
    "Why are you part of our translation project? Describe yourself, inspire others!": "Cogodla sy \u017a\u011bl na\u0161ogo p\u015be\u0142o\u017eowa\u0144skego projekta? Wopi\u0161 se, inspir\u011bruj druge!", 
    "Yes": "Jo", 
    "You have unsaved changes in this string. Navigating away will discard those changes.": "Sy njesk\u0142a\u017aone zm\u011bny w to\u015b tom znamu\u0161kowym rje\u015bazku. Ga\u017e p\u0161ec nawig\u011brujo\u0161, se to\u015b te zm\u011bny zgubiju.", 
    "Your Full Name": "Tw\u00f3jo dopo\u0142ne m\u011b", 
    "Your LinkedIn profile URL": "URL tw\u00f3jogo profila LinkedIn", 
    "Your Personal website/blog URL": "URL tw\u00f3jogo w\u00f3sobinskego websed\u0142a/bloga", 
    "Your Twitter username": "Tw\u00f3jo wu\u017eywarske m\u011b Twitter", 
    "Your account is inactive because an administrator deactivated it.": "Wa\u0161o konto jo inaktiwne, dokula\u017e administrator jo jo deaktiw\u011browa\u0142.", 
    "Your account needs activation.": "Tw\u00f3jo konto pomina se aktiw\u011browanje.", 
    "disabled": "znjem\u00f3\u017enjony", 
    "some anonymous user": "anonymny wu\u017eywa\u0155", 
    "someone": "n\u011bchten"
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

