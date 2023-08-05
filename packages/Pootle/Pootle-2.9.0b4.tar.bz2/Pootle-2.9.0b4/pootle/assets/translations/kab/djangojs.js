

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
      "%(count)s n tutlayt tcudd ar tuttra yinek.", 
      "%(count)s n tutlayin cuddent ar tuttra yinek."
    ], 
    "%(count)s project matches your query.": [
      "%(count)s n usefa\u1e5b yenme\u0263ra akked tuttra yinek.", 
      "%(count)s n isenfa\u1e5ben nme\u0263ran akked tuttra yinek."
    ], 
    "%(count)s user matches your query.": [
      "%(count)s n useqdac yenme\u0263ra akked tuttra inek.", 
      "%(count)s n iseqdacen nme\u0263ran akked tuttra inek."
    ], 
    "%(timeSince)s via file upload": "%(timeSince)s s tuzna n ufaylu", 
    "%s word": [
      "%s awal", 
      "%s awalen"
    ], 
    "%s's accepted suggestions": "Isumar yettwaqeblen n %s", 
    "%s's overwritten submissions": "Ittekkiyen n %s yettwasfe\u025bjen", 
    "%s's pending suggestions": "Isumar yettra\u01e7un n %s", 
    "%s's rejected suggestions": "Isumar yettwagin n %s", 
    "%s's submissions": "Attekki n %s", 
    "Accept": "Qbel", 
    "Account Activation": "Armad n umi\u1e0dan", 
    "Account Inactive": "Ami\u1e0dan inek ur yermid ara.", 
    "Active": "Urmid", 
    "Add Language": "Rnu tutlayt", 
    "Add Project": "Rnu asenfa\u1e5b", 
    "Add User": "Rnu aseqdac", 
    "Administrator": "Anebdal", 
    "After changing your password you will sign in automatically.": "Ticki tesnifled awal inek uffir, ad teqqne\u1e0d s wudem awurman.", 
    "All Languages": "Akk tutlayin", 
    "All Projects": "Akk isenfa\u1e5ben", 
    "An error occurred while attempting to sign in via %s.": "Te\u1e0dra-d tucc\u1e0da deg u\u025bra\u1e0d n tuqqna s %s.", 
    "An error occurred while attempting to sign in via your social account.": "Tedra-d tucc\u1e0da deg u\u025bra\u1e0d n tuqqna s umi\u1e0dan inek n tmetti.", 
    "Avatar": "Avatar", 
    "Cancel": "Sefsex", 
    "Clear all": "Sfe\u1e0d akk", 
    "Clear value": "Sfe\u1e0d azal", 
    "Close": "mdel", 
    "Code": "Tangalt", 
    "Collapse details": "Ffer talqayt", 
    "Congratulations! You have completed this task!": "Ayuz! Tfuke\u1e0d tawuri-agi!", 
    "Contact Us": "Nermes-a\u0263-d", 
    "Contributors, 30 Days": "Imttekkiyen, 30 n wussan", 
    "Creating new user accounts is prohibited.": "Timerna n imi\u1e0danen-nni\u1e0den n useqdac tegdel.", 
    "Delete": "Kkes", 
    "Deleted successfully.": "Yettwakkes akken iwata.", 
    "Didn't receive an email? Check if it was accidentally filtered out as spam, or try requesting another copy of the email.": "Ur d-rmised ara imayl? Senqed ma yella yekcem ar ukaram n ispamen, ne\u0263 \u025bre\u1e0d asuter n n\u0263el-nni\u1e0den n yimayl. ", 
    "Disabled": "Yensa", 
    "Discard changes.": "Sefsex asnifel", 
    "Edit Language": "\u1e92reg tutlayt", 
    "Edit My Public Profile": "\u1e92reg ama\u0263nu inu azayez", 
    "Edit Project": "\u1e92reg asenfa\u1e5b", 
    "Edit User": "\u1e92reg aseqdac", 
    "Edit the suggestion before accepting, if necessary": "\u1e92reg asumer send asentem, ma ilaq", 
    "Email": "Imayl", 
    "Email Address": "Tansa Imayl", 
    "Email Confirmation": "Asentem n yimayl", 
    "Enter your email address, and we will send you a message with the special link to reset your password.": "Sekcem tansa yinek imayl sakin ak-d-nazen izen igebren ase\u0263wen ime\u1e93li aken ad talse\u1e0d awennez n wawal-ik uffir.", 
    "Error while connecting to the server": "Tucc\u1e0dan di tuqqna ar uqeddac", 
    "Expand details": "Sken talqayt", 
    "File types": "Anawen n ifuyla", 
    "Filesystems": "Anagraw n ifuyla", 
    "Find language by name, code": "Af-d tutlayt s yisem, tangalt", 
    "Find project by name, code": "Af-d asenfa\u1e5b s yisem, tangalt", 
    "Find user by name, email, properties": "Af-d aseqdac s yisem, imayl, time\u1e93liyin", 
    "Full Name": "Isem ummid", 
    "Go back to browsing": "U\u0263al ar tunigin", 
    "Go to the next string (Ctrl+.)<br/><br/>Also:<br/>Next page: Ctrl+Shift+.<br/>Last page: Ctrl+Shift+End": "Ddu ar izirig d-iteddun (Ctrl+.)<br/><br/>Da\u0263en:<br/>Asebter d-iteddun: Ctrl+Shift+.<br/>Asebter aneggaru: Ctrl+Shift+End", 
    "Go to the previous string (Ctrl+,)<br/><br/>Also:<br/>Previous page: Ctrl+Shift+,<br/>First page: Ctrl+Shift+Home": "Ddu ar uzrir yezrin (Ctrl+,)<br/><br/>Da\u0263en:<br/>Asebter yezrin: Ctrl+Shift+,<br/>Asebter amezwaru: Ctrl+Shift+Home", 
    "Hide": "Ffer", 
    "Hide disabled": "ffer wid yensan", 
    "I forgot my password": "Ttu\u0263 awal-iw uffir", 
    "Ignore Files": "Zgel ifuyla", 
    "Languages": "Tutlayin", 
    "Less": "Drus", 
    "LinkedIn": "LinkedIn", 
    "LinkedIn profile URL": "Tansa URL n uma\u0263nu LinkedIn", 
    "Load More": "Sali-d ugar", 
    "Loading...": "Asali...", 
    "Login / Password": "Asulay / Awal uffir", 
    "More": "Ugar", 
    "More...": "Ugar...", 
    "My Public Profile": "Ama\u0263nu inu azayez", 
    "No": "Ala", 
    "No activity recorded in a given period": "Ulac armud yettwakelsen di twala d-ittunefken", 
    "No results found": "Ulac agmu\u1e0d", 
    "No results.": "Ulac agmu\u1e0d", 
    "No, thanks": "Ala, tanemmirt", 
    "Not found": "Ulac-it", 
    "Note: when deleting a user their contributions to the site, e.g. comments, suggestions and translations, are attributed to the anonymous user (nobody).": "Tazmilt: Tukksa n useqdac ad imudd akk attekki ines (iwenniten, isumar akked tsuqilin) i useqdac udrig.", 
    "Number of Plurals": "Am\u1e0dan n usget", 
    "Oops...": "Ihuh...", 
    "Overview": "Agzul", 
    "Password": "Awal uffir", 
    "Password changed, signing in...": "Awal uffir yettusnifel, tuqqna...", 
    "Permissions": "Tisirag", 
    "Personal description": "Aglam udmawan", 
    "Personal website URL": "Tansa yinek URL n usmell web udmawan", 
    "Please follow that link to continue the account creation.": "Ma ulac a\u0263ilif, ddu ar useqwen akken ad ternu\u1e0d ami\u1e0dan.", 
    "Please follow that link to continue the password reset procedure.": "Ma ulac a\u0263ilif, \u1e0dfe\u1e5b ase\u0263wen-agi akken ad tkemle\u1e0d awennez n wawal uffir.", 
    "Please select a valid user.": "Ma ulac a\u0263ilif, fren aseqdac ame\u0263tu.", 
    "Plural Equation": "Tagda n usget", 
    "Plural form %(index)s": "Tal\u0263a n usget %(index)s", 
    "Preview will be displayed here.": "Taskant ad tettwasken dagi.", 
    "Project / Language": "Asenfa\u1e5b / Tutlayt", 
    "Project Tree Style": "A\u0263anid n useklu n usenfa\u1e5b", 
    "Provide optional comment (will be publicly visible)": "Mudd-d awennit afrayan (ad twalin yemdanen)", 
    "Public Profile": "Ama\u0263nu azayez:", 
    "Quality Checks": "Asenqed n t\u0263ara", 
    "Reject": "Aggi", 
    "Reload page": "Ales asali n usebter", 
    "Repeat Password": "Ales awal uffir", 
    "Resend Email": "Ales tuzna n yimayl", 
    "Reset Password": "Ales awennez n wawal uffir", 
    "Reset Your Password": "Ales awennez n wawal inek uffir", 
    "Reviewed": "Yettwacegger", 
    "Save": "Sekles", 
    "Saved successfully.": "Yettwaskles akken iwata.", 
    "Score Change": "Asnifel n ugmu\u1e0d", 
    "Screenshot Search Prefix": "Azwir n unadi n un\u0263el n ugdil", 
    "Search Languages": "Nadi tutlayin", 
    "Search Projects": "Nadi isenfa\u1e5ben", 
    "Search Users": "Nadi iseqdacen", 
    "Select...": "Fren...", 
    "Send Email": "Azen imayl", 
    "Sending email to %s...": "Tuzna n yimayl ar %s...", 
    "Server error": "Tucc\u1e0da n uqeddac", 
    "Set New Password": "Sbadu awal uffir amaynut", 
    "Set a new password": "Sbadu awal uffir amaynut", 
    "Settings": "I\u0263ewaren", 
    "Short Bio": "Taseknudert tawezlant", 
    "Show": "Sken", 
    "Show disabled": "Wali wid yensan", 
    "Sign In": "Qqen", 
    "Sign In With %s": "Qqen s %s", 
    "Sign In With...": "Qqen s...", 
    "Sign Up": "Jerred", 
    "Sign in as an existing user": "Kcem s useqdac yellan", 
    "Sign up as a new user": "qqen s yisem-nni\u1e0den n useqdac", 
    "Signed in. Redirecting...": "Yeqqen, Awelle...", 
    "Signing in with an external service for the first time will automatically create an account for you.": "Tuqqna s umezlu az\u0263aray i tikelt tamezwarut ak-yernu ami\u1e0dan s wudem awurman.", 
    "Similar translations": "Tisuqilin yemgaraden", 
    "Social Services": "I\u1e93e\u1e0dwan n tmetti", 
    "Social Verification": "Asenqed n tmetti", 
    "Source Language": "Tutlayt n u\u0263balu", 
    "Special Characters": "Isekkilen ime\u1e93liyen", 
    "String Errors Contact": "Anermis i tucc\u1e0diwin deg izriren n isekkilen", 
    "Suggested": "Yettusumer", 
    "Team": "Tarba\u025bt", 
    "The password reset link was invalid, possibly because it has already been used. Please request a new password reset.": "Ase\u0263wen n uwennez n wawal uffir ma\u010d\u010di d ame\u0263tu, ahat yettwaseqdec yakan? Ma ulac a\u0263ilif suter awennez tikelt-nni\u1e0den n wawal inek uffir.", 
    "The server seems down. Try again later.": "Aqeddac yettban ye\u0263li. \u0190re\u1e0d tikelt-nni\u1e0den.", 
    "There are unsaved changes. Do you want to discard them?": "Llan isnifal ur yettwakelsen ara. Teb\u0263i\u1e0d ad ten-tesfesxe\u1e0d?", 
    "There is %(count)s language.": [
      "Tella %(count)s n tutlayt.", 
      "Llant %(count)s n tutlayin. Daw-a tid yettwarnan tagara-agi."
    ], 
    "There is %(count)s project.": [
      "Yella %(count)s  n usenfa\u1e5b.", 
      "Llan %(count)s  n isenfa\u1e5ben. Daw-a wid yettwarnan tagara-agi"
    ], 
    "There is %(count)s user.": [
      "Yella %(count)s n useqdac.", 
      "Llan %(count)s n iseqdacen. Daw-a wid yettwarnan tineggura agi."
    ], 
    "This email confirmation link expired or is invalid.": "Ase\u0263wen-agi n usentem n yimayl yezri yalan neq ahat ma\u010d\u010di d ame\u0263tu.", 
    "This string no longer exists.": "Azrir-agi ulac-it yakan.", 
    "To set or change your avatar for your email address (%(email)s), please go to gravatar.com.": "Akken ad tesbadud neq ad tesnifle\u1e0d avatar n tensa yinek imayl (%(email)s), ddu ma ulac a\u0263ilif ar gravatar.com.", 
    "Translated": "Yettusuqel", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project": "Iseqel-it %(fullname)s deg usenfa\u1e5b \u201c<span title=\"%(path)s\">%(project)s</span>\u201d", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project %(time_ago)s": "Isuqel-it %(fullname)s deg usenfa\u1e5b \u00ab <span title=\"%(path)s\">%(project)s</span> \u00bb %(time_ago)s", 
    "Try again": "E\u025bre\u1e0d tikkelt-nni\u1e0den", 
    "Twitter": "Twitter", 
    "Twitter username": "Isem n useqdac Twitter", 
    "Type to search": "Aru akken ad tnadi\u1e0d", 
    "Updating data": "Aleqqem n isefka", 
    "Use the search form to find the language, then click on a language to edit.": "Seqdec tiferkit n unadi tafe\u1e0d-d tutlayt, ssakin sit \u0263ef tutlayt, ad tes\u1e93erge\u1e0d.", 
    "Use the search form to find the project, then click on a project to edit.": "Seqdec tiferkit n unadi akken ad tafe\u1e0d asenfa\u1e5b, sakin sit \u0263ef usenfa\u1e5b akked ad yettwa\u1e93reg.", 
    "Use the search form to find the user, then click on a user to edit.": "Seqdec tiferkit n unadi akken ad tafe\u1e0d aseqdac, sakin sit \u0263ef useqdac akken ad yettwa\u1e93reg.", 
    "Username": "ISem n useqdac", 
    "We found a user with <span>%(email)s</span> email in our system. Please provide the password to finish the sign in procedure. This is a one-off procedure, which will establish a link between your Pootle and %(provider)s accounts.": "Nufa aseqdac s yimayl <span>%(email)s</span> deg unagraw-nne\u0263. Ma ulac a\u0263ilif, mudd-d awal uffir akken ad fake\u1e0d ajerred ar twuri-agi. D tagi i d tarrayt, ayen ara yeggen assa\u0263 gar Pootle inek akked imi\u1e0danen n %(provider)s.", 
    "We have sent an email containing the special link to <span>%s</span>": "Nuzen imayl igebren ase\u0263wen ime\u1e93li ar <span>%s</span>", 
    "We have sent an email containing the special link to <span>%s</span>. Please check your spam folder if you do not see the email.": "Nuzen imayl ighebren ase\u0263wen n urmad ar <span>%s</span>. Ma ulac a\u0263ilif, wali akaram n ispamen ma yella ur tufid ara imayl-nni.", 
    "We have sent an email containing the special link to the address used to register this account. Please check your spam folder if you do not see the email.": "Nuzen imayl igebren ase\u0263wen ame\u1e93li ar tensa yettwaseqdacen deg umi\u1e0dan-agi. Ma ulac a\u0263ilif, senqed  akaram inek n ispamen ma yella ur t-wala\u1e0d ara.", 
    "Website": "Asmel Web", 
    "Why are you part of our translation project? Describe yourself, inspire others!": "Acu\u0263er tettekka\u1e0d deg usenfa\u1e5b-nne\u0263 n tsuqilt?Seglem iman-ik, mudd amedya i wiya\u1e0d!", 
    "Yes": "Ih", 
    "You have unsaved changes in this string. Navigating away will discard those changes.": "\u0194ur-k isnifal ur yettwakelsen ara deg. Ma teddi\u1e0d sanga-nni\u1e0den isnifal inek ad \u1e5bu\u1e25en.", 
    "Your Full Name": "Isem inek ummid", 
    "Your LinkedIn profile URL": "Tansa inek URL n uma\u0263nu LinkedIn", 
    "Your Personal website/blog URL": "Tansa yinek URL n ublug.Asmel web udmawan", 
    "Your Twitter username": "\u1e92reg isem-iw n Twitter", 
    "Your account is inactive because an administrator deactivated it.": "Ami\u1e0dan inek ur yermid ara acku anebdal isens-it.", 
    "Your account needs activation.": "Ami\u1e0dan inek yessefk ad yettwarmed.", 
    "disabled": "yensa", 
    "some anonymous user": "yiwen n useqdac udrig", 
    "someone": "yiwen n useqdac"
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

