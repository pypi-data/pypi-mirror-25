

(function(globals) {

  var django = globals.django || (globals.django = {});

  
  django.pluralidx = function(n) {
    var v=0;
    if (typeof(v) == 'boolean') {
      return v ? 1 : 0;
    } else {
      return v;
    }
  };
  

  /* gettext library */

  django.catalog = django.catalog || {};
  
  var newcatalog = {
    "#%(position)s": "#%(\uc704\uce58)", 
    "%(count)s language matches your query.": [
      "%(count)s \uac1c\uc758 \uc5b8\uc5b4\uac00 \ub2f9\uc2e0\uc758 \ucffc\ub9ac\uc640 \ub9e4\uce58\ub429\ub2c8\ub2e4."
    ], 
    "%(count)s project matches your query.": [
      "%(count)s \uac1c\uc758 \ud504\ub85c\uc81d\ud2b8\uac00 \ub2f9\uc2e0\uc758 \ucffc\ub9ac\uc640 \ub9e4\uce58\ub429\ub2c8\ub2e4."
    ], 
    "%(count)s user matches your query.": [
      "%(count)s \uba85\uc758 \uc0ac\uc6a9\uc790\uac00 \ub2f9\uc2e0\uc758 \ucffc\ub9ac\uc640 \ub9e4\uce58\ub429\ub2c8\ub2e4."
    ], 
    "%(timeSince)s via file upload": "\ud30c\uc77c \uc5c5\ub85c\ub4dc %(timeSince)s ", 
    "%s word": [
      "%s \ub2e8\uc5b4\ub4e4"
    ], 
    "%s's accepted suggestions": "%s\uc758 \ubc1b\uc544\ub4e4\uc5ec\uc9c4 \uc81c\uc548", 
    "%s's overwritten submissions": "%s \uc911\ubcf5 \uc81c\ucd9c", 
    "%s's pending suggestions": "%s\uc758 \ubcf4\ub958\uc911\uc778 \uc81c\uc548\ub4e4", 
    "%s's rejected suggestions": "%s\uc5d0 \uc758\ud574 \uac70\ubd80\ub41c \uc81c\uc548", 
    "%s's submissions": "%s\uc758 \uc81c\uc548", 
    "Accept": "\uc218\ub77d", 
    "Account Activation": "\uacc4\uc815 \ud65c\uc131\ud654", 
    "Account Inactive": "\uacc4\uc815 \ube44\ud65c\uc131\ud654", 
    "Active": "\ud65c\uc131\ud654", 
    "Add Language": "\uc5b8\uc5b4 \ucd94\uac00", 
    "Add Project": "\ud504\ub85c\uc81d\ud2b8 \ucd94\uac00", 
    "Add User": "\uc0ac\uc6a9\uc790 \ucd94\uac00", 
    "Administrator": "\uad00\ub9ac\uc790", 
    "After changing your password you will sign in automatically.": "\ube44\ubc00\ubc88\ud638 \ubcc0\uacbd \ud6c4 \uc790\ub3d9\uc73c\ub85c \uc811\uc18d\ud558\uac8c \ub429\ub2c8\ub2e4.", 
    "All Languages": "\ubaa8\ub4e0 \uc5b8\uc5b4", 
    "All Projects": "\ubaa8\ub4e0 \ud504\ub85c\uc81d\ud2b8", 
    "An error occurred while attempting to sign in via %s.": "%s \ub85c \ub85c\uadf8\uc778 \ud558\ub294 \ub3d9\uc548 \uc624\ub958 \ubc1c\uc0dd.", 
    "An error occurred while attempting to sign in via your social account.": "SNS\uacc4\uc815\uc744 \ud1b5\ud55c \ub85c\uadf8\uc778 \uc2dc\ub3c4 \uc911 \uc624\ub958 \ubc1c\uc0dd.", 
    "Avatar": "\uc544\ubc14\ud0c0", 
    "Cancel": "\ucde8\uc18c", 
    "Clear all": "\ubaa8\ub450 \uc9c0\uc6b0\uae30", 
    "Clear value": "\uac12 \uc9c0\uc6b0\uae30", 
    "Close": "\ub2eb\uae30", 
    "Code": "\ucf54\ub4dc", 
    "Collapse details": "\uc138\ubd80\uc0ac\ud56d \uc228\uae30\uae30", 
    "Congratulations! You have completed this task!": "\ucd95\ud558\ud569\ub2c8\ub2e4! \uc774 \uc791\uc5c5\uc744 \uc644\ub8cc\ud558\uc168\uc2b5\ub2c8\ub2e4!", 
    "Contact Us": "\uc5f0\ub77d\ud558\uae30", 
    "Contributors, 30 Days": "30\uc77c \uc774\uc0c1 \uae30\uc5ec\uc790", 
    "Creating new user accounts is prohibited.": "\uc0c8 \uc0ac\uc6a9\uc790 \uacc4\uc815\uc0dd\uc131\uc774 \uae08\uc9c0\ub418\uc5c8\uc2b5\ub2c8\ub2e4.", 
    "Delete": "\uc0ad\uc81c", 
    "Deleted successfully.": "\uc131\uacf5\uc801\uc73c\ub85c \uc0ad\uc81c\ud558\uc600\uc2b5\ub2c8\ub2e4.", 
    "Didn't receive an email? Check if it was accidentally filtered out as spam, or try requesting another copy of the email.": "Email\uc744 \ubc1b\uc9c0 \ubabb\ud558\uc168\ub098\uc694? \ud639\uc2dc \uc2a4\ud338\uc73c\ub85c \ud544\ud130\ub9c1 \ub418\uc5c8\ub294\uc9c0 \ud655\uc778 \ud558\uc2dc\uac70\ub098, \ub2e4\ub978 email \uc8fc\uc18c\ub85c \uc694\uccad\ud558\uc138\uc694.", 
    "Disabled": "\uc0ac\uc6a9 \uc548 \ud568", 
    "Discard changes.": "\ubcc0\uacbd\ub0b4\uc6a9 \ucde8\uc18c\ud558\uae30.", 
    "Edit Language": "\uc5b8\uc5b4 \ud3b8\uc9d1", 
    "Edit My Public Profile": "\uc790\uc2e0\uc758 \uacf5\uac1c \ud504\ub85c\ud30c\uc77c \ud3b8\uc9d1\ud558\uae30", 
    "Edit Project": "\ud504\ub85c\uc81d\ud2b8 \ud3b8\uc9d1", 
    "Edit User": "\uc0ac\uc6a9\uc790 \ud3b8\uc9d1", 
    "Edit the suggestion before accepting, if necessary": "\ud544\uc694\ud55c \uacbd\uc6b0 \uc81c\uc548\uc744 \uc218\ub77d \ud558\uae30\uc804\uc5d0 \ud3b8\uc9d1\uc744 \uc644\ub8cc\ud558\uc138\uc694.", 
    "Email": "\uc774\uba54\uc77c", 
    "Email Address": "Email \uc8fc\uc18c", 
    "Email Confirmation": "\uc774\uba54\uc77c \uc778\uc99d", 
    "Enter your email address, and we will send you a message with the special link to reset your password.": "\ub2f9\uc2e0\uc758 email\uc8fc\uc18c\ub97c \uc785\ub825\ud558\uc138\uc694, \ub2f9\uc2e0\uc758 \uc554\ud638\ub97c \ucd08\uae30\ud654 \ud560 \uc218 \uc788\ub294 \ub9c1\ud06c\uac00 \ud3ec\ud568\ub41c \uba54\uc138\uc9c0\ub97c \ub2f9\uc2e0\uc5d0\uac8c \ubcf4\ub0b4\uaca0\uc2b5\ub2c8\ub2e4.", 
    "Error while connecting to the server": "\uc11c\ubc84\uc5f0\uacb0 \uc911 \uc624\ub958 \ubc1c\uc0dd", 
    "Expand details": "\uc138\ubd80\uc0ac\ud56d \ubcf4\uae30", 
    "Find language by name, code": "\uc774\ub984\uacfc \ucf54\ub4dc\ub85c \uc5b8\uc5b4 \ucc3e\uae30", 
    "Find project by name, code": "\uc774\ub984\uacfc \ucf54\ub4dc\ub97c \uc0ac\uc6a9\ud558\uc5ec \ud504\ub85c\uc81d\ud2b8 \ucc3e\uae30", 
    "Find user by name, email, properties": "\uc774\ub984, \uc774\uba54\uc77c, \ub4f1\ub85d\uc815\ubcf4\ub97c \uc774\uc6a9\ud558\uc5ec  \uc0ac\uc6a9\uc790 \ucc3e\uae30", 
    "Full Name": "\uc804\uccb4 \uc774\ub984", 
    "Go back to browsing": "\uac80\uc0c9\uc0c1\ud0dc\ub85c \ub3cc\uc544\uac00\uae30", 
    "Go to the next string (Ctrl+.)<br/><br/>Also:<br/>Next page: Ctrl+Shift+.<br/>Last page: Ctrl+Shift+End": "\ub2e4\uc74c \ubb38\uc7a5\uc73c\ub85c \ub118\uc5b4\uac00\uae30(ctrl+.)<br/><br/>\ub610\ub294:<br/>\ub2e4\uc74c \ud398\uc774\uc9c0 : Ctrl+Shift+.<br/>\ub9c8\uc9c0\ub9c9\ud398\uc774\uc9c0: Ctrl+Shift+End", 
    "Go to the previous string (Ctrl+,)<br/><br/>Also:<br/>Previous page: Ctrl+Shift+,<br/>First page: Ctrl+Shift+Home": "\uc774\uc804\uc758 \ubb38\uc790\uc5f4\ub85c \ub3cc\uc544\uac00\uae30(Ctrl+,)<br/><br/>\ub610\ub294:<br/>\uc774\uc804 \ud398\uc774\uc9c0: Ctrl+Shift+,<br/>\uccab \ud398\uc774\uc9c0: Ctrl+Shift+Home", 
    "Hide": "\uc228\uae30\uae30", 
    "I forgot my password": "\ube44\ubc00\ubc88\ud638\ub97c \uc78a\uc5b4\ubc84\ub838\uc2b5\ub2c8\ub2e4", 
    "Ignore Files": "\ubb34\uc2dc\ud560 \ud30c\uc77c\ub4e4", 
    "Languages": "\uc5b8\uc5b4", 
    "Less": "\uc801\uac8c", 
    "LinkedIn": "\ub9c1\ud06c\ub4dc\uc778", 
    "LinkedIn profile URL": "\ub9c1\ud06c\ub4dc\uc778 \ud504\ub85c\ud30c\uc77c URL", 
    "Load More": "\ub354 \ubd88\ub7ec\uc624\uae30", 
    "Loading...": "\ubd88\ub7ec\uc624\ub294 \uc911...", 
    "Login / Password": "\ub85c\uadf8\uc778 / \ube44\ubc00\ubc88\ud638", 
    "More": "\ub354\uc6b1", 
    "My Public Profile": "\ub098\uc758 \uacf5\uac1c \ud504\ub85c\ud30c\uc77c", 
    "No": "\uc544\ub2c8\uc694", 
    "No activity recorded in a given period": "\uc8fc\uc5b4\uc9c4 \uae30\uac04\uc5d0 \uae30\ub85d\ub41c \ud65c\ub3d9 \uc5c6\uc74c", 
    "No results found": "\uacb0\uacfc\uac00 \uc5c6\uc2b5\ub2c8\ub2e4", 
    "No results.": "\uacb0\uacfc \uc5c6\uc74c.", 
    "No, thanks": "\uc544\ub2c8\uc694, \uad1c\ucc2e\uc2b5\ub2c8\ub2e4", 
    "Not found": "\ucc3e\uc9c0 \ubabb\ud568", 
    "Note: when deleting a user their contributions to the site, e.g. comments, suggestions and translations, are attributed to the anonymous user (nobody).": "\uc8fc\uc758: \uc0ac\uc774\ud2b8\uc5d0\uc11c \uae30\uc5ec\ud55c \uc0ac\uc6a9\uc790\ub97c \uc0ad\uc81c\ud558\ub294 \uacbd\uc6b0, \uc8fc\uc11d, \uc81c\uc548, \uadf8\ub9ac\uace0 \ubc88\uc5ed\ub4e4\uacfc \uac19\uc740 \uac83\ub4e4\uc758 \uc18d\uc131\uc774 (\uadf8 \ub204\uad6c\ub3c4 \uc544\ub2cc) \uc775\uba85\uc758 \uc0ac\uc6a9\uc790\ub85c \ucc98\ub9ac\ub429\ub2c8\ub2e4.", 
    "Number of Plurals": "\ubcf5\uc218 \uc758 \uac2f\uc218", 
    "Oops...": "\uc5fc\ubcd1\ud560..", 
    "Overview": "\uac1c\uc694", 
    "Password": "\ube44\ubc00\ubc88\ud638", 
    "Password changed, signing in...": "\ube44\ubc00\ubc88\ud638 \ubcc0\uacbd \uc644\ub8cc, \uc811\uc18d\ud558\ub294 \uc911...", 
    "Permissions": "\uad8c\ud55c", 
    "Personal description": "\uac1c\uc778\ubcc4 \uc0c1\uc138\uc815\ubcf4", 
    "Personal website URL": "\uac1c\uc778 \uc6f9\uc0ac\uc774\ud2b8 URL", 
    "Please follow that link to continue the account creation.": "\uacc4\uc18d\ud574\uc11c \uacc4\uc815 \uc0dd\uc131\uc744 \uc9c4\ud589\ud558\uc2dc\ub824\uba74 \uadf8 \ub9c1\ud06c\ub97c \ub530\ub77c\uac00 \uc8fc\uc138\uc694.", 
    "Please follow that link to continue the password reset procedure.": "\ube44\ubc00\ubc88\ud638 \uc7ac\uc124\uc815 \uacfc\uc815\uc744 \uacc4\uc18d \ud558\uc2dc\ub824\uba74 \ub9c1\ud06c\ub97c \ub530\ub77c \uac00\uc8fc\uc138\uc694.", 
    "Please select a valid user.": "\uc720\ud6a8\ud55c \uc0ac\uc6a9\uc790\ub97c \uc120\ud0dd\ud558\uc2ed\uc2dc\uc624.", 
    "Plural Equation": "\ubcf5\uc218 \uc2dd", 
    "Plural form %(index)s": "%(index)s \uc758 \ubcf5\uc218\ud615", 
    "Preview will be displayed here.": "\ubbf8\ub9ac\ubcf4\uae30\ub294 \uc5ec\uae30\uc5d0 \ud45c\uc2dc\ub420 \uac83\uc785\ub2c8\ub2e4.", 
    "Project / Language": "\ud504\ub85c\uc81d\ud2b8 / \uc5b8\uc5b4", 
    "Project Tree Style": "\ud504\ub85c\uc81d\ud2b8 \ud2b8\ub9ac \uc2a4\ud0c0\uc77c", 
    "Provide optional comment (will be publicly visible)": "\uc120\ud0dd\uc801 \uc8fc\uc11d \uc81c\uacf5 (\uacf5\uac1c\uc801\uc73c\ub85c \ud45c\uc2dc\ub428)", 
    "Public Profile": "\uacf5\uac1c \ud504\ub85c\ud30c\uc77c", 
    "Quality Checks": "\ud004\ub7ec\ud2f0 \uccb4\ud06c", 
    "Reject": "\uac70\uc808", 
    "Reload page": "\ud398\uc774\uc9c0 \ub2e4\uc2dc \ubd88\ub7ec\uc624\uae30", 
    "Repeat Password": "\ube44\ubc00\ubc88\ud638 \ud655\uc778", 
    "Resend Email": "Email \ub2e4\uc2dc \ubcf4\ub0b4\uae30", 
    "Reset Password": "\ube44\ubc00\ubc88\ud638 \ucd08\uae30\ud654", 
    "Reset Your Password": "\ube44\ubc00\ubc88\ud638 \ucd08\uae30\ud654", 
    "Save": "\uc800\uc7a5", 
    "Saved successfully.": "\uc131\uacf5\uc801\uc73c\ub85c \uc800\uc7a5\ud588\uc2b5\ub2c8\ub2e4.", 
    "Score Change": "\uc810\uc218 \ubcc0\uacbd", 
    "Screenshot Search Prefix": "\uc2a4\ud06c\ub9b0\uc0f7 \ucc3e\uae30\uc6a9 \uc811\ub450\uc5b4", 
    "Search Languages": "\uc5b8\uc5b4 \uac80\uc0c9", 
    "Search Projects": "\ud504\ub85c\uc81d\ud2b8\ub97c \ucc3e\ub2e4", 
    "Search Users": "\uc0ac\uc6a9\uc790 \ucc3e\uae30", 
    "Select...": "\uc120\ud0dd\ud558\uae30...", 
    "Send Email": "Email \ubcf4\ub0b4\uae30", 
    "Sending email to %s...": "%s\uc5d0\uac8c \uc774\uba54\uc77c \uc804\uc1a1 \uc911...", 
    "Server error": "\uc11c\ubc84 \uc624\ub958", 
    "Set New Password": "\uc0c8 \ube44\ubc00\ubc88\ud638 \uc124\uc815", 
    "Set a new password": "\uc0c8 \ube44\ubc00\ubc88\ud638 \uc124\uc815", 
    "Settings": "\uc124\uc815", 
    "Short Bio": "\uc9e7\uc740 \uacbd\ub825", 
    "Show": "\ubcf4\uae30", 
    "Sign In": "\ub85c\uadf8\uc778", 
    "Sign In With %s": "%s \ub85c \uc811\uc18d\ud558\uae30", 
    "Sign In With...": "\uc811\uc18d\ud560 \uacc4\uc815\uc740...", 
    "Sign Up": "\uac00\uc785\ud558\uae30", 
    "Sign in as an existing user": "\uae30\uc874 \uc0ac\uc6a9\uc790\ub85c \uc811\uc18d\ud558\uae30", 
    "Sign up as a new user": "\uc2e0\uaddc \uc0ac\uc6a9\uc790\ub85c \uac00\uc785\ub4f1\ub85d", 
    "Signed in. Redirecting...": "\ub85c\uadf8\uc778 \uc644\ub8cc. \ub9ac\ub2e4\uc774\ub809\ud305 \uc911...", 
    "Signing in with an external service for the first time will automatically create an account for you.": "\uc678\ubd80 \uc11c\ube44\uc2a4\ub85c \ucd5c\ucd08 \uc811\uc18d\uc2dc \uc790\ub3d9\uc73c\ub85c \uacc4\uc815\uc774 \uc0dd\uc131\ub429\ub2c8\ub2e4.", 
    "Similar translations": "\uc720\uc0ac\ud55c \ubc88\uc5ed", 
    "Social Services": "SNS", 
    "Social Verification": "SNS \uc778\uc99d", 
    "Source Language": "\uc18c\uc2a4 \uc5b8\uc5b4", 
    "Special Characters": "\ud2b9\uc218\ubb38\uc790", 
    "String Errors Contact": "\ubb38\uc790\uc5f4 \uc5d0\ub7ec \uc5f0\uacb0", 
    "Suggested": "\ucd94\ucc9c", 
    "Team": "\ud300", 
    "The password reset link was invalid, possibly because it has already been used. Please request a new password reset.": "\ube44\ubc00\ubc88\ud638 \ucd08\uae30\ud654 \ub9c1\ud06c\uac00 \uc720\ud6a8\ud558\uc9c0 \uc54a\uc2b5\ub2c8\ub2e4, \uc544\ub9c8\ub3c4 \uc774\ubbf8 \uc0ac\uc6a9\ub41c \uac83 \uac19\uc2b5\ub2c8\ub2e4. \ube44\ubc00\ubc88\ud638 \ucd08\uae30\ud654\ub97c \ub2e4\uc2dc \uc694\uccad \ud558\uc138\uc694.", 
    "The server seems down. Try again later.": "\uc11c\ubc84\uac00 \ub2e4\uc6b4\ub41c\uac83\uc73c\ub85c \ubcf4\uc785\ub2c8\ub2e4. \ub098\uc911\uc5d0 \ub2e4\uc2dc \uc2dc\ub3c4\ud558\uc138\uc694.", 
    "There are unsaved changes. Do you want to discard them?": "\ubcc0\uacbd\uc0ac\ud56d\uc774 \uc800\uc7a5\ub418\uc9c0 \uc54a\uc558\uc2b5\ub2c8\ub2e4. \ubcc0\uacbd\uc0ac\ud56d\uc744 \ucde8\uc18c \ud558\uc2dc\uaca0\uc2b5\ub2c8\uae4c?", 
    "There is %(count)s language.": [
      "\uc5ec\uae30\uc5d0 %(count)s \uac1c\uc758 \uc5b8\uc5b4\uac00 \uc788\uc2b5\ub2c8\ub2e4. \uc544\ub798\uc5d0 \ucd5c\uadfc\uc5d0 \ucd94\uac00 \ub41c \uac83\ub4e4\uc774 \uc788\uc2b5\ub2c8\ub2e4."
    ], 
    "There is %(count)s project.": [
      "\uc5ec\uae30\uc5d0 %(count)s \uac1c\uc758 \ud504\ub85c\uc81d\ud2b8\uac00 \uc874\uc7ac\ud569\ub2c8\ub2e4. \uc544\ub798\uc5d0 \ucd5c\uadfc\uc5d0 \ucd94\uac00 \ub41c \uac83\ub4e4\uc774 \uc788\uc2b5\ub2c8\ub2e4."
    ], 
    "There is %(count)s user.": [
      "\uc5ec\uae30\uc5d0 %(count)s \uba85\uc758 \uc0ac\uc6a9\uc790\uac00 \uc874\uc7ac\ud569\ub2c8\ub2e4. \uc544\ub798\uc5d0 \ucd5c\uadfc\uc5d0 \ucd94\uac00 \ub41c \uac83\ub4e4\uc774 \uc788\uc2b5\ub2c8\ub2e4."
    ], 
    "This email confirmation link expired or is invalid.": "\uc774 \uc774\uba54\uc77c \uc778\uc99d\ub9c1\ud06c\ub294 \uc720\ud6a8\ud558\uc9c0 \uc54a\uac70\ub098 \ub9cc\ub8cc\ub418\uc5c8\uc2b5\ub2c8\ub2e4.", 
    "This string no longer exists.": "\uc774 \ubb38\uc790\uc5f4\uc740 \ub354 \uc774\uc0c1 \uc874\uc7ac\ud558\uc9c0 \uc54a\uc2b5\ub2c8\ub2e4.", 
    "To set or change your avatar for your email address (%(email)s), please go to gravatar.com.": "\ub2f9\uc2e0\uc758 \uc774\uba54\uc77c \uc8fc\uc18c (%(email)s) \uc5d0 \ud574\ub2f9\ud558\ub294 \uc544\ubc14\ud0c0\ub97c \ubcc0\uacbd\ud558\uac70\ub098 \uc124\uc815\ud558\uae30 \uc704\ud574\uc11c\ub294 gravartar.com\uc73c\ub85c \uc774\ub3d9 \ud558\uc138\uc694.", 
    "Translated": "\ubc88\uc5ed\ub428", 
    "Try again": "\ub2e4\uc2dc \uc2dc\ub3c4", 
    "Twitter": "\ud2b8\uc704\ud130", 
    "Twitter username": "\ud2b8\uc704\ud130 \uc0ac\uc6a9\uc790\uc774\ub984", 
    "Type to search": "\uac80\uc0c9\ud560 \uac83\uc744 \uc785\ub825\ud558\uc2dc\uc624", 
    "Updating data": "\ub370\uc774\ud0c0 \uc5c5\ub370\uc774\ud2b8\uc911", 
    "Use the search form to find the language, then click on a language to edit.": "\uc5b8\uc5b4\ub97c \ucc3e\uae30\uc704\ud574 \uac80\uc0c9\ucc3d\uc744 \uc0ac\uc6a9\ud558\uace0, \uadf8\ub9ac\uace0 \uc5b8\uc5b4\ub97c \ud3b8\uc9d1\ud558\uae30 \uc704\ud574 \ud074\ub9ad\ud55c\ub2e4.", 
    "Use the search form to find the project, then click on a project to edit.": "\ud504\ub85c\uc81d\ud2b8\ub97c \ucc3e\uae30 \uc704\ud574 \uac80\uc0c9\ucc3d\uc744 \uc0ac\uc6a9\ud558\uace0, \ud3b8\uc9d1\ud558\ub824\uba74 \ud574\ub2f9 \ud504\ub85c\uc81d\ud2b8\ub97c \ud074\ub9ad\ud558\uc138\uc694.", 
    "Use the search form to find the user, then click on a user to edit.": "\uc0ac\uc6a9\uc790\ub97c \ucc3e\uae30 \uc704\ud574 \uac80\uc0c9\ucc3d\uc744 \uc774\uc6a9\ud558\uace0, \ud3b8\uc9d1\uc744 \uc704\ud574 \ud574\ub2f9 \uc0ac\uc6a9\uc790\ub97c \ud074\ub9ad\ud558\uc138\uc694.", 
    "Username": "\uc0ac\uc6a9\uc790 \uc774\ub984", 
    "We have sent an email containing the special link to <span>%s</span>": "<span>%s</span>\ub85c \ub9c1\ud06c\uac00 \ud3ec\ud568\ub41c \uc774\uba54\uc77c\uc744 \ubcf4\ub0c8\uc2b5\ub2c8\ub2e4.", 
    "We have sent an email containing the special link to <span>%s</span>. Please check your spam folder if you do not see the email.": "<span>%s</span>\ub85c \ud2b9\ubcc4\ud55c \ub9c1\ud06c\uac00 \ud3ec\ud568\ub41c \uc774\uba54\uc77c\uc744 \ubcf4\ub0c8\uc2b5\ub2c8\ub2e4 \ub9cc\uc57d \uc774\uba54\uc77c \uc218\uc2e0\ub418\uc9c0 \uc54a\uc73c\uba74 \uc2a4\ud338\ud3f4\ub354\ub97c \uccb4\ud06c\ud558\uc138\uc694.", 
    "We have sent an email containing the special link to the address used to register this account. Please check your spam folder if you do not see the email.": "\ud574\ub2f9 \uacc4\uc815\uc744 \ub4f1\ub85d\ud558\uae30 \uc704\ud574 \uc0ac\uc6a9\ub41c \uc8fc\uc18c\ub85c \ud2b9\ubcc4\ud55c \ub9c1\ud06c\uac00 \ud3ec\ud568\ub41c \uc774\uba54\uc77c\uc744 \ubcf4\ub0c8\uc2b5\ub2c8\ub2e4. \ub9cc\uc57d \uc774\uba54\uc77c\uc774 \uc218\uc2e0\ub418\uc9c0 \uc54a\uc558\uc73c\uba74 \uc2a4\ud338\ud3f4\ub354\ub97c \ud655\uc778 \ud558\uc138\uc694.", 
    "Website": "\uc6f9\uc0ac\uc774\ud2b8", 
    "Why are you part of our translation project? Describe yourself, inspire others!": "\ubcf8 \ubc88\uc5ed \ud504\ub85c\uc81d\ud2b8\uc758 \uc77c\uc6d0\uc774 \ub418\ub824\ub294 \uc774\uc720\ub97c \uc54c\ub824\uc8fc\uc2dc\uaca0\uc5b4\uc694? \uc880 \ub354 \ubcf8\uc778\uc5d0 \ub300\ud574\uc11c \uc54c\ub824\uc8fc\uc2dc\uace0, \ub2e4\ub978 \uc0ac\ub78c\ub4e4\uc5d0\uac8c\ub3c4 \uc790\uadf9\uc744 \uc8fc\uc138\uc694!", 
    "Yes": "\ub124", 
    "You have unsaved changes in this string. Navigating away will discard those changes.": "\uc774 \ubb38\uc790\uc5f4\uc5d0 \uc800\uc7a5\ub418\uc9c0 \uc54a\uc740 \ubcc0\uacbd \uc0ac\ud56d\uc774 \uc788\uc2b5\ub2c8\ub2e4. \ub2e4\ub978 \ud398\uc774\uc9c0\ub85c \uc774\ub3d9\uc2dc \uadf8 \ubcc0\uacbd \uc0ac\ud56d\uc744 \ucde8\uc18c\ud569\ub2c8\ub2e4.", 
    "Your Full Name": "\uc804\uccb4 \uc774\ub984", 
    "Your LinkedIn profile URL": "\ub9c1\ud06c\ub4dc\uc778 \ud504\ub85c\ud30c\uc77c URL", 
    "Your Personal website/blog URL": "\uac1c\uc778 \uc6f9\uc0ac\uc774\ud2b8/\ube14\ub85c\uadf8 URL", 
    "Your Twitter username": "\ud2b8\uc704\ud130 \uc0ac\uc6a9\uc790 \uc774\ub984", 
    "Your account is inactive because an administrator deactivated it.": "\uad00\ub9ac\uc790\uc5d0 \uc758\ud574 \uacc4\uc815\uc774 \ube44\ud65c\uc131\ud654 \ub418\uc5c8\uc2b5\ub2c8\ub2e4.", 
    "Your account needs activation.": "\ud574\ub2f9 \uacc4\uc815\uc744 \ud65c\uc131\ud654 \uc2dc\ucf1c \uc8fc\uc138\uc694.", 
    "disabled": "\uc0ac\uc6a9 \uc548 \ud568", 
    "some anonymous user": "\uc57d\uac04\uc758 \uc775\uba85 \uc0ac\uc6a9\uc790", 
    "someone": "\ub204\uad70\uac00"
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

