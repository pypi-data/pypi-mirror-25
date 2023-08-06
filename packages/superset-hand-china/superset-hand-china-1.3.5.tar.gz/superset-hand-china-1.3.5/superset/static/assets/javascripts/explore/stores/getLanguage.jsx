
const $ = window.$ = require('jquery');

export function getLanguage() {
  const locale = $.ajax({
    url: '/superset/rest/api/getLocale',
    async: false,
  });
  return locale.responseText;
  // let defaultLocale = 'en';
  // $.ajax({
  //   url: '/superset/rest/api/get_locale',
  //   async: false,
  //   success(data) {
  //     defaultLocale = data.language;
  //   },
  // });
  // return defaultLocale;
}
