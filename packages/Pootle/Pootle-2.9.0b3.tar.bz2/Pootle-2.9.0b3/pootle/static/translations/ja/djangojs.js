

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
      "\u30af\u30a8\u30ea\u306b %(count)s \u306e\u8a00\u8a9e\u304c\u30de\u30c3\u30c1\u3057\u307e\u3057\u305f\u3002"
    ], 
    "%(count)s project matches your query.": [
      "\u30af\u30a8\u30ea\u306b %(count)s \u4ef6\u306e\u30d7\u30ed\u30b8\u30a7\u30af\u30c8\u304c\u30de\u30c3\u30c1\u3057\u307e\u3057\u305f\u3002"
    ], 
    "%(count)s user matches your query.": [
      "\u30af\u30a8\u30ea\u306b %(count)s \u540d\u306e\u30e6\u30fc\u30b6\u30fc\u304c\u30de\u30c3\u30c1\u3057\u307e\u3057\u305f\u3002"
    ], 
    "%(timeSince)s via file upload": "%(timeSince)s \u306b\u30d5\u30a1\u30a4\u30eb\u3092\u30a2\u30c3\u30d7\u30ed\u30fc\u30c9", 
    "%s word": [
      "%s \u8a9e"
    ], 
    "%s's accepted suggestions": "%s \u306e\u63a1\u7528\u3055\u308c\u305f\u63d0\u6848", 
    "%s's overwritten submissions": "%s \u306e\u4e0a\u66f8\u304d\u3059\u308b\u63d0\u51fa", 
    "%s's pending suggestions": "%s \u306e\u7559\u4fdd\u4e2d\u306e\u63d0\u6848", 
    "%s's rejected suggestions": "%s \u306e\u5374\u4e0b\u3055\u308c\u305f\u63d0\u6848", 
    "%s's submissions": "%s \u306e\u63d0\u51fa", 
    "Accept": "\u53d7\u8afe", 
    "Account Activation": "\u30a2\u30ab\u30a6\u30f3\u30c8\u306e\u6709\u52b9\u5316", 
    "Account Inactive": "\u6709\u52b9\u5316\u3055\u308c\u3066\u3044\u306a\u3044\u30a2\u30ab\u30a6\u30f3\u30c8", 
    "Active": "\u6709\u52b9", 
    "Add Language": "\u8a00\u8a9e\u3092\u8ffd\u52a0", 
    "Add Project": "\u30d7\u30ed\u30b8\u30a7\u30af\u30c8\u3092\u8ffd\u52a0", 
    "Add User": "\u30e6\u30fc\u30b6\u30fc\u3092\u8ffd\u52a0", 
    "Administrator": "\u7ba1\u7406\u8005", 
    "After changing your password you will sign in automatically.": "\u30d1\u30b9\u30ef\u30fc\u30c9\u306e\u5909\u66f4\u5f8c\u3001\u81ea\u52d5\u7684\u306b\u30b5\u30a4\u30f3\u30a4\u30f3\u3057\u307e\u3059\u3002", 
    "All Languages": "\u3059\u3079\u3066\u306e\u8a00\u8a9e", 
    "All Projects": "\u3059\u3079\u3066\u306e\u30d7\u30ed\u30b8\u30a7\u30af\u30c8", 
    "An error occurred while attempting to sign in via %s.": "%s \u7d4c\u7531\u3067\u306e\u30b5\u30a4\u30f3\u30a4\u30f3\u4e2d\u306b\u30a8\u30e9\u30fc\u304c\u767a\u751f\u3057\u307e\u3057\u305f\u3002", 
    "An error occurred while attempting to sign in via your social account.": "\u30bd\u30fc\u30b7\u30e3\u30eb\u30a2\u30ab\u30a6\u30f3\u30c8\u7d4c\u7531\u3067\u306e\u30b5\u30a4\u30f3\u30a4\u30f3\u4e2d\u306b\u30a8\u30e9\u30fc\u304c\u767a\u751f\u3057\u307e\u3057\u305f\u3002", 
    "Avatar": "\u30a2\u30d0\u30bf\u30fc", 
    "Cancel": "\u30ad\u30e3\u30f3\u30bb\u30eb", 
    "Clear all": "\u3059\u3079\u3066\u6d88\u53bb", 
    "Clear value": "\u5024\u3092\u6d88\u53bb", 
    "Close": "\u9589\u3058\u308b", 
    "Code": "\u30b3\u30fc\u30c9", 
    "Collapse details": "\u8a73\u7d30\u3092\u6298\u308a\u305f\u305f\u3080", 
    "Congratulations! You have completed this task!": "\u304a\u3081\u3067\u3068\u3046\u3054\u3056\u3044\u307e\u3059\u3002\u3059\u3079\u3066\u306e\u6587\u5b57\u5217\u306b\u76ee\u3092\u901a\u3057\u307e\u3057\u305f\u3002", 
    "Contact Us": "\u304a\u554f\u3044\u5408\u308f\u305b", 
    "Contributors, 30 Days": "30 \u65e5\u9593\u306e\u8ca2\u732e\u8005", 
    "Creating new user accounts is prohibited.": "\u65b0\u3057\u3044\u30a2\u30ab\u30a6\u30f3\u30c8\u306e\u4f5c\u6210\u306f\u7981\u6b62\u3055\u308c\u3066\u3044\u307e\u3059\u3002", 
    "Delete": "\u524a\u9664", 
    "Deleted successfully.": "\u6b63\u5e38\u306b\u524a\u9664\u3055\u308c\u307e\u3057\u305f\u3002", 
    "Didn't receive an email? Check if it was accidentally filtered out as spam, or try requesting another copy of the email.": "\u30e1\u30fc\u30eb\u3092\u53d7\u3051\u53d6\u308c\u307e\u305b\u3093\u3067\u3057\u305f\u304b\uff1f \u30b9\u30d1\u30e0\u306b\u5206\u985e\u3055\u308c\u3066\u3044\u306a\u3044\u304b\u78ba\u8a8d\u3059\u308b\u304b\u3001\u30e1\u30fc\u30eb\u306e\u518d\u9001\u4fe1\u3092\u8981\u6c42\u3057\u3066\u304f\u3060\u3055\u3044\u3002", 
    "Disabled": "\u7121\u52b9", 
    "Discard changes.": "\u5909\u66f4\u3092\u7834\u68c4\u3059\u308b\u3002", 
    "Edit Language": "\u8a00\u8a9e\u3092\u7de8\u96c6", 
    "Edit My Public Profile": "\u81ea\u5206\u306e\u516c\u958b\u30d7\u30ed\u30d5\u30a3\u30fc\u30eb\u3092\u7de8\u96c6\u3059\u308b", 
    "Edit Project": "\u30d7\u30ed\u30b8\u30a7\u30af\u30c8\u3092\u7de8\u96c6", 
    "Edit User": "\u30e6\u30fc\u30b6\u30fc\u3092\u7de8\u96c6", 
    "Edit the suggestion before accepting, if necessary": "\u53d7\u8afe\u3059\u308b\u524d\u306b\u3001\u5fc5\u8981\u3067\u3042\u308c\u3070\u63d0\u6848\u3092\u7de8\u96c6\u3057\u3066\u304f\u3060\u3055\u3044", 
    "Email": "\u30e1\u30fc\u30eb\u30a2\u30c9\u30ec\u30b9", 
    "Email Address": "\u30e1\u30fc\u30eb\u30a2\u30c9\u30ec\u30b9", 
    "Email Confirmation": "\u30e1\u30fc\u30eb\u78ba\u8a8d", 
    "Enter your email address, and we will send you a message with the special link to reset your password.": "\u3042\u306a\u305f\u306e\u30e1\u30fc\u30eb\u30a2\u30c9\u30ec\u30b9\u3092\u5165\u529b\u3057\u3066\u304f\u3060\u3055\u3044\u3002\u30d1\u30b9\u30ef\u30fc\u30c9\u3092\u30ea\u30bb\u30c3\u30c8\u3059\u308b\u305f\u3081\u306e\u7279\u5225\u306a\u30ea\u30f3\u30af\u3092\u542b\u3080\u30e1\u30c3\u30bb\u30fc\u30b8\u304c\u9001\u4fe1\u3055\u308c\u307e\u3059\u3002", 
    "Error while connecting to the server": "\u30b5\u30fc\u30d0\u30fc\u306b\u63a5\u7d9a\u3059\u308b\u969b\u306b\u30a8\u30e9\u30fc\u304c\u767a\u751f\u3057\u307e\u3057\u305f", 
    "Expand details": "\u8a73\u7d30\u3092\u5c55\u958b\u3059\u308b", 
    "File types": "\u30d5\u30a1\u30a4\u30eb\u306e\u7a2e\u985e", 
    "Filesystems": "\u30d5\u30a1\u30a4\u30eb\u30b7\u30b9\u30c6\u30e0", 
    "Find language by name, code": "\u8a00\u8a9e\u3092\u540d\u524d\u3084\u30b3\u30fc\u30c9\u3067\u691c\u7d22", 
    "Find project by name, code": "\u30d7\u30ed\u30b8\u30a7\u30af\u30c8\u3092\u540d\u524d\u3084\u30b3\u30fc\u30c9\u3067\u691c\u7d22", 
    "Find user by name, email, properties": "\u30e6\u30fc\u30b6\u30fc\u3092\u540d\u524d\u3084\u30e1\u30fc\u30eb\u30a2\u30c9\u30ec\u30b9\u3001\u30d7\u30ed\u30d1\u30c6\u30a3\u30fc\u3067\u691c\u7d22", 
    "Full Name": "\u30d5\u30eb\u30cd\u30fc\u30e0", 
    "Go back to browsing": "\u30d6\u30e9\u30a6\u30b8\u30f3\u30b0\u3078\u623b\u308b", 
    "Go to the next string (Ctrl+.)<br/><br/>Also:<br/>Next page: Ctrl+Shift+.<br/>Last page: Ctrl+Shift+End": "\u6b21\u306e\u6587\u5b57\u5217\u3078\u79fb\u52d5 (Ctrl+.)<br/><br/>\u4ed6\u306e\u64cd\u4f5c:<br/>\u6b21\u306e\u30da\u30fc\u30b8: Ctrl+Shift+.<br/>\u6700\u5f8c\u306e\u30da\u30fc\u30b8: Ctrl+Shift+End", 
    "Go to the previous string (Ctrl+,)<br/><br/>Also:<br/>Previous page: Ctrl+Shift+,<br/>First page: Ctrl+Shift+Home": "\u524d\u306e\u6587\u5b57\u5217\u3078\u623b\u308b (Ctrl+,)<br/><br/>\u4ed6\u306e\u64cd\u4f5c:<br/>\u524d\u306e\u30da\u30fc\u30b8: Ctrl+Shift+,<br/>\u6700\u521d\u306e\u30da\u30fc\u30b8: Ctrl+Shift+Home", 
    "Hide": "\u96a0\u3059", 
    "Hide disabled": "\u7121\u52b9\u306a\u3082\u306e\u3092\u96a0\u3059", 
    "I forgot my password": "\u30d1\u30b9\u30ef\u30fc\u30c9\u3092\u5fd8\u308c\u307e\u3057\u305f", 
    "Ignore Files": "\u30d5\u30a1\u30a4\u30eb\u3092\u7121\u8996", 
    "Languages": "\u8a00\u8a9e", 
    "Less": "\u6e1b\u3089\u3059", 
    "LinkedIn": "LinkedIn", 
    "LinkedIn profile URL": "LinkedIn\u306e\u30d7\u30ed\u30d5\u30a3\u30fc\u30ebURL", 
    "Load More": "\u3055\u3089\u306b\u8aad\u307f\u8fbc\u3080", 
    "Loading...": "\u8aad\u307f\u8fbc\u307f\u4e2d...", 
    "Login / Password": "\u30ed\u30b0\u30a4\u30f3 / \u30d1\u30b9\u30ef\u30fc\u30c9", 
    "More": "\u5897\u3084\u3059", 
    "More...": "\u5897\u3084\u3059...", 
    "My Public Profile": "\u516c\u958b\u30d7\u30ed\u30d5\u30a3\u30fc\u30eb", 
    "No": "\u3044\u3044\u3048", 
    "No activity recorded in a given period": "\u6307\u5b9a\u3055\u308c\u305f\u671f\u9593\u306b\u8a18\u9332\u3055\u308c\u305f\u6d3b\u52d5\u306f\u3042\u308a\u307e\u305b\u3093", 
    "No results found": "\u7d50\u679c\u306f\u3042\u308a\u307e\u305b\u3093", 
    "No results.": "\u8a72\u5f53\u3059\u308b\u3082\u306e\u306f\u3042\u308a\u307e\u305b\u3093\u3002", 
    "No, thanks": "\u3044\u3044\u3048\u3001\u304a\u65ad\u308a\u3057\u307e\u3059", 
    "Not found": "\u898b\u3064\u304b\u308a\u307e\u305b\u3093\u3067\u3057\u305f", 
    "Note: when deleting a user their contributions to the site, e.g. comments, suggestions and translations, are attributed to the anonymous user (nobody).": "\u6ce8\u610f: \u30e6\u30fc\u30b6\u30fc\u3092\u524a\u9664\u3059\u308b\u3068\u3001\u305d\u306e\u30e6\u30fc\u30b6\u30fc\u306e\u30b3\u30e1\u30f3\u30c8\u3001\u63d0\u6848\u3001\u7ffb\u8a33\u306a\u3069\u306e\u8ca2\u732e\u306f\u3001\u533f\u540d\u306e\u30e6\u30fc\u30b6\u30fc (nobody) \u306e\u3082\u306e\u3068\u3057\u3066\u5206\u985e\u3055\u308c\u307e\u3059\u3002", 
    "Number of Plurals": "\u8907\u6570\u5f62\u306e\u6570", 
    "Oops...": "\u7533\u3057\u8a33\u3042\u308a\u307e\u305b\u3093...", 
    "Overview": "\u6982\u8981", 
    "Password": "\u30d1\u30b9\u30ef\u30fc\u30c9", 
    "Password changed, signing in...": "\u30d1\u30b9\u30ef\u30fc\u30c9\u304c\u5909\u66f4\u3055\u308c\u307e\u3057\u305f\u3002\u30b5\u30a4\u30f3\u30a4\u30f3\u3057\u3066\u304f\u3060\u3055\u3044...", 
    "Permissions": "\u6a29\u9650", 
    "Personal description": "\u81ea\u5df1\u7d39\u4ecb", 
    "Personal website URL": "\u500b\u4eba\u30a6\u30a7\u30d6\u30b5\u30a4\u30c8\u306eURL", 
    "Please follow that link to continue the account creation.": "\u30ea\u30f3\u30af\u3092\u30af\u30ea\u30c3\u30af\u306e\u4e0a\u3001\u30a2\u30ab\u30a6\u30f3\u30c8\u4f5c\u6210\u306b\u9032\u3093\u3067\u304f\u3060\u3055\u3044\u3002", 
    "Please follow that link to continue the password reset procedure.": "\u30d1\u30b9\u30ef\u30fc\u30c9\u30ea\u30bb\u30c3\u30c8\u306e\u624b\u7d9a\u304d\u3092\u9032\u3081\u308b\u306b\u306f\u3001\u6b21\u306e\u30ea\u30f3\u30af\u3092\u30af\u30ea\u30c3\u30af\u3057\u3066\u304f\u3060\u3055\u3044\u3002", 
    "Please select a valid user.": "\u6709\u52b9\u306a\u30e6\u30fc\u30b6\u30fc\u3092\u9078\u629e\u3057\u3066\u304f\u3060\u3055\u3044\u3002", 
    "Plural Equation": "\u8907\u6570\u5f62\u3068\u540c\u7b49", 
    "Plural form %(index)s": "\u8907\u6570\u5f62 %(index)s", 
    "Preview will be displayed here.": "\u3053\u3053\u306b\u30d7\u30ec\u30d3\u30e5\u30fc\u304c\u8868\u793a\u3055\u308c\u307e\u3059\u3002", 
    "Project / Language": "\u30d7\u30ed\u30b8\u30a7\u30af\u30c8 / \u8a00\u8a9e", 
    "Project Tree Style": "\u30d7\u30ed\u30b8\u30a7\u30af\u30c8\u30fb\u30c4\u30ea\u30fc\u30fb\u30b9\u30bf\u30a4\u30eb", 
    "Provide optional comment (will be publicly visible)": "\u4efb\u610f\u306e\u30b3\u30e1\u30f3\u30c8\u3092\u8a18\u5165\u3057\u3066\u304f\u3060\u3055\u3044 (\u516c\u958b\u3055\u308c\u307e\u3059)", 
    "Public Profile": "\u516c\u958b\u30d7\u30ed\u30d5\u30a3\u30fc\u30eb", 
    "Quality Checks": "\u30af\u30aa\u30ea\u30c6\u30a3\u30fc\u30fb\u30c1\u30a7\u30c3\u30af", 
    "Reject": "\u62d2\u5426", 
    "Reload page": "\u30da\u30fc\u30b8\u3092\u518d\u8aad\u307f\u8fbc\u307f", 
    "Repeat Password": "\u30d1\u30b9\u30ef\u30fc\u30c9\u306e\u518d\u5165\u529b", 
    "Resend Email": "\u30e1\u30fc\u30eb\u3092\u518d\u9001\u4fe1", 
    "Reset Password": "\u30d1\u30b9\u30ef\u30fc\u30c9\u306e\u30ea\u30bb\u30c3\u30c8", 
    "Reset Your Password": "\u30d1\u30b9\u30ef\u30fc\u30c9\u3092\u30ea\u30bb\u30c3\u30c8", 
    "Reviewed": "\u67fb\u8aad\u6e08\u307f", 
    "Save": "\u4fdd\u5b58", 
    "Saved successfully.": "\u6b63\u5e38\u306b\u4fdd\u5b58\u3055\u308c\u307e\u3057\u305f\u3002", 
    "Score Change": "\u30b9\u30b3\u30a2\u306e\u5909\u66f4", 
    "Screenshot Search Prefix": "\u30b9\u30af\u30ea\u30fc\u30f3\u30b7\u30e7\u30c3\u30c8\u691c\u7d22\u306e\u63a5\u982d\u8f9e", 
    "Search Languages": "\u8a00\u8a9e\u3092\u691c\u7d22", 
    "Search Projects": "\u30d7\u30ed\u30b8\u30a7\u30af\u30c8\u3092\u691c\u7d22", 
    "Search Users": "\u30e6\u30fc\u30b6\u30fc\u3092\u691c\u7d22", 
    "Select...": "\u9078\u629e...", 
    "Send Email": "\u30e1\u30fc\u30eb\u3092\u9001\u4fe1", 
    "Sending email to %s...": "%s \u3078\u30e1\u30fc\u30eb\u3092\u9001\u4fe1\u3057\u3066\u3044\u307e\u3059...", 
    "Server error": "\u30b5\u30fc\u30d0\u30fc \u30a8\u30e9\u30fc", 
    "Set New Password": "\u65b0\u3057\u3044\u30d1\u30b9\u30ef\u30fc\u30c9\u3092\u8a2d\u5b9a", 
    "Set a new password": "\u65b0\u3057\u3044\u30d1\u30b9\u30ef\u30fc\u30c9\u3092\u8a2d\u5b9a", 
    "Settings": "\u8a2d\u5b9a", 
    "Short Bio": "\u7c21\u5358\u306a\u81ea\u5df1\u7d39\u4ecb", 
    "Show": "\u8868\u793a\u3059\u308b", 
    "Show disabled": "\u7121\u52b9\u306a\u3082\u306e\u3092\u8868\u793a", 
    "Sign In": "\u30b5\u30a4\u30f3\u30a4\u30f3", 
    "Sign In With %s": "%s \u3067\u30b5\u30a4\u30f3\u30a4\u30f3", 
    "Sign In With...": "\u30b5\u30a4\u30f3\u30a4\u30f3...", 
    "Sign Up": "\u30a2\u30ab\u30a6\u30f3\u30c8\u767b\u9332", 
    "Sign in as an existing user": "\u65e2\u5b58\u30e6\u30fc\u30b6\u30fc\u3068\u3057\u3066\u30b5\u30a4\u30f3\u30a4\u30f3", 
    "Sign up as a new user": "\u65b0\u898f\u30e6\u30fc\u30b6\u30fc\u3068\u3057\u3066\u30a2\u30ab\u30a6\u30f3\u30c8\u767b\u9332", 
    "Signed in. Redirecting...": "\u30b5\u30a4\u30f3\u30a4\u30f3\u3057\u307e\u3057\u305f\u3002\u30ea\u30c0\u30a4\u30ec\u30af\u30c8\u3057\u3066\u3044\u307e\u3059...", 
    "Signing in with an external service for the first time will automatically create an account for you.": "\u5916\u90e8\u30b5\u30fc\u30d3\u30b9\u3067\u521d\u3081\u3066\u30b5\u30a4\u30f3\u30a4\u30f3\u3059\u308b\u3068\u3001\u81ea\u52d5\u7684\u306b\u30a2\u30ab\u30a6\u30f3\u30c8\u304c\u4f5c\u6210\u3055\u308c\u307e\u3059\u3002", 
    "Similar translations": "\u985e\u4f3c\u7ffb\u8a33", 
    "Social Services": "\u30bd\u30fc\u30b7\u30e3\u30eb\u30b5\u30fc\u30d3\u30b9", 
    "Social Verification": "\u30bd\u30fc\u30b7\u30e3\u30eb\u691c\u8a3c", 
    "Source Language": "\u5143\u306e\u8a00\u8a9e", 
    "Special Characters": "\u7279\u6b8a\u6587\u5b57", 
    "String Errors Contact": "\u6587\u5b57\u5217\u30a8\u30e9\u30fc\u306e\u554f\u3044\u5408\u308f\u305b", 
    "Suggested": "\u63d0\u6848", 
    "Team": "\u30c1\u30fc\u30e0", 
    "The password reset link was invalid, possibly because it has already been used. Please request a new password reset.": "\u30d1\u30b9\u30ef\u30fc\u30c9\u30ea\u30bb\u30c3\u30c8\u306e\u30ea\u30f3\u30af\u304c\u6b63\u3057\u304f\u3042\u308a\u307e\u305b\u3093\u3002\u304a\u305d\u3089\u304f\u3001\u4f7f\u7528\u6e08\u307f\u306e\u3088\u3046\u3067\u3059\u3002\u65b0\u3057\u304f\u30d1\u30b9\u30ef\u30fc\u30c9\u306e\u30ea\u30bb\u30c3\u30c8\u3092\u8981\u6c42\u3057\u3066\u304f\u3060\u3055\u3044\u3002", 
    "The server seems down. Try again later.": "\u30b5\u30fc\u30d0\u30fc\u304c\u505c\u6b62\u3057\u3066\u3044\u308b\u3088\u3046\u3067\u3059\u3002\u5f8c\u3067\u3082\u3046\u4e00\u5ea6\u8a66\u3057\u3066\u304f\u3060\u3055\u3044\u3002", 
    "There are unsaved changes. Do you want to discard them?": "\u4fdd\u5b58\u3055\u308c\u3066\u3044\u306a\u3044\u5909\u66f4\u304c\u3042\u308a\u307e\u3059\u3002\u3053\u308c\u3089\u3092\u7834\u68c4\u3057\u3066\u3082\u3088\u308d\u3057\u3044\u3067\u3059\u304b\uff1f", 
    "There is %(count)s language.": [
      "%(count)s \u306e\u8a00\u8a9e\u304c\u3042\u308a\u307e\u3059\u3002\u4ee5\u4e0b\u306f\u6700\u8fd1\u8ffd\u52a0\u3055\u308c\u305f\u8a00\u8a9e\u3067\u3059\u3002"
    ], 
    "There is %(count)s project.": [
      "%(count)s \u4ef6\u306e\u30d7\u30ed\u30b8\u30a7\u30af\u30c8\u304c\u3042\u308a\u307e\u3059\u3002\u4ee5\u4e0b\u306f\u6700\u8fd1\u8ffd\u52a0\u3055\u308c\u305f\u30d7\u30ed\u30b8\u30a7\u30af\u30c8\u3067\u3059\u3002"
    ], 
    "There is %(count)s user.": [
      "%(count)s \u540d\u306e\u30e6\u30fc\u30b6\u30fc\u304c\u3044\u307e\u3059\u3002\u4ee5\u4e0b\u306f\u6700\u8fd1\u8ffd\u52a0\u3055\u308c\u305f\u30e6\u30fc\u30b6\u30fc\u3067\u3059\u3002"
    ], 
    "This email confirmation link expired or is invalid.": "\u3053\u306e\u30e1\u30fc\u30eb\u78ba\u8a8d\u306e\u30ea\u30f3\u30af\u306f\u6709\u52b9\u671f\u9650\u5207\u308c\u304b\u4e0d\u6b63\u3067\u3059\u3002", 
    "This string no longer exists.": "\u3053\u306e\u6587\u5b57\u5217\u306f\u5b58\u5728\u3057\u307e\u305b\u3093\u3002", 
    "To set or change your avatar for your email address (%(email)s), please go to gravatar.com.": "\u3042\u306a\u305f\u306e\u30e1\u30fc\u30eb\u30a2\u30c9\u30ec\u30b9 (%(email)s) \u306e\u30a2\u30d0\u30bf\u30fc\u3092 gravatar.com \u3067\u8a2d\u5b9a\u307e\u305f\u306f\u5909\u66f4\u3067\u304d\u307e\u3059\u3002", 
    "Translated": "\u7ffb\u8a33\u6e08\u307f", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project": "%(fullname)s \u306b\u3088\u308b \u201c<span title=\"%(path)s\">%(project)s</span>\u201d \u30d7\u30ed\u30b8\u30a7\u30af\u30c8\u306e\u7ffb\u8a33", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project %(time_ago)s": "%(fullname)s \u306b\u3088\u308b \u201c<span title=\"%(path)s\">%(project)s</span>\u201d \u30d7\u30ed\u30b8\u30a7\u30af\u30c8\u306e\u7ffb\u8a33 (%(time_ago)s)", 
    "Try again": "\u518d\u8a66\u884c", 
    "Twitter": "Twitter", 
    "Twitter username": "Twitter \u30e6\u30fc\u30b6\u30fc\u540d", 
    "Type to search": "\u691c\u7d22\u8a9e\u3092\u5165\u529b\u3057\u3066\u304f\u3060\u3055\u3044\u3002", 
    "Updating data": "\u30c7\u30fc\u30bf\u3092\u66f4\u65b0\u4e2d", 
    "Use the search form to find the language, then click on a language to edit.": "\u691c\u7d22\u30d5\u30a9\u30fc\u30e0\u3092\u4f7f\u7528\u3057\u3066\u8a00\u8a9e\u3092\u898b\u3064\u3051\u3001\u8a00\u8a9e\u3092\u30af\u30ea\u30c3\u30af\u3057\u3066\u7de8\u96c6\u3057\u307e\u3059\u3002", 
    "Use the search form to find the project, then click on a project to edit.": "\u691c\u7d22\u30d5\u30a9\u30fc\u30e0\u3092\u4f7f\u7528\u3057\u3066\u30d7\u30ed\u30b8\u30a7\u30af\u30c8\u3092\u898b\u3064\u3051\u3001\u30d7\u30ed\u30b8\u30a7\u30af\u30c8\u3092\u30af\u30ea\u30c3\u30af\u3057\u3066\u7de8\u96c6\u3057\u307e\u3059\u3002", 
    "Use the search form to find the user, then click on a user to edit.": "\u691c\u7d22\u30d5\u30a9\u30fc\u30e0\u3092\u4f7f\u7528\u3057\u3066\u30e6\u30fc\u30b6\u30fc\u3092\u898b\u3064\u3051\u3001\u30e6\u30fc\u30b6\u30fc\u3092\u30af\u30ea\u30c3\u30af\u3057\u3066\u7de8\u96c6\u3057\u307e\u3059\u3002", 
    "Username": "\u30e6\u30fc\u30b6\u30fc\u540d", 
    "We found a user with <span>%(email)s</span> email in our system. Please provide the password to finish the sign in procedure. This is a one-off procedure, which will establish a link between your Pootle and %(provider)s accounts.": "<span>%(email)s</span> \u306e\u30e1\u30fc\u30eb\u30a2\u30c9\u30ec\u30b9\u3067\u767b\u9332\u3055\u308c\u305f\u30e6\u30fc\u30b6\u30fc\u304c\u898b\u3064\u304b\u308a\u307e\u3057\u305f\u3002\u30b5\u30a4\u30f3\u30a4\u30f3\u624b\u7d9a\u304d\u3092\u5b8c\u4e86\u3059\u308b\u306b\u306f\u30d1\u30b9\u30ef\u30fc\u30c9\u3092\u5165\u529b\u3057\u3066\u304f\u3060\u3055\u3044\u3002\u3053\u306e\u624b\u7d9a\u304d\u306f\u4e00\u5ea6\u9650\u308a\u3067\u3042\u308a\u3001\u3042\u306a\u305f\u306e Pootle \u30a2\u30ab\u30a6\u30f3\u30c8\u3068 %(provider)s \u30a2\u30ab\u30a6\u30f3\u30c8\u306e\u9593\u306e\u30ea\u30f3\u30af\u3092\u78ba\u7acb\u3057\u307e\u3059\u3002", 
    "We have sent an email containing the special link to <span>%s</span>": "\u7279\u5225\u306a\u30ea\u30f3\u30af\u3092\u542b\u3080\u30e1\u30fc\u30eb\u3092 <span>%s</span> \u306b\u9001\u4fe1\u3057\u307e\u3057\u305f", 
    "We have sent an email containing the special link to <span>%s</span>. Please check your spam folder if you do not see the email.": "\u7279\u5225\u306a\u30ea\u30f3\u30af\u3092\u542b\u3080\u30e1\u30fc\u30eb\u3092 <span>%s</span> \u306b\u9001\u4fe1\u3057\u307e\u3057\u305f\u3002\u30e1\u30fc\u30eb\u304c\u898b\u3064\u304b\u3089\u306a\u3044\u5834\u5408\u306f\u8ff7\u60d1\u30e1\u30fc\u30eb\u30d5\u30a9\u30eb\u30c0\u3082\u78ba\u8a8d\u3057\u3066\u304f\u3060\u3055\u3044\u3002", 
    "We have sent an email containing the special link to the address used to register this account. Please check your spam folder if you do not see the email.": "\u7279\u5225\u306a\u30ea\u30f3\u30af\u3092\u542b\u3080\u30e1\u30fc\u30eb\u3092\u3001\u672c\u30a2\u30ab\u30a6\u30f3\u30c8\u306e\u767b\u9332\u306b\u4f7f\u7528\u3055\u308c\u305f\u30a2\u30c9\u30ec\u30b9\u306b\u9001\u4fe1\u3057\u307e\u3057\u305f\u3002\u30e1\u30fc\u30eb\u304c\u898b\u3064\u304b\u3089\u306a\u3044\u5834\u5408\u306f\u8ff7\u60d1\u30e1\u30fc\u30eb\u30d5\u30a9\u30eb\u30c0\u3082\u78ba\u8a8d\u3057\u3066\u304f\u3060\u3055\u3044\u3002", 
    "Website": "\u30a6\u30a7\u30d6\u30b5\u30a4\u30c8", 
    "Why are you part of our translation project? Describe yourself, inspire others!": "\u3053\u306e\u7ffb\u8a33\u30d7\u30ed\u30b8\u30a7\u30af\u30c8\u306b\u53c2\u52a0\u3057\u305f\u7406\u7531\u306f\uff1f \u81ea\u5df1\u7d39\u4ecb\u3092\u66f8\u3044\u3066\u4ed6\u306e\u4eba\u3092\u6d3b\u6c17\u4ed8\u3051\u3066\u304f\u3060\u3055\u3044\uff01", 
    "Yes": "\u306f\u3044", 
    "You have unsaved changes in this string. Navigating away will discard those changes.": "\u3053\u306e\u6587\u5b57\u5217\u306e\u5909\u66f4\u306f\u4fdd\u5b58\u3055\u308c\u3066\u3044\u307e\u305b\u3093\u3002\u79fb\u52d5\u3059\u308b\u3068\u5909\u66f4\u304c\u7834\u68c4\u3055\u308c\u307e\u3059\u3002", 
    "Your Full Name": "\u3042\u306a\u305f\u306e\u6c0f\u540d", 
    "Your LinkedIn profile URL": "LinkedIn \u30d7\u30ed\u30d5\u30a3\u30fc\u30eb URL", 
    "Your Personal website/blog URL": "\u500b\u4eba\u306e\u30a6\u30a7\u30d6\u30b5\u30a4\u30c8\u307e\u305f\u306f\u30d6\u30ed\u30b0 URL", 
    "Your Twitter username": "Twitter \u30e6\u30fc\u30b6\u30fc\u540d", 
    "Your account is inactive because an administrator deactivated it.": "\u7ba1\u7406\u8005\u304c\u7121\u52b9\u5316\u3057\u305f\u305f\u3081\u3001\u3042\u306a\u305f\u306e\u30a2\u30ab\u30a6\u30f3\u30c8\u306f\u6709\u52b9\u3067\u306f\u3042\u308a\u307e\u305b\u3093\u3002", 
    "Your account needs activation.": "\u3042\u306a\u305f\u306e\u30a2\u30ab\u30a6\u30f3\u30c8\u306f\u6709\u52b9\u5316\u304c\u5fc5\u8981\u3067\u3059\u3002", 
    "disabled": "\u7121\u52b9", 
    "some anonymous user": "\u533f\u540d\u30e6\u30fc\u30b6\u30fc", 
    "someone": "\u8ab0\u304b"
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

