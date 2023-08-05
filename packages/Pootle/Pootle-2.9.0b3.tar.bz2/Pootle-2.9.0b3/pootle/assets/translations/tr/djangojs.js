

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
      "%(count)s dil sorgunuzla e\u015fle\u015fiyor.", 
      "%(count)s dil sorgunuzla e\u015fle\u015fiyor."
    ], 
    "%(count)s project matches your query.": [
      "%(count)s proje sorgunuzla e\u015fle\u015fiyor.", 
      "%(count)s proje sorgunuzla e\u015fle\u015fiyor."
    ], 
    "%(count)s user matches your query.": [
      "%(count)s kullan\u0131c\u0131 sorgunuzla e\u015fle\u015fiyor.", 
      "%(count)s kullan\u0131c\u0131 sorgunuzla e\u015fle\u015fiyor."
    ], 
    "%(timeSince)s via file upload": "%(timeSince)s arac\u0131l\u0131\u011f\u0131yla dosya g\u00f6nderme", 
    "%s word": [
      "%s kelime", 
      "%s kelime"
    ], 
    "%s's accepted suggestions": "%s kullan\u0131c\u0131s\u0131n\u0131n kabul edilen \u00f6nerileri", 
    "%s's overwritten submissions": "%s kullan\u0131c\u0131s\u0131n\u0131n \u00fczerine yaz\u0131lan sunu\u015flar\u0131", 
    "%s's pending suggestions": "%s kullan\u0131c\u0131s\u0131n\u0131n bekleyen \u00f6nerileri", 
    "%s's rejected suggestions": "%s kullan\u0131c\u0131s\u0131n\u0131n reddedilen \u00f6nerileri", 
    "%s's submissions": "%s kullan\u0131c\u0131s\u0131n\u0131n sunu\u015flar\u0131", 
    "Accept": "Kabul Et", 
    "Account Activation": "Hesap Etkinle\u015ftirmesi", 
    "Account Inactive": "Hesap Devre D\u0131\u015f\u0131", 
    "Active": "Etkin", 
    "Add Language": "Dil Ekle", 
    "Add Project": "Proje Ekle", 
    "Add User": "Kullan\u0131c\u0131 Ekle", 
    "Administrator": "Y\u00f6netici", 
    "After changing your password you will sign in automatically.": "Parolan\u0131z de\u011fi\u015ftikten sonra otomatik olarak giri\u015f yapacaks\u0131n\u0131z.", 
    "All Languages": "T\u00fcm Diller", 
    "All Projects": "T\u00fcm Projeler", 
    "An error occurred while attempting to sign in via %s.": "%s arac\u0131l\u0131\u011f\u0131yla giri\u015f yapmaya \u00e7al\u0131\u015f\u0131rken bir hata meydana geldi.", 
    "An error occurred while attempting to sign in via your social account.": "Sosyal hesab\u0131n\u0131z arac\u0131l\u0131\u011f\u0131yla giri\u015f yapmaya \u00e7al\u0131\u015f\u0131rken bir hata meydana geldi.", 
    "Avatar": "Avatar", 
    "Cancel": "\u0130ptal", 
    "Clear all": "T\u00fcm\u00fcn\u00fc temizle", 
    "Clear value": "De\u011feri temizle", 
    "Close": "Kapat", 
    "Code": "Kod", 
    "Collapse details": "Ayr\u0131nt\u0131lar\u0131 daralt", 
    "Congratulations! You have completed this task!": "Tebrikler! Bu g\u00f6revi tamamlad\u0131n\u0131z!", 
    "Contact Us": "Bize Ula\u015f\u0131n", 
    "Contributors, 30 Days": "Katk\u0131da Bulunanlar, 30 G\u00fcnl\u00fck", 
    "Creating new user accounts is prohibited.": "Yeni kullan\u0131c\u0131 hesaplar\u0131 olu\u015fturma yasaklanm\u0131\u015ft\u0131r.", 
    "Delete": "Sil", 
    "Deleted successfully.": "Ba\u015far\u0131l\u0131 olarak silindi.", 
    "Didn't receive an email? Check if it was accidentally filtered out as spam, or try requesting another copy of the email.": "Bir eposta almad\u0131n\u0131z m\u0131? Kazara istenmeyen ileti olarak s\u00fcz\u00fcld\u00fcyse kontrol edin ya da epostan\u0131n ba\u015fka bir kopyas\u0131n\u0131 istemeye \u00e7al\u0131\u015f\u0131n.", 
    "Disabled": "Etkisizle\u015ftirildi", 
    "Discard changes.": "De\u011fi\u015fikliklerden vazge\u00e7.", 
    "Edit Language": "Dili D\u00fczenle", 
    "Edit My Public Profile": "Ortak Profilimi D\u00fczenle", 
    "Edit Project": "Projeyi D\u00fczenle", 
    "Edit User": "Kullan\u0131c\u0131y\u0131 D\u00fczenle", 
    "Edit the suggestion before accepting, if necessary": "E\u011fer gerekliyse, kabul etmeden \u00f6nce \u00f6neriyi d\u00fczenleyin", 
    "Email": "Eposta", 
    "Email Address": "ePosta Adresi", 
    "Email Confirmation": "Eposta Onay\u0131", 
    "Enter your email address, and we will send you a message with the special link to reset your password.": "ePosta adresinizi girin ve parolan\u0131z\u0131 s\u0131f\u0131rlaman\u0131z i\u00e7in \u00f6zel ba\u011flant\u0131 i\u00e7eren bir iletiyi size g\u00f6nderelim.", 
    "Error while connecting to the server": "Sunucuya ba\u011flan\u0131rken hata oldu", 
    "Expand details": "Ayr\u0131nt\u0131lar\u0131 geni\u015flet", 
    "File types": "Dosya t\u00fcrleri", 
    "Filesystems": "Dosya sistemleri", 
    "Find language by name, code": "Dili ad\u0131na, koda g\u00f6re bul", 
    "Find project by name, code": "Projeyi ad\u0131na, koda g\u00f6re bul", 
    "Find user by name, email, properties": "Kullan\u0131c\u0131y\u0131 ad\u0131na, epostaya, \u00f6zelliklere g\u00f6re bul", 
    "Full Name": "Tam Ad\u0131", 
    "Go back to browsing": "G\u00f6zatmaya geri d\u00f6n", 
    "Go to the next string (Ctrl+.)<br/><br/>Also:<br/>Next page: Ctrl+Shift+.<br/>Last page: Ctrl+Shift+End": "Sonraki sat\u0131ra git (Ctrl+.)<br/><br/>Ayr\u0131ca:<br/>Sonraki sayfa: Ctrl+Shift+.<br/>Son sayfa: Ctrl+Shift+End", 
    "Go to the previous string (Ctrl+,)<br/><br/>Also:<br/>Previous page: Ctrl+Shift+,<br/>First page: Ctrl+Shift+Home": "\u00d6nceki sat\u0131ra git (Ctrl+,)<br/><br/>Ayr\u0131ca:<br/>\u00d6nceki sayfa: Ctrl+Shift+,<br/>\u0130lk sayfa: Ctrl+Shift+Home", 
    "Hide": "Gizle", 
    "Hide disabled": "Gizle etkisizle\u015ftirildi", 
    "I forgot my password": "Parolam\u0131 unuttum", 
    "Ignore Files": "Dosyalar\u0131 Yoksay", 
    "Languages": "Diller", 
    "Less": "Daha az", 
    "LinkedIn": "LinkedIn", 
    "LinkedIn profile URL": "LinkedIn profil URL'si", 
    "Load More": "Daha Fazla Y\u00fckle", 
    "Loading...": "Y\u00fckleniyor...", 
    "Login / Password": "Oturum a\u00e7 / Parola", 
    "More": "Daha fazla", 
    "More...": "Daha fazla...", 
    "My Public Profile": "Ortak Profilim", 
    "No": "Hay\u0131r", 
    "No activity recorded in a given period": "Verilen s\u00fcre i\u00e7erisinde kaydedilmi\u015f etkinlik yok", 
    "No results found": "Bulunan sonu\u00e7lar yok", 
    "No results.": "Sonu\u00e7 yok.", 
    "No, thanks": "Hay\u0131r, te\u015fekk\u00fcrler", 
    "Not found": "Bulunamad\u0131", 
    "Note: when deleting a user their contributions to the site, e.g. comments, suggestions and translations, are attributed to the anonymous user (nobody).": "Not: bir kullan\u0131c\u0131 silindi\u011finde siteye yapt\u0131\u011f\u0131 katk\u0131lar, \u00f6rne\u011fin yorumlar, \u00f6neriler ve \u00e7eviriler, isimsiz kullan\u0131c\u0131ya (nobody) d\u00f6n\u00fc\u015f\u00fcr.", 
    "Number of Plurals": "\u00c7o\u011ful Say\u0131s\u0131", 
    "Oops...": "T\u00fch...", 
    "Overview": "Genel Bak\u0131\u015f", 
    "Password": "Parola", 
    "Password changed, signing in...": "Parola de\u011fi\u015ftirildi, giri\u015f yap\u0131l\u0131yor...", 
    "Permissions": "\u0130zinler", 
    "Personal description": "Ki\u015fisel tan\u0131m", 
    "Personal website URL": "Ki\u015fisel web sitesi URL'si", 
    "Please follow that link to continue the account creation.": "Hesap olu\u015fturmaya devam etmek i\u00e7in l\u00fctfen \u015fu ba\u011flant\u0131y\u0131 takip edin.", 
    "Please follow that link to continue the password reset procedure.": "Parola s\u0131f\u0131rlama i\u015flemine devam etmek i\u00e7in l\u00fctfen \u015fu ba\u011flant\u0131y\u0131 takip edin.", 
    "Please select a valid user.": "L\u00fctfen ge\u00e7erli bir kullan\u0131c\u0131 se\u00e7in.", 
    "Plural Equation": "\u00c7o\u011ful E\u015fitli\u011fi", 
    "Plural form %(index)s": "\u00c7o\u011ful formu %(index)s", 
    "Preview will be displayed here.": "\u00d6nizleme burada g\u00f6r\u00fcnt\u00fclenecektir.", 
    "Project / Language": "Proje / Dil", 
    "Project Tree Style": "Proje A\u011fac\u0131 Stili", 
    "Provide optional comment (will be publicly visible)": "\u0130ste\u011fe ba\u011fl\u0131 yorum sa\u011flar (herkese a\u00e7\u0131k olarak g\u00f6r\u00fcnecektir)", 
    "Public Profile": "Ortak Profil", 
    "Quality Checks": "Kalite Kontrolleri", 
    "Reject": "Reddet", 
    "Reload page": "Sayfay\u0131 yeniden y\u00fckle", 
    "Repeat Password": "Parola Tekrar\u0131", 
    "Resend Email": "Epostay\u0131 Yeniden G\u00f6nder", 
    "Reset Password": "Parolay\u0131 S\u0131f\u0131rla", 
    "Reset Your Password": "Parolan\u0131z\u0131 S\u0131f\u0131rlay\u0131n", 
    "Reviewed": "\u0130ncelenmi\u015f", 
    "Save": "Kaydet", 
    "Saved successfully.": "Ba\u015far\u0131l\u0131 olarak kaydedildi.", 
    "Score Change": "Skor De\u011fi\u015fikli\u011fi", 
    "Screenshot Search Prefix": "Ekran G\u00f6r\u00fcnt\u00fcs\u00fc Arama \u00d6neki", 
    "Search Languages": "Dilleri Ara", 
    "Search Projects": "Projeleri Ara", 
    "Search Users": "Kullan\u0131c\u0131lar\u0131 Ara", 
    "Select...": "Se\u00e7...", 
    "Send Email": "ePosta G\u00f6nder", 
    "Sending email to %s...": "%s adresine eposta g\u00f6nderiliyor...", 
    "Server error": "Sunucu hatas\u0131", 
    "Set New Password": "Yeni Parola Ayarla", 
    "Set a new password": "Yeni bir parola ayarlay\u0131n", 
    "Settings": "Ayarlar", 
    "Short Bio": "K\u0131sa \u00d6zge\u00e7mi\u015f", 
    "Show": "G\u00f6ster", 
    "Show disabled": "G\u00f6ster etkisizle\u015ftirildi", 
    "Sign In": "Giri\u015f Yap", 
    "Sign In With %s": "%s ile Giri\u015f Yap\u0131n", 
    "Sign In With...": "\u015eununla Giri\u015f Yap\u0131n...", 
    "Sign Up": "Kaydol", 
    "Sign in as an existing user": "Varolan bir kullan\u0131c\u0131 olarak giri\u015f yap\u0131n", 
    "Sign up as a new user": "Yeni bir kullan\u0131c\u0131 olarak kaydolun", 
    "Signed in. Redirecting...": "Giri\u015f yap\u0131ld\u0131. Y\u00f6nlendiriliyor...", 
    "Signing in with an external service for the first time will automatically create an account for you.": "\u0130lk defa harici bir hizmet ile giri\u015f yapmak otomatik olarak sizin i\u00e7in bir hesap olu\u015fturacak.", 
    "Similar translations": "Benzer \u00e7eviriler", 
    "Social Services": "Sosyal Hizmetler", 
    "Social Verification": "Sosyal Do\u011frulama", 
    "Source Language": "Kaynak Dil", 
    "Special Characters": "\u00d6zel Karakterler", 
    "String Errors Contact": "Dizgi Hatalar\u0131 \u0130leti\u015fimi", 
    "Suggested": "\u00d6nerilen", 
    "Team": "Tak\u0131m", 
    "The password reset link was invalid, possibly because it has already been used. Please request a new password reset.": "Parola s\u0131f\u0131rlama ba\u011flant\u0131s\u0131 ge\u00e7ersiz oldu, muhtemelen zaten kullan\u0131ld\u0131\u011f\u0131 i\u00e7indir. L\u00fctfen yeni bir parola s\u0131f\u0131rlamas\u0131 isteyin.", 
    "The server seems down. Try again later.": "Sunucu kapal\u0131 g\u00f6r\u00fcn\u00fcyor. Daha sonra tekrar deneyin.", 
    "There are unsaved changes. Do you want to discard them?": "Kaydedilmemi\u015f de\u011fi\u015fiklikler var. Bunlardan vazge\u00e7mek istiyor musunuz?", 
    "There is %(count)s language.": [
      "%(count)s dil var.", 
      "%(count)s dil var. A\u015fa\u011f\u0131da birden fazla olanlar ise en son eklenenlerdir."
    ], 
    "There is %(count)s project.": [
      "%(count)s proje var.", 
      "%(count)s proje var. A\u015fa\u011f\u0131da birden fazla olanlar ise en son eklenenlerdir."
    ], 
    "There is %(count)s user.": [
      "%(count)s kullan\u0131c\u0131 var.", 
      "%(count)s kullan\u0131c\u0131 var. A\u015fa\u011f\u0131da birden fazla olanlar ise en son eklenenlerdir."
    ], 
    "This email confirmation link expired or is invalid.": "Bu eposta onaylama ba\u011flant\u0131s\u0131 s\u00fcresi sona erdi ya da ge\u00e7ersiz.", 
    "This string no longer exists.": "Bu sat\u0131r art\u0131k mevcut de\u011fil.", 
    "To set or change your avatar for your email address (%(email)s), please go to gravatar.com.": "Eposta adresinizdeki (%(email)s) avatar'\u0131n\u0131z\u0131 ayarlamak ya da de\u011fi\u015ftirmek i\u00e7in l\u00fctfen gravatar.com adresine gidin.", 
    "Translated": "\u00c7evrilmi\u015f", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project": "\u201c<span title=\"%(path)s\">%(project)s</span>\u201d projesinde %(fullname)s taraf\u0131ndan \u00e7evrildi", 
    "Translated by %(fullname)s in \u201c<span title=\"%(path)s\">%(project)s</span>\u201d project %(time_ago)s": "\u201c<span title=\"%(path)s\">%(project)s</span>\u201d projesinde %(time_ago)s %(fullname)s taraf\u0131ndan \u00e7evrildi", 
    "Try again": "Tekrar deneyin", 
    "Twitter": "Twitter", 
    "Twitter username": "Twitter kullan\u0131c\u0131 ad\u0131", 
    "Type to search": "Aranan\u0131 yaz\u0131n", 
    "Updating data": "Veri g\u00fcncelleniyor", 
    "Use the search form to find the language, then click on a language to edit.": "Dili bulmak i\u00e7in arama formunu kullan\u0131n, ondan sonra d\u00fczenlemek i\u00e7in bir dile t\u0131klay\u0131n.", 
    "Use the search form to find the project, then click on a project to edit.": "Projeyi bulmak i\u00e7in arama formunu kullan\u0131n, ondan sonra d\u00fczenlemek i\u00e7in bir projeye t\u0131klay\u0131n.", 
    "Use the search form to find the user, then click on a user to edit.": "Kullan\u0131c\u0131y\u0131 bulmak i\u00e7in arama formunu kullan\u0131n, ondan sonra d\u00fczenlemek i\u00e7in bir kullan\u0131c\u0131ya t\u0131klay\u0131n.", 
    "Username": "Kullan\u0131c\u0131 ad\u0131", 
    "We found a user with <span>%(email)s</span> email in our system. Please provide the password to finish the sign in procedure. This is a one-off procedure, which will establish a link between your Pootle and %(provider)s accounts.": "Sistemimizde <span>%(email)s</span> epostas\u0131 ile bir kullan\u0131c\u0131 bulduk. L\u00fctfen giri\u015f yapma i\u015flemini tamamlamak i\u00e7in parola girin. Bu, Pootle ve %(provider)s hesaplar\u0131n\u0131z aras\u0131nda bir ba\u011flant\u0131 kuracak olan tek seferlik bir i\u015flemdir.", 
    "We have sent an email containing the special link to <span>%s</span>": "\u00d6zel ba\u011flant\u0131y\u0131 i\u00e7eren bir epostay\u0131 <span>%s</span> adresine g\u00f6nderdik", 
    "We have sent an email containing the special link to <span>%s</span>. Please check your spam folder if you do not see the email.": "\u00d6zel ba\u011flant\u0131y\u0131 i\u00e7eren bir epostay\u0131 <span>%s</span> adresine g\u00f6nderdik. E\u011fer epostay\u0131 g\u00f6rm\u00fcyorsan\u0131z, l\u00fctfen istenmeyen mesajlar klas\u00f6r\u00fcn\u00fc kontrol edin.", 
    "We have sent an email containing the special link to the address used to register this account. Please check your spam folder if you do not see the email.": "\u00d6zel ba\u011flant\u0131y\u0131 i\u00e7eren bir epostay\u0131 bu hesaba kay\u0131t olmak i\u00e7in kulland\u0131\u011f\u0131n\u0131z adrese g\u00f6nderdik. E\u011fer epostay\u0131 g\u00f6rm\u00fcyorsan\u0131z, l\u00fctfen istenmeyen mesajlar klas\u00f6r\u00fcn\u00fc kontrol edin.", 
    "Website": "Web sitesi", 
    "Why are you part of our translation project? Describe yourself, inspire others!": "\u00c7eviri projemizin neden bir par\u00e7as\u0131s\u0131n\u0131z? Kendinizi tan\u0131t\u0131n, di\u011ferlerine ilham verin!", 
    "Yes": "Evet", 
    "You have unsaved changes in this string. Navigating away will discard those changes.": "Bu sat\u0131rda kaydedilmemi\u015f de\u011fi\u015fiklikleriniz var. Buradan ayr\u0131lmak bu de\u011fi\u015fiklikleri yoksayacak.", 
    "Your Full Name": "Tam Ad\u0131n\u0131z", 
    "Your LinkedIn profile URL": "LinkedIn profil URL'niz", 
    "Your Personal website/blog URL": "Ki\u015fisel web sitesi/blog URL'si", 
    "Your Twitter username": "Twitter kullan\u0131c\u0131 ad\u0131n\u0131z", 
    "Your account is inactive because an administrator deactivated it.": "Hesab\u0131n\u0131z devre d\u0131\u015f\u0131 \u00e7\u00fcnk\u00fc bir y\u00f6netici devre d\u0131\u015f\u0131 b\u0131rakm\u0131\u015f.", 
    "Your account needs activation.": "Hesab\u0131n\u0131z\u0131n etkinle\u015ftirilmesi gerekiyor.", 
    "disabled": "etkisizle\u015ftirildi", 
    "some anonymous user": "baz\u0131 isimsiz kullan\u0131c\u0131lar", 
    "someone": "birisi"
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

