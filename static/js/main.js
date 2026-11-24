/**
 * KisanSAATHI 2.0 - Client Interactions
 * Pure Vanilla JavaScript (No Node.js, no build tool required).
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile navigation menu toggle
    const menuToggle = document.getElementById('menu-toggle');
    const navLinks = document.getElementById('nav-links');
    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            const expanded = navLinks.classList.contains('active');
            menuToggle.setAttribute('aria-expanded', expanded);
        });
    }

    // 2. Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });

    // 3. Tab switching helper
    const tabButtons = document.querySelectorAll('[data-tab-target]');
    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-tab-target');
            const parent = btn.closest('.tab-container');
            if (parent) {
                parent.querySelectorAll('[data-tab-target]').forEach(b => b.classList.remove('active'));
                parent.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
                btn.classList.add('active');
                const targetPane = document.getElementById(targetId);
                if (targetPane) targetPane.classList.add('active');
            }
        });
    });
});

// 4. Voice Speech Assistance (Web Speech API)
window.KisanVoice = {
    speakText: function(text, lang) {
        if (!('speechSynthesis' in window)) {
            alert("Voice synthesis is not supported in this browser.");
            return;
        }
        window.speechSynthesis.cancel(); // Stop any pending speech
        const utterance = new SpeechSynthesisUtterance(text);
        if (lang === 'hi') utterance.lang = 'hi-IN';
        else if (lang === 'pa') utterance.lang = 'pa-IN';
        else utterance.lang = 'en-IN';
        utterance.rate = 0.95; // Slightly slower for clear rural comprehension
        window.speechSynthesis.speak(utterance);
    },

    startSpeechRecognition: function(targetInputId, callback) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            alert("Voice recognition is not supported in your browser. Please type your message.");
            return;
        }
        const recognition = new SpeechRecognition();
        recognition.lang = 'hi-IN';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.onstart = function() {
            const micBtn = document.getElementById('mic-indicator');
            if (micBtn) micBtn.classList.add('recording');
        };

        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            const inputField = document.getElementById(targetInputId);
            if (inputField) inputField.value = transcript;
            if (callback) callback(transcript);
        };

        recognition.onerror = function(event) {
            console.error("Speech recognition error:", event.error);
        };

        recognition.onend = function() {
            const micBtn = document.getElementById('mic-indicator');
            if (micBtn) micBtn.classList.remove('recording');
        };

        recognition.start();
    }
};
