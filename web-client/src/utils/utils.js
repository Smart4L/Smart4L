/**
 * 
 * @param {String} str String you want to Capitalize the first letter
 * @return {String} Your string Capitalized
 */
export const Capitalize = (str) => {
    return str.charAt(0).toUpperCase() + str.slice(1)
};