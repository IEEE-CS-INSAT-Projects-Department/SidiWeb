export const UserContext = (function () {
    let state = {
        user: null,
        token: null,
        isLoggedIn: false
    };

    function loadFromStorage() {
        const saved = localStorage.getItem('sidi_auth');
        if (saved) {
            try {
                const parsed = JSON.parse(saved);
                state.user = parsed.user || null;
                state.token = parsed.token || null;
                state.isLoggedIn = !!parsed.token;
            } catch (e) {
                localStorage.removeItem('sidi_auth');
            }
        }
    }

    function saveToStorage() {
        localStorage.setItem('sidi_auth', JSON.stringify({
            user: state.user,
            token: state.token
        }));
    }

    function login(user, token) {
        state.user = user;
        state.token = token;
        state.isLoggedIn = true;
        saveToStorage();
    }

    function logout() {
        state.user = null;
        state.token = null;
        state.isLoggedIn = false;
        localStorage.removeItem('sidi_auth');
    }

    function getUser() {
        return state.user;
    }

    function getToken() {
        return state.token;
    }

    function isAuthenticated() {
        return state.isLoggedIn;
    }

    loadFromStorage();

    return { login, logout, getUser, getToken, isAuthenticated };
})();
