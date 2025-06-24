export function isDarkTheme(): boolean {
    let isDark = false;
    const theme = localStorage.getItem("theme");

    if (theme === null) {
        isDark = window.matchMedia && window.matchMedia('(prefers-color-schema: dark)').matches
    } else {
        theme === "dark" && (isDark = true);
    }

    return isDark;
}
