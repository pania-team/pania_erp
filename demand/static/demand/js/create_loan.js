document.addEventListener("DOMContentLoaded", function() {
    // مدیریت جابجایی بین فیلدهای فرم با کلید Enter
    const formInputs = document.querySelectorAll("input, textarea");

    formInputs.forEach((input, index) => {
        input.addEventListener("keydown", function(event) {
            if (event.key === "Enter") {
                event.preventDefault();  // جلوگیری از رفتار پیش‌فرض (مثل ارسال فرم)
                const nextInput = formInputs[index + 1];  // به فیلد بعدی برود
                if (nextInput) {
                    nextInput.focus();
                }
            }
        });
    });

    // تبدیل عدد به حروف و نمایش واحد "تومان"
    const amountField = document.querySelector('#id_total_amount');
    const amountToWordsField = document.createElement('div');
    amountToWordsField.id = 'amount-to-words';
    amountToWordsField.style.marginTop = '5px';
    amountToWordsField.style.fontSize = '12px';
    amountToWordsField.style.fontFamily = 'Vazirmatn, sans-serif';
    amountField.parentNode.appendChild(amountToWordsField);

    // گوش دادن به تغییرات در فیلد مبلغ
    amountField.addEventListener('input', function () {
        const amount = parseInt(amountField.value, 10);
        if (!isNaN(amount)) {
            amountToWordsField.innerHTML = convertNumberToWords(amount);  // استفاده از innerHTML به جای textContent
        } else {
            amountToWordsField.textContent = '';  // در صورت وارد نکردن عدد
        }
    });

    // تابع برای تبدیل عدد به حروف
    function convertNumberToWords(num) {
        const units = [
            '', 'یک', 'دو', 'سه', 'چهار', 'پنج', 'شش', 'هفت', 'هشت', 'نه'
        ];
        const tens = [
            '', '', 'بیست', 'سی', 'چهل', 'پنجاه', 'شصت', 'هفتاد', 'هشتاد', 'نود'
        ];
        const hundreds = [
            '', 'صد', 'دویست', 'سیصد', 'چهارصد', 'پانصد', 'ششصد', 'هفتصد', 'هشتصد', 'نهصد'
        ];

        const thousands = [
            '', 'هزار', 'میلیون', 'میلیارد', 'تریلیون'
        ];

        if (num === 0) return 'صفر <span class="toman">تومان</span>';

        let word = '';
        let thousandCounter = 0;  // برای محاسبه هر بخش هزارگان و میلیون‌ها و...

        // تقسیم عدد به بخش‌های هزارگان
        while (num > 0) {
            const chunk = num % 1000;
            if (chunk > 0) {
                word = convertChunk(chunk) + (thousands[thousandCounter] ? ' ' + thousands[thousandCounter] : '') + ' ' + word;
            }
            num = Math.floor(num / 1000);
            thousandCounter++;
        }

        return '<span class="amount-text">' + word.trim() + ' <span class="toman">تومان</span></span>';

        // تابع برای تبدیل هر بخش کمتر از 1000
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
