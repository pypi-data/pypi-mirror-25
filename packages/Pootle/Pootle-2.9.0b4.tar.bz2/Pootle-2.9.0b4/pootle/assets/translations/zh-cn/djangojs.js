

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
      "%(count)s \u79cd\u8bed\u8a00\u5339\u914d\u60a8\u7684\u67e5\u8be2\u3002"
    ], 
    "%(count)s project matches your query.": [
      "%(count)s \u4e2a\u9879\u76ee\u5339\u914d\u60a8\u7684\u67e5\u8be2\u3002"
    ], 
    "%(count)s user matches your query.": [
      "\u5171\u6709%(count)s \u4e2a\u7528\u6237\u7b26\u5408\u60a8\u7684\u67e5\u8be2\u6761\u4ef6\u3002%(count)s \u4e2a\u7528\u6237\u7b26\u5408\u60a8\u7684\u67e5\u8be2\u6761\u4ef6\u3002"
    ], 
    "%(timeSince)s via file upload": "%(timeSince)\u79d2\u901a\u8fc7\u6587\u4ef6\u4e0a\u4f20", 
    "%s word": [
      "%s \u8bcd %s \u8bcd"
    ], 
    "%s's accepted suggestions": "%s \u7684\u83b7\u51c6\u5efa\u8bae", 
    "%s's overwritten submissions": "%s \u7684\u88ab\u8986\u76d6\u7684\u63d0\u4ea4", 
    "%s's pending suggestions": "%s \u7684\u5f85\u5ba1\u5efa\u8bae", 
    "%s's rejected suggestions": "%s \u7684\u88ab\u62d2\u5efa\u8bae", 
    "%s's submissions": "%s \u7684\u63d0\u4ea4", 
    "Accept": "\u63a5\u53d7", 
    "Account Activation": "\u5e10\u53f7\u6fc0\u6d3b", 
    "Account Inactive": "\u8d26\u53f7\u5df2\u505c\u7528", 
    "Active": "\u6d3b\u8dc3", 
    "Add Language": "\u6dfb\u52a0\u8bed\u8a00", 
    "Add Project": "\u6dfb\u52a0\u9879\u76ee", 
    "Add User": "\u6dfb\u52a0\u7528\u6237", 
    "Administrator": "\u7ba1\u7406\u5458", 
    "After changing your password you will sign in automatically.": "\u66f4\u6539\u60a8\u7684\u5bc6\u7801\u540e\uff0c\u60a8\u5c06\u81ea\u52a8\u767b\u5f55\u3002", 
    "All Languages": "\u6240\u6709\u8bed\u8a00", 
    "All Projects": "\u6240\u6709\u9879\u76ee", 
    "An error occurred while attempting to sign in via %s.": "\u8bd5\u56fe\u901a\u8fc7%s\u767b\u9646\u65f6\u53d1\u751f\u4e86\u9519\u8bef\u3002", 
    "An error occurred while attempting to sign in via your social account.": "\u8bd5\u56fe\u901a\u8fc7\u60a8\u7684\u793e\u4ea4\u7f51\u7edc\u8d26\u6237\u767b\u9646\u65f6\u53d1\u751f\u4e86\u9519\u8bef\u3002", 
    "Avatar": "\u5934\u50cf", 
    "Cancel": "\u53d6\u6d88", 
    "Clear all": "\u5168\u90e8\u6e05\u9664", 
    "Clear value": "\u6e05\u9664\u503c", 
    "Close": "\u5173\u95ed", 
    "Code": "\u4ee3\u7801", 
    "Collapse details": "\u6536\u8d77\u7ec6\u8282", 
    "Congratulations! You have completed this task!": "\u795d\u8d3a\u60a8\uff0c\u60a8\u5df2\u5b8c\u6210\u5168\u90e8\u9879\u76ee\uff01", 
    "Contact Us": "\u8054\u7cfb\u6211\u4eec", 
    "Contributors, 30 Days": "\u8d21\u732e\u8005\uff0c30\u5929", 
    "Creating new user accounts is prohibited.": "\u4e0d\u5141\u8bb8\u6ce8\u518c\u65b0\u7528\u6237\u3002", 
    "Delete": "\u5220\u9664", 
    "Deleted successfully.": "\u5220\u9664\u6210\u529f\u3002", 
    "Didn't receive an email? Check if it was accidentally filtered out as spam, or try requesting another copy of the email.": "\u6ca1\u6709\u6536\u5230\u90ae\u4ef6\uff1f\u8bf7\u68c0\u67e5\u662f\u4e0d\u662f\u88ab\u5f52\u7c7b\u4e3a\u5783\u573e\u90ae\u4ef6\uff0c\u6216\u8005\u8bf7\u6c42\u518d\u6b21\u53d1\u9001", 
    "Disabled": "\u5df2\u7981\u7528", 
    "Discard changes.": "\u820d\u5f03\u66f4\u6539", 
    "Edit Language": "\u7f16\u8f91\u8bed\u8a00", 
    "Edit My Public Profile": "\u7f16\u8f91\u6211\u7684\u516c\u5f00\u4e2a\u4eba\u8d44\u6599", 
    "Edit Project": "\u7f16\u8f91\u9879\u76ee", 
    "Edit User": "\u7f16\u8f91\u7528\u6237", 
    "Edit the suggestion before accepting, if necessary": "\u5982\u679c\u5fc5\u8981\u7684\u8bdd\u8bf7\u5728\u63a5\u53d7\u524d\u7f16\u8f91\u6b64\u5efa\u8bae", 
    "Email": "\u7535\u5b50\u90ae\u4ef6\u5730\u5740", 
    "Email Address": "\u7535\u5b50\u90ae\u4ef6\u5730\u5740", 
    "Email Confirmation": "\u7535\u5b50\u90ae\u4ef6\u786e\u8ba4", 
    "Enter your email address, and we will send you a message with the special link to reset your password.": "\u8bf7\u8f93\u5165\u4f60\u7684\u7535\u5b50\u90ae\u4ef6\u5730\u5740\uff0c\u6211\u4eec\u4f1a\u628a\u4e00\u5c01\u5305\u542b\u5bc6\u7801\u91cd\u7f6e\u94fe\u63a5\u7684\u90ae\u4ef6\u53d1\u9001\u5230\u4f60\u7684\u90ae\u7bb1\u91cc\u3002", 
    "Error while connecting to the server": "\u8fde\u63a5\u5230\u670d\u52a1\u5668\u65f6\u51fa\u9519", 
    "Expand details": "\u5c55\u5f00\u7ec6\u8282", 
    "File types": "\u6587\u4ef6\u7c7b\u578b", 
    "Filesystems": "\u6587\u4ef6\u7cfb\u7edf", 
    "Find language by name, code": "\u6309\u540d\u79f0\u6216\u4ee3\u7801\u67e5\u627e\u8bed\u8a00", 
    "Find project by name, code": "\u6309\u540d\u79f0\u6216\u4ee3\u7801\u67e5\u627e\u9879\u76ee", 
    "Find user by name, email, properties": "\u6309\u540d\u79f0\u3001\u7535\u5b50\u90ae\u4ef6\u5730\u5740\u6216\u5c5e\u6027\u67e5\u627e\u7528\u6237", 
    "Full Name": "\u5168\u540d", 
    "Go back to browsing": "\u8fd4\u56de\u6d4f\u89c8", 
    "Go to the next string (Ctrl+.)<br/><br/>Also:<br/>Next page: Ctrl+Shift+.<br/>Last page: Ctrl+Shift+End": "\u8f6c\u5230\u4e0b\u4e00\u4e2a\u5b57\u7b26\u4e32 (Ctrl+.)<br/><br/>\u4e5f\u53ef\u4ee5\uff1a<br/>\u4e0b\u4e00\u9875\uff1aCtrl+Shift+.<br/>\u6700\u540e\u4e00\u9875\uff1aCtrl+Shift+End", 
    "Go to the previous string (Ctrl+,)<br/><br/>Also:<br/>Previous page: Ctrl+Shift+,<br/>First page: Ctrl+Shift+Home": "\u8f6c\u5230\u4e0a\u4e00\u4e2a\u5b57\u7b26\u4e32 (Ctrl+.)<br/><br/>\u4e5f\u53ef\u4ee5\uff1a<br/>\u4e0a\u4e00\u9875\uff1aCtrl+Shift+,<br/>\u7b2c\u4e00\u9875\uff1aCtrl+Shift+Home", 
    "Hide": "\u9690\u85cf", 
    "Hide disabled": "\u9690\u85cf\u5df2\u7981\u7528", 
    "I forgot my password": "\u6211\u5fd8\u8bb0\u4e86\u5bc6\u7801", 
    "Ignore Files": "\u5ffd\u7565\u6587\u4ef6", 
    "Languages": "\u8bed\u8a00", 
    "Less": "\u66f4\u5c11", 
    "LinkedIn": "LinkedIn", 
    "LinkedIn profile URL": "LinkedIn \u4e2a\u4eba\u8d44\u6599\u7f51\u5740", 
    "Load More": "\u52a0\u8f7d\u66f4\u591a", 
    "Loading...": "\u6b63\u5728\u52a0\u8f7d...", 
    "Login / Password": "\u767b\u5f55/\u5bc6\u7801", 
    "More": "\u66f4\u591a", 
    "More...": "\u66f4\u591a\u4fe1\u606f...", 
    "My Public Profile": "\u6211\u7684\u516c\u5f00\u4e2a\u4eba\u8d44\u6599", 
    "No": "\u5426", 
    "No activity recorded in a given period": "\u6307\u5b9a\u5468\u671f\u5185\u6ca1\u6709\u6d3b\u52a8\u8bb0\u5f55", 
    "No results found": "\u672a\u627e\u5230\u7ed3\u679c", 
    "No results.": "\u6ca1\u6709\u7ed3\u679c\u3002", 
    "No, thanks": "\u4e0d\uff0c\u8c22\u4e86", 
    "Not found": "\u672a\u627e\u5230", 
    "Note: when deleting a user their contributions to the site, e.g. comments, suggestions and translations, are attributed to the anonymous user (nobody).": "\u6ce8\u610f\uff1a\u5220\u9664\u7528\u6237\u5c06\u4f7f\u5176\u7684\u8d21\u732e\uff0c\u5982\u8bc4\u8bba\u3001\u5efa\u8bae\u548c\u7ffb\u8bd1\u5f52\u4e8e\u533f\u540d\u7528\u6237\u3002", 
    "Number of Plurals": "\u590d\u6570\u5f62\u5f0f\u6570\u91cf", 
    "Oops...": "Oops...", 
    "Overview": "\u6982\u89c8", 
    "Password": "\u5bc6\u7801", 
    "Password changed, signing in...": "\u5bc6\u7801\u5df2\u66f4\u6539\uff0c\u6b63\u5728\u767b\u5f55...", 
    "Permissions": "\u6743\u9650", 
    "Personal description": "\u4e2a\u4eba\u4ecb\u7ecd", 
    "Personal website URL": "\u4e2a\u4eba\u7f51\u7ad9\u7f51\u5740", 
    "Please follow that link to continue the account creation.": "\u8bf7\u70b9\u51fb\u8fd9\u4e2a\u94fe\u63a5\u7ee7\u7eed\u521b\u5efa\u5e10\u53f7\u3002", 
    "Please follow that link to continue the password reset procedure.": "\u8bf7\u70b9\u51fb\u8be5\u94fe\u63a5\u7ee7\u7eed\u5bc6\u7801\u91cd\u7f6e\u8fc7\u7a0b\u3002", 
    "Please select a valid user.": "\u8bf7\u9009\u62e9\u4e00\u4e2a\u6709\u6548\u7684\u7528\u6237\u3002", 
    "Plural Equation": "\u590d\u6570\u8868\u8fbe\u5f0f", 
    "Plural form %(index)s": "\u590d\u6570\u5f62\u5f0f %(index)s", 
    "Preview will be displayed here.": "\u9884\u89c8\u5c06\u663e\u793a\u5728\u8fd9\u91cc\u3002", 
    "Project / Language": "\u9879\u76ee / \u8bed\u8a00", 
    "Project Tree Style": "\u9879\u76ee\u6811\u6837\u5f0f", 
    "Provide optional comment (will be publicly visible)": "\u63d0\u4f9b\u53ef\u9009\u7684\u8bc4\u8bba\uff08\u5c06\u4f1a\u88ab\u516c\u5f00\u770b\u5230\uff09", 
    "Public Profile": "\u516c\u5f00\u4e2a\u4eba\u8d44\u6599", 
    "Quality Checks": "\u8d28\u91cf\u68c0\u67e5", 
    "Reject": "\u62d2\u7edd", 
    "Reload page": "\u91cd\u65b0\u8f7d\u5165\u9875\u9762", 
    "Repeat Password": "\u91cd\u590d\u5bc6\u7801", 
    "Resend Email": "\u91cd\u53d1\u7535\u5b50\u90ae\u4ef6", 
    "Reset Password": "\u91cd\u8bbe\u5bc6\u7801", 
    "Reset Your Password": "\u91cd\u8bbe\u60a8\u7684\u5bc6\u7801", 
    "Reviewed": "\u5df2\u5ba1\u9605", 
    "Save": "\u4fdd\u5b58", 
    "Saved successfully.": "\u4fdd\u5b58\u6210\u529f\u3002", 
    "Score Change": "\u5f97\u5206\u53d8\u5316", 
    "Screenshot Search Prefix": "\u5c4f\u5e55\u622a\u56fe\u641c\u7d22\u524d\u7f00", 
    "Search Languages": "\u641c\u7d22\u8bed\u8a00", 
    "Search Projects": "\u641c\u7d22\u9879\u76ee", 
    "Search Users": "\u641c\u7d22\u7528\u6237", 
    "Select...": "\u9009\u62e9...", 
    "Send Email": "\u53d1\u9001\u90ae\u4ef6", 
    "Sending email to %s...": "\u6b63\u5728\u5411 %s \u53d1\u9001\u7535\u5b50\u90ae\u4ef6", 
    "Server error": "\u670d\u52a1\u5668\u9519\u8bef", 
    "Set New Password": "\u8bbe\u7f6e\u65b0\u5bc6\u7801", 
    "Set a new password": "\u8bbe\u7f6e\u65b0\u5bc6\u7801", 
    "Settings": "\u8bbe\u7f6e", 
    "Short Bio": "\u4e2a\u4eba\u7b80\u4ecb", 
    "Show": "\u663e\u793a", 
    "Show disabled": "\u663e\u793a\u5df2\u7981\u7528", 
    "Sign In": "\u767b\u5f55", 
    "Sign In With %s": "\u4f7f\u7528%s\u767b\u9646", 
    "Sign In With...": "\u901a\u8fc7\u5176\u4ed6\u65b9\u5f0f\u767b\u5f55", 
    "Sign Up": "\u6ce8\u518c", 
    "Sign in as an existing user": "\u4ee5\u73b0\u6709\u7528\u6237\u767b\u5f55", 
    "Sign up as a new user": "\u6ce8\u518c\u65b0\u5e10\u6237", 
    "Signed in. Redirecting...": "\u5df2\u767b\u5f55\u3002\u6b63\u5728\u8df3\u8f6c...", 
    "Signing in with an external service for the first time will automatically create an account for you.": "\u4f7f\u7528\u5916\u90e8\u8d26\u6237\u7b2c\u4e00\u6b21\u767b\u9646\u65f6\u4f1a\u81ea\u52a8\u4e3a\u60a8\u521b\u5efa\u4e00\u4e2a\u8d26\u6237", 
    "Similar translations": "\u7c7b\u4f3c\u7684\u7ffb\u8bd1", 
    "Social Services": "\u793e\u4ea4\u670d\u52a1", 
    "Social Verification": "\u793e\u4f1a\u9a8c\u8bc1", 
    "Source Language": "\u6e90\u8bed\u8a00", 
    "Special Characters": "\u7279\u6b8a\u5b57\u7b26", 
    "String Errors Contact": "\u5b57\u7b26\u4e32\u9519\u8bef", 
    "Suggested": "\u5efa\u8bae\u7684", 
    "Team": "\u56e2\u961f", 
    "The password reset link was invalid, possibly because it has already been used. Please request a new password reset.": "\u5bc6\u7801\u91cd\u7f6e\u94fe\u63a5\u65e0\u6548\uff0c\u53ef\u80fd\u662f\u56e0\u4e3a\u5b83\u5df2\u7ecf\u88ab\u4f7f\u7528\u4e86\u3002\u8bf7\u91cd\u65b0\u91cd\u7f6e\u5bc6\u7801\u3002", 
    "The server seems down. Try again later.": "\u670d\u52a1\u5668\u4f3c\u4e4e\u5b95\u673a\u4e86\u3002\u8bf7\u60a8\u7a0d\u540e\u91cd\u8bd5\u3002", 
    "There are unsaved changes. Do you want to discard them?": "\u5c1a\u6709\u672a\u4fdd\u5b58\u7684\u66f4\u6539\u3002\u60a8\u8981\u820d\u5f03\u5b83\u4eec\u5417\uff1f", 
    "There is %(count)s language.": [
      "\u8fd9\u91cc\u6709 %(count)s \u79cd\u8bed\u8a00\u3002\u4e0b\u9762\u662f\u6700\u8fd1\u6dfb\u52a0\u7684\u3002"
    ], 
    "There is %(count)s project.": [
      "\u8fd9\u91cc\u6709 %(count)s \u4e2a\u9879\u76ee\u3002\u8fd9\u91cc\u6709 %(count)s \u4e2a\u9879\u76ee\u3002\u4ee5\u4e0b\u9879\u76ee\u6309\u7167\u6700\u8fd1\u6dfb\u52a0\u65f6\u95f4\u6392\u5e8f\u3002"
    ], 
    "There is %(count)s user.": [
      "\u8fd9\u91cc\u6709 %(count)s \u4e2a\u7528\u6237\u3002\u8fd9\u91cc\u6709 %(count)s \u4e2a\u7528\u6237\u3002\u4e0b\u9762\u663e\u793a\u7684\u662f\u6700\u8fd1\u6ce8\u518c\u7684\u7528\u6237\u3002"
    ], 
    "This email confirmation link expired or is invalid.": "\u8fd9\u4e2a\u786e\u8ba4\u94fe\u63a5\u5df2\u5931\u6548\u6216\u662f\u65e0\u6548\u7684", 
    "This string no longer exists.": "\u8fd9\u4e2a\u5b57\u7b26\u4e32\u5df2\u4e0d\u5b58\u5728\u3002", 
    "To set or change your avatar for your email address (%(email)s), please go to gravatar.com.": "\u8981\u8bbe\u7f6e\u6216\u8005\u66f4\u6539\u5c06\u7528\u4e8e\u60a8\u7684\u7535\u5b50\u90ae\u4ef6\u5730\u5740 (%(email)s) \u7684\u5934\u50cf\uff0c\u8bf7\u8bbf\u95ee gravatar.com\u3002", 
    "Translated": "\u5df2\u7ffb\u8bd1", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project": "\u5df2\u88ab %(fullname)s \u5728 &ldquo;<span title=\"%(path)s\">%(project)s</span>&rdquo; \u9879\u76ee\u4e2d\u7ffb\u8bd1", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project %(time_ago)s": "\u7531 %(fullname)s \u7ffb\u8bd1\u4e8e &ldquo;<span title=\"%(path)s\">%(project)s</span>&rdquo; \u9879\u76ee\u4e2d %(time_ago)s", 
    "Try again": "\u91cd\u8bd5", 
    "Twitter": "Twitter", 
    "Twitter username": "Twitter \u7528\u6237\u540d", 
    "Type to search": "\u8f93\u5165\u8fdb\u884c\u641c\u7d22", 
    "Updating data": "\u66f4\u65b0\u6570\u636e", 
    "Use the search form to find the language, then click on a language to edit.": "\u4f7f\u7528\u641c\u7d22\u8868\u5355\u67e5\u627e\u8bed\u8a00\uff0c\u7136\u540e\u70b9\u51fb\u4e00\u4e2a\u8bed\u8a00\u4ee5\u7f16\u8f91\u3002", 
    "Use the search form to find the project, then click on a project to edit.": "\u4f7f\u7528\u641c\u7d22\u8868\u683c\u6765\u67e5\u627e\u9879\u76ee\uff0c\u7136\u540e\u70b9\u51fb\u4e00\u4e2a\u9879\u76ee\u4ee5\u7f16\u8f91\u3002", 
    "Use the search form to find the user, then click on a user to edit.": "\u4f7f\u7528\u641c\u7d22\u8868\u5355\u67e5\u627e\u7528\u6237\uff0c\u7136\u540e\u70b9\u51fb\u7528\u6237\u4ee5\u7f16\u8f91\u3002", 
    "Username": "\u7528\u6237\u540d", 
    "We found a user with <span>%(email)s</span> email in our system. Please provide the password to finish the sign in procedure. This is a one-off procedure, which will establish a link between your Pootle and %(provider)s accounts.": "\u6211\u4eec\u53d1\u73b0\u5df2\u7ecf\u6709\u4e00\u4e2a\u7528\u6237\u4f7f\u7528 <span>%s</span> \u7684\u90ae\u7bb1\u5730\u5740\u6ce8\u518c\u4e86\u3002\u8bf7\u8f93\u5165\u5bc6\u7801\u6765\u5b8c\u6210\u767b\u9646\u3002\u8fd9\u53ea\u662f\u4e2a\u4e00\u6b21\u6027\u7684\u64cd\u4f5c\uff0c\u4e4b\u540e\u4f60\u7684Pootle\u8d26\u6237\u5c06\u4f1a\u548c %s \u8d26\u6237\u7ed1\u5b9a\u3002", 
    "We have sent an email containing the special link to <span>%s</span>": "\u6211\u4eec\u5df2\u7ecf\u53d1\u9001\u4e86\u4e00\u5c01\u7535\u5b50\u90ae\u4ef6\uff0c\u8be5\u90ae\u4ef6\u4e2d\u5305\u542b\u4e86<span>%s</span>\u7684\u94fe\u63a5\u3002", 
    "We have sent an email containing the special link to <span>%s</span>. Please check your spam folder if you do not see the email.": "\u6211\u4eec\u5df2\u7ecf\u53d1\u9001\u4e86\u4e00\u5c01\u7535\u5b50\u90ae\u4ef6\uff0c\u8be5\u90ae\u4ef6\u4e2d\u5305\u542b\u4e86<span>%s</span>\u7684\u94fe\u63a5\u3002", 
    "We have sent an email containing the special link to the address used to register this account. Please check your spam folder if you do not see the email.": "\u6211\u4eec\u5df2\u7ecf\u53d1\u9001\u4e86\u4e00\u5c01\u7535\u5b50\u90ae\u4ef6\uff0c\u8be5\u90ae\u4ef6\u4e2d\u542b\u6709\u7528\u4e8e\u6ce8\u518c\u8be5\u5e10\u53f7\u7684\u94fe\u63a5\u3002", 
    "Website": "\u7f51\u7ad9", 
    "Why are you part of our translation project? Describe yourself, inspire others!": "\u4f60\u4e3a\u4f55\u6210\u4e3a\u4e86\u7ffb\u8bd1\u9879\u76ee\u7684\u4e00\u5458\uff1f\u4ecb\u7ecd\u81ea\u5df1\uff0c\u6fc0\u52b1\u4ed6\u4eba\uff01", 
    "Yes": "\u662f", 
    "You have unsaved changes in this string. Navigating away will discard those changes.": "\u4f60\u5728\u8fd9\u4e2a\u5355\u5143\u6709\u672a\u4fdd\u5b58\u7684\u6570\u636e\u3002\u79bb\u5f00\u4f1a\u4e22\u5931\u8fd9\u4e9b\u6570\u636e\u3002", 
    "Your Full Name": "\u60a8\u7684\u5168\u540d", 
    "Your LinkedIn profile URL": "\u60a8\u7684 LinkedIn \u4e2a\u4eba\u8d44\u6599\u7f51\u5740", 
    "Your Personal website/blog URL": "\u60a8\u7684\u4e2a\u4eba\u7f51\u7ad9/\u535a\u5ba2\u7f51\u5740", 
    "Your Twitter username": "\u60a8\u7684 Twitter \u7528\u6237\u540d", 
    "Your account is inactive because an administrator deactivated it.": "\u60a8\u7684\u5e10\u53f7\u5df2\u88ab\u7ba1\u7406\u5458\u505c\u7528\u3002", 
    "Your account needs activation.": "\u60a8\u7684\u5e10\u53f7\u9700\u8981\u6fc0\u6d3b\u3002", 
    "disabled": "\u5df2\u7981\u7528", 
    "some anonymous user": "\u4e00\u4e9b\u533f\u540d\u7528\u6237", 
    "someone": "\u67d0\u4eba"
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

