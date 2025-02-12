document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('form');
    const steps = document.querySelectorAll('.form-step');
    const stepIndicators = document.querySelectorAll('.step');
    const nextButtons = document.querySelectorAll('#next-button');
    const backButtons = document.querySelectorAll('#back-button');
    const submitButton = document.getElementById('submit-button');
    const termsAgreement = document.getElementById('terms-agreement');
    let currentStep = 0;

    submitButton.disabled = true;

    termsAgreement.addEventListener('change', function () {
        submitButton.disabled = !this.checked;

        if (this.checked) {
            submitButton.title = '';
        } else {
            submitButton.title = translations[currentLanguage].termsError;
        }
    });

    function showStep(stepIndex) {
        steps.forEach((step, index) => {
            step.classList.remove('active');
            stepIndicators[index].classList.remove('active');
        });
        steps[stepIndex].classList.add('active');
        stepIndicators[stepIndex].classList.add('active');
        currentStep = stepIndex;

        if (stepIndex === 2) { // Terms step
            submitButton.disabled = !termsAgreement.checked;
        }
    }


    function validateStep(stepIndex) {
        const currentStepElement = steps[stepIndex];
        const inputs = currentStepElement.querySelectorAll('input[required], select[required]');
        let isValid = true;

        inputs.forEach(input => {
            if (!input.value) {
                isValid = false;
                input.classList.add('error');
            } else {
                input.classList.remove('error');
            }
        });

        return isValid;
    }

    nextButtons.forEach(button => {
        button.addEventListener('click', () => {
            if (validateStep(currentStep)) {
                showStep(currentStep + 1);
            }
        });
    });

    backButtons.forEach(button => {
        button.addEventListener('click', () => {
            showStep(currentStep - 1);
        });
    });

    const dateInput = document.getElementById('age');
    if (dateInput) {
        const today = new Date();
        const maxDate = today.toISOString().split('T')[0];
        dateInput.max = maxDate;

        const minDate = new Date();
        minDate.setFullYear(minDate.getFullYear() - 30);
        dateInput.min = minDate.toISOString().split('T')[0];

        const calendarIcon = dateInput.previousElementSibling;
        if (calendarIcon) {
            calendarIcon.style.cursor = 'pointer';
            calendarIcon.addEventListener('click', () => {
                dateInput.showPicker();
            });
        }
    }


    const languageSelect = document.getElementById('languageSelect');
    let currentLanguage = localStorage.getItem('language') || 'az';

    languageSelect.value = currentLanguage;
    updateLanguage(currentLanguage);

    languageSelect.addEventListener('change', (e) => {
        const newLanguage = e.target.value;
        updateLanguage(newLanguage);
        localStorage.setItem('language', newLanguage);
    });

    function updateLanguage(language) {
        currentLanguage = language;

        document.querySelectorAll('[data-translate]').forEach(element => {
            const key = element.getAttribute('data-translate');
            if (translations[language] && translations[language][key]) {
                if (element.tagName === 'OPTION') {
                    element.text = translations[language][key];
                } else {
                    element.textContent = translations[language][key];
                }
            }
        });


        document.querySelectorAll('[data-translate-placeholder]').forEach(element => {
            const key = element.getAttribute('data-translate-placeholder');
            if (translations[language] && translations[language][key]) {
                element.placeholder = translations[language][key];
            }
        });

        document.querySelectorAll('select').forEach(select => {
            Array.from(select.options).forEach(option => {
                if (option.getAttribute('data-translate')) {
                    const key = option.getAttribute('data-translate');
                    if (translations[language] && translations[language][key]) {
                        option.text = translations[language][key];
                    }
                }
            });
        });
    }

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        if (!validateStep(currentStep)) {
            return;
        }

        if (!termsAgreement.checked) {
            alert(translations[currentLanguage].pleaseAcceptTerms);
            return;
        }

        const parent_info = document.getElementById('parent-info').value;
        const parent_number = document.getElementById('phone').value;
        const player_info = document.getElementById('football-player-info').value;
        const player_birth_date = document.getElementById('age').value;
        const player_adress = document.getElementById('location').value;
        const player_club = document.getElementById('club').value;
        const player_position = document.getElementById('position').value;
        const player_strong_foot = document.getElementById('foot').value;

        try {
            const response = await fetch("http://207.154.217.44:8000/api/v1/sheet/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    parent_info: parent_info,
                    parent_number: parent_number,
                    player_info: player_info,
                    player_birth_date: player_birth_date,
                    player_adress: player_adress,
                    player_club: player_club,
                    player_position: player_position,
                    player_strong_foot: player_strong_foot
                })
            });
        } catch (error) {
            console.error("Error:", error);
            alert("An error occurred. Please try again.");
        }
    });
});