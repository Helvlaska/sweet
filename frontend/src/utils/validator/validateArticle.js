import { isValid, makeContentPattern } from "../validator.jsx";

function validateArticle(name, value) {
    switch (name) {
        case "article_title": {
            if (typeof value !== "string" || value.trim() === "") {
                return false;
            }
            const TITLE_PATTERN = makeContentPattern(200, 3);
            return isValid(value, TITLE_PATTERN);
        }

        case "article_content": {
            if (typeof value !== "string" || value.trim() === "") {
                return false;
            }
            const CONTENT_PATTERN = makeContentPattern(50000, 20, true);
            return isValid(value, CONTENT_PATTERN);
        }

        default:
            return true;
    }
}

export { validateArticle };
