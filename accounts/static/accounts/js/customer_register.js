
document.addEventListener("DOMContentLoaded", function() {
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
});

