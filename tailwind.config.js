// eslint-disable-next-line no-undef
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
  // eslint-disable-next-line no-undef
  plugins: [require("@tailwindcss/forms")],
};
