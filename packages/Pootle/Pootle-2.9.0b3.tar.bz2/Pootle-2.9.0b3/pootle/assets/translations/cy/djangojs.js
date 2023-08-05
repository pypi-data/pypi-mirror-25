

(function(globals) {

  var django = globals.django || (globals.django = {});

  
  django.pluralidx = function(n) {
    var v=(n==2) ? 1 : 0;
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
      "%(count)s iaith yn cydweddu \u00e2'ch ymholiad.", 
      "%(count)s iaith yn cydweddu \u00e2'ch ymholiad."
    ], 
    "%(count)s project matches your query.": [
      "%(count)s project yn cydweddu \u00e2'ch ymholiad.", 
      "%(count)s project yn cydweddu \u00e2'ch ymholiad."
    ], 
    "%(count)s user matches your query.": [
      "%(count)s defnyddiwr yn cyfateb i'ch ymholiad.", 
      "%(count)s defnyddiwr yn cyfateb i'ch ymholiad."
    ], 
    "%(timeSince)s via file upload": "%(timeSince)s drwy lwytho ffeil", 
    "%s word": [
      "%s gair", 
      "%s gair"
    ], 
    "%s's accepted suggestions": "Awgrymiadau %s wedi eu derbyn", 
    "%s's overwritten submissions": "Awgrymiadau %s wedi eu trosysgrifennu", 
    "%s's pending suggestions": "Awgrymiadau %s yn disgwyl cymeradwyaeth", 
    "%s's rejected suggestions": "Awgrymiadau %s wedi eu gwrthod", 
    "%s's submissions": "Awgrymiadau %s", 
    "Accept": "Derbyn", 
    "Account Activation": "Gweithredu Cyfrif", 
    "Account Inactive": "Cyfrif Anweithredol", 
    "Active": "Gweithredol", 
    "Add Language": "Ychwanegu Iaith", 
    "Add Project": "Ychwanegu Project", 
    "Add User": "Ychwanegu Defnyddiwr", 
    "Administrator": "Gweinyddwr", 
    "After changing your password you will sign in automatically.": "Wedi newid eich cyfrinair byddwch yn mewngofndi'n awtomatig.", 
    "All Languages": "Pob Iaith", 
    "All Projects": "Pob Project", 
    "An error occurred while attempting to sign in via %s.": "Digwyddodd gwall wrth geisio mewngofnodi drwy %s.", 
    "An error occurred while attempting to sign in via your social account.": "Digwyddodd gwall wrth geisio mewngofnodi drwy eich cyfrif cymdeithasol.", 
    "Avatar": "Afatar", 
    "Cancel": "Diddymu", 
    "Clear all": "Clirio popeth", 
    "Clear value": "Clirio'r gwerth", 
    "Close": "Cau", 
    "Code": "Cod", 
    "Collapse details": "Lleihau'r manylion", 
    "Congratulations! You have completed this task!": "Llongyfarchiadau! Rydych wedi cwblhau'r dasg!", 
    "Contact Us": "Cysylltu \u00e2 ni", 
    "Contributors, 30 Days": "Cyfranwyr, 30 Diwrnod", 
    "Creating new user accounts is prohibited.": "Mae creu cyfrifon defnyddwyr newydd wedi ei wahardd.", 
    "Delete": "Dileu", 
    "Deleted successfully.": "Dil\u00ebwyd yn llwyddiannus.", 
    "Didn't receive an email? Check if it was accidentally filtered out as spam, or try requesting another copy of the email.": "Heb dderbyn yr e-bost? Gwiriwch os cafodd ei hidlo ar ddamwain fel sbam neu gofynnwch am gopi arall o'r e-bost.", 
    "Disabled": "Analluogwyd", 
    "Discard changes.": "Hepgor y newidiadau.", 
    "Edit Language": "Golygu Iaith", 
    "Edit My Public Profile": "Golygu fy Mhroffil Cyhoeddus", 
    "Edit Project": "Golygu Project", 
    "Edit User": "Golygu Defnyddiwr", 
    "Edit the suggestion before accepting, if necessary": "Golygu awgrym cyn ei dderbyn, os oes angen", 
    "Email": "E-bost", 
    "Email Address": "Cyfeiriad E-bost", 
    "Email Confirmation": "E-bost Cadarnhad", 
    "Enter your email address, and we will send you a message with the special link to reset your password.": "Rhowch eich cyfeiriad e-bost a byddwn yn anfon neges atoch gyda dolen arbennig er mwyn ailosod eich cyfrinair.", 
    "Error while connecting to the server": "Gwall wrth gysylltu \u00e2'r gweinydd", 
    "Expand details": "Ehangu'r manylion", 
    "File types": "Math o ffeil", 
    "Filesystems": "Systemau Ffeiliau", 
    "Find language by name, code": "Canfod iaith yn \u00f4l enw, cod", 
    "Find project by name, code": "Canfod project yn \u00f4l enw, cod", 
    "Find user by name, email, properties": "Canfod defnyddiwr yn \u00f4l enw, e-bost, priodweddau", 
    "Full Name": "Enw Llawn", 
    "Go back to browsing": "Mynd n\u00f4l i bori", 
    "Go to the next string (Ctrl+.)<br/><br/>Also:<br/>Next page: Ctrl+Shift+.<br/>Last page: Ctrl+Shift+End": "Ewch i'r llinyn nesaf (Ctrl+.)<br/><br/>Hefyd:<br/>Tudalen nesaf: Ctrl+Shift+.<br/>Tudalen olaf: Ctrl+Shift+End", 
    "Go to the previous string (Ctrl+,)<br/><br/>Also:<br/>Previous page: Ctrl+Shift+,<br/>First page: Ctrl+Shift+Home": "Ewch i'r llinyn blaenorol (Ctrl+,)<br/><br/>Hefyd:<br/>Tudalen flaenorol: Ctrl+Shift+,<br/>Tudalen gyntaf: Ctrl+Shift+Home", 
    "Hide": "Cuddio", 
    "Hide disabled": "Cuddio'r analluogwyd", 
    "I forgot my password": "Wedi anghofio fy nghyfrinair", 
    "Ignore Files": "Anwybyddu Ffeiliau", 
    "Languages": "Ieithoedd", 
    "Less": "Llai", 
    "LinkedIn": "LinkedIn", 
    "LinkedIn profile URL": "URL proffil LinkedIn", 
    "Load More": "Llwytho Rhagor", 
    "Loading...": "Llwytho...", 
    "Login / Password": "Mewngofnodi / Cyfrinair", 
    "More": "Rhagor", 
    "More...": "Rhagor...", 
    "My Public Profile": "Fy Mhroffil Cyhoeddus", 
    "No": "Na", 
    "No activity recorded in a given period": "Dim gweithgaredd o fewn amser penodol", 
    "No results found": "Heb ganfod canlyniadau", 
    "No results.": "Dim canlyniad.", 
    "No, thanks": "Na, dim diolch", 
    "Not found": "Heb ei ganfod", 
    "Note: when deleting a user their contributions to the site, e.g. comments, suggestions and translations, are attributed to the anonymous user (nobody).": "Sylw: wrth ddileu defnyddiwr bydd eu cyfraniad i'r wefan, e.e. sylwadau, awgrymiadau a chyfieithiadau yn cael eu tadogi i ddefnyddiwr anhysbys (neb).", 
    "Number of Plurals": "Nifer y Lluosogion", 
    "Oops...": "Wps...", 
    "Overview": "Trosolwg", 
    "Password": "Cyfrinair", 
    "Password changed, signing in...": "Mae'r cyfrinair wedi ei newid, mewngofnodi...", 
    "Permissions": "Caniat\u00e2d", 
    "Personal description": "Disgrifiad personol", 
    "Personal website URL": "URL gwefan bersonol", 
    "Please follow that link to continue the account creation.": "Dilynwch y ddolen i barhau i greu'r cyfrif.", 
    "Please follow that link to continue the password reset procedure.": "Dilynwch y ddolen i barhau'r broses o ailosod y cyfrinair.", 
    "Please select a valid user.": "Dewiswch ddefnyddiwr dilys.", 
    "Plural Equation": "Hafaliad Lluosog", 
    "Plural form %(index)s": "Ffurf lluosog %(index)s", 
    "Preview will be displayed here.": "Bydd y rhagolwg yn cael ei ddangos yma.", 
    "Project / Language": "Prosiect / Iaith", 
    "Project Tree Style": "Arddull Coeden y Project", 
    "Provide optional comment (will be publicly visible)": "Darparu sylw dewisol (bydd ar gael yn gyhoeddus)", 
    "Public Profile": "Proffil Cyhoeddus", 
    "Quality Checks": "Gwiriad Ansawdd", 
    "Reject": "Gwrthod", 
    "Reload page": "Ail lwytho tudalen", 
    "Repeat Password": "Ailadrodd y Cyfrinair", 
    "Resend Email": "Ail anfon E-bost", 
    "Reset Password": "Ailosod y Cyfrinair", 
    "Reset Your Password": "Ailosod eich Cyfrinair", 
    "Reviewed": "Adolygu", 
    "Save": "Cadw", 
    "Saved successfully.": "Cadwyd yn llwyddiannus.", 
    "Score Change": "Newid Sg\u00f4r", 
    "Screenshot Search Prefix": "Rhagosodiad Chwilio Llun Sgrin", 
    "Search Languages": "Chwilio drwy'r Ieithoedd", 
    "Search Projects": "Chwilio Drwy'r Projectau", 
    "Search Users": "Chwilio'r Defnyddwyr", 
    "Select...": "Dewis...", 
    "Send Email": "Anfon E-bost", 
    "Sending email to %s...": "Anfon e-bost at %s...", 
    "Server error": "Gwall gweinydd", 
    "Set New Password": "Gosod Cyfrinair Newydd", 
    "Set a new password": "Gosod cyfrinair newydd", 
    "Settings": "Gosodiadau", 
    "Short Bio": "Hanes byr", 
    "Show": "Dangos", 
    "Show disabled": "Dangos yr analluogwyd", 
    "Sign In": "Mewngofnodi", 
    "Sign In With %s": "Mewngofnodi Gyda %s", 
    "Sign In With...": "Mewngofnodi gyda...", 
    "Sign Up": "Ymuno", 
    "Sign in as an existing user": "Mewngofnodi fel defnyddiwr cyfredol", 
    "Sign up as a new user": "Ymuno fel defnyddiwr newydd", 
    "Signed in. Redirecting...": "Wedi mewngofnodi. Ailgyfeirio...", 
    "Signing in with an external service for the first time will automatically create an account for you.": "Bydd mewngofnodi drwy wasanaeth allanol am y tro cyntaf y creu cyfrif yn awtomatig ar eich cyfer.", 
    "Similar translations": "Cyfieithiadau tebyg", 
    "Social Services": "Gwasanaethau Cymdeithasol", 
    "Social Verification": "Dilysiad Cymdeithasol", 
    "Source Language": "Iaith Ffynhonnell", 
    "Special Characters": "Nodau Arbennig", 
    "String Errors Contact": "Cyswllt Gwallau Llinyn", 
    "Suggested": "Awgrymu", 
    "Team": "T\u00eem", 
    "The password reset link was invalid, possibly because it has already been used. Please request a new password reset.": "Mae'r ddolen ailosod cyfrinair yn annilys o bosib am ei fod eisoes wedi ei ddefnyddio. Gofynnwch i'r cyfrinair gael ei ailosod.", 
    "The server seems down. Try again later.": "Mae'r gweinydd i weld wedi torri. Ceisiwch rhywbryd eto.", 
    "There are unsaved changes. Do you want to discard them?": "Mae yna newidiadau sydd heb eu cadw. Hoffech chi eu hepgor?", 
    "There is %(count)s language.": [
      "Mae yna %(count)s iaith.", 
      "Mae yna %(count)s iaith. Isod y mae'r ieithoedd ychwanegwyd yn fwyaf diweddar."
    ], 
    "There is %(count)s project.": [
      "Mae yna %(count)s project.", 
      "Mae yna %(count)s project. Isod mae'r rhai diweddaraf i'w hychwanegu."
    ], 
    "There is %(count)s user.": [
      "Mae %(count)s defnyddwyr.", 
      "Mae %(count)s defnyddwyr. Isod mae'r rhai diweddaraf i'w hychwanegu."
    ], 
    "This email confirmation link expired or is invalid.": "Mae'r e-bost dolen cadarnhad wedi dod i ben neu yn annilys.", 
    "This string no longer exists.": "Nid yw'r llinyn hwn yn bodoli.", 
    "To set or change your avatar for your email address (%(email)s), please go to gravatar.com.": "I osod neu newid afatar eich cyfeiriad e-bost (%(email)s), ewch i gravatar.com.", 
    "Translated": "Cyfieithu", 
    "Try again": "Ceisiwch eto", 
    "Twitter": "Twitter", 
    "Twitter username": "Enw defnyddiwr Twitter", 
    "Type to search": "Teipiwch i chwilio", 
    "Updating data": "Diweddaru data", 
    "Use the search form to find the language, then click on a language to edit.": "Defnyddiwch y ffurflen chwilio i ganfod iaith ac yna glicio ar iaith i'w golygu.", 
    "Use the search form to find the project, then click on a project to edit.": "Defnyddiwch y ffurflen chwilio i ganfod project ac yna clicio ar y project i'w olygu.", 
    "Use the search form to find the user, then click on a user to edit.": "Defnyddiwch y ffurflen chwilio i ganfod defnyddiwr, yna cliciwch ar ddefnyddiwr i'w olygu.", 
    "Username": "Enw Defnyddiwr", 
    "We found a user with <span>%(email)s</span> email in our system. Please provide the password to finish the sign in procedure. This is a one-off procedure, which will establish a link between your Pootle and %(provider)s accounts.": "Rydym wedi darganfod defnyddiwr gydag e-bost<span>%(email)s</span> yn ein system. Rhowch y cyfrinair i orffen y drefn mewngofnodi. Mae hyn yn drefn unwaith ac am byth, a bydd yn sefydlu cysylltiad rhwng eich cyfrifon Pootle a chyfrifon %(provider)s.", 
    "We have sent an email containing the special link to <span>%s</span>": "Rydym wedi anfon e-bost sy'n cynnwys dolen arbennig at <span>%s</span>", 
    "We have sent an email containing the special link to <span>%s</span>. Please check your spam folder if you do not see the email.": "Rydym wedi anfon e-bost sy'n cynnwys dolen arbennig at <span>%s</span>. Gwiriwch eich ffolder sbam os nad ydych yn gweld yr e-bost.", 
    "We have sent an email containing the special link to the address used to register this account. Please check your spam folder if you do not see the email.": "Rydym wedi anfon e-bost yn cynnwys dolen arbennig at y cyfeiriad defnyddiwyd i gofrestru'r cyfrif hwn. Gwiriwch eich ffolder sbam os nad ydych yn gweld yr e-bost.", 
    "Website": "Gwefan", 
    "Why are you part of our translation project? Describe yourself, inspire others!": "Pam ydych chi'n rhan o'n prosiect cyfieithu? Disgrifiwch eich hun, ysbrydolwch eraill!", 
    "Yes": "Iawn", 
    "You have unsaved changes in this string. Navigating away will discard those changes.": "Mae gennych newidiadau heb eu cadw yn llinyn hwn. Bydd symud i ffwrdd yn golygu colli'r newidiadau hyn.", 
    "Your Full Name": "Eich Enw Llawn", 
    "Your LinkedIn profile URL": "URL eich proffil LinkedIn", 
    "Your Personal website/blog URL": "URL eich gwefan/blog personol", 
    "Your Twitter username": "Eich enw defnyddiwr Twitter", 
    "Your account is inactive because an administrator deactivated it.": "Mae eich cyfrif yn anweithredol gan fod gweinyddwr wedi ei ddadweithredu.", 
    "Your account needs activation.": "Mae eich cyfrif angen ei weithredu.", 
    "disabled": "analluogwyd", 
    "some anonymous user": "rhyw ddefnyddiwr anhysbys", 
    "someone": "rhywun"
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

