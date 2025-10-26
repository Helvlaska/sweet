import { isValid, makeContentPattern } from "../validator.jsx";

function validateForum(name, value) {
    switch (name) {
        case "forum_post_title": {
            if (typeof value !== "string" || value.trim() === "") {
                return false;
            }
            const TITLE_PATTERN = makeContentPattern(150, 3);
            return isValid(value, TITLE_PATTERN);
        }

        case "forum_post_content": {
            if (typeof value !== "string" || value.trim() === "") {
                return false;
            }
            const CONTENT_PATTERN = makeContentPattern(10000, 5, true);
            return isValid(value, CONTENT_PATTERN);
        }

        case "comment_content": {
            if (typeof value !== "string" || value.trim() === "") {
                return false;
            }
            const COMMENT_PATTERN = makeContentPattern(300, 3, true);
            return isValid(value, COMMENT_PATTERN);
        }

        default:
            return true;
    }
}

export { validateForum };
