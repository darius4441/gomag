/*eslint no-undef: "error"*/
/*eslint-env node*/
const formKitTailwind = require("@formkit/themes/tailwindcss");

module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx,vue}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        kPrimaryColor: "#034159",
        kSecondaryColor: "#025951",
        kTertiaryColor: "#02735E",
        kWhiteColor: "#FFFDFA",
        kDarkColor: "#011C26",
      },
    },
  },
  plugins: [formKitTailwind],
};
