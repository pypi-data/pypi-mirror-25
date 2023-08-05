

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
    "#%(position)s": "#%(position)s", 
    "%(count)s language matches your query.": [
      "%(count)s \u062a\u0649\u0644 \u0633\u06c8\u0631\u06c8\u0634\u062a\u06c8\u0631\u06c8\u0634\u0649\u06ad\u0649\u0632\u06af\u06d5 \u0645\u0627\u0633 \u0643\u06d0\u0644\u0649\u062f\u06c7."
    ], 
    "%(count)s project matches your query.": [
      "\u0633\u06c8\u0631\u06c8\u0634\u062a\u06c8\u0631\u06c8\u0634\u0649\u06ad\u0649\u0632\u06af\u06d5 %(count)s \u0642\u06c7\u0631\u06c7\u0644\u06c7\u0634 \u0645\u0627\u0633 \u0643\u06d0\u0644\u0649\u062f\u06c7."
    ], 
    "%(count)s user matches your query.": [
      "\u0633\u06c8\u0631\u06c8\u0634\u062a\u06c8\u0631\u06c8\u0634\u0649\u06ad\u0649\u0632\u06af\u06d5 %(count)s \u0626\u0649\u0634\u0644\u06d5\u062a\u0643\u06c8\u0686\u0649 \u0645\u0627\u0633 \u0643\u06d0\u0644\u0649\u062f\u06c7."
    ], 
    "%(timeSince)s via file upload": "%(timeSince)s \u0626\u0627\u0631\u0642\u0649\u0644\u0649\u0642 \u06be\u06c6\u062c\u062c\u06d5\u062a \u064a\u0648\u0644\u0644\u0627\u0634", 
    "%s word": [
      "%s \u0633\u06c6\u0632"
    ], 
    "%s's accepted suggestions": "%s \u0646\u0649\u06ad \u0642\u0648\u0628\u06c7\u0644 \u0642\u0649\u0644\u0649\u0646\u063a\u0627\u0646 \u062a\u06d5\u0643\u0644\u0649\u067e\u0644\u0649\u0631\u0649", 
    "%s's overwritten submissions": "%s \u0646\u0649\u06ad \u0642\u0627\u067e\u0644\u0649\u06cb\u06d5\u062a\u0643\u06d5\u0646 \u062a\u0627\u067e\u0634\u06c7\u0631\u063a\u0627\u0646\u0644\u0649\u0631\u0649", 
    "%s's pending suggestions": "%s \u0646\u0649\u06ad \u0643\u06c8\u062a\u06c8\u06cb\u0627\u062a\u0642\u0627\u0646 \u062a\u06d5\u0643\u0644\u0649\u067e\u0644\u0649\u0631\u0649", 
    "%s's rejected suggestions": "%s \u0646\u0649\u06ad \u0631\u06d5\u062a \u0642\u0649\u0644\u0649\u0646\u063a\u0627\u0646 \u062a\u06d5\u0643\u0644\u0649\u067e\u0644\u0649\u0631\u0649", 
    "%s's submissions": "%s \u0646\u0649\u06ad \u062a\u0627\u067e\u0634\u06c7\u0631\u063a\u0627\u0646\u0644\u0649\u0631\u0649", 
    "Accept": "\u0642\u0648\u0634\u06c7\u0644", 
    "Account Activation": "\u06be\u06d0\u0633\u0627\u0628\u0627\u062a \u0626\u0627\u0643\u062a\u0649\u067e\u0644\u0627\u0634", 
    "Account Inactive": "\u06be\u06d0\u0633\u0627\u0628\u0627\u062a \u0686\u06d5\u0643\u0644\u06d5\u0646\u06af\u06d5\u0646", 
    "Active": "\u0626\u0627\u0643\u062a\u0649\u067e", 
    "Add Language": "\u062a\u0649\u0644 \u0642\u0648\u0634", 
    "Add Project": "\u0642\u06c7\u0631\u06c7\u0644\u06c7\u0634 \u0642\u0648\u0634", 
    "Add User": "\u0626\u0649\u0634\u0644\u06d5\u062a\u0643\u06c8\u0686\u0649 \u0642\u0648\u0634", 
    "Administrator": "\u0628\u0627\u0634\u0642\u06c7\u0631\u063a\u06c7\u0686\u0649", 
    "After changing your password you will sign in automatically.": "\u0626\u0649\u0645\u0646\u0649 \u0626\u06c6\u0632\u06af\u06d5\u0631\u062a\u0643\u06d5\u0646\u062f\u0649\u0646 \u0643\u06d0\u064a\u0649\u0646 \u0626\u06c6\u0632\u0644\u06c8\u0643\u0649\u062f\u0649\u0646 \u062a\u0649\u0632\u0649\u0645\u063a\u0627 \u0643\u0649\u0631\u0649\u0633\u0649\u0632.", 
    "All Languages": "\u0628\u0627\u0631\u0644\u0649\u0642 \u062a\u0649\u0644\u0644\u0627\u0631", 
    "All Projects": "\u06be\u06d5\u0645\u0645\u06d5 \u0642\u06c7\u0631\u06c7\u0644\u06c7\u0634\u0644\u0627\u0631", 
    "An error occurred while attempting to sign in via %s.": "\u202b%s \u0633\u0627\u0644\u0627\u06be\u0649\u064a\u0649\u062a\u0649\u062f\u06d5 \u062a\u0649\u0632\u0649\u0645\u063a\u0627 \u0643\u0649\u0631\u06af\u06d5\u0646\u062f\u06d5 \u062e\u0627\u062a\u0627\u0644\u0649\u0642 \u0643\u06c6\u0631\u06c8\u0644\u062f\u0649.", 
    "An error occurred while attempting to sign in via your social account.": "\u0626\u0649\u062c\u062a\u0649\u0645\u0627\u0626\u0649\u064a \u0626\u0627\u0644\u0627\u0642\u06d5 \u06be\u06d0\u0633\u0627\u0628\u0627\u062a\u0649\u06ad\u0649\u0632 \u0626\u0627\u0631\u0642\u0649\u0644\u0649\u0642 \u062a\u0649\u0632\u0649\u0645\u063a\u0627 \u0643\u0649\u0631\u0649\u0634\u0646\u0649 \u0633\u0649\u0646\u0649\u063a\u0627\u0646\u062f\u0627 \u062e\u0627\u062a\u0627\u0644\u0649\u0642 \u0643\u06c6\u0631\u06c8\u0644\u062f\u0649.", 
    "Avatar": "\u0628\u0627\u0634 \u0633\u06c8\u0631\u06d5\u062a", 
    "Cancel": "\u06cb\u0627\u0632 \u0643\u06d5\u0686", 
    "Clear all": "\u06be\u06d5\u0645\u0645\u0649\u0646\u0649 \u062a\u0627\u0632\u0649\u0644\u0627", 
    "Clear value": "\u0642\u0649\u0645\u0645\u0649\u062a\u0649\u0646\u0649 \u062a\u0627\u0632\u0649\u0644\u0627", 
    "Close": "\u062a\u0627\u0642\u0627", 
    "Code": "\u0643\u0648\u062f", 
    "Collapse details": "\u062a\u06d5\u067e\u0633\u0649\u0644\u0627\u062a\u0649\u0646\u0649 \u0642\u0627\u062a\u0644\u0627", 
    "Congratulations! You have completed this task!": "\u0645\u06c7\u0628\u0627\u0631\u06d5\u0643 \u0628\u0648\u0644\u0633\u06c7\u0646! \u0628\u06c7 \u06cb\u06d5\u0632\u0649\u067e\u0649\u0646\u0649 \u062a\u0627\u0645\u0627\u0645\u0644\u0649\u062f\u0649\u06ad\u0649\u0632!", 
    "Contact Us": "\u0628\u0649\u0632 \u0628\u0649\u0644\u06d5\u0646 \u0626\u0627\u0644\u0627\u0642\u0649\u0644\u0649\u0634\u0649\u06ad", 
    "Contributors, 30 Days": "\u062a\u06c6\u06be\u067e\u0649\u0643\u0627\u0631\u0644\u0627\u0631\u060c 30 \u0643\u06c8\u0646", 
    "Creating new user accounts is prohibited.": "\u064a\u06d0\u06ad\u0649 \u0626\u0649\u0634\u0644\u06d5\u062a\u0643\u06c8\u0686\u0649\u0646\u0649 \u062e\u06d5\u062a\u0644\u0649\u062a\u0649\u0634 \u0686\u06d5\u0643\u0644\u06d5\u0646\u06af\u06d5\u0646.", 
    "Delete": "\u0626\u06c6\u0686\u06c8\u0631", 
    "Deleted successfully.": "\u0645\u06c7\u06cb\u06d5\u067e\u067e\u06d5\u0642\u0649\u064a\u06d5\u062a\u0644\u0649\u0643 \u0626\u06c6\u0686\u06c8\u0631\u06c8\u0644\u062f\u0649.", 
    "Didn't receive an email? Check if it was accidentally filtered out as spam, or try requesting another copy of the email.": "\u062a\u0648\u0631\u062e\u06d5\u062a\u0646\u0649 \u062a\u0627\u067e\u0634\u06c7\u0631\u06c7\u06cb\u0627\u0644\u0645\u0649\u062f\u0649\u06ad\u0649\u0632\u0645\u06c7\u061f \u0626\u06d5\u062e\u0644\u06d5\u062a \u062e\u06d5\u062a\u0644\u06d5\u0631 \u0642\u0627\u062a\u0627\u0631\u0649\u063a\u0627 \u0643\u0649\u0631\u0649\u067e \u0642\u0627\u0644\u062f\u0649\u0645\u06c7 \u062a\u06d5\u0643\u0634\u06c8\u0631\u06c8\u067e \u0628\u06d0\u0642\u0649\u06ad \u064a\u0627\u0643\u0649 \u062a\u0648\u0631\u062e\u06d5\u062a\u0646\u0649 \u0642\u0627\u064a\u062a\u0627 \u064a\u0648\u0644\u0644\u0627\u0634\u0646\u0649 \u0626\u0649\u0644\u062a\u0649\u0645\u0627\u0633 \u0642\u0649\u0644\u0649\u06ad.", 
    "Disabled": "\u0686\u06d5\u0643\u0644\u06d5\u0646\u06af\u06d5\u0646", 
    "Discard changes.": "\u0626\u06c6\u0632\u06af\u06d5\u0631\u062a\u0649\u0634\u0644\u06d5\u0631\u0646\u0649 \u062a\u0627\u0634\u0644\u0649\u06cb\u06d5\u062a", 
    "Edit Language": "\u062a\u0649\u0644 \u062a\u06d5\u06be\u0631\u0649\u0631", 
    "Edit My Public Profile": "\u0626\u0627\u0645\u0645\u0649\u06cb\u0649 \u0633\u06d5\u067e\u0644\u0649\u0645\u06d5 \u06be\u06c6\u062c\u062c\u0649\u062a\u0649\u0645\u0646\u0649 \u062a\u06d5\u06be\u0631\u0649\u0631\u0644\u06d5", 
    "Edit Project": "\u0642\u06c7\u0631\u06c7\u0644\u06c7\u0634 \u062a\u06d5\u06be\u0631\u0649\u0631", 
    "Edit User": "\u0626\u0649\u0634\u0644\u06d5\u062a\u0643\u06c8\u0686\u0649 \u062a\u06d5\u06be\u0631\u0649\u0631", 
    "Edit the suggestion before accepting, if necessary": "\u0626\u06d5\u06af\u06d5\u0631 \u0632\u06c6\u0631\u06c8\u0631 \u0628\u0648\u0644\u0633\u0627\u060c \u0642\u0648\u0644\u0644\u0649\u0646\u0649\u0634\u062a\u0649\u0646 \u0626\u0649\u0644\u06af\u0649\u0631\u0649 \u062a\u06d5\u06cb\u0633\u0649\u064a\u06d5\u0646\u0649 \u062a\u06d5\u06be\u0631\u0649\u0631\u0644\u06d5\u06ad", 
    "Email": "\u062a\u0648\u0631\u062e\u06d5\u062a", 
    "Email Address": "\u062a\u0648\u0631\u062e\u06d5\u062a \u0626\u0627\u062f\u0631\u06d0\u0633\u0649", 
    "Email Confirmation": "\u062a\u0648\u0631\u062e\u06d5\u062a \u062c\u06d5\u0632\u0645\u0644\u06d5\u0634", 
    "Enter your email address, and we will send you a message with the special link to reset your password.": "\u062a\u0648\u0631\u062e\u06d5\u062a \u0626\u0627\u062f\u0631\u06d0\u0633\u0649\u06ad\u0649\u0632\u0646\u0649 \u0643\u0649\u0631\u06af\u06c8\u0632\u06c8\u06ad\u060c \u0628\u0649\u0632 \u0626\u0649\u0645\u0646\u0649 \u0642\u0627\u064a\u062a\u0627 \u0626\u06c6\u0632\u06af\u06d5\u0631\u062a\u0649\u062f\u0649\u063a\u0627\u0646 \u0626\u06c7\u0644\u0627\u0646\u0645\u0649\u0646\u0649 \u0626\u06c6\u0632 \u0626\u0649\u0686\u0649\u06af\u06d5 \u0626\u0627\u0644\u063a\u0627\u0646 \u062a\u0648\u0631\u062e\u06d5\u062a\u0646\u0649 \u062e\u06d5\u062a \u0633\u0627\u0646\u062f\u06c7\u0642\u0649\u06ad\u0649\u0632\u063a\u0627 \u064a\u0648\u0644\u0644\u0627\u064a\u0645\u0649\u0632.", 
    "Error while connecting to the server": "\u0645\u06c7\u0644\u0627\u0632\u0649\u0645\u06d0\u062a\u0649\u0631\u063a\u0627 \u0628\u0627\u063a\u0644\u0627\u0646\u063a\u0627\u0646\u062f\u0627 \u062e\u0627\u062a\u0627\u0644\u0649\u0642 \u0643\u06c6\u0631\u06c8\u0644\u062f\u0649", 
    "Expand details": "\u062a\u06d5\u067e\u0633\u0649\u0644\u0627\u062a\u0649\u0646\u0649 \u064a\u0627\u064a", 
    "File types": "\u06be\u06c6\u062c\u062c\u06d5\u062a \u062a\u0649\u067e\u0649", 
    "Filesystems": "\u06be\u06c6\u062c\u062c\u06d5\u062a \u0633\u0649\u0633\u062a\u06d0\u0645\u0649\u0633\u0649", 
    "Find language by name, code": "\u062a\u0649\u0644\u0646\u0649 \u0626\u0649\u0633\u0645\u0649 \u064a\u0627\u0643\u0649 \u0643\u0648\u062f\u0649 \u0628\u0648\u064a\u0649\u0686\u06d5 \u0626\u0649\u0632\u062f\u06d5", 
    "Find project by name, code": "\u0642\u06c7\u0631\u06c7\u0644\u06c7\u0634\u0646\u0649 \u0626\u0649\u0633\u0645\u0649\u060c \u0643\u0648\u062f\u0649 \u0628\u0648\u064a\u0649\u0686\u06d5 \u0626\u0649\u0632\u062f\u06d5", 
    "Find user by name, email, properties": "\u0626\u0649\u0634\u0644\u06d5\u062a\u0643\u06c8\u0686\u0649\u0646\u0649 \u0626\u0649\u0633\u0645\u0649\u060c \u062a\u0648\u0631\u062e\u06d5\u062a\u060c \u062e\u0627\u0633\u0644\u0649\u0642 \u0628\u0648\u064a\u0649\u0686\u06d5 \u0626\u0649\u0632\u062f\u06d5", 
    "Full Name": "\u062a\u0648\u0644\u06c7\u0642 \u0626\u0627\u062a\u0649", 
    "Go back to browsing": "\u0643\u06c6\u0632 \u064a\u06c8\u06af\u06c8\u0631\u062a\u06c8\u0634\u0643\u06d5 \u0642\u0627\u064a\u062a", 
    "Go to the next string (Ctrl+.)<br/><br/>Also:<br/>Next page: Ctrl+Shift+.<br/>Last page: Ctrl+Shift+End": "\u0643\u06d0\u064a\u0649\u0646\u0643\u0649 \u062a\u0649\u0632\u0649\u0642\u0642\u0627 \u064a\u06c6\u062a\u0643\u0649\u0644\u0649\u0634\u062a\u06d5 (Ctrl+.)<br/><br/> \u064a\u06d5\u0646\u06d5: <br/>\u0643\u06d0\u064a\u0649\u0646\u0643\u0649 \u0628\u06d5\u062a: Ctrl+Shift+.<br/>\u0626\u0627\u062e\u0649\u0631\u0642\u0649 \u0628\u06d5\u062a: Ctrl+Shift+End", 
    "Go to the previous string (Ctrl+,)<br/><br/>Also:<br/>Previous page: Ctrl+Shift+,<br/>First page: Ctrl+Shift+Home": "\u0626\u0627\u0644\u062f\u0649\u0646\u0642\u0649 \u062a\u0649\u0632\u0649\u0642\u0642\u0627 \u064a\u06c6\u062a\u0643\u0649\u0644\u0649\u0634\u062a\u06d5 (Ctrl+,)<br/><br/>\u064a\u06d5\u0646\u06d5:<br/>\u0626\u0627\u0644\u062f\u0649\u0646\u0642\u0649 \u0628\u06d5\u062a: Ctrl+Shift+,<br/>\u0628\u0649\u0631\u0649\u0646\u0686\u0649 \u0628\u06d5\u062a: Ctrl+Shift+Home", 
    "Hide": "\u064a\u0648\u0634\u06c7\u0631", 
    "Hide disabled": "\u064a\u0648\u0634\u06c7\u0631\u06c7\u0634 \u0686\u06d5\u0643\u0644\u06d5\u0646\u06af\u06d5\u0646", 
    "I forgot my password": "\u0626\u0649\u0645\u0646\u0649 \u0626\u06c7\u0646\u06c7\u062a\u062a\u06c7\u0645", 
    "Ignore Files": "\u06be\u06c6\u062c\u062c\u06d5\u062a\u0643\u06d5 \u067e\u06d5\u0631\u06cb\u0627 \u0642\u0649\u0644\u0645\u0627", 
    "Languages": "\u062a\u0649\u0644\u0644\u0627\u0631", 
    "Less": "\u062a\u06d0\u062e\u0649\u0645\u06c7 \u0626\u0627\u0632", 
    "LinkedIn": "LinkedIn", 
    "LinkedIn profile URL": "\u202bLinkedIn \u0633\u06d5\u067e\u0644\u0649\u0645\u06d5 \u06be\u06c6\u062c\u062c\u06d5\u062a \u062a\u0648\u0631 \u0626\u0627\u062f\u0631\u06d0\u0633\u0649", 
    "Load More": "\u062a\u06d0\u062e\u0649\u0645\u06c7 \u0643\u06c6\u067e \u064a\u06c8\u0643\u0644\u06d5", 
    "Loading...": "\u064a\u06c8\u0643\u0644\u06d5\u06cb\u0627\u062a\u0649\u062f\u06c7\u2026", 
    "Login / Password": "\u062a\u0649\u0632\u0649\u0645\u063a\u0627 \u0643\u0649\u0631 /\u0626\u0649\u0645", 
    "More": "\u062a\u06d0\u062e\u0649\u0645\u06c7 \u0643\u06c6\u067e", 
    "More...": "\u062a\u06d0\u062e\u0649\u0645\u06c7 \u0643\u06c6\u067e\u2026", 
    "My Public Profile": "\u0626\u0627\u0645\u0645\u0649\u06cb\u0649 \u0633\u06d5\u067e\u0644\u0649\u0645\u06d5 \u06be\u06c6\u062c\u062c\u0649\u062a\u0649\u0645", 
    "No": "\u064a\u0627\u0642", 
    "No activity recorded in a given period": "\u0628\u06d0\u0631\u0649\u0644\u06af\u06d5\u0646 \u0645\u06d5\u0632\u06af\u0649\u0644\u062f\u06d5 \u0626\u0627\u0643\u062a\u0649\u067e \u062e\u0627\u062a\u0649\u0631\u06d5 \u064a\u0648\u0642", 
    "No results found": "\u0646\u06d5\u062a\u0649\u062c\u06d5 \u062a\u06d0\u067e\u0649\u0644\u0645\u0649\u062f\u0649", 
    "No results.": "\u0646\u06d5\u062a\u0649\u062c\u06d5 \u064a\u0648\u0642.", 
    "No, thanks": "\u064a\u0627\u0642\u060c \u0631\u06d5\u06be\u0645\u06d5\u062a", 
    "Not found": "\u062a\u06d0\u067e\u0649\u0644\u0645\u0649\u062f\u0649", 
    "Note: when deleting a user their contributions to the site, e.g. comments, suggestions and translations, are attributed to the anonymous user (nobody).": "\u062f\u0649\u0642\u0642\u06d5\u062a: \u0626\u0649\u0634\u0644\u06d5\u062a\u0643\u06c8\u0686\u0649 \u0626\u06c6\u0686\u06c8\u0631\u06c8\u0644\u0633\u06d5 \u0626\u06c7\u0646\u0649\u06ad \u062a\u06c6\u06be\u067e\u0649\u0633\u0649\u060c \u0645\u06d5\u0633\u0649\u0644\u06d5\u0646 \u0628\u0627\u06be\u0627\u060c \u062a\u06d5\u0643\u0644\u0649\u067e \u06cb\u06d5 \u062a\u06d5\u0631\u062c\u0649\u0645\u0649\u0644\u0649\u0631\u0649 \u0626\u0627\u062a\u0633\u0649\u0632 \u0626\u0649\u0634\u0644\u06d5\u062a\u0643\u06c8\u0686\u0649\u06af\u06d5 \u062a\u06d5\u06cb\u06d5 \u0628\u0648\u0644\u0649\u062f\u06c7.", 
    "Number of Plurals": "\u0643\u06c6\u067e\u0644\u06c8\u0643 \u0633\u0627\u0646\u0649", 
    "Oops...": "\u06cb\u0627\u064a\u064a\u06d5\u064a\u2026", 
    "Overview": "\u0642\u0649\u0633\u0642\u0649\u0686\u06d5 \u0628\u0627\u064a\u0627\u0646", 
    "Password": "\u0626\u0649\u0645", 
    "Password changed, signing in...": "\u0626\u0649\u0645 \u0626\u06c6\u0632\u06af\u06d5\u0631\u062f\u0649\u060c \u062a\u0649\u0632\u0649\u0645\u063a\u0627 \u0643\u0649\u0631\u0649\u06cb\u0627\u062a\u0649\u062f\u06c7\u2026", 
    "Permissions": "\u06be\u0648\u0642\u06c7\u0642\u0644\u0627\u0631", 
    "Personal description": "\u0634\u06d5\u062e\u0633\u0649\u064a \u0686\u06c8\u0634\u06d5\u0646\u062f\u06c8\u0631\u06c8\u0634", 
    "Personal website URL": "\u0634\u06d5\u062e\u0633\u0649\u064a \u062a\u0648\u0631\u062a\u06c7\u0631\u0627 \u0626\u0627\u062f\u0631\u06d0\u0633\u0649", 
    "Please follow that link to continue the account creation.": "\u0628\u06c7 \u0626\u06c7\u0644\u0627\u0646\u0645\u0649\u0646\u0649 \u0686\u06d0\u0643\u0649\u067e \u06be\u06d0\u0633\u0627\u0628\u0627\u062a \u0642\u06c7\u0631\u06c7\u0634\u0646\u0649 \u062f\u0627\u06cb\u0627\u0645\u0644\u0627\u0634\u062a\u06c7\u0631\u06c7\u06ad.", 
    "Please follow that link to continue the password reset procedure.": "\u0626\u06c7\u0644\u0627\u0646\u0645\u0649\u0646\u0649 \u0686\u06d0\u0643\u0649\u067e \u0626\u0649\u0645 \u0642\u0627\u064a\u062a\u06c7\u0631\u06c7\u06cb\u06d0\u0644\u0649\u0634 \u062c\u06d5\u0631\u064a\u0627\u0646\u0649\u0646\u0649 \u062f\u0627\u06cb\u0627\u0645\u0644\u0627\u0634\u062a\u06c7\u0631\u06c7\u06ad.", 
    "Please select a valid user.": "\u0626\u0649\u0646\u0627\u06cb\u06d5\u062a\u0644\u0649\u0643 \u0626\u0649\u0634\u0644\u06d5\u062a\u0643\u06c8\u0686\u0649\u062f\u0649\u0646 \u0628\u0649\u0631\u0646\u0649 \u062a\u0627\u0644\u0644\u0627\u06ad.", 
    "Plural Equation": "\u0643\u06c6\u067e\u0644\u06c8\u0643 \u0626\u0649\u067e\u0627\u062f\u0649\u0633\u0649", 
    "Plural form %(index)s": "\u0643\u06c6\u067e\u0644\u06c8\u0643 \u0634\u06d5\u0643\u0644\u0649 %(index)s", 
    "Preview will be displayed here.": "\u0626\u0627\u0644\u062f\u0649\u0646 \u0643\u06c6\u0632\u0649\u062a\u0649\u0634 \u0628\u06c7 \u062c\u0627\u064a\u062f\u0627 \u0643\u06c6\u0631\u0633\u0649\u062a\u0649\u0644\u0649\u062f\u06c7.", 
    "Project / Language": "\u0642\u06c7\u0631\u06c7\u0644\u06c7\u0634/\u062a\u0649\u0644", 
    "Project Tree Style": "\u0642\u06c7\u0631\u06c7\u0644\u06c7\u0634 \u0634\u0627\u062e \u0626\u06c7\u0633\u0644\u06c7\u0628\u0649", 
    "Provide optional comment (will be publicly visible)": "\u062a\u0627\u0644\u0644\u0627\u0634\u0686\u0627\u0646 \u0626\u0649\u0632\u0627\u06be\u0627\u062a \u062a\u06d5\u0645\u0649\u0646\u0644\u06d5\u06ad (\u06be\u06d5\u0645\u0645\u06d5\u064a\u0644\u06d5\u0646 \u0643\u06c6\u0631\u06d5\u0644\u06d5\u064a\u062f\u06c7)", 
    "Public Profile": "\u0626\u0627\u0645\u0645\u0649\u06cb\u0649 \u0633\u06d5\u067e\u0644\u0649\u0645\u06d5 \u06be\u06c6\u062c\u062c\u06d5\u062a", 
    "Quality Checks": "\u0633\u06c8\u067e\u06d5\u062a \u062a\u06d5\u0643\u0634\u06c8\u0631\u06c8\u0634", 
    "Reject": "\u0631\u06d5\u062a \u0642\u0649\u0644", 
    "Reload page": "\u0628\u06d5\u062a\u0646\u0649 \u0642\u0627\u064a\u062a\u0627 \u064a\u06c8\u0643\u0644\u06d5", 
    "Repeat Password": "\u0626\u0649\u0645 \u062a\u06d5\u0643\u0631\u0627\u0631\u0644\u0627", 
    "Resend Email": "\u062a\u0648\u0631\u062e\u06d5\u062a\u0646\u0649 \u0642\u0627\u064a\u062a\u0627 \u064a\u0648\u0644\u0644\u0627", 
    "Reset Password": "\u0626\u0649\u0645\u0646\u0649 \u0626\u06d5\u0633\u0644\u0649\u06af\u06d5 \u0642\u0627\u064a\u062a\u06c7\u0631\u06c7\u0634", 
    "Reset Your Password": "\u0626\u0649\u0645\u0646\u0649 \u0626\u06d5\u0633\u0644\u0649\u06af\u06d5 \u0642\u0627\u064a\u062a\u06c7\u0631", 
    "Reviewed": "\u062a\u06d5\u0643\u0634\u06c8\u0631\u06c8\u0644\u06af\u06d5\u0646", 
    "Save": "\u0633\u0627\u0642\u0644\u0627", 
    "Saved successfully.": "\u0645\u06c7\u06cb\u06d5\u067e\u067e\u06d5\u0642\u0649\u064a\u06d5\u062a\u0644\u0649\u0643 \u0633\u0627\u0642\u0644\u0627\u0646\u062f\u0649.", 
    "Score Change": "\u0646\u06d5\u062a\u0649\u062c\u06d5 \u0626\u06c6\u0632\u06af\u0649\u0631\u0649\u0634\u0649", 
    "Screenshot Search Prefix": "\u0626\u06d0\u0643\u0631\u0627\u0646 \u0643\u06d5\u0633\u0645\u0649\u0633\u0649 \u0626\u0649\u0632\u062f\u06d5\u0634 \u0626\u0627\u0644\u062f\u0649 \u0642\u0648\u0634\u06c7\u0644\u063a\u06c7\u0686\u0649", 
    "Search Languages": "\u062a\u0649\u0644 \u0626\u0649\u0632\u062f\u06d5", 
    "Search Projects": "\u0642\u06c7\u0631\u06c7\u0644\u06c7\u0634 \u0626\u0649\u0632\u062f\u06d5", 
    "Search Users": "\u0626\u0649\u0634\u0644\u06d5\u062a\u0643\u06c8\u0686\u0649 \u0626\u0649\u0632\u062f\u06d5", 
    "Select...": "\u062a\u0627\u0644\u0644\u0627\u2026", 
    "Send Email": "\u062a\u0648\u0631\u062e\u06d5\u062a \u064a\u0648\u0644\u0644\u0627", 
    "Sending email to %s...": "\u06be\u0627\u0632\u0649\u0631 %s \u063a\u0627 \u062a\u0648\u0631\u062e\u06d5\u062a \u064a\u0648\u0644\u0644\u0627\u06cb\u0627\u062a\u0649\u062f\u06c7\u2026", 
    "Server error": "\u0645\u06c7\u0644\u0627\u0632\u0649\u0645\u06d0\u062a\u0649\u0631 \u062e\u0627\u062a\u0627\u0644\u0649\u0642\u0649", 
    "Set New Password": "\u064a\u06d0\u06ad\u0649 \u0626\u0649\u0645 \u062a\u06d5\u06ad\u0634\u06d5\u0634", 
    "Set a new password": "\u064a\u06d0\u06ad\u0649 \u0626\u0649\u0645 \u062a\u06d5\u06ad\u0634\u06d5\u0643", 
    "Settings": "\u062a\u06d5\u06ad\u0634\u06d5\u0643\u0644\u06d5\u0631", 
    "Short Bio": "\u0642\u0649\u0633\u0642\u0649\u0686\u06d5 \u062a\u0648\u0646\u06c7\u0634\u062a\u06c7\u0631\u06c7\u0634", 
    "Show": "\u0643\u06c6\u0631\u0633\u06d5\u062a", 
    "Show disabled": "\u0643\u06c6\u0631\u0633\u0649\u062a\u0649\u0634 \u0686\u06d5\u0643\u0644\u06d5\u0646\u06af\u06d5\u0646", 
    "Sign In": "\u062a\u0649\u0632\u0649\u0645\u063a\u0627 \u0643\u0649\u0631", 
    "Sign In With %s": "\u062a\u0649\u0632\u0649\u0645\u063a\u0627 %s \u0628\u0649\u0644\u06d5\u0646 \u0643\u0649\u0631\u0649\u06ad", 
    "Sign In With...": "\u0628\u0627\u0634\u0642\u0649\u0686\u06d5 \u062a\u0649\u0632\u0649\u0645\u063a\u0627 \u0643\u0649\u0631\u0649\u0634\u2026", 
    "Sign Up": "\u062e\u06d5\u062a\u0644\u06d5\u062a", 
    "Sign in as an existing user": "\u0645\u06d5\u06cb\u062c\u06c7\u062a \u0626\u0649\u0634\u0644\u06d5\u062a\u0643\u06c8\u0686\u0649 \u0633\u06c8\u067e\u0649\u062a\u0649\u062f\u06d5 \u062a\u0649\u0632\u0649\u0645\u063a\u0627 \u0643\u0649\u0631\u0649\u06ad", 
    "Sign up as a new user": "\u064a\u06d0\u06ad\u0649 \u0626\u0649\u0634\u0644\u06d5\u062a\u0643\u06c8\u0686\u0649 \u062e\u06d5\u062a\u0644\u0649\u062a\u0649\u0634", 
    "Signed in. Redirecting...": "\u062a\u0649\u0632\u0649\u0645\u063a\u0627 \u0643\u0649\u0631\u062f\u0649. \u0646\u0649\u0634\u0627\u0646\u0646\u0649 \u064a\u06c6\u062a\u0643\u06d5\u06cb\u0627\u062a\u0649\u062f\u06c7\u2026", 
    "Signing in with an external service for the first time will automatically create an account for you.": "\u0633\u0649\u0631\u062a\u0642\u0649 \u06be\u06d0\u0633\u0627\u0628\u0627\u062a \u0626\u0627\u0631\u0642\u0649\u0644\u0649\u0642 \u062a\u06c7\u0646\u062c\u0649 \u0642\u06d0\u062a\u0649\u0645 \u062a\u0649\u0632\u0649\u0645\u063a\u0627 \u0643\u0649\u0631\u06af\u06d5\u0646\u062f\u06d5 \u0626\u06c6\u0632\u0644\u06c8\u0643\u0649\u062f\u0649\u0646 \u0633\u0649\u0632\u06af\u06d5 \u064a\u06d0\u06ad\u0649 \u06be\u06d0\u0633\u0627\u0628\u0627\u062a\u062a\u0649\u0646 \u0628\u0649\u0631\u0646\u0649 \u0642\u06c7\u0631\u0649\u062f\u06c7", 
    "Similar translations": "\u0626\u0648\u062e\u0634\u0627\u064a\u062f\u0649\u063a\u0627\u0646 \u062a\u06d5\u0631\u062c\u0649\u0645\u0649\u0644\u06d5\u0631", 
    "Social Services": "\u0626\u0649\u062c\u062a\u0649\u0645\u0627\u0626\u0649\u064a \u0645\u06c7\u0644\u0627\u0632\u0649\u0645\u06d5\u062a\u0644\u06d5\u0631", 
    "Social Verification": "\u0626\u0649\u062c\u062a\u0649\u0645\u0627\u0626\u0649\u064a \u062f\u06d5\u0644\u0649\u0644\u0644\u06d5\u0634", 
    "Source Language": "\u0645\u06d5\u0646\u0628\u06d5 \u062a\u0649\u0644", 
    "Special Characters": "\u0626\u0627\u0644\u0627\u06be\u0649\u062f\u06d5 \u06be\u06d5\u0631\u067e\u0644\u06d5\u0631", 
    "String Errors Contact": "\u06be\u06d5\u0631\u067e \u062a\u0649\u0632\u0645\u0649\u0633\u0649 \u062e\u0627\u062a\u0627\u0644\u0649\u0642 \u0626\u0627\u0644\u0627\u0642\u0649\u0633\u0649", 
    "Suggested": "\u062a\u06d5\u06cb\u0633\u0649\u064a\u06d5 \u0642\u0649\u0644\u0649\u0646\u063a\u0627\u0646", 
    "Team": "\u0642\u0648\u0634\u06c7\u0646", 
    "The password reset link was invalid, possibly because it has already been used. Please request a new password reset.": "\u0626\u0649\u0645\u0646\u0649 \u0626\u06d5\u0633\u0644\u0649\u06af\u06d5 \u0642\u0627\u064a\u062a\u06c7\u0631\u06c7\u0634 \u0626\u06c7\u0627\u0644\u0646\u0645\u0649\u0633\u0649 \u0626\u0649\u0646\u0627\u06cb\u06d5\u062a\u0633\u0649\u0632\u060c \u0628\u06d5\u0644\u0643\u0649\u0645 \u0626\u06c7 \u0626\u0627\u0644\u0644\u0649\u0628\u06c7\u0631\u06c7\u0646 \u0626\u0649\u0634\u0644\u0649\u062a\u0649\u0644\u0649\u067e \u0628\u0648\u0644\u063a\u0627\u0646. \u064a\u06d0\u06ad\u0649\u062f\u0649\u0646 \u0626\u0649\u0645\u0646\u0649 \u0626\u06d5\u0633\u0644\u0649\u06af\u06d5 \u0642\u0627\u064a\u062a\u06c7\u0631\u06c7\u0634 \u0626\u0649\u0644\u062a\u0649\u0645\u0627\u0633\u0649 \u0626\u06d5\u06cb\u06d5\u062a\u0649\u06ad.", 
    "The server seems down. Try again later.": "\u0645\u06c7\u0644\u0627\u0632\u0649\u0645\u06d0\u062a\u0649\u0631 \u062a\u0627\u0642\u0627\u0644\u063a\u0627\u0646\u062f\u06d5\u0643 \u062a\u06c7\u0631\u0649\u062f\u06c7. \u0633\u06d5\u0644 \u062a\u06c7\u0631\u06c7\u067e \u0642\u0627\u064a\u062a\u0627 \u0633\u0649\u0646\u0627\u06ad.", 
    "There are unsaved changes. Do you want to discard them?": "\u062a\u06d0\u062e\u0649 \u0633\u0627\u0642\u0644\u0649\u0645\u0649\u063a\u0627\u0646 \u0626\u06c6\u0632\u06af\u06d5\u0631\u062a\u0649\u0634\u0644\u06d5\u0631 \u0628\u0627\u0631. \u0626\u06c7\u0644\u0627\u0631\u0646\u0649 \u062a\u0627\u0634\u0644\u0649\u06cb\u06d0\u062a\u06d5\u0645\u0633\u0649\u0632\u061f", 
    "There is %(count)s language.": [
      "%(count)s \u062a\u0649\u0644 \u0628\u0627\u0631. \u062a\u06c6\u06cb\u06d5\u0646\u062f\u0649\u0643\u0649\u0644\u0649\u0631\u0649 \u064a\u06d0\u0642\u0649\u0646\u062f\u0627 \u0642\u0648\u0634\u06c7\u0644\u063a\u0627\u0646\u0644\u0649\u0631\u0649."
    ], 
    "There is %(count)s project.": [
      "%(count)s \u0642\u06c7\u0631\u06c7\u0644\u06c7\u0634 \u0628\u0627\u0631. \u0626\u0627\u0633\u062a\u0649\u062f\u0649\u0643\u0649 \u0628\u0649\u0631\u062f\u0649\u0646 \u0643\u06c6\u067e \u0628\u0648\u0644\u063a\u0627\u0646\u0644\u0649\u0631\u0649 \u064a\u06d0\u0642\u0649\u0646\u062f\u0627 \u0642\u0648\u0634\u06c7\u0644\u063a\u0627\u0646\u0644\u0649\u0631\u0649."
    ], 
    "There is %(count)s user.": [
      "%(count)s \u0626\u0649\u0634\u0644\u06d5\u062a\u0643\u06c8\u0686\u0649 \u0628\u0627\u0631. \u062a\u06c6\u06cb\u06d5\u0646\u062f\u06d5 \u0643\u06c6\u0631\u06c8\u0646\u06af\u0649\u0646\u0649 \u064a\u06d0\u0642\u0649\u0646\u062f\u0627 \u062a\u0649\u0632\u0649\u0645\u0644\u0627\u062a\u0642\u0627\u0646 \u0626\u0649\u0634\u0644\u06d5\u062a\u0643\u06c8\u0686\u0649\u0644\u06d5\u0631."
    ], 
    "This email confirmation link expired or is invalid.": "\u0628\u06c7 \u062a\u0648\u0631\u062e\u06d5\u062a\u062a\u0649\u0643\u0649 \u062c\u06d5\u0632\u0645\u0644\u06d5\u0634 \u0626\u06c7\u0644\u0627\u0646\u0645\u0649\u0633\u0649\u0646\u0649\u06ad \u06cb\u0627\u0642\u062a\u0649 \u0626\u06c6\u062a\u0643\u06d5\u0646 \u064a\u0627\u0643\u0649 \u0626\u0649\u0646\u0627\u06cb\u06d5\u062a\u0633\u0649\u0632.", 
    "This string no longer exists.": "\u0628\u06c7 \u062a\u0649\u0632\u0649\u0642 \u0626\u06d5\u0645\u062f\u0649 \u0645\u06d5\u06cb\u062c\u06c7\u062f \u0626\u06d5\u0645\u06d5\u0633.", 
    "To set or change your avatar for your email address (%(email)s), please go to gravatar.com.": "\u062a\u0648\u0631\u062e\u06d5\u062a \u0626\u0627\u062f\u0631\u06d0\u0633\u0649\u06ad\u0649\u0632 (%(email)s) \u0646\u0649\u06ad \u0628\u0627\u0634 \u0633\u06c8\u0631\u0649\u062a\u0649\u06ad\u0649\u0632\u0646\u0649 \u062a\u06d5\u06ad\u0634\u06d5\u0634 \u064a\u0627\u0643\u0649 \u0626\u06c6\u0632\u06af\u06d5\u0631\u062a\u0649\u0634\u062a\u06d5\u060c gravatar.com \u0646\u0649 \u0632\u0649\u064a\u0627\u0631\u06d5\u062a \u0642\u0649\u0644\u0649\u06ad.", 
    "Translated": "\u062a\u06d5\u0631\u062c\u0649\u0645\u06d5 \u0642\u0649\u0644\u0649\u0646\u063a\u0627\u0646", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project": " \u201c<span title=\"%(path)s\">%(project)s</span>\u201d \u0642\u06c7\u0631\u06c7\u0644\u06c7\u0634\u0649\u062f\u0627 %(fullname)s \u062a\u06d5\u0631\u062c\u0649\u0645\u06d5 \u0642\u0649\u0644\u062f\u0649", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project %(time_ago)s": " \u201c<span title=\"%(path)s\">%(project)s</span>\u201d \u0642\u06c7\u0631\u06c7\u0644\u06c7\u0634\u0649\u062f\u0627 %(time_ago)s \u062f\u06d5 %(fullname)s  \u062a\u06d5\u0631\u062c\u0649\u0645\u06d5 \u0642\u0649\u0644\u062f\u0649", 
    "Try again": "\u0642\u0627\u064a\u062a\u0627 \u0633\u0649\u0646\u0627", 
    "Twitter": "Twitter", 
    "Twitter username": "\u202bTwitter \u0626\u0649\u0634\u0644\u06d5\u062a\u0643\u06c8\u0686\u0649 \u0626\u0627\u062a\u0649", 
    "Type to search": "\u0626\u0649\u0632\u062f\u06d5\u064a\u062f\u0649\u063a\u0627\u0646\u0646\u0649 \u0643\u0649\u0631\u06af\u06c8\u0632\u06c8\u06ad", 
    "Updating data": "\u0633\u0627\u0646\u0644\u0649\u0642 \u0645\u06d5\u0644\u06c7\u0645\u0627\u062a\u0644\u0627\u0631\u0646\u0649 \u064a\u06d0\u06ad\u0649\u0644\u0627\u06cb\u0627\u062a\u0649\u062f\u06c7", 
    "Use the search form to find the language, then click on a language to edit.": "\u062a\u0649\u0644 \u0626\u0649\u0632\u062f\u06d5\u0634 \u0626\u06c8\u0686\u06c8\u0646 \u0626\u0649\u0632\u062f\u06d5\u0634 \u062c\u06d5\u062f\u06cb\u0649\u0644\u0649\u0646\u0649 \u0626\u0649\u0634\u0644\u0649\u062a\u0649\u06ad\u060c \u0626\u0627\u0646\u062f\u0649\u0646 \u062a\u06d5\u06be\u0631\u0649\u0631\u0644\u06d5\u064a\u062f\u0649\u063a\u0627\u0646 \u062a\u0649\u0644\u062f\u0649\u0646 \u0628\u0649\u0631\u0646\u0649 \u062a\u0627\u0644\u0644\u0627\u06ad.", 
    "Use the search form to find the project, then click on a project to edit.": "\u0642\u06c7\u0631\u06c7\u0644\u06c7\u0634\u0646\u0649 \u0626\u0649\u0632\u062f\u06d5\u0634 \u0626\u06c8\u0686\u06c8\u0646 \u0626\u0649\u0632\u062f\u06d5\u0634 \u062c\u06d5\u062f\u06cb\u0649\u0644\u0649\u0646\u0649 \u0626\u0649\u0634\u0644\u0649\u062a\u0649\u06ad\u060c \u0626\u0627\u0646\u062f\u0649\u0646 \u062a\u06d5\u06be\u0631\u0649\u0631\u0644\u06d5\u064a\u062f\u0649\u063a\u0627\u0646 \u0642\u06c7\u0631\u06c7\u0644\u06c7\u0634\u0646\u0649 \u0628\u0649\u0631\u0646\u0649 \u0686\u06d0\u0643\u0649\u06ad.", 
    "Use the search form to find the user, then click on a user to edit.": "\u0626\u0649\u0634\u0644\u06d5\u062a\u0643\u06c8\u0686\u0649 \u0626\u0649\u0632\u062f\u06d5\u0634 \u0626\u06c8\u0686\u06c8\u0646 \u0626\u0649\u0632\u062f\u06d5\u0634 \u062c\u06d5\u062f\u06cb\u0649\u0644\u0649\u0646\u0649 \u0626\u0649\u0634\u0644\u0649\u062a\u0649\u06ad\u060c \u0626\u0627\u0646\u062f\u0649\u0646 \u062a\u06d5\u06be\u0631\u0649\u0631\u0644\u06d5\u064a\u062f\u0649\u063a\u0627\u0646 \u0626\u0649\u0634\u0644\u06d5\u062a\u0643\u06c8\u0686\u0649\u062f\u0649\u0646 \u0628\u0649\u0631\u0646\u0649 \u0686\u06d0\u0643\u0649\u06ad.", 
    "Username": "\u0626\u0649\u0634\u0644\u06d5\u062a\u0643\u06c8\u0686\u0649 \u0626\u0627\u062a\u0649", 
    "We found a user with <span>%(email)s</span> email in our system. Please provide the password to finish the sign in procedure. This is a one-off procedure, which will establish a link between your Pootle and %(provider)s accounts.": "\u0633\u0649\u0633\u062a\u06d0\u0645\u0649\u0645\u0649\u0632\u062f\u0627 <span>%(email)s</span> \u062a\u0648\u0631\u062e\u06d5\u062a \u0626\u0627\u062f\u0631\u06d0\u0633\u0649 \u0628\u0627\u0631 \u0626\u0649\u0634\u0644\u06d5\u062a\u0643\u06c8\u0686\u0649 \u0628\u0627\u064a\u0642\u0627\u0644\u062f\u0649. \u062a\u0649\u0632\u0649\u0645\u063a\u0627 \u0643\u0649\u0631\u0649\u0634\u0646\u0649 \u062a\u0627\u0645\u0627\u0645\u0644\u0627\u0634 \u0626\u06c8\u0686\u06c8\u0646 \u0626\u0649\u0645\u0646\u0649 \u062a\u06d5\u0645\u0649\u0646\u0644\u06d5\u06ad. \u0628\u06c7 Pootle \u06cb\u06d5 %(provider)s \u06be\u06d0\u0633\u0627\u0628\u0627\u062a \u0626\u0627\u0631\u0649\u0633\u0649\u062f\u0627 \u0626\u06c7\u0644\u0627\u0646\u0645\u0627 \u0642\u06c7\u0631\u06c7\u0634\u062a\u0649\u0643\u0649 \u0628\u0649\u0631 \u0642\u06d0\u062a\u0649\u0645\u0644\u0649\u0642 \u062c\u06d5\u0631\u064a\u0627\u0646.", 
    "We have sent an email containing the special link to <span>%s</span>": "\u0628\u0649\u0632 \u0628\u0649\u0631 \u067e\u0627\u0631\u0686\u06d5 \u062a\u0648\u0631\u062e\u06d5\u062a \u0626\u06d5\u06cb\u06d5\u062a\u062a\u06c7\u0642\u060c \u062e\u06d5\u062a\u062a\u06d5 <span>%s</span> \u0646\u0649\u06ad \u0626\u06c7\u0644\u0627\u0646\u0645\u0649\u0633\u0649 \u0628\u0627\u0631.", 
    "We have sent an email containing the special link to <span>%s</span>. Please check your spam folder if you do not see the email.": "\u0628\u0649\u0632 \u0628\u0649\u0631 \u067e\u0627\u0631\u0686\u06d5 \u062a\u0648\u0631\u062e\u06d5\u062a \u0626\u06d5\u06cb\u06d5\u062a\u062a\u06c7\u0642\u060c \u062e\u06d5\u062a\u062a\u06d5 <span>%s</span> \u0646\u0649\u06ad \u0626\u06c7\u0644\u0627\u0646\u0645\u0649\u0633\u0649 \u0628\u0627\u0631. \u0626\u06d5\u06af\u06d5\u0631 \u062a\u0648\u0631\u062e\u06d5\u062a\u0646\u0649 \u0643\u06c6\u0631\u0645\u0649\u06af\u06d5\u0646 \u0628\u0648\u0644\u0633\u0649\u06ad\u0649\u0632 \u0626\u06d5\u062e\u0644\u06d5\u062a \u062e\u06d5\u062a\u0644\u06d5\u0631 \u0642\u0649\u0633\u0642\u06c7\u0686\u0649\u0646\u0649 \u062a\u06d5\u06ad\u0634\u06c8\u0631\u06c8\u06ad.", 
    "We have sent an email containing the special link to the address used to register this account. Please check your spam folder if you do not see the email.": "\u06be\u06d0\u0633\u0627\u0628\u0627\u062a \u062e\u06d5\u062a\u0644\u0649\u062a\u0649\u0634 \u0626\u06c7\u0644\u0627\u0646\u0645\u0649\u0633\u0649\u0646\u0649 \u0626\u06c6\u0632 \u0626\u0649\u0686\u0649\u06af\u06d5 \u0626\u0627\u0644\u063a\u0627\u0646 \u0626\u0627\u062f\u0631\u06d0\u0633 \u0628\u0627\u0631 \u062a\u0648\u0631\u062e\u06d5\u062a \u0626\u06d5\u06cb\u06d5\u062a\u062a\u06c7\u0642. \u0626\u06d5\u06af\u06d5\u0631 \u062a\u0648\u0631\u062e\u06d5\u062a\u0646\u0649 \u062a\u0627\u067e\u0634\u06c7\u0631\u06c7\u06cb\u0627\u0644\u0645\u0649\u063a\u0627\u0646 \u0628\u0648\u0644\u0633\u0649\u06ad\u0649\u0632 \u0626\u06d5\u062e\u0644\u06d5\u062a \u062e\u06d5\u062a\u0644\u06d5\u0631 \u0642\u0649\u0633\u0642\u06c7\u0686\u0649\u0646\u0649 \u062a\u06d5\u0643\u0634\u06c8\u0631\u06c8\u06ad.", 
    "Website": "\u062a\u0648\u0631\u062a\u06c7\u0631\u0627", 
    "Why are you part of our translation project? Describe yourself, inspire others!": "\u0633\u0649\u0632 \u0646\u06d0\u0645\u06d5 \u0626\u06c8\u0686\u06c8\u0646 \u062a\u06d5\u0631\u062c\u0649\u0645\u06d5 \u0642\u06c7\u0631\u06c7\u0644\u06c7\u0634\u0649\u0645\u0649\u0632\u0646\u0649\u06ad \u0628\u0649\u0631 \u0626\u06d5\u0632\u0627\u0633\u0649 \u0628\u0648\u0644\u062f\u0649\u06ad\u0649\u0632\u061f \u0626\u06c6\u0632\u0649\u06ad\u0649\u0632\u0646\u0649 \u062a\u0648\u0646\u06c7\u0634\u062a\u06c7\u0631\u06c7\u06ad\u060c \u0628\u0627\u0634\u0642\u0649\u0644\u0627\u0631\u0646\u0649 \u0631\u0649\u063a\u0628\u06d5\u062a\u0644\u06d5\u0646\u062f\u06c8\u0631\u06c8\u06ad!", 
    "Yes": "\u06be\u06d5\u0626\u06d5", 
    "You have unsaved changes in this string. Navigating away will discard those changes.": "\u0628\u06c7 \u062a\u0649\u0632\u0649\u0642\u062a\u0627 \u062a\u06d0\u062e\u0649 \u0633\u0627\u0642\u0644\u0649\u0645\u0649\u063a\u0627\u0646 \u0626\u06c6\u0632\u06af\u06d5\u0631\u062a\u0649\u0634\u0649\u06ad\u0649\u0632 \u0628\u0627\u0631. \u0626\u0627\u064a\u0631\u0649\u0644\u0633\u0649\u06ad\u0649\u0632 \u0628\u06c7 \u0633\u0627\u0646\u0644\u0649\u0642 \u0645\u06d5\u0644\u06c7\u0645\u0627\u062a\u0644\u0627\u0631 \u064a\u0648\u0642\u0649\u0644\u0649\u062f\u06c7.", 
    "Your Full Name": "\u062a\u0648\u0644\u06c7\u0642 \u0626\u0649\u0633\u0645\u0649\u06ad\u0649\u0632", 
    "Your LinkedIn profile URL": "\u0633\u0649\u0632\u0646\u0649\u06ad LinkedIn \u0634\u06d5\u062e\u0633\u0649\u064a \u0626\u06c7\u0686\u06c7\u0631 \u062a\u0648\u0631 \u0626\u0627\u062f\u0631\u06d0\u0633\u0649\u06ad\u0649\u0632", 
    "Your Personal website/blog URL": "\u0634\u06d5\u062e\u0633\u0649\u064a \u062a\u0648\u0631\u062a\u06c7\u0631\u0627/\u0628\u0649\u0644\u0648\u06af \u062a\u0648\u0631 \u0626\u0627\u062f\u0631\u06d0\u0633\u0649\u06ad\u0649\u0632", 
    "Your Twitter username": "\u0633\u0649\u0632\u0646\u0649\u06ad Twitter \u0626\u0649\u0633\u0645\u0649\u06ad\u0649\u0632", 
    "Your account is inactive because an administrator deactivated it.": "\u06be\u06d0\u0633\u0627\u0628\u0627\u062a\u0649\u06ad\u0649\u0632 \u0626\u0627\u0643\u062a\u0649\u067e \u0626\u06d5\u0645\u06d5\u0633 \u0686\u06c8\u0646\u0643\u0649 \u0626\u06c7\u0646\u0649 \u0628\u0627\u0634\u0642\u06c7\u0631\u063a\u06c7\u0686\u0649 \u062a\u0648\u062e\u062a\u0649\u062a\u0649\u06cb\u06d5\u062a\u0643\u06d5\u0646.", 
    "Your account needs activation.": "\u06be\u06d0\u0633\u0627\u0628\u0627\u062a\u0649\u06ad\u0649\u0632\u0646\u0649 \u0626\u0627\u0643\u062a\u0649\u067e\u0644\u0627\u0634 \u0632\u06c6\u0631\u06c8\u0631.", 
    "disabled": "\u0686\u06d5\u0643\u0644\u06d5\u0646\u06af\u06d5\u0646", 
    "some anonymous user": "\u0628\u06d5\u0632\u0649 \u0626\u0627\u062a\u0633\u0649\u0632 \u0626\u0649\u0634\u0644\u06d5\u062a\u0643\u06c8\u0686\u0649", 
    "someone": "\u0628\u0649\u0631\u0633\u0649"
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

