document.addEventListener("DOMContentLoaded", function() {
    const formInputs = document.querySelectorAll("input, textarea");

    formInputs.forEach((input, index) => {
        input.addEventListener("keydown", function(event) {
            if (event.key === "Enter") {
                event.preventDefault();
                const nextInput = formInputs[index + 1];
                if (nextInput) {
                    nextInput.focus();
                }
            }
        });
    });

    const amountField = document.querySelector('#id_price');
    const dailyPriceField = document.querySelector('#id_daily_price');

    const amountToWordsField = document.createElement('div');
    amountToWordsField.id = 'amount-to-words';
    amountField.parentNode.appendChild(amountToWordsField);

    amountField.addEventListener('input', function () {
        const amount = parseInt(amountField.value, 10);
        if (!isNaN(amount)) {
            amountToWordsField.innerHTML = convertNumberToWords(amount);
        } else {
            amountToWordsField.innerHTML = '';
        }
    });

    dailyPriceField.addEventListener('input', function () {
        const dailyPrice = parseInt(dailyPriceField.value, 10);
        if (!isNaN(dailyPrice)) {
            amountToWordsField.innerHTML = convertNumberToWords(dailyPrice);
        } else {
            amountToWordsField.innerHTML = '';
        }
    });

    function convertNumberToWords(num) {
        const units = ['', 'یک', 'دو', 'سه', 'چهار', 'پنج', 'شش', 'هفت', 'هشت', 'نه'];
        const tens = ['', '', 'بیست', 'سی', 'چهل', 'پنجاه', 'شصت', 'هفتاد', 'هشتاد', 'نود'];
        const hundreds = ['', 'صد', 'دویست', 'سیصد', 'چهارصد', 'پانصد', 'ششصد', 'هفتصد', 'هشتصد', 'نهصد'];
        const thousands = ['', 'هزار', 'میلیون', 'میلیارد', 'تریلیون'];

        if (num === 0) return `<span class="amount-text">صفر</span> <span class="currency">تومان</span>`;

        let word = '';
        let thousandCounter = 0;

        while (num > 0) {
            const chunk = num % 1000;
            if (chunk > 0) {
                word = convertChunk(chunk) + (thousands[thousandCounter] ? ' ' + thousands[thousandCounter] : '') + ' ' + word;
            }
            num = Math.floor(num / 1000);
            thousandCounter++;
        }

        return `<span class="amount-text">${word.trim()}</span> <span class="toman">تومان</span>`;

        function convertChunk(chunk) {
            const unitsPart = units[chunk % 10];
            const tensPart = tens[Math.floor(chunk / 10) % 10];
            const hundredsPart = hundreds[Math.floor(chunk / 100)];

            let result = '';
            if (hundredsPart) result += hundredsPart;
            if (tensPart) result += (result ? ' و ' : '') + tensPart;
            if (unitsPart) result += (result ? ' و ' : '') + unitsPart;
            return result;
        }
    }
});
