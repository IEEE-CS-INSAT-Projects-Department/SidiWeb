import { loginUser, registerUser } from '../../services/authService.js';
import { validateLogin, validateSignup } from './validate.js';
import { UserContext } from '../../context/userContext.js';

document.addEventListener('DOMContentLoaded', () => {
    // 1. Password Visibility Toggle
    document.querySelectorAll('.eye-toggle').forEach(btn => {
        btn.addEventListener('click', () => {
            const input = btn.closest('.password-box').querySelector('input');
            const isPassword = input.type === 'password';
            input.type = isPassword ? 'text' : 'password';

            btn.innerHTML = isPassword ? `
                <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24"/>
                    <line x1="1" y1="1" x2="23" y2="23"/>
                </svg>` : `
                <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                    <circle cx="12" cy="12" r="3"/>
                </svg>`;
        });
    });

    // 2. Form Submission Logic
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            clearErrors(loginForm);
            const errors = validateLogin(email, password);
            if (Object.keys(errors).length > 0) {
                showErrors(loginForm, errors);
                return;
            }

            try {
                const data = await loginUser(email, password);
                UserContext.login(data.user, data.token);
                window.location.href = '../../../index.html';
            } catch (err) {
                showGeneralError(loginForm, err.message);
            }
        });
    }

    if (signupForm) {
        signupForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const firstName = document.getElementById('first-name').value;
            const lastName = document.getElementById('last-name').value;
            const email = document.getElementById('signup-email').value;
            const password = document.getElementById('signup-password').value;
            const confirmPassword = document.getElementById('confirm-password').value;

            clearErrors(signupForm);
            const errors = validateSignup(firstName, lastName, email, password, confirmPassword);
            if (Object.keys(errors).length > 0) {
                showErrors(signupForm, errors);
                return;
            }

            try {
                const data = await registerUser(`${firstName} ${lastName}`, email, password);
                UserContext.login(data.user, data.token);
                window.location.href = '../../../index.html';
            } catch (err) {
                showGeneralError(signupForm, err.message);
            }
        });
    }

    // 3. Helper Functions
    function showErrors(form, errors) {
        for (const [fieldId, message] of Object.entries(errors)) {
            let input = form.querySelector(`#${fieldId === 'email' && form.id === 'signup-form' ? 'signup-email' :
                fieldId === 'password' && form.id === 'signup-form' ? 'signup-password' :
                    fieldId}`);
            if (fieldId === 'firstName') input = document.getElementById('first-name');
            if (fieldId === 'lastName') input = document.getElementById('last-name');

            if (input) {
                const fieldDiv = input.closest('.field');
                let errorSpan = fieldDiv.querySelector('.error-msg');
                if (!errorSpan) {
                    errorSpan = document.createElement('span');
                    errorSpan.className = 'error-msg';
                    errorSpan.style.color = '#ef4444';
                    errorSpan.style.fontSize = '0.8rem';
                    errorSpan.style.marginTop = '0.2rem';
                    fieldDiv.appendChild(errorSpan);
                }
                errorSpan.textContent = message;
                input.style.borderColor = '#ef4444';
            }
        }
    }

    function clearErrors(form) {
        form.querySelectorAll('.error-msg').forEach(el => el.remove());
        form.querySelectorAll('input').forEach(el => el.style.borderColor = '');
        const genErr = form.querySelector('.general-error');
        if (genErr) genErr.remove();
    }

    function showGeneralError(form, message) {
        const errDiv = document.createElement('div');
        errDiv.className = 'general-error';
        errDiv.textContent = message;
        errDiv.style.backgroundColor = '#fef2f2';
        errDiv.style.color = '#ef4444';
        errDiv.style.padding = '0.75rem';
        errDiv.style.borderRadius = '0.5rem';
        errDiv.style.marginBottom = '1rem';
        form.prepend(errDiv);
    }
});
