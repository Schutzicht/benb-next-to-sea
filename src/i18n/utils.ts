export const languages = {
    nl: 'Nederlands',
    en: 'English',
    de: 'Deutsch',
};

export const defaultLang = 'nl';

export function getLangFromUrl(url: URL) {
    const [, lang] = url.pathname.split('/');
    if (lang in languages) return lang as keyof typeof languages;
    return defaultLang;
}
