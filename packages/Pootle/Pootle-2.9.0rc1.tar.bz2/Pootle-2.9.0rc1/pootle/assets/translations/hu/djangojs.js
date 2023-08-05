

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
    "#%(position)s": "%(position)s.", 
    "%(count)s language matches your query.": [
      "%(count)s nyelv felel meg a lek\u00e9rdez\u00e9snek.", 
      "%(count)s nyelv felel meg a lek\u00e9rdez\u00e9snek."
    ], 
    "%(count)s project matches your query.": [
      "%(count)s projekt felel meg a lek\u00e9rdez\u00e9snek.", 
      "%(count)s projekt felel meg a lek\u00e9rdez\u00e9snek."
    ], 
    "%(count)s user matches your query.": [
      "%(count)s felhaszn\u00e1l\u00f3 felel meg a lek\u00e9rdez\u00e9snek.", 
      "%(count)s felhaszn\u00e1l\u00f3 felel meg a lek\u00e9rdez\u00e9snek."
    ], 
    "%(timeSince)s via file upload": "%(timeSince)s f\u00e1jlfelt\u00f6lt\u00e9sen kereszt\u00fcl", 
    "%s word": [
      "%s sz\u00f3", 
      "%s sz\u00f3"
    ], 
    "%s's accepted suggestions": "%s elfogadta a javaslatokat", 
    "%s's overwritten submissions": "%s fel\u00fcl\u00edrt bek\u00fcld\u00e9sei", 
    "%s's pending suggestions": "%s f\u00fcgg\u0151 javaslatai", 
    "%s's rejected suggestions": "%s elutas\u00edtott javaslatai", 
    "%s's submissions": "%s bek\u00fcld\u00e9sei", 
    "Accept": "Elfogad\u00e1s", 
    "Account Activation": "Fi\u00f3kaktiv\u00e1l\u00e1s", 
    "Account Inactive": "A fi\u00f3k inakt\u00edv", 
    "Active": "Akt\u00edv", 
    "Add Language": "Nyelv hozz\u00e1ad\u00e1sa", 
    "Add Project": "Projekt hozz\u00e1ad\u00e1sa", 
    "Add User": "Felhaszn\u00e1l\u00f3 hozz\u00e1ad\u00e1sa", 
    "Administrator": "Adminisztr\u00e1tor", 
    "After changing your password you will sign in automatically.": "A jelsz\u00f3 megv\u00e1ltoztat\u00e1sa ut\u00e1n automatikusan be lesz l\u00e9ptetve.", 
    "All Languages": "Minden nyelv", 
    "All Projects": "Minden projekt", 
    "An error occurred while attempting to sign in via %s.": "Hiba t\u00f6rt\u00e9nt egy %s bejelentkez\u00e9si k\u00eds\u00e9rlet sor\u00e1n.", 
    "An error occurred while attempting to sign in via your social account.": "Hiba t\u00f6rt\u00e9nt a k\u00f6z\u00f6ss\u00e9gi fi\u00f3kj\u00e1n kereszt\u00fcl val\u00f3 bejelentkez\u00e9sre tett k\u00eds\u00e9rlet sor\u00e1n.", 
    "Avatar": "Avatar", 
    "Cancel": "M\u00e9gse", 
    "Clear all": "\u00d6sszes t\u00f6rl\u00e9se", 
    "Clear value": "\u00c9rt\u00e9k t\u00f6rl\u00e9se", 
    "Close": "Bez\u00e1r\u00e1s", 
    "Code": "K\u00f3d", 
    "Collapse details": "R\u00e9szletek elrejt\u00e9se", 
    "Congratulations! You have completed this task!": "Gratul\u00e1lunk! Befejezte ezt a feladatot!", 
    "Contact Us": "Kapcsolat", 
    "Contributors, 30 Days": "K\u00f6zrem\u0171k\u00f6d\u0151k, 30 nap", 
    "Creating new user accounts is prohibited.": "\u00daj felhaszn\u00e1l\u00f3i fi\u00f3kok l\u00e9trehoz\u00e1sa tilos.", 
    "Delete": "T\u00f6rl\u00e9s", 
    "Deleted successfully.": "Sikeresen t\u00f6r\u00f6lve.", 
    "Didn't receive an email? Check if it was accidentally filtered out as spam, or try requesting another copy of the email.": "Nem kapott e-mailt? Ellen\u0151rizze, hogy nem ker\u00fclt-e v\u00e9letlen\u00fcl a lev\u00e9lszem\u00e9t k\u00f6z\u00e9, vagy pr\u00f3b\u00e1ljon \u00faj e-mailt k\u00e9rni.", 
    "Disabled": "Letiltva", 
    "Discard changes.": "V\u00e1ltoztat\u00e1sok elvet\u00e9se.", 
    "Edit Language": "Nyelv szerkeszt\u00e9se", 
    "Edit My Public Profile": "Nyilv\u00e1nos profil szerkeszt\u00e9se", 
    "Edit Project": "Projekt szerkeszt\u00e9se", 
    "Edit User": "Felhaszn\u00e1l\u00f3 szerkeszt\u00e9se", 
    "Edit the suggestion before accepting, if necessary": "Elfogad\u00e1s el\u0151tt szerkessze a javaslatot, ha sz\u00fcks\u00e9ges", 
    "Email": "E-mail", 
    "Email Address": "E-mail c\u00edm", 
    "Email Confirmation": "E-mail meger\u0151s\u00edt\u00e9s", 
    "Enter your email address, and we will send you a message with the special link to reset your password.": "Adja meg e-mail c\u00edm\u00e9t, \u00e9s elk\u00fcldj\u00fck a jelsz\u00f3 vissza\u00e1ll\u00edt\u00e1s\u00e1hoz sz\u00fcks\u00e9ges speci\u00e1lis hivatkoz\u00e1st.", 
    "Error while connecting to the server": "Hiba a kiszolg\u00e1l\u00f3hoz val\u00f3 kapcsol\u00f3d\u00e1s k\u00f6zben", 
    "Expand details": "R\u00e9szletek megjelen\u00edt\u00e9se", 
    "File types": "F\u00e1jlt\u00edpusok", 
    "Filesystems": "F\u00e1jlrendszerek", 
    "Find language by name, code": "Nyelv keres\u00e9se n\u00e9v, k\u00f3d alapj\u00e1n", 
    "Find project by name, code": "Projekt keres\u00e9se n\u00e9v, k\u00f3d alapj\u00e1n", 
    "Find user by name, email, properties": "Felhaszn\u00e1l\u00f3 keres\u00e9se n\u00e9v, e-mail tulajdons\u00e1gok szerint", 
    "Full Name": "Teljes n\u00e9v", 
    "Go back to browsing": "Vissza a tall\u00f3z\u00e1shoz", 
    "Go to the next string (Ctrl+.)<br/><br/>Also:<br/>Next page: Ctrl+Shift+.<br/>Last page: Ctrl+Shift+End": "Ugr\u00e1s a k\u00f6vetkez\u0151 karakterl\u00e1ncra (Ctrl+.)<br/><br/>Tov\u00e1bb\u00e1:<br/>K\u00f6vetkez\u0151 oldal: Ctrl+Shift+.<br/>Utols\u00f3 oldal: Ctrl+Shift+End", 
    "Go to the previous string (Ctrl+,)<br/><br/>Also:<br/>Previous page: Ctrl+Shift+,<br/>First page: Ctrl+Shift+Home": "Ugr\u00e1s az el\u0151z\u0151 karakterl\u00e1ncra (Ctrl+,)<br/><br/>Tov\u00e1bb\u00e1:<br/>El\u0151z\u0151 oldal: Ctrl+Shift+,<br/>Els\u0151 oldal: Ctrl+Shift+Home", 
    "Hide": "Elrejt\u00e9s", 
    "Hide disabled": "Letiltottak elrejt\u00e9se", 
    "I forgot my password": "Elfelejtett jelsz\u00f3", 
    "Ignore Files": "F\u00e1jlok figyelmen k\u00edv\u00fcl hagy\u00e1sa", 
    "Languages": "Nyelvek", 
    "Less": "Kevesebb", 
    "LinkedIn": "LinkedIn", 
    "LinkedIn profile URL": "LinkedIn profil URL", 
    "Load More": "T\u00f6bb bet\u00f6lt\u00e9se", 
    "Loading...": "Bet\u00f6lt\u00e9s\u2026", 
    "Login / Password": "Bejelentkez\u00e9s / Jelsz\u00f3", 
    "More": "T\u00f6bb", 
    "More...": "T\u00f6bb\u2026", 
    "My Public Profile": "Nyilv\u00e1nos profil", 
    "No": "Nem", 
    "No activity recorded in a given period": "Nincs feljegyezve tev\u00e9kenys\u00e9g a megadott id\u0151szakban", 
    "No results found": "Nincs tal\u00e1lat", 
    "No results.": "Nincs tal\u00e1lat.", 
    "No, thanks": "Nem, k\u00f6sz\u00f6n\u00f6m", 
    "Not found": "Nem tal\u00e1lhat\u00f3", 
    "Note: when deleting a user their contributions to the site, e.g. comments, suggestions and translations, are attributed to the anonymous user (nobody).": "Megjegyz\u00e9s: felhaszn\u00e1l\u00f3 t\u00f6rl\u00e9sekor az oldalon v\u00e9gzett m\u00f3dos\u00edt\u00e1sai, p\u00e9ld\u00e1ul megjegyz\u00e9sek, javaslatok \u00e9s ford\u00edt\u00e1sok a n\u00e9vtelen felhaszn\u00e1l\u00f3 (nobody) tulajdon\u00e1ba ker\u00fclnek.", 
    "Number of Plurals": "T\u00f6bbes alakok sz\u00e1ma", 
    "Oops...": "Hopp\u00e1\u2026", 
    "Overview": "\u00c1ttekint\u00e9s", 
    "Password": "Jelsz\u00f3", 
    "Password changed, signing in...": "A jelsz\u00f3 megv\u00e1ltozott, bejelentkez\u00e9s\u2026", 
    "Permissions": "Jogosults\u00e1gok", 
    "Personal description": "Szem\u00e9lyes le\u00edr\u00e1s", 
    "Personal website URL": "Szem\u00e9lyes weboldal URL", 
    "Please follow that link to continue the account creation.": "K\u00f6vesse azt a hivatkoz\u00e1st a fi\u00f3k l\u00e9trehoz\u00e1s\u00e1nak folytat\u00e1s\u00e1hoz.", 
    "Please follow that link to continue the password reset procedure.": "K\u00f6vesse ezt a hivatkoz\u00e1st a jelsz\u00f3-vissza\u00e1ll\u00edt\u00e1si folyamat folytat\u00e1s\u00e1hoz.", 
    "Please select a valid user.": "V\u00e1lasszon egy \u00e9rv\u00e9nyes felhaszn\u00e1l\u00f3t.", 
    "Plural Equation": "T\u00f6bbes alakok egyenlete", 
    "Plural form %(index)s": "%(index)s. t\u00f6bbes alak", 
    "Preview will be displayed here.": "Az el\u0151n\u00e9zet itt jelenik meg.", 
    "Project / Language": "Projekt / Nyelv", 
    "Project Tree Style": "Projektfa st\u00edlus", 
    "Provide optional comment (will be publicly visible)": "Tov\u00e1bbi megjegyz\u00e9s hozz\u00e1ad\u00e1sa (ez nyilv\u00e1nos lesz)", 
    "Public Profile": "Nyilv\u00e1nos profil", 
    "Quality Checks": "Min\u0151s\u00e9g-ellen\u0151rz\u00e9sek", 
    "Reject": "Elutas\u00edt\u00e1s", 
    "Reload page": "Oldal \u00fajrat\u00f6lt\u00e9se", 
    "Repeat Password": "Jelsz\u00f3 ism\u00e9tl\u00e9se", 
    "Resend Email": "E-mail \u00fajrak\u00fcld\u00e9se", 
    "Reset Password": "Jelsz\u00f3 vissza\u00e1ll\u00edt\u00e1sa", 
    "Reset Your Password": "Jelsz\u00f3 vissza\u00e1ll\u00edt\u00e1sa", 
    "Reviewed": "Lektor\u00e1lva", 
    "Save": "Ment\u00e9s", 
    "Saved successfully.": "Sikeresen mentve.", 
    "Score Change": "Pontsz\u00e1mm\u00f3dos\u00edt\u00e1s", 
    "Screenshot Search Prefix": "K\u00e9perny\u0151k\u00e9p-keres\u00e9s el\u0151tagja", 
    "Search Languages": "Nyelvek keres\u00e9se", 
    "Search Projects": "Projektek keres\u00e9se", 
    "Search Users": "Felhaszn\u00e1l\u00f3keres\u00e9s", 
    "Select...": "V\u00e1lasszon\u2026", 
    "Send Email": "E-mail k\u00fcld\u00e9se", 
    "Sending email to %s...": "E-mail k\u00fcld\u00e9se ide: %s\u2026", 
    "Server error": "Kiszolg\u00e1l\u00f3hiba", 
    "Set New Password": "\u00daj jelsz\u00f3 be\u00e1ll\u00edt\u00e1sa", 
    "Set a new password": "\u00daj jelsz\u00f3 be\u00e1ll\u00edt\u00e1sa", 
    "Settings": "Be\u00e1ll\u00edt\u00e1sok", 
    "Short Bio": "R\u00f6vid bemutatkoz\u00e1s", 
    "Show": "Megjelen\u00edt\u00e9s", 
    "Show disabled": "Letiltottak megjelen\u00edt\u00e9se", 
    "Sign In": "Bejelentkez\u00e9s", 
    "Sign In With %s": "Bejelentkez\u00e9s ezzel: %s", 
    "Sign In With...": "Bejelentkez\u00e9s ezzel\u2026", 
    "Sign Up": "Regisztr\u00e1ci\u00f3", 
    "Sign in as an existing user": "Bejelentkez\u00e9s megl\u00e9v\u0151 felhaszn\u00e1l\u00f3k\u00e9nt", 
    "Sign up as a new user": "Regisztr\u00e1ci\u00f3 \u00faj felhaszn\u00e1l\u00f3k\u00e9nt", 
    "Signed in. Redirecting...": "Bejelentkezett. \u00c1tir\u00e1ny\u00edt\u00e1s\u2026", 
    "Signing in with an external service for the first time will automatically create an account for you.": "K\u00fcls\u0151 szolg\u00e1ltat\u00e1son kereszt\u00fcli els\u0151 bejelentkez\u00e9skor automatikusan l\u00e9trej\u00f6n a fi\u00f3k.", 
    "Similar translations": "Hasonl\u00f3 ford\u00edt\u00e1sok", 
    "Social Services": "K\u00f6z\u00f6ss\u00e9gi szolg\u00e1ltat\u00e1sok", 
    "Social Verification": "K\u00f6z\u00f6ss\u00e9gi ellen\u0151rz\u00e9s", 
    "Source Language": "Forr\u00e1snyelv", 
    "Special Characters": "Speci\u00e1lis karakterek", 
    "String Errors Contact": "Karakterl\u00e1nchib\u00e1k kapcsolattart\u00f3ja", 
    "Suggested": "Javasolt", 
    "Team": "Csapat", 
    "The password reset link was invalid, possibly because it has already been used. Please request a new password reset.": "A jelsz\u00f3-vissza\u00e1ll\u00edt\u00e1si hivatkoz\u00e1s \u00e9rv\u00e9nytelen volt, val\u00f3sz\u00edn\u0171leg m\u00e1r felhaszn\u00e1lta. K\u00e9rjen \u00faj jelsz\u00f3-vissza\u00e1ll\u00edt\u00e1st.", 
    "The server seems down. Try again later.": "\u00dagy t\u0171nik, a kiszolg\u00e1l\u00f3 le\u00e1llt. Pr\u00f3b\u00e1lja meg k\u00e9s\u0151bb.", 
    "There are unsaved changes. Do you want to discard them?": "A m\u00f3dos\u00edt\u00e1sok m\u00e9g nincsenek mentve. El szeretn\u00e9 menteni ezeket?", 
    "There is %(count)s language.": [
      "%(count)s nyelv van.", 
      "%(count)s nyelv van. Al\u00e1bb l\u00e1that\u00f3k a legut\u00f3bb felvettek."
    ], 
    "There is %(count)s project.": [
      "%(count)s projekt van.", 
      "%(count)s projekt van. Al\u00e1bb l\u00e1that\u00f3k a legut\u00f3bb felvettek."
    ], 
    "There is %(count)s user.": [
      "%(count)s felhaszn\u00e1l\u00f3 van.", 
      "%(count)s felhaszn\u00e1l\u00f3 van. Al\u00e1bb l\u00e1that\u00f3k a legut\u00f3bb felvettek."
    ], 
    "This email confirmation link expired or is invalid.": "Ez az e-mail meger\u0151s\u00edt\u00e9si hivatkoz\u00e1s lej\u00e1rt vagy \u00e9rv\u00e9nytelen.", 
    "This string no longer exists.": "Ez a karakterl\u00e1nc m\u00e1r nem l\u00e9tezik.", 
    "To set or change your avatar for your email address (%(email)s), please go to gravatar.com.": "Az e-mail c\u00edm\u00e9hez (%(email)s) tartoz\u00f3 avatar be\u00e1ll\u00edt\u00e1s\u00e1hoz vagy m\u00f3dos\u00edt\u00e1s\u00e1hoz keresse fel a gravatar.com oldalt.", 
    "Translated": "Leford\u00edtott", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project": "Ford\u00edtotta: %(fullname)s, itt: \u201e<span title=\"%(path)s\">%(project)s</span>\u201d projekt", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project %(time_ago)s": "Ford\u00edtotta: %(fullname)s, itt: \u201e<span title=\"%(path)s\">%(project)s</span>\u201d projekt, %(time_ago)s", 
    "Try again": "Pr\u00f3b\u00e1lja \u00fajra", 
    "Twitter": "Twitter", 
    "Twitter username": "Twitter felhaszn\u00e1l\u00f3n\u00e9v", 
    "Type to search": "G\u00e9peljen a keres\u00e9shez", 
    "Updating data": "Adatok friss\u00edt\u00e9se", 
    "Use the search form to find the language, then click on a language to edit.": "A keres\u00e9si \u0171rlappal keresse meg a nyelvet, majd kattintson r\u00e1 a szerkeszt\u00e9s\u00e9hez.", 
    "Use the search form to find the project, then click on a project to edit.": "A keres\u00e9si \u0171rlappal keresse meg a projektet, majd kattintson r\u00e1 a szerkeszt\u00e9shez.", 
    "Use the search form to find the user, then click on a user to edit.": "A keres\u00e9si \u0171rlappal keresse meg a felhaszn\u00e1l\u00f3t, majd kattintson r\u00e1 a szerkeszt\u00e9s\u00e9hez.", 
    "Username": "Felhaszn\u00e1l\u00f3n\u00e9v", 
    "We found a user with <span>%(email)s</span> email in our system. Please provide the password to finish the sign in procedure. This is a one-off procedure, which will establish a link between your Pootle and %(provider)s accounts.": "Tal\u00e1ltunk egy felhaszn\u00e1l\u00f3t a rendszerben ezzel az e-mail c\u00edmmel: <span>%s</span>. Adja meg a jelsz\u00f3t a bejelentkez\u00e9si folyamat befejez\u00e9s\u00e9hez. Ez egy egyszeri l\u00e9p\u00e9s a Pootle \u00e9s a(z) %(provider)s fi\u00f3kjai k\u00f6zti kapcsolat l\u00e9trehoz\u00e1s\u00e1hoz.", 
    "We have sent an email containing the special link to <span>%s</span>": "Elk\u00fcldt\u00fcnk egy e-mailt a speci\u00e1lis hivatkoz\u00e1ssal ide: <span>%s</span>", 
    "We have sent an email containing the special link to <span>%s</span>. Please check your spam folder if you do not see the email.": "Elk\u00fcldt\u00fcnk egy e-mailt a speci\u00e1lis hivatkoz\u00e1ssal ide: <span>%s</span>. Ellen\u0151rizze a lev\u00e9lszem\u00e9t mapp\u00e1j\u00e1t, ha nem l\u00e1tja az e-mailt.", 
    "We have sent an email containing the special link to the address used to register this account. Please check your spam folder if you do not see the email.": "Elk\u00fcldt\u00fcnk egy e-mailt a speci\u00e1lis hivatkoz\u00e1ssal a fi\u00f3k regisztr\u00e1l\u00e1s\u00e1ra haszn\u00e1lt c\u00edmre. Ellen\u0151rizze a lev\u00e9lszem\u00e9t mapp\u00e1j\u00e1t, ha nem l\u00e1tja az e-mailt.", 
    "Website": "Weboldal", 
    "Why are you part of our translation project? Describe yourself, inspire others!": "Mi\u00e9rt vesz r\u00e9szt ford\u00edt\u00e1si projekt\u00fcnkben? Mutatkozzon be, mutasson p\u00e9ld\u00e1t!", 
    "Yes": "Igen", 
    "You have unsaved changes in this string. Navigating away will discard those changes.": "A karakterl\u00e1ncban mentetlen m\u00f3dos\u00edt\u00e1sok vannak. M\u00e1s oldalra l\u00e9pve ezek elvesznek.", 
    "Your Full Name": "A teljes neve", 
    "Your LinkedIn profile URL": "LinkedIn profil URL-je", 
    "Your Personal website/blog URL": "Szem\u00e9lyes weboldala/blog URL-je", 
    "Your Twitter username": "Twitter felhaszn\u00e1l\u00f3neve", 
    "Your account is inactive because an administrator deactivated it.": "Fi\u00f3kja inakt\u00edv, mert egy adminisztr\u00e1tor letiltotta.", 
    "Your account needs activation.": "A fi\u00f3kj\u00e1t aktiv\u00e1lni kell.", 
    "disabled": "letiltva", 
    "some anonymous user": "egy n\u00e9vtelen felhaszn\u00e1l\u00f3", 
    "someone": "valaki"
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

