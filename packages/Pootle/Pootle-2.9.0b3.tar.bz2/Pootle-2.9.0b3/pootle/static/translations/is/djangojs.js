

(function(globals) {

  var django = globals.django || (globals.django = {});

  
  django.pluralidx = function(n) {
    var v=(n%10!=1 || n%100==11);
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
      "%(count)s tungum\u00e1l samsvarar fyrirspurn \u00feinni.", 
      "%(count)s tungum\u00e1l samsvara fyrirspurn \u00feinni."
    ], 
    "%(count)s project matches your query.": [
      "%(count)s verkefni samsvarar fyrirspurn \u00feinni.", 
      "%(count)s verkefni samsvara fyrirspurn \u00feinni."
    ], 
    "%(count)s user matches your query.": [
      "%(count)s notandi samsvarar fyrirspurn \u00feinni.", 
      "%(count)s notendur samsvara fyrirspurn \u00feinni."
    ], 
    "%(timeSince)s via file upload": "%(timeSince)s me\u00f0 innsendri skr\u00e1", 
    "%s word": [
      "%s or\u00f0", 
      "%s or\u00f0"
    ], 
    "%s's accepted suggestions": "%s vi\u00f0urkenndar upp\u00e1stungur", 
    "%s's overwritten submissions": "%s yfirskrifa\u00f0ar upp\u00e1stungur", 
    "%s's pending suggestions": "%s \u00f3kl\u00e1ra\u00f0ar upp\u00e1stungur", 
    "%s's rejected suggestions": "%s upp\u00e1stungum sem hefur veri\u00f0 hafna\u00f0", 
    "%s's submissions": "%s upp\u00e1stungur", 
    "Accept": "Sam\u00feykkja", 
    "Account Activation": "Virkjun a\u00f0gangs", 
    "Account Inactive": "A\u00f0gangur er \u00f3virkur", 
    "Active": "Virkt", 
    "Add Language": "B\u00e6ta vi\u00f0 tungum\u00e1li", 
    "Add Project": "B\u00e6ta vi\u00f0 verkefni", 
    "Add User": "B\u00e6ta vi\u00f0 notanda", 
    "Administrator": "Kerfisstj\u00f3ri", 
    "After changing your password you will sign in automatically.": "Eftir a\u00f0 lykilor\u00f0inu hefur veri\u00f0 breytt ver\u00f0ur\u00f0u sj\u00e1lfvirkt skr\u00e1\u00f0/ur inn.", 
    "All Languages": "\u00d6ll tungum\u00e1l", 
    "All Projects": "\u00d6ll verkefni", 
    "An error occurred while attempting to sign in via %s.": "\u00d3v\u00e6nt villa kom upp \u00feegar reynt var a\u00f0 skr\u00e1 inn me\u00f0 %s.", 
    "An error occurred while attempting to sign in via your social account.": "\u00d3v\u00e6nt villa kom upp \u00feegar reynt var a\u00f0 skr\u00e1 inn me\u00f0 a\u00f0gangi \u00e1 samf\u00e9lagsmi\u00f0li.", 
    "Avatar": "Au\u00f0kennismynd", 
    "Cancel": "H\u00e6tta vi\u00f0", 
    "Clear all": "Hreinsa allt", 
    "Clear value": "Hreinsa gildi", 
    "Close": "Loka", 
    "Code": "K\u00f3\u00f0i", 
    "Collapse details": "Loka sm\u00e1atri\u00f0um", 
    "Congratulations! You have completed this task!": "Til hamingju, \u00fe\u00fa hefur loki\u00f0 \u00feessu verki!", 
    "Contact Us": "Haf\u00f0u samband vi\u00f0 okkur", 
    "Contributors, 30 Days": "\u00de\u00e1tttakendur, 30 dagar", 
    "Creating new user accounts is prohibited.": "Banna\u00f0 er a\u00f0 b\u00faa til n\u00fdja notendaa\u00f0ganga.", 
    "Delete": "Ey\u00f0a", 
    "Deleted successfully.": "T\u00f3kst a\u00f0 ey\u00f0a.", 
    "Didn't receive an email? Check if it was accidentally filtered out as spam, or try requesting another copy of the email.": "F\u00e9kkstu ekki t\u00f6lvup\u00f3stinn? Athuga\u00f0u hvort hann hafi veri\u00f0 s\u00eda\u00f0ur \u00fat sem ruslp\u00f3stur, e\u00f0a pr\u00f3fa\u00f0u a\u00f0 bi\u00f0ja aftur um sendinguna.", 
    "Disabled": "\u00d3virkt", 
    "Discard changes.": "Henda breytingum.", 
    "Edit Language": "Breyta tungum\u00e1li", 
    "Edit My Public Profile": "Breyta opinberri notandas\u00ed\u00f0u minni", 
    "Edit Project": "Breyta verkefni", 
    "Edit User": "Breyta notanda", 
    "Edit the suggestion before accepting, if necessary": "Breyttu till\u00f6gunni \u00e1\u00f0ur en \u00fe\u00fa sam\u00feykkir hana, ef \u00feess er \u00fe\u00f6rf", 
    "Email": "T\u00f6lvup\u00f3stfang", 
    "Email Address": "T\u00f6lvup\u00f3stfang", 
    "Email Confirmation": "Sta\u00f0festing \u00ed t\u00f6lvup\u00f3sti", 
    "Enter your email address, and we will send you a message with the special link to reset your password.": "Sl\u00e1\u00f0u inn netfangi\u00f0 sem \u00fe\u00fa skr\u00e1\u00f0ir \u00feig me\u00f0, vi\u00f0 munum senda tengil \u00e1 \u00fea\u00f0 sem \u00fe\u00fa getur nota\u00f0 til a\u00f0 breyta lykilor\u00f0inu \u00fe\u00ednu.", 
    "Error while connecting to the server": "Villa vi\u00f0 a\u00f0 tengjast \u00fej\u00f3ni", 
    "Expand details": "Birta sm\u00e1atri\u00f0i", 
    "File types": "Skr\u00e1ategundir", 
    "Filesystems": "Skr\u00e1akerfi", 
    "Find language by name, code": "Finna tungum\u00e1l eftir nafni, k\u00f3\u00f0a", 
    "Find project by name, code": "Finna verkefni eftir nafni, k\u00f3\u00f0a", 
    "Find user by name, email, properties": "Finndu notanda eftir nafni, t\u00f6lvup\u00f3stfangi, eiginleikum", 
    "Full Name": "Fullt nafn", 
    "Go back to browsing": "Fara aftur \u00ed vafur", 
    "Go to the next string (Ctrl+.)<br/><br/>Also:<br/>Next page: Ctrl+Shift+.<br/>Last page: Ctrl+Shift+End": "Fara \u00e1 n\u00e6sta streng (Ctrl+.)<br/><br/>Einnig:<br/>N\u00e6sta s\u00ed\u00f0a: Ctrl+Shift+.<br/>S\u00ed\u00f0asta s\u00ed\u00f0a: Ctrl+Shift+End", 
    "Go to the previous string (Ctrl+,)<br/><br/>Also:<br/>Previous page: Ctrl+Shift+,<br/>First page: Ctrl+Shift+Home": "Fara \u00e1 fyrri streng (Ctrl+,)<br/><br/>Einnig:<br/>Fyrri s\u00ed\u00f0a: Ctrl+Shift+,<br/>Fyrsta s\u00ed\u00f0a: Ctrl+Shift+Home", 
    "Hide": "Fela", 
    "Hide disabled": "Fela \u00f3virkt", 
    "I forgot my password": "\u00c9g gleymdi lykilor\u00f0inu m\u00ednu", 
    "Ignore Files": "Hunsa skr\u00e1r", 
    "Languages": "Tungum\u00e1l", 
    "Less": "Minna", 
    "LinkedIn": "LinkedIn", 
    "LinkedIn profile URL": "Sl\u00f3\u00f0 \u00e1 LinkedIn notandasni\u00f0", 
    "Load More": "Hla\u00f0a inn meiru", 
    "Loading...": "Hle\u00f0 inn...", 
    "Login / Password": "Innskr\u00e1ning / Lykilor\u00f0", 
    "More": "Meira", 
    "More...": "Meira...", 
    "My Public Profile": "Opinber notandas\u00ed\u00f0a m\u00edn", 
    "No": "Nei", 
    "No activity recorded in a given period": "Engin virkni skr\u00e1\u00f0 \u00e1 uppgefnu t\u00edmabili", 
    "No results found": "Engar ni\u00f0urst\u00f6\u00f0ur fundust", 
    "No results.": "Engar ni\u00f0urst\u00f6\u00f0ur.", 
    "No, thanks": "Nei, takk", 
    "Not found": "Fannst ekki", 
    "Note: when deleting a user their contributions to the site, e.g. comments, suggestions and translations, are attributed to the anonymous user (nobody).": "Athuga\u00f0u: \u00feegar notanda er eytt ver\u00f0a \u00f6ll framl\u00f6g hans \u00e1 \u00feessum vef, \u00fe.e.a.s. athugasemdir, till\u00f6gur og \u00fe\u00fd\u00f0ingar, merkt sem fr\u00e1 nafnlausum notanda (nobody).", 
    "Number of Plurals": "Fleirt\u00f6lur", 
    "Oops...": "\u00dabbs...", 
    "Overview": "Yfirlit", 
    "Password": "Lykilor\u00f0", 
    "Password changed, signing in...": "Lykilor\u00f0i breytt, skr\u00e1i inn...", 
    "Permissions": "Heimildir", 
    "Personal description": "Pers\u00f3nul\u00fdsing", 
    "Personal website URL": "Sl\u00f3\u00f0 \u00e1 eigi\u00f0 vefsv\u00e6\u00f0i", 
    "Please follow that link to continue the account creation.": "Fylgdu \u00feessum tengli til a\u00f0 halda \u00e1fram me\u00f0 a\u00f0 stofna a\u00f0ganginn.", 
    "Please follow that link to continue the password reset procedure.": "Fylgdu \u00feessum tengli til a\u00f0 halda \u00e1fram me\u00f0 a\u00f0 endurstilla lykilor\u00f0i\u00f0.", 
    "Please select a valid user.": "Veldu einhvern gildan notanda.", 
    "Plural Equation": "Fleirt\u00f6lujafna", 
    "Plural form %(index)s": "Fleirt\u00f6luform %(index)s", 
    "Preview will be displayed here.": "Forsko\u00f0un mun birtast h\u00e9r.", 
    "Project / Language": "Verkefni / Tungum\u00e1l", 
    "Project Tree Style": "Greinast\u00edll verkefnis", 
    "Provide optional comment (will be publicly visible)": "Settu inn athugasemd ef \u00fe\u00fa vilt (ver\u00f0ur \u00f6llum s\u00fdnileg)", 
    "Public Profile": "Opinberar uppl\u00fdsingar", 
    "Quality Checks": "G\u00e6\u00f0apr\u00f3fanir", 
    "Reject": "Hafna", 
    "Reload page": "Endurlesa s\u00ed\u00f0u", 
    "Repeat Password": "Endurtaka lykilor\u00f0", 
    "Resend Email": "Endursenda t\u00f6lvup\u00f3st", 
    "Reset Password": "Endurstilla lykilor\u00f0", 
    "Reset Your Password": "Endurstilltu lykilor\u00f0i\u00f0 \u00feitt", 
    "Reviewed": "Yfirfari\u00f0", 
    "Save": "Vista", 
    "Saved successfully.": "T\u00f3kst a\u00f0 vista.", 
    "Score Change": "Breyting \u00e1 skori", 
    "Screenshot Search Prefix": "Leitarforskeyti skj\u00e1myndar", 
    "Search Languages": "Leita a\u00f0 tungum\u00e1li", 
    "Search Projects": "Leita a\u00f0 verkefni", 
    "Search Users": "Leita a\u00f0 notendum", 
    "Select...": "Velja...", 
    "Send Email": "Senda t\u00f6lvup\u00f3st", 
    "Sending email to %s...": "Sendi t\u00f6lvup\u00f3st til %s...", 
    "Server error": "Villa fr\u00e1 \u00fej\u00f3ni", 
    "Set New Password": "Stilla n\u00fdtt lykilor\u00f0", 
    "Set a new password": "Stilla n\u00fdtt lykilor\u00f0", 
    "Settings": "Stillingar", 
    "Short Bio": "Stutt \u00e6vi\u00e1grip", 
    "Show": "S\u00fdna", 
    "Show disabled": "Birta \u00f3virkt", 
    "Sign In": "Skr\u00e1 inn", 
    "Sign In With %s": "Skr\u00e1 inn me\u00f0 %s", 
    "Sign In With...": "Skr\u00e1 inn me\u00f0...", 
    "Sign Up": "Skr\u00e1 sig", 
    "Sign in as an existing user": "Skr\u00e1 inn sem \u00feegar skr\u00e1\u00f0ur notandi", 
    "Sign up as a new user": "Skr\u00e1 inn sem n\u00fdr notandi", 
    "Signed in. Redirecting...": "Skr\u00e1\u00f0ur inn. Endurbeini...", 
    "Signing in with an external service for the first time will automatically create an account for you.": "Fyrsta innskr\u00e1ning me\u00f0 ytri \u00fej\u00f3nustu mun b\u00faa til a\u00f0gang fyrir \u00feig.", 
    "Similar translations": "Svipa\u00f0ar \u00fe\u00fd\u00f0ingar", 
    "Social Services": "Samf\u00e9lagsmi\u00f0lar", 
    "Social Verification": "Sannvottun \u00e1 samf\u00e9lagsmi\u00f0li", 
    "Source Language": "Upprunatungum\u00e1l", 
    "Special Characters": "S\u00e9rt\u00e1kn", 
    "String Errors Contact": "Tengili\u00f0ur vegna villna \u00ed textastrengjum", 
    "Suggested": "Stungi\u00f0 upp\u00e1", 
    "Team": "Teymi", 
    "The password reset link was invalid, possibly because it has already been used. Please request a new password reset.": "Tengill fyrir a\u00f0 endurstilla lykilor\u00f0 var \u00f3gildur, l\u00edklega vegna \u00feess a\u00f0 \u00feegar er b\u00fai\u00f0 a\u00f0 nota hann. Vinsamlega n\u00e1\u00f0u \u00fe\u00e9r \u00ed a\u00f0ra bei\u00f0ni um endurstillingu \u00e1 lykilor\u00f0i.", 
    "The server seems down. Try again later.": "\u00dej\u00f3nninn vir\u00f0ist vera ni\u00f0ri. Vinsamlega reyndu s\u00ed\u00f0ar.", 
    "There are unsaved changes. Do you want to discard them?": "\u00dea\u00f0 eru \u00f3vista\u00f0ar breytingar. Viltu henda \u00feeim?", 
    "There is %(count)s language.": [
      "\u00dea\u00f0 er %(count)s tungum\u00e1l.", 
      "\u00dea\u00f0 eru %(count)s tungum\u00e1l."
    ], 
    "There is %(count)s project.": [
      "\u00dea\u00f0 er %(count)s verkefni.", 
      "\u00dea\u00f0 eru %(count)s verkefni."
    ], 
    "There is %(count)s user.": [
      "\u00dea\u00f0 er %(count)s notandi.", 
      "\u00dea\u00f0 eru %(count)s notendur. Fyrir ne\u00f0an eru \u00feeir sem s\u00ed\u00f0ast var b\u00e6tt vi\u00f0."
    ], 
    "This email confirmation link expired or is invalid.": "Tengill til sta\u00f0festingar me\u00f0 t\u00f6lvup\u00f3sti er \u00fatrunninn e\u00f0a \u00f3gildur.", 
    "This string no longer exists.": "\u00deessi strengur er ekki lengur til sta\u00f0ar.", 
    "To set or change your avatar for your email address (%(email)s), please go to gravatar.com.": "\u00de\u00fa getur stillt kennimyndina fyrir t\u00f6lvup\u00f3stfangi\u00f0 (%(email)s) \u00e1 gravatar.com.", 
    "Translated": "B\u00fai\u00f0 a\u00f0 \u00fe\u00fd\u00f0a", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project": "\u00de\u00fdtt af %(fullname)s \u00ed \u201c<span title=\"%(path)s\">%(project)s</span>\u201d verkefninu", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project %(time_ago)s": "\u00de\u00fdtt af %(fullname)s \u00ed \u201c<span title=\"%(path)s\">%(project)s</span>\u201d verkefninu fyrir %(time_ago)s s\u00ed\u00f0an", 
    "Try again": "Reyndu aftur", 
    "Twitter": "Twitter", 
    "Twitter username": "Twitter notandanafn", 
    "Type to search": "Skrifa\u00f0u til a\u00f0 leita...", 
    "Updating data": "Uppf\u00e6ri g\u00f6gn", 
    "Use the search form to find the language, then click on a language to edit.": "Nota\u00f0u leitarformi\u00f0 til a\u00f0 finna tungum\u00e1li\u00f0, smelltu s\u00ed\u00f0an \u00e1 heiti tungum\u00e1lsins til a\u00f0 breyta.", 
    "Use the search form to find the project, then click on a project to edit.": "Nota\u00f0u leitarformi\u00f0 til a\u00f0 finna verkefni\u00f0, smelltu s\u00ed\u00f0an \u00e1 heiti verkefnisins til a\u00f0 breyta.", 
    "Use the search form to find the user, then click on a user to edit.": "Nota\u00f0u leitarformi\u00f0 til a\u00f0 finna notandann, smelltu s\u00ed\u00f0an \u00e1 nafn notandans til a\u00f0 breyta.", 
    "Username": "Notandanafn", 
    "We found a user with <span>%(email)s</span> email in our system. Please provide the password to finish the sign in procedure. This is a one-off procedure, which will establish a link between your Pootle and %(provider)s accounts.": "Vi\u00f0 fundum notanda me\u00f0 t\u00f6lvup\u00f3stfangi\u00f0 <span>%(email)s</span> \u00e1 kerfinu okkar. Gef\u00f0u upp lykilor\u00f0i\u00f0 til a\u00f0 lj\u00faka innskr\u00e1ningarferlinu. \u00dea\u00f0 er eins-skiptis a\u00f0ger\u00f0, sem mun koma \u00e1 sambandi milli Pootle-\u00fej\u00f3nsins og a\u00f0ganga %(provider)s.", 
    "We have sent an email containing the special link to <span>%s</span>": "Vi\u00f0 erum b\u00fain a\u00f0 senda t\u00f6lvup\u00f3st me\u00f0 s\u00e9rst\u00f6kum tengli til <span>%s</span>", 
    "We have sent an email containing the special link to <span>%s</span>. Please check your spam folder if you do not see the email.": "Vi\u00f0 h\u00f6fum sent s\u00e9rstakan tengil til <span>%s</span>. Endilega sko\u00f0a\u00f0u \u00ed ruslp\u00f3stm\u00f6ppuna \u00fe\u00edna ef \u00fe\u00fa s\u00e9r\u00f0 ekki t\u00f6lvup\u00f3stinn.", 
    "We have sent an email containing the special link to the address used to register this account. Please check your spam folder if you do not see the email.": "Vi\u00f0 h\u00f6fum sent s\u00e9rstakan tengil \u00e1 t\u00f6lvup\u00f3stfangi\u00f0 sem var nota\u00f0 til a\u00f0 skr\u00e1 \u00feennan a\u00f0gang. Endilega sko\u00f0a\u00f0u \u00ed ruslp\u00f3stm\u00f6ppuna \u00fe\u00edna ef \u00fe\u00fa s\u00e9r\u00f0 ekki t\u00f6lvup\u00f3stinn.", 
    "Website": "Vefsv\u00e6\u00f0i", 
    "Why are you part of our translation project? Describe yourself, inspire others!": "Hvers vegna tekur \u00fe\u00fa \u00fe\u00e1tt \u00ed \u00feessu \u00fe\u00fd\u00f0ingarverkefni? L\u00fdstu sj\u00e1lf/um \u00fe\u00e9r, vertu hvatning fyrir a\u00f0ra!", 
    "Yes": "J\u00e1", 
    "You have unsaved changes in this string. Navigating away will discard those changes.": "\u00de\u00fa ert me\u00f0 \u00f3vista\u00f0ar breytingar \u00ed \u00feessum streng. Ef \u00fe\u00fa heldur \u00e1fram mun \u00feessum breytingum ver\u00f0a hent.", 
    "Your Full Name": "Fullt nafn \u00feitt", 
    "Your LinkedIn profile URL": "LinkedIn notandasni\u00f0i\u00f0 mitt", 
    "Your Personal website/blog URL": "Sl\u00f3\u00f0 \u00e1 \u00feitt eigi\u00f0 vefsv\u00e6\u00f0i/blogg", 
    "Your Twitter username": "Twitter notandanafni\u00f0 \u00feitt", 
    "Your account is inactive because an administrator deactivated it.": "A\u00f0gangurinn \u00feinn er \u00f3virkur vegna \u00feess a\u00f0 stj\u00f3rnandi ger\u00f0i hann \u00f3virkan.", 
    "Your account needs activation.": "Virkja \u00fearf a\u00f0ganginn \u00feinn.", 
    "disabled": "\u00f3virkt", 
    "some anonymous user": "einhver nafnlaus notandi", 
    "someone": "einhver"
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

