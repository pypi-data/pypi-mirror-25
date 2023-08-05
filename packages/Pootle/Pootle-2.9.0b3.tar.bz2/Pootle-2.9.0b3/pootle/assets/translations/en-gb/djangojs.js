

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
      "%(count)s language matches your query.", 
      "%(count)s languages match your query."
    ], 
    "%(count)s project matches your query.": [
      "%(count)s project matches your query.", 
      "%(count)s projects match your query."
    ], 
    "%(count)s user matches your query.": [
      "%(count)s user matches your query.", 
      "%(count)s users match your query."
    ], 
    "%(timeSince)s via file upload": "%(timeSince)s via file upload", 
    "%s word": [
      "%s word", 
      "%s words"
    ], 
    "%s's accepted suggestions": "%s's accepted suggestions", 
    "%s's overwritten submissions": "%s's overwritten submissions", 
    "%s's pending suggestions": "%s's pending suggestions", 
    "%s's rejected suggestions": "%s's rejected suggestions", 
    "%s's submissions": "%s's submissions", 
    "Accept": "Accept", 
    "Account Activation": "Account Activation", 
    "Account Inactive": "Account Inactive", 
    "Active": "Active", 
    "Add Language": "Add Language", 
    "Add Project": "Add Project", 
    "Add User": "Add User", 
    "Administrator": "Administrator", 
    "After changing your password you will sign in automatically.": "After changing your password you will sign in automatically.", 
    "All Languages": "All Languages", 
    "All Projects": "All Projects", 
    "An error occurred while attempting to sign in via %s.": "An error occurred while attempting to sign in via %s.", 
    "An error occurred while attempting to sign in via your social account.": "An error occurred while attempting to sign in via your social account.", 
    "Avatar": "Avatar", 
    "Cancel": "Cancel", 
    "Clear all": "Clear all", 
    "Clear value": "Clear value", 
    "Close": "Close", 
    "Code": "Code", 
    "Collapse details": "Collapse details", 
    "Congratulations! You have completed this task!": "Congratulations! You have completed this task!", 
    "Contact Us": "Contact Us", 
    "Contributors, 30 Days": "Contributors, 30 Days", 
    "Creating new user accounts is prohibited.": "Creating new user accounts is prohibited.", 
    "Delete": "Delete", 
    "Deleted successfully.": "Deleted successfully.", 
    "Didn't receive an email? Check if it was accidentally filtered out as spam, or try requesting another copy of the email.": "Didn't receive an email? Check if it was accidentally filtered out as spam, or try requesting another copy of the email.", 
    "Disabled": "Disabled", 
    "Discard changes.": "Discard changes.", 
    "Edit Language": "Edit Language", 
    "Edit My Public Profile": "Edit My Public Profile", 
    "Edit Project": "Edit Project", 
    "Edit User": "Edit User", 
    "Edit the suggestion before accepting, if necessary": "Edit the suggestion before accepting, if necessary", 
    "Email": "Email", 
    "Email Address": "Email Address", 
    "Email Confirmation": "Email Confirmation", 
    "Enter your email address, and we will send you a message with the special link to reset your password.": "Enter your email address, and we will send you a message with the special link to reset your password.", 
    "Error while connecting to the server": "Error while connecting to the server", 
    "Expand details": "Expand details", 
    "File types": "File types", 
    "Filesystems": "Filesystems", 
    "Find language by name, code": "Find language by name, code", 
    "Find project by name, code": "Find project by name, code", 
    "Find user by name, email, properties": "Find user by name, email, properties", 
    "Full Name": "Full Name", 
    "Go back to browsing": "Go back to browsing", 
    "Go to the next string (Ctrl+.)<br/><br/>Also:<br/>Next page: Ctrl+Shift+.<br/>Last page: Ctrl+Shift+End": "Go to the next string (Ctrl+.)<br/><br/>Also:<br/>Next page: Ctrl+Shift+.<br/>Last page: Ctrl+Shift+End", 
    "Go to the previous string (Ctrl+,)<br/><br/>Also:<br/>Previous page: Ctrl+Shift+,<br/>First page: Ctrl+Shift+Home": "Go to the previous string (Ctrl+,)<br/><br/>Also:<br/>Previous page: Ctrl+Shift+,<br/>First page: Ctrl+Shift+Home", 
    "Hide": "Hide", 
    "Hide disabled": "Hide disabled", 
    "I forgot my password": "I forgot my password", 
    "Ignore Files": "Ignore Files", 
    "Languages": "Languages", 
    "Less": "Less", 
    "LinkedIn": "LinkedIn", 
    "LinkedIn profile URL": "LinkedIn profile URL", 
    "Load More": "Load More", 
    "Loading...": "Loading\u2026", 
    "Login / Password": "Login / Password", 
    "More": "More", 
    "More...": "More...", 
    "My Public Profile": "My Public Profile", 
    "No": "No", 
    "No activity recorded in a given period": "No activity recorded in a given period", 
    "No results found": "No results found", 
    "No results.": "No results.", 
    "No, thanks": "No, thanks", 
    "Not found": "Not found", 
    "Note: when deleting a user their contributions to the site, e.g. comments, suggestions and translations, are attributed to the anonymous user (nobody).": "Note: when deleting a user their contributions to the site, e.g. comments, suggestions and translations, are attributed to the anonymous user (nobody).", 
    "Number of Plurals": "Number of Plurals", 
    "Oops...": "Oops...", 
    "Overview": "Overview", 
    "Password": "Password", 
    "Password changed, signing in...": "Password changed, signing in...", 
    "Permissions": "Permissions", 
    "Personal description": "Personal description", 
    "Personal website URL": "Personal website URL", 
    "Please follow that link to continue the account creation.": "Please follow that link to continue the account creation.", 
    "Please follow that link to continue the password reset procedure.": "Please follow that link to continue the password reset procedure.", 
    "Please select a valid user.": "Please select a valid user.", 
    "Plural Equation": "Plural Equation", 
    "Plural form %(index)s": "Plural form %(index)s", 
    "Preview will be displayed here.": "Preview will be displayed here.", 
    "Project / Language": "Project / Language", 
    "Project Tree Style": "Project Tree Style", 
    "Provide optional comment (will be publicly visible)": "Provide optional comment (will be publicly visible)", 
    "Public Profile": "Public Profile", 
    "Quality Checks": "Quality Checks", 
    "Reject": "Reject", 
    "Reload page": "Reload page", 
    "Repeat Password": "Repeat Password", 
    "Resend Email": "Resend Email", 
    "Reset Password": "Reset Password", 
    "Reset Your Password": "Reset Your Password", 
    "Reviewed": "Reviewed", 
    "Save": "Save", 
    "Saved successfully.": "Saved successfully.", 
    "Score Change": "Score Change", 
    "Screenshot Search Prefix": "Screenshot Search Prefix", 
    "Search Languages": "Search Languages", 
    "Search Projects": "Search Projects", 
    "Search Users": "Search Users", 
    "Select...": "Select...", 
    "Send Email": "Send Email", 
    "Sending email to %s...": "Sending email to %s...", 
    "Server error": "Server error", 
    "Set New Password": "Set New Password", 
    "Set a new password": "Set a new password", 
    "Settings": "Settings", 
    "Short Bio": "Short Bio", 
    "Show": "Show", 
    "Show disabled": "Show disabled", 
    "Sign In": "Sign In", 
    "Sign In With %s": "Sign In With %s", 
    "Sign In With...": "Sign In With...", 
    "Sign Up": "Sign Up", 
    "Sign in as an existing user": "Sign in as an existing user", 
    "Sign up as a new user": "Sign up as a new user", 
    "Signed in. Redirecting...": "Signed in. Redirecting...", 
    "Signing in with an external service for the first time will automatically create an account for you.": "Signing in with an external service for the first time will automatically create an account for you.", 
    "Similar translations": "Similar translations", 
    "Social Services": "Social Services", 
    "Social Verification": "Social Verification", 
    "Source Language": "Source Language", 
    "Special Characters": "Special Characters", 
    "String Errors Contact": "String Errors Contact", 
    "Suggested": "Suggested", 
    "Team": "Team", 
    "The password reset link was invalid, possibly because it has already been used. Please request a new password reset.": "The password reset link was invalid, possibly because it has already been used. Please request a new password reset.", 
    "The server seems down. Try again later.": "The server seems down. Try again later.", 
    "There are unsaved changes. Do you want to discard them?": "There are unsaved changes. Do you want to discard them?", 
    "There is %(count)s language.": [
      "There is %(count)s language.", 
      "There are %(count)s languages. Below are the most recently added ones."
    ], 
    "There is %(count)s project.": [
      "There is %(count)s project.", 
      "There are %(count)s projects. Below are the most recently added ones."
    ], 
    "There is %(count)s user.": [
      "There is %(count)s user.", 
      "There are %(count)s users. Below are the most recently added ones."
    ], 
    "This email confirmation link expired or is invalid.": "This email confirmation link expired or is invalid.", 
    "This string no longer exists.": "This string no longer exists.", 
    "To set or change your avatar for your email address (%(email)s), please go to gravatar.com.": "To set or change your avatar for your email address (%(email)s), please go to gravatar.com.", 
    "Translated": "Translated", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project": "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project %(time_ago)s": "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project %(time_ago)s", 
    "Try again": "Try again", 
    "Twitter": "Twitter", 
    "Twitter username": "Twitter username", 
    "Type to search": "Type to search", 
    "Updating data": "Updating data", 
    "Use the search form to find the language, then click on a language to edit.": "Use the search form to find the language, then click on a language to edit.", 
    "Use the search form to find the project, then click on a project to edit.": "Use the search form to find the project, then click on a project to edit.", 
    "Use the search form to find the user, then click on a user to edit.": "Use the search form to find the user, then click on a user to edit.", 
    "Username": "Username", 
    "We found a user with <span>%(email)s</span> email in our system. Please provide the password to finish the sign in procedure. This is a one-off procedure, which will establish a link between your Pootle and %(provider)s accounts.": "We found a user with <span>%(email)s</span> email in our system. Please provide the password to finish the sign in procedure. This is a one-off procedure, which will establish a link between your Pootle and %(provider)s accounts.", 
    "We have sent an email containing the special link to <span>%s</span>": "We have sent an email containing the special link to <span>%s</span>", 
    "We have sent an email containing the special link to <span>%s</span>. Please check your spam folder if you do not see the email.": "We have sent an email containing the special link to <span>%s</span>. Please check your spam folder if you do not see the email.", 
    "We have sent an email containing the special link to the address used to register this account. Please check your spam folder if you do not see the email.": "We have sent an email containing the special link to the address used to register this account. Please check your spam folder if you do not see the email.", 
    "Website": "Website", 
    "Why are you part of our translation project? Describe yourself, inspire others!": "Why are you part of our translation project? Describe yourself, inspire others!", 
    "Yes": "Yes", 
    "You have unsaved changes in this string. Navigating away will discard those changes.": "You have unsaved changes in this string. Navigating away will discard those changes.", 
    "Your Full Name": "Your Full Name", 
    "Your LinkedIn profile URL": "Your LinkedIn profile URL", 
    "Your Personal website/blog URL": "Your Personal website/blog URL", 
    "Your Twitter username": "Your Twitter username", 
    "Your account is inactive because an administrator deactivated it.": "Your account is inactive because an administrator deactivated it.", 
    "Your account needs activation.": "Your account needs activation.", 
    "disabled": "disabled", 
    "some anonymous user": "some anonymous user", 
    "someone": "someone"
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

